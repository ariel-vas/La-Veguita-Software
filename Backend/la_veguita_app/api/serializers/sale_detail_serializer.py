from rest_framework import serializers
from ..models import SaleDetail


class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = '__all__'