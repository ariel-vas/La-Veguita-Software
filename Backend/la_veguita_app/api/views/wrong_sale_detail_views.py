from django.shortcuts import render
from rest_framework import generics
from ..models import WrongSaleDetail
from ..serializers import WrongSaleDetailSerializer


"""
    get:
    Retorna una lista de todos los detalles erroneos de boleta existentes.

    post:
    Crea un nuevo detalle erroneo de boleta.

    Entradas (POST):


    Salidas (GET/POST):

"""
class WrongSaleDetailListCreate(generics.ListCreateAPIView):
    queryset = WrongSaleDetail.objects.all()
    serializer_class = WrongSaleDetailSerializer


"""
    get:
    Retorna un detalle erroneo de boleta específica mediante su ID.

    put/patch:
    Actualiza los datos de un detalle erroneo de boleta existente.

    delete:
    Elimina una detalle erroneo de boleta por su ID.

    Parámetros de URL:
        - id_wrong_sale_detail (int): ID del detalle erroneo de boleta a consultar, actualizar o eliminar.

    Entradas (PUT/PATCH):
    
    Salidas:

"""
class WrongSaleDetailRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = WrongSaleDetail.objects.all()
    serializer_class = WrongSaleDetailSerializer
    lookup_field = "id_wrong_sale_detail"
