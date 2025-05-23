from rest_framework import serializers
from ..models import Batch, Product


class BatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch
        fields = '__all__'