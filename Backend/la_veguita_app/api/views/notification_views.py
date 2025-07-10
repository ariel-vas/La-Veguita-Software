from django.shortcuts import render
from rest_framework import generics
from ..models import Notification
from ..serializers import NotificationSerializer

"""
    Vista API para listar y crear registros de notificaciones.

    Métodos soportados:
    - GET: Retorna la lista de todas las notificaciones.
    - POST: Permite crear una nueva notificación.

    Entradas (GET):
    - No requiere entradas.

    Salidas (GET):
    - "id_notification": "entero (autogenerado)"
    - "state": "cadena (máx. 50 caracteres) ready or pending"
    - "date_of_completion": "fecha y hora (opcional, formato ISO 8601)"
    - "id_batch": "cadena (ID del batch relacionado)"
    - "expiration_date": "fecha y hora (formato ISO 8601, no editable)"
    - "name_product": "cadena (máx. 150 caracteres, no editable)"

    Entradas (POST):
    - "state": "cadena (opcional, valor por defecto: 'pending')"
    - "date_of_completion": "fecha y hora (opcional, formato ISO 8601)"
    - "id_batch": "cadena (ID del batch relacionado)"

    Salidas (POST):
    - "id_notification": "entero (autogenerado)"
    - "state": "cadena"
    - "date_of_completion": "fecha y hora"
    - "id_batch": "cadena"
    - "expiration_date": "fecha y hora"
    - "name_product": "cadena"
    """
class NotificationListCreate(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer



"""
    Vista API para recuperar, actualizar o eliminar una notificación específica.

    Métodos soportados:
    - GET: Recupera una notificación por su ID.
    - PUT/PATCH: Actualiza una notificación existente.
    - DELETE: Elimina la notificación y elimina el batch asociado si no tiene más notificaciones.

    Entradas (GET):
    - "id_notification": "entero (en la URL)"

    Salidas (GET):
    - "id_notification": "entero"
    - "state": "cadena"
    - "date_of_completion": "fecha y hora"
    - "id_batch": "cadena"
    - "expiration_date": "fecha y hora"
    - "name_product": "cadena"

    Entradas (PUT/PATCH):
    - "state": "cadena" (opcional)
    - "date_of_completion": "fecha y hora" (opcional)
    - "id_batch": "cadena" (opcional)

    Salidas (PUT/PATCH):
    - "id_notification": "entero"
    - "state": "cadena"
    - "date_of_completion": "fecha y hora"
    - "id_batch": "cadena"
    - "expiration_date": "fecha y hora"
    - "name_product": "cadena"

    Entradas (DELETE):
    - "id_notification": "entero (en la URL)"

    Salidas (DELETE):
    - Sin contenido (204 No Content)
    """
class NotificationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = "id_notification"