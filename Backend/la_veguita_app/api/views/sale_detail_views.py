from django.utils.timezone import now
from django.db.models import Sum, F, FloatField, Value
from django.db.models.functions import ExtractMonth, Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from ..models import SaleDetail, Product, Batch, Category
from ..serializers import SaleDetailSerializer
from django.utils.dateparse import parse_date
import calendar


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


class Top10ProductsRevenue(APIView):
    def get(self, request):
        # Parámetros opcionales
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        queryset = SaleDetail.objects.all()

        if month and year:
            try:
                month = int(month)
                year = int(year)
                queryset = queryset.filter(
                    sale__datetime__month=month,
                    sale__datetime__year=year
                )
            except ValueError:
                return Response({"error": "Mes y año deben ser enteros válidos."}, status=status.HTTP_400_BAD_REQUEST)

        # Agrupar y ordenar por cantidad vendida
        product_sales = (
            queryset
            .values('product__id_product', 'product__name')
            .annotate(total_revenue=Sum('subtotal'))
            .order_by('-total_sold')[:10]  # TOP 10
        )

        return Response({
            "filter": {
                "month": month,
                "year": year
            },
            "top_10_products": product_sales
        }, status=status.HTTP_200_OK)
    
class Bottom10ProductsByRevenueView(APIView):
    def get(self, request):
        # Parámetros opcionales
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        queryset = SaleDetail.objects.all()

        if month and year:
            try:
                month = int(month)
                year = int(year)
                queryset = queryset.filter(
                    sale__datetime__month=month,
                    sale__datetime__year=year
                )
            except ValueError:
                return Response({"error": "Mes y año deben ser enteros válidos."}, status=status.HTTP_400_BAD_REQUEST)

        # Agrupar por producto, sumar subtotal, y ordenar ascendente
        product_sales = (
            queryset
            .values('product__id_product', 'product__name')
            .annotate(total_revenue=Sum('subtotal'))
            .order_by('total_revenue')[:10]
        )

        return Response({
            "filter": {
                "month": month,
                "year": year
            },
            "bottom_10_products_by_revenue": product_sales
        }, status=status.HTTP_200_OK)
    
class DailySalesReportView(APIView):
    def get(self, request):
        # Leer parámetro obligatorio: ?date=YYYY-MM-DD
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "El parámetro 'date' es obligatorio (formato YYYY-MM-DD)."}, status=status.HTTP_400_BAD_REQUEST)

        date = parse_date(date_str)
        if not date:
            return Response({"error": "Fecha inválida. Usa el formato YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar ventas del día
        sales = SaleDetail.objects.filter(sale__datetime__date=date)

        # Agrupar por producto
        report = (
            sales
            .values(
                product_id=F('product__id_product'),
                product_name=F('product__name'),
                exit_unit=F('product__exit_stock_unit'),
            )
            .annotate(
                total_quantity=Sum('quantity'),
                total_subtotal=Sum('subtotal')
            )
            .order_by('product_name')
        )

        return Response({
            "report_date": date,
            "products_sold": report
        }, status=status.HTTP_200_OK)

class MonthlyRevenueVsCostByProductView(APIView):
    def get(self, request):
        product_name = request.query_params.get('product_name')
        year = request.query_params.get('year')

        if not product_name or not year:
            return Response({"error": "Debes proporcionar 'product_name' y 'year'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "'year' debe ser un número entero."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(name__iexact=product_name)
        except Product.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener ingreso mensual agrupado por mes
        ingreso_por_mes = SaleDetail.objects.filter(
            product=product,
            sale_date__year=year
        ).annotate(
            mes=ExtractMonth('sale_date')
        ).values('mes').annotate(
            ingreso=Coalesce(Sum('subtotal'), 0)
        ).order_by('mes')

        # Crear diccionario mes->ingreso para consulta rápida
        ingreso_dict = {item['mes']: float(item['ingreso']) for item in ingreso_por_mes}

        # Obtener cantidad ingresada en bodega agrupada por mes (si tienes fecha en Batch)
        cantidad_por_mes = Batch.objects.filter(
            product=product,
            batch_date__year=year
        ).annotate(
            mes=ExtractMonth('batch_date')
        ).values('mes').annotate(
            cantidad=Coalesce(Sum('quantity'), 0)
        ).order_by('mes')

        cantidad_dict = {item['mes']: float(item['cantidad']) for item in cantidad_por_mes}

        # Para costo mensual, multiplicamos cantidad por precio compra (supone precio estable)
        # Si el precio puede cambiar, necesitarías otro enfoque.
        precio_compra_unitario = float(product.purchase_price)

        resultados = []
        for mes in range(1, 13):
            ingreso_mes = ingreso_dict.get(mes, 0.0)
            cantidad_mes = cantidad_dict.get(mes, 0.0)
            costo_mes = cantidad_mes * precio_compra_unitario
            utilidad_mes = ingreso_mes - costo_mes

            resultados.append({
                "mes_num": mes,
                "mes_nombre": calendar.month_name[mes],
                "ingreso": round(ingreso_mes, 2),
                "cantidad_ingresada": round(cantidad_mes, 2),
                "costo": round(costo_mes, 2),
                "utilidad": round(utilidad_mes, 2),
            })

        return Response({
            "product_id": product.id_product,
            "product_name": product.name,
            "year": year,
            "monthly_report": resultados
        })

class MonthlyRevenueVsCostByCategoryView(APIView):
    def get(self, request):
        category_name = request.query_params.get('category')
        year = request.query_params.get('year')

        if not category_name or not year:
            return Response({"error": "Debes proporcionar 'category' y 'year'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "'year' debe ser un número entero."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener productos de la categoría
        products = Product.objects.filter(category__name__iexact=category_name)
        if not products.exists():
            return Response({"error": "No se encontraron productos en esta categoría."}, status=status.HTTP_404_NOT_FOUND)

        # IDs de los productos para filtrar ventas y batches
        product_ids = products.values_list('id', flat=True)

        # Ingreso mensual por ventas
        ingreso_por_mes = SaleDetail.objects.filter(
            product_id__in=product_ids,
            sale_date__year=year
        ).annotate(
            mes=ExtractMonth('sale_date')
        ).values('mes').annotate(
            ingreso=Coalesce(Sum('subtotal'), 0)
        ).order_by('mes')
        ingreso_dict = {item['mes']: float(item['ingreso']) for item in ingreso_por_mes}

        # Cantidad mensual ingresada en bodega
        cantidad_por_mes = Batch.objects.filter(
            product_id__in=product_ids,
            batch_date__year=year
        ).annotate(
            mes=ExtractMonth('batch_date')
        ).values('mes', 'product_id').annotate(
            cantidad=Coalesce(Sum('quantity'), 0)
        )

        # Calcular costo mensual: sumar por producto (cantidad * precio compra)
        costo_dict = {}
        cantidad_dict = {}

        for item in cantidad_por_mes:
            mes = item['mes']
            cantidad = float(item['cantidad'])
            producto = products.get(id=item['product_id'])
            precio = float(producto.purchase_price)
            costo = cantidad * precio

            cantidad_dict[mes] = cantidad_dict.get(mes, 0) + cantidad
            costo_dict[mes] = costo_dict.get(mes, 0) + costo

        # Resultado final por mes
        resultados = []
        for mes in range(1, 13):
            ingreso = ingreso_dict.get(mes, 0.0)
            cantidad = cantidad_dict.get(mes, 0.0)
            costo = costo_dict.get(mes, 0.0)
            utilidad = ingreso - costo

            resultados.append({
                "mes_num": mes,
                "mes_nombre": calendar.month_name[mes],
                "ingreso": round(ingreso, 2),
                "cantidad_ingresada": round(cantidad, 2),
                "costo": round(costo, 2),
                "utilidad": round(utilidad, 2)
            })

        return Response({
            "category": category_name,
            "year": year,
            "monthly_report": resultados
        })
    
    
class MonthlyGrossProfitView(APIView):
    def get(self, request):
        year = request.query_params.get('year')

        if not year:
            return Response({"error": "Debes proporcionar 'year'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "'year' debe ser un número entero."}, status=status.HTTP_400_BAD_REQUEST)

        # Ingreso por mes (sumar ventas)
        ingreso_por_mes = SaleDetail.objects.filter(
            sale_date__year=year
        ).annotate(
            mes=ExtractMonth('sale_date')
        ).values('mes').annotate(
            ingreso=Coalesce(Sum('subtotal'), 0.0)
        )
        ingreso_dict = {item['mes']: float(item['ingreso']) for item in ingreso_por_mes}

        # Costos por mes (sumar cantidad × precio de compra por producto)
        cantidad_por_mes = Batch.objects.filter(
            batch_date__year=year
        ).annotate(
            mes=ExtractMonth('batch_date')
        ).values('mes', 'product_id').annotate(
            cantidad=Coalesce(Sum('quantity'), 0.0)
        )

        # Calcular costos por mes
        costo_dict = {}
        for item in cantidad_por_mes:
            mes = item['mes']
            cantidad = float(item['cantidad'])
            try:
                producto = Product.objects.get(id=item['product_id'])
                precio = float(producto.purchase_price)
                costo = cantidad * precio
                costo_dict[mes] = costo_dict.get(mes, 0.0) + costo
            except Product.DoesNotExist:
                continue

        # Generar resultado por mes
        resultado = []
        for mes in range(1, 13):
            ingreso = ingreso_dict.get(mes, 0.0)
            costo = costo_dict.get(mes, 0.0)
            ganancia = ingreso - costo

            resultado.append({
                "mes_num": mes,
                "mes_nombre": calendar.month_name[mes],
                "ingreso_total": round(ingreso, 2),
                "costo_total": round(costo, 2),
                "ganancia_bruta": round(ganancia, 2)
            })

        return Response({
            "year": year,
            "monthly_gross_profit": resultado
        })