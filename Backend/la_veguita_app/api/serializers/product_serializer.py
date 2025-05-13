from rest_framework import serializers
from ..models import Product, Category, SubCategory, Supplier
from .subcategory_serializer import SubCategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    # accept names for relations
    category = serializers.CharField(required=False, allow_blank=True)
    supplier = serializers.CharField(required=False, allow_blank=True)

    # accept subcategory names on input
    subcategory_names = serializers.ListField(
        child=serializers.CharField(), required=False, write_only=True
    )

    # use full SubcategorySerializer on output
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id_product',
                  'name',
                  'description',
                  'purchase_price',
                  'sale_price_unit',
                  'sale_price_kilo',
                  'wholesale_price',
                  'wholesale_quantity',
                  'discount_surcharge',
                  'stock',
                  'critical_stock',
                  'stock_unit',
                  'composed_product',
                  'category', 'supplier', 'subcategories', 'subcategory_names']

    def validate_category(self, value):
        if not value.strip():
            return None
        return value

    def validate_supplier(self, value):
        if not value.strip():
            return None
        return value

    def create(self, validated_data):
        # Pop raw values
        cat_name = validated_data.pop('category', None)
        supp_name = validated_data.pop('supplier', None)
        subcat_names = validated_data.pop('subcategory_names', [])

        # Resolve Category
        category = None
        if cat_name:
            category, _ = Category.objects.get_or_create(name=cat_name)

        # Resolve Supplier
        supplier = None
        if supp_name:
            supplier, _ = Supplier.objects.get_or_create(name=supp_name)

        # Create Product
        product = Product.objects.create(
            category=category,
            supplier=supplier,
            **validated_data
        )

        # Resolve Subcategories
        seen = set()
        for name in subcat_names:
            nm = name.strip()
            if not nm or nm in seen:
                continue
            seen.add(nm)
            subcat, _ = SubCategory.objects.get_or_create(name=nm)
            subcat.products.add(product)

        return product

    def update(self, instance, validated_data):
        cat_name = validated_data.pop('category', None)
        supp_name = validated_data.pop('supplier', None)
        subcat_names = validated_data.pop('subcategory_names', None)

        if cat_name is not None:
            category = None
            if cat_name:
                category, _ = Category.objects.get_or_create(name=cat_name)
            instance.category = category

        if supp_name is not None:
            supplier = None
            if supp_name:
                supplier, _ = Supplier.objects.get_or_create(name=supp_name)
            instance.supplier = supplier

        if subcat_names is not None:
            instance.subcategories.clear()
            seen = set()
            for name in subcat_names:
                nm = name.strip()
                if not nm or nm in seen:
                    continue
                seen.add(nm)
                subcat, _ = SubCategory.objects.get_or_create(name=nm)
                subcat.products.add(instance)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.purchase_price = validated_data.get('purchase_price', instance.purchase_price)
        instance.sale_price_unit = validated_data.get('sale_price_unit', instance.sale_price_unit)
        instance.sale_price_kilo = validated_data.get('sale_price_kilo', instance.sale_price_kilo)
        instance.wholesale_price = validated_data.get('wholesale_price', instance.wholesale_price)
        instance.wholesale_quantity = validated_data.get('wholesale_quantity', instance.wholesale_quantity)
        instance.discount_surcharge = validated_data.get('discount_surcharge', instance.discount_surcharge)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.critical_stock = validated_data.get('critical_stock', instance.critical_stock)
        instance.stock_unit = validated_data.get('stock_unit', instance.stock_unit)
        instance.composed_product = validated_data.get('composed_product', instance.composed_product)
        instance.save()

        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # show related names
        rep['category'] = instance.category.name if instance.category else None
        rep['supplier'] = instance.supplier.name if instance.supplier else None
        rep['subcategories'] = [sc.name for sc in instance.subcategories.all()]
        return rep