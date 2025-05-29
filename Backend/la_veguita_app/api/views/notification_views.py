from django.shortcuts import render
from rest_framework import generics
from ..models import Notification
from ..serializers import NotificationSerializer


class NotificationListCreate(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = "id_notification"