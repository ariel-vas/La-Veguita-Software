from rest_framework import serializers
from ..models import Batch, Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'