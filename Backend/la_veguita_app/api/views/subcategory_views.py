from django.shortcuts import render
from rest_framework import generics
from ..models import SubCategory, Product
from ..serializers import SubCategorySerializer, ProductSerializer

"""
    get:
    Retorna una lista de todas las subcategorías existentes.

    post:
    Crea una nueva subcategoría.

    Entradas (POST):
        - name (str): Nombre único de la subcategoría.
        - products (list[int], opcional): Lista de IDs de productos asociados.

    Salidas (GET/POST):
        - id_subcategory (int): ID de la subcategoría.
        - name (str): Nombre de la subcategoría.
        - products (list): Lista de productos relacionados (si se incluyen en la serialización).
"""
class SubCategoryListCreate(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


"""
    get:
    Retorna una subcategoría específica mediante su ID.

    put/patch:
    Actualiza los datos de una subcategoría existente.

    delete:
    Elimina una subcategoría por su ID.

    Parámetros de URL:
        - id_subcategory (int): ID de la subcategoría a consultar, actualizar o eliminar.

    Entradas (PUT/PATCH):
        - name (str): Nombre de la subcategoría (único).
        - products (list[int], opcional): IDs de productos a asociar.

    Salidas:
        - id_subcategory (int): ID de la subcategoría.
        - name (str): Nombre de la subcategoría.
        - products (list): Lista de productos relacionados (si se incluyen en la serialización).
"""
class SubCategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    lookup_field = "id_subcategory"


"""
    get:
    Retorna una lista de productos asociados a una subcategoría específica.

    Parámetros de URL:
        - id_subcategory (int): ID de la subcategoría cuyos productos se desean listar.

    Salidas:
        - id_product (str): Código de producto.
        - description (str): Descripción del producto.
        - stock (int): Cantidad en stock.
        - price (int): Precio de venta.
        - ...otros campos definidos en ProductSerializer.
"""
class ProductsBySubCategory(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs['id_subcategory']
        return Product.objects.filter(subcategories__id_subcategory=subcategory_id)