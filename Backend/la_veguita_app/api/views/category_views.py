from django.shortcuts import render
from rest_framework import generics
from ..models import Category, Product
from ..serializers import CategorySerializer, ProductSerializer

"""
    Vista API para listar y crear registros de categorías.

    Métodos soportados:
    - GET: Retorna la lista de todas las categorías.
    - POST: Permite crear una nueva categoría.

    Entradas (GET):
    - No requiere entradas.

    Salidas (GET):
    - "id_category": "decimal (mínimo 0, sin decimales)"
    - "name": "cadena (única, máx. 100 caracteres)"

    Entradas (POST):
    - "name": "cadena (única, máx. 100 caracteres)"

    Salidas (POST):
    - "id_category": "decimal (mínimo 0, sin decimales)"
    - "name": "cadena (única, máx. 100 caracteres)"
"""
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


"""
    Vista API para recuperar, actualizar o eliminar una categoría específica.

    Métodos soportados:
    - GET: Recupera una categoría por su ID.
    - PUT/PATCH: Actualiza parcialmente o completamente una categoría.
    - DELETE: Elimina la categoría especificada.

    Entradas (GET):
    - "id_category": "decimal (mínimo 0, sin decimales) (en la URL)"

    Salidas (GET):
    - "id_category": "decimal (mínimo 0, sin decimales)"
    - "name": "cadena (única, máx. 100 caracteres)"

    Entradas (PUT/PATCH):
    - "name": "cadena (única, máx. 100 caracteres)" (opcional)

    Salidas (PUT/PATCH):
    - "id_category": "decimal (mínimo 0, sin decimales)"
    - "name": "cadena (única, máx. 100 caracteres)"

    Entradas (DELETE):
    - "id_category": "decimal (mínimo 0, sin decimales) (en la URL)"

    Salidas (DELETE):
    - Sin contenido (204 No Content)
"""
class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id_category"

"""
    Vista API para listar los productos asociados a una categoría específica.

    Métodos soportados:
    - GET: Lista todos los productos que pertenecen a una categoría indicada.

    Entradas (GET):
    - "id_category": "decimal (mínimo 0, sin decimales) (en la URL)"

    Salidas (GET):
    - "id_product": "entero"
    - "name": "cadena"
    - "description": "cadena"
    - "category": "decimal (ID de la categoría asociada)"
    - ... (otros campos definidos en el ProductSerializer)
"""
class ProductsByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['id_category']
        return Product.objects.filter(category__id_category=category_id)