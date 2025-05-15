from django.shortcuts import render
from rest_framework import generics
from ..models import SaleDetail
from ..serializers import SaleDetailSerializer


class SaleDetailListCreate(generics.ListCreateAPIView):
    queryset = SaleDetail.objects.all()
    serializer_class = SaleDetailSerializer


class SaleDetailRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaleDetail.objects.all()
    serializer_class = SaleDetailSerializer

    def get_object(self):
        sale_id = self.kwargs['sale_id']
        product_id = self.kwargs['product_id']
        return SaleDetail.objects.get(sale__id_sale=sale_id, product__id_product=product_id)