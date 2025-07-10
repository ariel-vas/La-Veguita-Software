from django.shortcuts import render
from rest_framework import generics
from ..models import Product
from ..serializers import ProductSerializer


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
    queryset = Product.objects.prefetch_related('subcategories')
    serializer_class = ProductSerializer


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
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):  # TODO: DO SOFT DELETE
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id_product"

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
        return Product.objects.filter(category__name__iexact=category_name)


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
        return Product.objects.filter(subcategories__name__iexact=subcategory_name).distinct()