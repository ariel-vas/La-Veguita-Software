from django.shortcuts import render
from rest_framework import generics
from ..models import Supplier
from ..serializers import SupplierSerializer

"""
    get:
    Retorna una lista de todos los proveedores registrados.

    post:
    Crea un nuevo proveedor.

    Entradas (POST):
        - rut (str): RUT del proveedor (único).
        - name (str): Nombre del proveedor.
        - line (str): Línea de productos o actividad del proveedor.
        - address (str): Dirección del proveedor.
        - commune (str): Comuna del proveedor.
        - city (str): Ciudad del proveedor.
        - telephone (str, opcional): Teléfono fijo.
        - cellphone (str, opcional): Teléfono móvil.
        - email (str, opcional): Correo electrónico.

    Salidas (GET/POST):
        - rut (str): RUT del proveedor.
        - name (str): Nombre del proveedor.
        - line (str): Línea de productos o actividad.
        - address (str): Dirección.
        - commune (str): Comuna.
        - city (str): Ciudad.
        - telephone (str): Teléfono fijo (si aplica).
        - cellphone (str): Teléfono móvil (si aplica).
        - email (str): Correo electrónico (si aplica).
"""
class SupplierListCreate(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


"""
    get:
    Retorna los detalles de un proveedor específico mediante su RUT.

    put/patch:
    Actualiza los datos de un proveedor existente.

    delete:
    Elimina un proveedor identificado por su RUT.

    Parámetros de URL:
        - rut (str): RUT del proveedor a consultar, modificar o eliminar.

    Entradas (PUT/PATCH):
        - name (str): Nombre del proveedor.
        - line (str): Línea de productos o actividad.
        - address (str): Dirección.
        - commune (str): Comuna.
        - city (str): Ciudad.
        - telephone (str, opcional): Teléfono fijo.
        - cellphone (str, opcional): Teléfono móvil.
        - email (str, opcional): Correo electrónico.

    Salidas:
        - rut (str): RUT del proveedor.
        - name (str): Nombre del proveedor.
        - line (str): Línea de productos o actividad.
        - address (str): Dirección.
        - commune (str): Comuna.
        - city (str): Ciudad.
        - telephone (str): Teléfono fijo (si aplica).
        - cellphone (str): Teléfono móvil (si aplica).
        - email (str): Correo electrónico (si aplica).
"""
class SupplierRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    lookup_field = "rut"