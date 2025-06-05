from rest_framework import serializers
from ..models import Product, Category, SubCategory, Supplier


class ProductSerializer(serializers.ModelSerializer):

    # Handle Foreign key and ManyToManyField relations through Slugs
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    supplier = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Supplier.objects.all(),
        required=False,
        allow_null=True
    )
    subcategories = serializers.SlugRelatedField(
        slug_field='name',
        queryset=SubCategory.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Product
        fields = ['id_product',
                  'description',
                  'purchase_price',
                  'sale_price',
                  'wholesale_price',
                  'wholesale_quantity',
                  'discount_surcharge',
                  'stock',
                  'critical_stock',
                  'entry_stock_unit',
                  'exit_stock_unit',
                  'composed_product',
                  'checked',
                  'category', 'supplier', 'subcategories']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # show related names
        rep['category'] = instance.category.name if instance.category else None
        rep['supplier'] = instance.supplier.name if instance.supplier else None
        rep['subcategories'] = [sc.name for sc in instance.subcategories.all()]
        return rep