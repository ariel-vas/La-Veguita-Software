from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from ..models import Product
from ..serializers import ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(active=True)


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = "id_product"

    def get_queryset(self):
        return Product.objects.filter(active=True)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.active = False
        product.save()
        return Response({"message": "Producto eliminado exitosamente."}, status=status.HTTP_200_OK)


class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_name = self.kwargs['category']
        return Product.objects.filter(category__name__iexact=category_name, active=True)


class ProductBySubCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_name = self.kwargs['subcategory']
        return Product.objects.filter(subcategories__name__iexact=subcategory_name, active=True).distinct()