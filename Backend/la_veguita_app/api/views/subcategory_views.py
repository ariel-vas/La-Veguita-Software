from django.shortcuts import render
from rest_framework import generics
from ..models import SubCategory, Product
from ..serializers import SubCategorySerializer, ProductSerializer


class SubCategoryListCreate(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    lookup_field = "id_subcategory"


class ProductsBySubCategory(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs['id_subcategory']
        return Product.objects.filter(subcategories__id_subcategory=subcategory_id)