from rest_framework import serializers
from ..models import WrongSaleDetail


class WrongSaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrongSaleDetail
        fields = '__all__'