from datetime import date, datetime, timedelta
from django.utils.timezone import now
from django.db.models import Sum, DecimalField
from django.db.models.functions import ExtractMonth, ExtractYear, Coalesce
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

        # Agrupar y ordenar por ingresos totales (revenue)
        product_sales = (
            queryset
            .values('product__id_product', 'product__description')  # Cambiado 'name' por 'description'
            .annotate(total_revenue=Sum('subtotal'))
            .order_by('-total_revenue')[:10]  # Corregido: ordenar por total_revenue
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
            .values('product__id_product', 'product__description')
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
            .values('product__id_product','product__description','product__exit_stock_unit')
            .annotate(
                total_quantity=Sum('quantity'),
                total_subtotal=Sum('subtotal')
            )
            .order_by('product__description')
        )

        return Response({
            "report_date": date,
            "products_sold": report
        }, status=status.HTTP_200_OK)

class MonthlyRevenueVsCostByProductView(APIView):
    def get(self, request):
        product_description = request.query_params.get('product_description')
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not product_description or not year or not month:
            return Response({"error": "Debes proporcionar 'product_description', 'year' y 'month'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"error": "'year' y 'month' deben ser números enteros."}, status=status.HTTP_400_BAD_REQUEST)

        if month < 1 or month > 12:
            return Response({"error": "'month' debe estar entre 1 y 12."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(description__iexact=product_description)
        except Product.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Función auxiliar para restar meses
        def restar_meses(fecha, meses):
            año = fecha.year
            mes = fecha.month
            
            mes -= meses
            while mes <= 0:
                mes += 12
                año -= 1
            
            return datetime(año, mes, 1)

        # Calcular fecha de inicio (12 meses antes del mes/año seleccionado)
        fecha_fin = datetime(year, month, 1)
        fecha_inicio = restar_meses(fecha_fin, 11)

        # Obtener ingreso mensual agrupado por año y mes
        # Calculamos el mes siguiente para el límite superior
        if fecha_fin.month < 12:
            fecha_limite = datetime(fecha_fin.year, fecha_fin.month + 1, 1)
        else:
            fecha_limite = datetime(fecha_fin.year + 1, 1, 1)

        ingreso_por_mes = SaleDetail.objects.filter(
            product=product,
            sale__datetime__gte=fecha_inicio,
            sale__datetime__lt=fecha_limite
        ).annotate(
            año=ExtractYear('sale__datetime'),
            mes=ExtractMonth('sale__datetime')
        ).values('año', 'mes').annotate(
            ingreso=Coalesce(Sum('subtotal', output_field=DecimalField()), 0, output_field=DecimalField())
        ).order_by('año', 'mes')

        # Crear diccionario (año, mes)->ingreso para consulta rápida
        ingreso_dict = {(item['año'], item['mes']): float(item['ingreso']) for item in ingreso_por_mes}

        # Obtener cantidad ingresada en bodega agrupada por año y mes
        cantidad_por_mes = Batch.objects.filter(
            product=product,
            entry_date__gte=fecha_inicio,
            entry_date__lt=fecha_limite
        ).annotate(
            año=ExtractYear('entry_date'),
            mes=ExtractMonth('entry_date')
        ).values('año', 'mes').annotate(
            cantidad=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField())
        ).order_by('año', 'mes')

        cantidad_dict = {(item['año'], item['mes']): float(item['cantidad']) for item in cantidad_por_mes}

        # Para costo mensual, multiplicamos cantidad por precio compra
        precio_compra_unitario = float(product.purchase_price)

        # Función auxiliar para sumar meses
        def sumar_mes(fecha):
            año = fecha.year
            mes = fecha.month + 1
            
            if mes > 12:
                mes = 1
                año += 1
            
            return datetime(año, mes, 1)

        resultados = []
        fecha_actual = fecha_inicio
        
        # Generar los últimos 12 meses
        for i in range(12):
            año_actual = fecha_actual.year
            mes_actual = fecha_actual.month
            
            ingreso_mes = ingreso_dict.get((año_actual, mes_actual), 0.0)
            cantidad_mes = cantidad_dict.get((año_actual, mes_actual), 0.0)
            costo_mes = cantidad_mes * precio_compra_unitario
            utilidad_mes = ingreso_mes - costo_mes

            resultados.append({
                "año": año_actual,
                "mes_num": mes_actual,
                "mes_nombre": calendar.month_name[mes_actual],
                "ingreso": round(ingreso_mes, 2),
                "cantidad_ingresada": round(cantidad_mes, 2),
                "costo": round(costo_mes, 2),
                "utilidad": round(utilidad_mes, 2),
            })
            
            # Avanzar al siguiente mes
            fecha_actual = sumar_mes(fecha_actual)

        return Response({
            "product_id": product.id_product,
            "product_description": product.description,
            "fecha_inicio": fecha_inicio.strftime("%Y-%m"),
            "fecha_fin": fecha_fin.strftime("%Y-%m"),
            "monthly_report": resultados
        }, status=status.HTTP_200_OK)

class MonthlyRevenueVsCostByCategoryView(APIView):
    def get(self, request):
        category_name = request.query_params.get('category')
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not category_name or not year or not month:
            return Response({"error": "Debes proporcionar 'category', 'year' y 'month'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"error": "'year' y 'month' deben ser números enteros."}, status=status.HTTP_400_BAD_REQUEST)

        if month < 1 or month > 12:
            return Response({"error": "'month' debe estar entre 1 y 12."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener productos de la categoría
        products = Product.objects.filter(category__name__iexact=category_name)
        if not products.exists():
            return Response({"error": "No se encontraron productos en esta categoría."}, status=status.HTTP_404_NOT_FOUND)

        # IDs de los productos para filtrar ventas y batches
        product_ids = products.values_list('id_product', flat=True)

        # Función auxiliar para restar meses
        def restar_meses(fecha, meses):
            año = fecha.year
            mes = fecha.month
            
            mes -= meses
            while mes <= 0:
                mes += 12
                año -= 1
            
            return datetime(año, mes, 1)

        # Calcular fecha de inicio (12 meses antes del mes/año seleccionado)
        fecha_fin = datetime(year, month, 1)
        fecha_inicio = restar_meses(fecha_fin, 11)

        # Calculamos el mes siguiente para el límite superior
        if fecha_fin.month < 12:
            fecha_limite = datetime(fecha_fin.year, fecha_fin.month + 1, 1)
        else:
            fecha_limite = datetime(fecha_fin.year + 1, 1, 1)

        # Ingreso mensual por ventas
        ingreso_por_mes = SaleDetail.objects.filter(
            product__id_product__in=product_ids,
            sale__datetime__gte=fecha_inicio,
            sale__datetime__lt=fecha_limite
        ).annotate(
            año=ExtractYear('sale__datetime'),
            mes=ExtractMonth('sale__datetime')
        ).values('año', 'mes').annotate(
            ingreso=Coalesce(Sum('subtotal', output_field=DecimalField()), 0, output_field=DecimalField())
        ).order_by('año', 'mes')

        # Crear diccionario (año, mes)->ingreso para consulta rápida
        ingreso_dict = {(item['año'], item['mes']): float(item['ingreso']) for item in ingreso_por_mes}

        # Cantidad mensual ingresada en bodega
        cantidad_por_mes = Batch.objects.filter(
            product__id_product__in=product_ids,
            entry_date__gte=fecha_inicio,
            entry_date__lt=fecha_limite
        ).annotate(
            año=ExtractYear('entry_date'),
            mes=ExtractMonth('entry_date')
        ).values('año', 'mes', 'product__id_product').annotate(
            cantidad=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField())
        )

        # Calcular costo mensual: sumar por producto (cantidad * precio compra)
        costo_dict = {}
        cantidad_dict = {}

        for item in cantidad_por_mes:
            año = item['año']
            mes = item['mes']
            clave_mes = (año, mes)
            cantidad = float(item['cantidad'])
            producto = products.get(id_product=item['product__id_product'])
            precio = float(producto.purchase_price)
            costo = cantidad * precio

            cantidad_dict[clave_mes] = cantidad_dict.get(clave_mes, 0) + cantidad
            costo_dict[clave_mes] = costo_dict.get(clave_mes, 0) + costo

        # Función auxiliar para sumar meses
        def sumar_mes(fecha):
            año = fecha.year
            mes = fecha.month + 1
            
            if mes > 12:
                mes = 1
                año += 1
            
            return datetime(año, mes, 1)

        # Resultado final por mes
        resultados = []
        fecha_actual = fecha_inicio
        
        # Generar los últimos 12 meses
        for i in range(12):
            año_actual = fecha_actual.year
            mes_actual = fecha_actual.month
            clave_mes = (año_actual, mes_actual)
            
            ingreso = ingreso_dict.get(clave_mes, 0.0)
            cantidad = cantidad_dict.get(clave_mes, 0.0)
            costo = costo_dict.get(clave_mes, 0.0)
            utilidad = ingreso - costo

            resultados.append({
                "año": año_actual,
                "mes_num": mes_actual,
                "mes_nombre": calendar.month_name[mes_actual],
                "ingreso": round(ingreso, 2),
                "cantidad_ingresada": round(cantidad, 2),
                "costo": round(costo, 2),
                "utilidad": round(utilidad, 2)
            })
            
            # Avanzar al siguiente mes
            fecha_actual = sumar_mes(fecha_actual)

        return Response({
            "category": category_name,
            "fecha_inicio": fecha_inicio.strftime("%Y-%m"),
            "fecha_fin": fecha_fin.strftime("%Y-%m"),
            "monthly_report": resultados
        }, status=status.HTTP_200_OK)
    
    
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
            sale__datetime__year=year
        ).annotate(
            mes=ExtractMonth('sale__datetime')
        ).values('mes').annotate(
            ingreso=Coalesce(Sum('subtotal', output_field=DecimalField()), 0, output_field=DecimalField())
        )
        ingreso_dict = {item['mes']: float(item['ingreso']) for item in ingreso_por_mes}

        # Costos por mes (sumar cantidad × precio de compra por producto)
        cantidad_por_mes = Batch.objects.filter(
            entry_date__year=year
        ).annotate(
            mes=ExtractMonth('entry_date')
        ).values('mes', 'product__id_product').annotate(
            cantidad=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField())
        )

        # Calcular costos por mes
        costo_dict = {}
        for item in cantidad_por_mes:
            mes = item['mes']
            cantidad = float(item['cantidad'])
            try:
                producto = Product.objects.get(id_product=item['product__id_product'])
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
        }, status=status.HTTP_200_OK)
    
class Top10MostProfitableProductsView(APIView):
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response({"error": "Debes proporcionar 'month' y 'year'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = int(month)
            year = int(year)
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")
        except ValueError:
            return Response({"error": "'month' y 'year' deben ser números enteros válidos. El mes debe estar entre 1 y 12."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener ingresos por producto en el mes/año especificado
        ingresos_por_producto = SaleDetail.objects.filter(
            sale__datetime__month=month,
            sale__datetime__year=year
        ).values(
            'product__id_product',
            'product__description'
        ).annotate(
            ingreso_total=Coalesce(Sum('subtotal', output_field=DecimalField()), 0, output_field=DecimalField())
        )

        # Crear diccionario producto_id -> ingreso
        ingresos_dict = {item['product__id_product']: float(item['ingreso_total']) for item in ingresos_por_producto}
        
        # Crear diccionario producto_id -> descripción
        productos_info = {item['product__id_product']: item['product__description'] for item in ingresos_por_producto}

        # Obtener costos por producto en el mes/año especificado (cantidad ingresada * precio compra)
        costos_por_producto = Batch.objects.filter(
            entry_date__month=month,
            entry_date__year=year
        ).values(
            'product__id_product'
        ).annotate(
            cantidad_total=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField())
        )

        # Calcular costos por producto
        costos_dict = {}
        for item in costos_por_producto:
            product_id = item['product__id_product']
            cantidad = float(item['cantidad_total'])
            
            try:
                producto = Product.objects.get(id_product=product_id)
                precio_compra = float(producto.purchase_price)
                costo_total = cantidad * precio_compra
                costos_dict[product_id] = costo_total
                
                # Agregar descripción si no existe (por si un producto tiene costos pero no ventas)
                if product_id not in productos_info:
                    productos_info[product_id] = producto.description
                    
            except Product.DoesNotExist:
                continue

        # Calcular rentabilidad por producto
        rentabilidad_productos = []
        
        # Obtener todos los productos que tuvieron actividad (ingresos o costos)
        todos_productos = set(ingresos_dict.keys()) | set(costos_dict.keys())
        
        for product_id in todos_productos:
            ingreso = ingresos_dict.get(product_id, 0.0)
            costo = costos_dict.get(product_id, 0.0)
            rentabilidad = ingreso - costo
            
            # Solo incluir productos con rentabilidad calculable
            if product_id in productos_info:
                rentabilidad_productos.append({
                    'product_id': product_id,
                    'product_description': productos_info[product_id],
                    'ingreso_total': round(ingreso, 2),
                    'costo_total': round(costo, 2),
                    'rentabilidad': round(rentabilidad, 2)
                })

        # Ordenar por rentabilidad descendente y tomar top 10
        top_10_rentables = sorted(rentabilidad_productos, key=lambda x: x['rentabilidad'], reverse=True)[:10]

        return Response({
            "filter": {
                "month": month,
                "month_name": calendar.month_name[month],
                "year": year
            },
            "top_10_most_profitable_products": top_10_rentables
        }, status=status.HTTP_200_OK)
    
class ProductInventoryFlowView(APIView):
    def get(self, request, product_id):
        if not product_id:
            return Response({"error": "Debes proporcionar 'product_id'."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar que el producto existe
        try:
            product = Product.objects.get(id_product=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener fecha actual
        today = date.today()
        current_month = today.month
        current_year = today.year

        # Calcular rango de fechas (desde el mes siguiente del año pasado hasta el mes actual)
        start_month = current_month + 1 if current_month < 12 else 1
        start_year = current_year - 1 if current_month < 12 else current_year

        # Generar lista de meses a consultar
        months_to_query = []
        temp_month = start_month
        temp_year = start_year
        
        for _ in range(12):
            months_to_query.append((temp_month, temp_year))
            temp_month += 1
            if temp_month > 12:
                temp_month = 1
                temp_year += 1

        # Obtener ventas por mes
        sales_data = SaleDetail.objects.filter(
            product__id_product=product_id
        ).annotate(
            mes=ExtractMonth('sale__datetime'),
            año=ExtractYear('sale__datetime')
        ).values('mes', 'año').annotate(
            cantidad_vendida=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField()),
        )

        # Crear diccionario de ventas (mes, año) -> datos
        sales_dict = {}
        for item in sales_data:
            key = (item['mes'], item['año'])
            sales_dict[key] = {
                'cantidad_vendida': float(item['cantidad_vendida'])
            }

        # Obtener restock (entradas de inventario) por mes
        restock_data = Batch.objects.filter(
            product__id_product=product_id
        ).annotate(
            mes=ExtractMonth('entry_date'),
            año=ExtractYear('entry_date')
        ).values('mes', 'año').annotate(
            cantidad_ingresada=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField())
        )

        # Crear diccionario de restock (mes, año) -> datos
        restock_dict = {}
        for item in restock_data:
            key = (item['mes'], item['año'])
            restock_dict[key] = {
                'cantidad_ingresada': float(item['cantidad_ingresada'])
            }

        # Generar reporte mensual
        monthly_flow = []
        
        for month, year in months_to_query:
            key = (month, year)
            
            # Datos de ventas
            sales_info = sales_dict.get(key, {'cantidad_vendida': 0.0})
            cantidad_vendida = sales_info['cantidad_vendida']
            
            # Datos de restock
            restock_info = restock_dict.get(key, {'cantidad_ingresada': 0.0})
            cantidad_ingresada = restock_info['cantidad_ingresada']
            
            # Calcular flujo neto (positivo = entrada, negativo = salida)
            flujo_neto = cantidad_ingresada - cantidad_vendida
            
            
            monthly_flow.append({
                "mes_num": month,
                "mes_nombre": calendar.month_name[month],
                "año": year,
                "cantidad_vendida": round(cantidad_vendida, 4),
                "cantidad_ingresada": round(cantidad_ingresada, 4),
                "flujo_neto": round(flujo_neto, 4)
            })

        return Response({
            "product_id": product.id_product,
            "product_description": product.description,
            "current_stock": float(product.stock),
            "period": {
                "from": f"{calendar.month_name[start_month]} {start_year}",
                "to": f"{calendar.month_name[current_month]} {current_year}"
            },
            "inventory_flow": monthly_flow,
            "summary": {
                "total_sold_12_months": round(sum(item['cantidad_vendida'] for item in monthly_flow), 4),
                "total_restocked_12_months": round(sum(item['cantidad_ingresada'] for item in monthly_flow), 4),
                "net_flow_12_months": round(sum(item['flujo_neto'] for item in monthly_flow), 4)
            }
        }, status=status.HTTP_200_OK)
    
class ProductSalesVarianceView(APIView):
    def get(self, request):
        product_id = request.query_params.get('product_id')
        selected_month = request.query_params.get('month')
        selected_year = request.query_params.get('year')
        
        if not product_id:
            return Response({"error": "Debes proporcionar 'product_id'."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar que el producto existe
        try:
            product = Product.objects.get(id_product=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener fecha actual o usar la seleccionada
        today = date.today()
        if selected_month and selected_year:
            try:
                current_month = int(selected_month)
                current_year = int(selected_year)
                
                # Validar que el mes esté en rango válido
                if current_month < 1 or current_month > 12:
                    return Response({"error": "El mes debe estar entre 1 y 12."}, status=status.HTTP_400_BAD_REQUEST)
                    
            except ValueError:
                return Response({"error": "Mes y año deben ser números enteros."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            current_month = today.month
            current_year = today.year

        # Obtener ventas del mes seleccionado
        ventas_mes_seleccionado = SaleDetail.objects.filter(
            product__id_product=product_id,
            sale__datetime__month=current_month,
            sale__datetime__year=current_year
        ).aggregate(
            cantidad_vendida=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField()),
            ingresos=Coalesce(Sum('subtotal', output_field=DecimalField()), 0, output_field=DecimalField())
        )

        # Calcular mes anterior
        if current_month == 1:
            mes_anterior = 12
            año_mes_anterior = current_year - 1
        else:
            mes_anterior = current_month - 1
            año_mes_anterior = current_year

        # Obtener ventas del mes anterior
        ventas_mes_anterior = SaleDetail.objects.filter(
            product__id_product=product_id,
            sale__datetime__month=mes_anterior,
            sale__datetime__year=año_mes_anterior
        ).aggregate(
            cantidad_vendida=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField()),
            ingresos=Coalesce(Sum('subtotal', output_field=DecimalField()), 0, output_field=DecimalField())
        )

        # Calcular mes anterior 2 (dos meses atrás)
        if mes_anterior == 1:
            mes_anterior_2 = 12
            año_mes_anterior_2 = año_mes_anterior - 1
        else:
            mes_anterior_2 = mes_anterior - 1
            año_mes_anterior_2 = año_mes_anterior

        # Obtener ventas del mes anterior 2
        ventas_mes_anterior_2 = SaleDetail.objects.filter(
            product__id_product=product_id,
            sale__datetime__month=mes_anterior_2,
            sale__datetime__year=año_mes_anterior_2
        ).aggregate(
            cantidad_vendida=Coalesce(Sum('quantity', output_field=DecimalField()), 0, output_field=DecimalField()),
            ingresos=Coalesce(Sum('subtotal', output_field=DecimalField()), 0, output_field=DecimalField())
        )

        # Convertir a float para cálculos
        cantidad_mes_seleccionado = float(ventas_mes_seleccionado['cantidad_vendida'])
        cantidad_mes_anterior = float(ventas_mes_anterior['cantidad_vendida'])
        cantidad_mes_anterior_2 = float(ventas_mes_anterior_2['cantidad_vendida'])

        # Calcular varianza porcentual del mes anterior con respecto al mes seleccionado
        varianza_mes_anterior = 0
        if cantidad_mes_anterior > 0:
            varianza_mes_anterior = ((cantidad_mes_seleccionado - cantidad_mes_anterior) / cantidad_mes_anterior) * 100
        elif cantidad_mes_seleccionado > 0:
            varianza_mes_anterior = 100  # -100% si el mes seleccionado fue 0 pero el anterior tuvo ventas

        # Calcular varianza porcentual del mes anterior 2 con respecto al mes seleccionado
        varianza_mes_anterior_2 = 0
        if cantidad_mes_anterior_2 > 0:
            varianza_mes_anterior_2 = ((cantidad_mes_seleccionado - cantidad_mes_anterior_2) / cantidad_mes_anterior_2) * 100
        elif cantidad_mes_seleccionado > 0:
            varianza_mes_anterior_2 = 100  # -100% si el mes seleccionado fue 0 pero el anterior 2 tuvo ventas

        return Response({
            "product_id": product.id_product,
            "product_description": product.description,
            "analysis_date": today.strftime('%Y-%m-%d'),
            "mes_seleccionado": {
                "mes": f"{calendar.month_name[current_month]} {current_year}",
                "mes_num": current_month,
                "año": current_year,
                "cantidad_vendida": round(cantidad_mes_seleccionado, 4),
                "automatico": not (selected_month and selected_year)
            },
            "mes_anterior": {
                "mes": f"{calendar.month_name[mes_anterior]} {año_mes_anterior}",
                "mes_num": mes_anterior,
                "año": año_mes_anterior,
                "cantidad_vendida": round(cantidad_mes_anterior, 4),
                "varianza_porcentual": round(varianza_mes_anterior, 2)
            },
            "mes_anterior_2": {
                "mes": f"{calendar.month_name[mes_anterior_2]} {año_mes_anterior_2}",
                "mes_num": mes_anterior_2,
                "año": año_mes_anterior_2,
                "cantidad_vendida": round(cantidad_mes_anterior_2, 4),
                "varianza_porcentual": round(varianza_mes_anterior_2, 2)
            }
        }, status=status.HTTP_200_OK)