from rest_framework import serializers
from ..models import Batch, Product


class BatchSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Product.objects.all()
    )

    class Meta:
        model = Batch
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # show related names
        rep['product'] = instance.product.name
        return rep