from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache
from ..models import Product
from ..serializers import ProductSerializer


CACHE_TIMEOUT = 86400  # 24 hour of cache


# Helper function to update or add product in cache list
def update_product_in_cache_list(product_data):
    products_list = cache.get('products_all')
    if products_list is not None:
        for idx, p in enumerate(products_list):
            if p['id_product'] == product_data['id_product']:
                products_list[idx] = product_data
                break
        else:
            products_list.append(product_data)
        cache.set('products_all', products_list, timeout=CACHE_TIMEOUT)


# Helper function to remove product in cache list
def remove_product_from_cache_list(product_id):
    products_list = cache.get('products_all')
    if products_list is not None:
        products_list = [p for p in products_list if p['id_product'] != product_id]
        cache.set('products_all', products_list, timeout=CACHE_TIMEOUT)

"""
    Vista API para crear un nuevo producto.

    Métodos soportados:
    - POST: Crea un nuevo producto.

    Entradas (POST):
    - "id_product": "cadena única (máx. 50 caracteres)"
    - "description": "cadena (máx. 150 caracteres)"
    - "purchase_price": "decimal (mínimo 0)"
    - "sale_price": "decimal (mínimo 0)"
    - "wholesale_price": "decimal (mínimo 0)"
    - "wholesale_quantity": "decimal (mínimo 0)"
    - "discount_surcharge": "decimal"
    - "stock": "decimal (mínimo 0)"
    - "critical_stock": "decimal (mínimo 0)"
    - "entry_stock_unit": "cadena (opciones: 'unit', 'kilo')"
    - "exit_stock_unit": "cadena (opciones: 'unit', 'kilo')"
    - "composed_product": "booleano"
    - "checked": "booleano"
    - "category": "decimal (ID de categoría, opcional)"
    - "supplier": "entero (ID de proveedor, opcional)"
    - "active": "booleano"

    Salidas (POST):
    - Mismos campos enviados, incluyendo validaciones y tipos definidos.
"""
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        product = serializer.save()

        # save product to cache
        cache.set(f'product:{product.id_product}', ProductSerializer(product).data, timeout=CACHE_TIMEOUT)

        # add to cache list
        update_product_in_cache_list(ProductSerializer(product).data)


"""
    Vista API para listar todos los productos registrados.

    Métodos soportados:
    - GET: Lista todos los productos disponibles.

    Entradas (GET):
    - No requiere entradas.

    Salidas (GET):
    - "id_product": "cadena única"
    - "description": "cadena"
    - "purchase_price": "decimal"
    - "sale_price": "decimal"
    - "wholesale_price": "decimal"
    - "wholesale_quantity": "decimal"
    - "discount_surcharge": "decimal"
    - "stock": "decimal"
    - "critical_stock": "decimal"
    - "entry_stock_unit": "cadena"
    - "exit_stock_unit": "cadena"
    - "composed_product": "booleano"
    - "checked": "booleano"
    - "category": "decimal (ID de categoría)"
    - "supplier": "entero (ID de proveedor)"
    - "active": "booleano"
"""
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        # first search on cache
        products_list = cache.get('products_all')
        if products_list is None:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            products_list = serializer.data
            cache.set('products_all', products_list, timeout=CACHE_TIMEOUT)
        return Response(products_list)

    def get_queryset(self):
        return Product.objects.filter(active=True)

"""
    Vista API para obtener, actualizar o eliminar un producto específico.

    Métodos soportados:
    - GET: Recupera un producto por su ID.
    - PUT/PATCH: Actualiza un producto.
    - DELETE: Elimina un producto (en el futuro, eliminará lógicamente mediante 'active').

    Entradas (GET):
    - "id_product": "cadena única (en la URL)"

    Salidas (GET):
    - Todos los campos del producto (ver ProductListView)

    Entradas (PUT/PATCH):
    - Campos editables del producto (ver ProductCreateView)

    Salidas (PUT/PATCH):
    - Producto actualizado (ver ProductListView)

    Entradas (DELETE):
    - "id_product": "cadena única (en la URL)"

    Salidas (DELETE):
    - Sin contenido (204 No Content)
"""
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = "id_product"

    def get_queryset(self):
        return Product.objects.filter(active=True)

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get(self.lookup_field)
        product_data = cache.get(f'product:{product_id}')
        if product_data is None:
            instance = self.get_object()
            product_data = ProductSerializer(instance).data
            cache.set(f'product:{product_id}', product_data, timeout=CACHE_TIMEOUT)
        return Response(product_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # update individual cache
        product_data = ProductSerializer(product).data
        cache.set(f'product:{product.id_product}', product_data, timeout=CACHE_TIMEOUT)

        # update cache list
        update_product_in_cache_list(product_data)

        return Response(product_data)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.active = False
        product.save()

        # delete from cache and cache list
        cache.delete(f'product:{product.id_product}')
        remove_product_from_cache_list(product.id_product)

        return Response({"message": "Producto eliminado exitosamente."}, status=status.HTTP_200_OK)

"""
    Vista API para listar productos filtrados por nombre exacto de categoría.

    Métodos soportados:
    - GET: Lista los productos que pertenecen a una categoría específica.

    Entradas (GET):
    - "category": "cadena (nombre exacto de la categoría, en la URL)"

    Salidas (GET):
    - Lista de productos asociados a la categoría (ver ProductListView)
"""
class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_name = self.kwargs['category']

        return Product.objects.filter(category__name__iexact=category_name, active=True)


"""
    Vista API para listar productos filtrados por nombre exacto de subcategoría.

    Métodos soportados:
    - GET: Lista los productos que pertenecen a una subcategoría específica.

    Entradas (GET):
    - "subcategory": "cadena (nombre exacto de la subcategoría, en la URL)"

    Salidas (GET):
    - Lista de productos asociados a la subcategoría (ver ProductListView)
"""

class ProductBySubCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_name = self.kwargs['subcategory']
        return Product.objects.filter(subcategories__name__iexact=subcategory_name, active=True).distinct()
      