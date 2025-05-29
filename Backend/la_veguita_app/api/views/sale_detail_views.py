from django.utils.timezone import now
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
    
class MonthlyProductSalesView(APIView):
    def get(self, request, id_product):
        today = now()
        # Obtener mes y año desde query params, o usar los actuales
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        try:
            month = int(month) if month else today.month
            year = int(year) if year else today.year
        except ValueError:
            return Response({"error": "Mes y año deben ser números enteros válidos."}, status=status.HTTP_400_BAD_REQUEST)

        if not (1 <= month <= 12):
            return Response({"error": "El mes debe estar entre 1 y 12."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar por mes y año
        sales = SaleDetail.objects.filter(
            product_id=id_product,
            sale__datetime__year=year,
            sale__datetime__month=month
        )

        total_quantity = sales.aggregate(total=Sum('quantity'))['total'] or 0

        return Response({
            "product_id": id_product,
            "year": year,
            "month": month,
            "quantity_sold": float(total_quantity)
        }, status=status.HTTP_200_OK)
