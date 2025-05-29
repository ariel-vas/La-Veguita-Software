from django.shortcuts import render
from rest_framework import generics
from ..models import Product
from ..serializers import ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('subcategories')
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id_product"

class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_name = self.kwargs['category']
        return Product.objects.filter(category__name__iexact=category_name)
    
class ProductBySubCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_name = self.kwargs['subcategory']
        return Product.objects.filter(subcategories__name__iexact=subcategory_name).distinct()