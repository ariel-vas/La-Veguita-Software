from datetime import timedelta
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from ..models import Batch, Notification
from ..serializers import BatchSerializer


class BatchListCreate(generics.ListCreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer


class BatchRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    lookup_field = "id_batch"

class BatchExpiringSoonView(APIView):
    def get(self, request):
        today = now().date()
        threshold_date = today + timedelta(days=5)

        # 1. Filtrar los batches que vencen en ≤ 5 días o ya vencieron
        batches = Batch.objects.filter(expiration_date__lte=threshold_date)

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
