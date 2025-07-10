from datetime import timedelta
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from ..models import Batch, Notification
from ..serializers import BatchSerializer

"""
    Vista API para listar y crear registros de batches.

    Métodos soportados:
    - GET: Retorna la lista de todos los batches.
    - POST: Permite crear un nuevo batch.

    Entradas (GET):
    - No requiere entradas.
    Salidas (GET):
    - "id_batch": "cadena única"
    - "starting_quantity": "decimal (mínimo 0)"
    - "quantity": "decimal"
    - "unit": "cadena (opciones: 'unit', 'kilo')"
    - "entry_date": "cadena (YYYY-MM-DD)"
    - "expiration_date": "cadena (YYYY-MM-DD)"
    - "product": "entero (ID de producto)"

    Entradas (POST):
    - "id_batch": "cadena única"
    - "starting_quantity": "decimal (mínimo 0)"
    - "quantity": "decimal"
    - "unit": "cadena (opciones: 'unit', 'kilo')"
    - "entry_date": "cadena (YYYY-MM-DD)"
    - "expiration_date": "cadena (YYYY-MM-DD)"
    - "product": "entero (ID de producto)"

    Salidas (POST):
    - "id_batch": "cadena única"
    - "starting_quantity": "decimal (mínimo 0)"
    - "quantity": "decimal"
    - "unit": "cadena (opciones: 'unit', 'kilo')"
    - "entry_date": "cadena (YYYY-MM-DD)"
    - "expiration_date": "cadena (YYYY-MM-DD)"
    - "product": "entero (ID de producto)"
"""
class BatchListCreate(generics.ListCreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

"""
    Vista API para recuperar, actualizar o eliminar un batch específico.

    Métodos soportados:
    - GET: Recupera un batch por su ID.
    - PUT/PATCH: Actualiza parcialmente o completamente un batch existente.
    - DELETE: Elimina el batch especificado.

    Entradas (GET):
    - "id_batch": "cadena única (en la URL)"

    Salidas (GET):
    - "id_batch": "cadena única"
    - "starting_quantity": "decimal (mínimo 0)"
    - "quantity": "decimal"
    - "unit": "cadena (opciones: 'unit', 'kilo')"
    - "entry_date": "cadena (YYYY-MM-DD)"
    - "expiration_date": "cadena (YYYY-MM-DD)"
    - "product": "entero (ID de producto)"

    Entradas (PUT/PATCH):
    - "starting_quantity": "decimal (mínimo 0)" (opcional)
    - "quantity": "decimal" (opcional)
    - "unit": "cadena (opciones: 'unit', 'kilo')" (opcional)
    - "entry_date": "cadena (YYYY-MM-DD)" (opcional)
    - "expiration_date": "cadena (YYYY-MM-DD)" (opcional)
    - "product": "entero (ID de producto)" (opcional)

    Salidas (PUT/PATCH):
    - "id_batch": "cadena única"
    - "starting_quantity": "decimal (mínimo 0)"
    - "quantity": "decimal"
    - "unit": "cadena (opciones: 'unit', 'kilo')"
    - "entry_date": "cadena (YYYY-MM-DD)"
    - "expiration_date": "cadena (YYYY-MM-DD)"
    - "product": "entero (ID de producto)"

    Entradas (DELETE):
    - "id_batch": "cadena única (en la URL)"

    Salidas (DELETE):
    - Sin contenido (204 No Content)
"""
class BatchRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    lookup_field = "id_batch"

"""
    Vista personalizada para obtener batches que vencen en ≤ 5 días y generar notificaciones si corresponde.

    Métodos soportados:
    - GET: Retorna los batches cuya fecha de expiración es en 5 días o menos desde la fecha actual
      y que aún tienen cantidad disponible. Se crean notificaciones si no existen previamente.

    Entradas (GET):
    - No requiere entradas.

    Salidas (GET):
    - "message": "cadena"
    - "notifications_created": "lista de enteros (IDs de notificaciones creadas)"
    - "batches": "lista de objetos Batch"

    Cada objeto Batch incluye:
    - "id_batch": "cadena única"
    - "starting_quantity": "decimal (mínimo 0)"
    - "quantity": "decimal"
    - "unit": "cadena (opciones: 'unit', 'kilo')"
    - "entry_date": "cadena (YYYY-MM-DD)"
    - "expiration_date": "cadena (YYYY-MM-DD)"
    - "product": "entero (ID de producto)"
"""
class BatchExpiringSoonView(APIView):
    def get(self, request):
        today = now().date()
        threshold_date = today + timedelta(days=5)

        # 1. Filtrar los batches que vencen en ≤ 5 días o ya vencieron
        batches = Batch.objects.filter(expiration_date__lte=threshold_date).exclude(quantity=0)

        # 2. Para cada batch, revisar si ya tiene una notificación
        created_notifications = []
        for batch in batches:
            if not Notification.objects.filter(id_batch=batch).exists():
                notif = Notification.objects.create(id_batch=batch)
                created_notifications.append(notif.id_notification)

        # 3. Serializar y retornar los batches filtrados
        serializer = BatchSerializer(batches, many=True)
        return Response({
            "message": "Batches encontrados y notificaciones creadas si era necesario.",
            "notifications_created": created_notifications,
            "batches": serializer.data
        }, status=status.HTTP_200_OK)
