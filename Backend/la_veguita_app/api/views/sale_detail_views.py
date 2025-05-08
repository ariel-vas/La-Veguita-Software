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
    lookup_field = "id_sale_detail"