from django.shortcuts import render
from rest_framework import generics
from ..models import SubCategory
from ..serializers import SubCategorySerializer

class SubCategoryListCreate(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    lookup_field = "id_subcategory"