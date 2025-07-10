import pdfplumber
import gc
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import PDFUploadSerializer, ProductSerializer, CategorySerializer, SupplierSerializer
from ..models import Product, Category, Supplier

"""
    post:
    Procesa un archivo PDF con una tabla de productos. Extrae filas válidas para crear o actualizar productos.

    Cada fila debe tener 13 columnas específicas. Las filas inválidas serán ignoradas. Se identifican los productos por su `id_product`.

    Entradas (multipart/form-data):
        - file (File): Archivo PDF que contiene una o más tablas de productos.

    Proceso:
        - Crea productos si no existen.
        - Actualiza productos si han cambiado.
        - Ignora productos sin cambios.
        - Registra errores de validación si los datos no son válidos.

    Salida (JSON):
        - message (str): Estado general del procesamiento.
        - total_count (int): Total de filas procesadas.
        - update_count (int): Productos actualizados.
        - create_count (int): Productos creados.
        - invalid_count (int): Filas inválidas.
        - no_change_count (int): Productos que no necesitaban cambios.
"""
class ProductsPDFProcessingView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['file']
            update_count = 0
            create_count = 0
            invalid_count = 0
            no_change_count = 0

            try:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        for table in page.extract_tables():
                            for row in table:
                                valid_row = self.get_validated_product_row(row)
                                if valid_row is not None:
                                    created = self.create_or_modify_product(valid_row)
                                    if created == -1:
                                        invalid_count += 1
                                    elif created == 0:
                                        no_change_count += 1
                                    elif created == 1:
                                        update_count += 1
                                    elif created == 2:
                                        create_count += 1
                        page.flush_cache()
                        page.get_textmap.cache_clear()
                del pdf_file
                gc.collect()

                return Response({
                    "message": "PDF processed successfully.",
                    "total_count": update_count + create_count + invalid_count + no_change_count,
                    "update_count": update_count,
                    "create_count": create_count,
                    "invalid_count": invalid_count,
                    "no_change_count": no_change_count
                })
            except Exception as e:
                return Response({"error": f"Failed to process PDF: {str(e)}"}, status=400)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_validated_product_row(self, row):
        validated_row = {}
        if isinstance(row, list) and len(row) == 13:
            if (row[1] is None or  # TODO: VALIDACION MAS COMPLETA DE CADA CAMPO
                    row[2] is None or
                    row[1] == '' or
                    row[2] == '' or
                    not row[8].isdigit()):  # if code or name is invalid or empty, or family is not id
                print("EXCLUDING INVALID ROW: " + str(row))
                return None

            # row dictionary creation
            validated_row["id_product"] = row[1]
            validated_row["description"] = row[2]
            validated_row["purchase_price"] = row[6]
            validated_row["sale_price"] = row[3]
            validated_row["wholesale_price"] = row[4]
            validated_row["wholesale_quantity"] = row[5]
            validated_row["discount_surcharge"] = row[12]
            validated_row["critical_stock"] = row[11]
            if row[7].strip() == "PESABLE":
                validated_row["exit_stock_unit"] = "kilo"
            else:
                validated_row["exit_stock_unit"] = "unit"

            # handle foreign keys
            try:
                category = Category.objects.get(id_category=row[8])
                validated_row["category"] = category.name
            except Category.DoesNotExist:
                validated_row["category"] = ""
                print(f"WARNING: Category with code {row[8]} does not exist, defaulting to blank category.")
            try:
                supplier = Supplier.objects.get(rut=row[9])
                validated_row["supplier"] = supplier.rut
            except Supplier.DoesNotExist:
                validated_row["supplier"] = ""
                print(f"WARNING: Supplier with rut {row[9]} does not exist, defaulting to blank supplier.")

            # added defaults for app exclusive attributes
            validated_row["stock"] = "0"
            validated_row["entry_stock_unit"] = "unit"
            validated_row["composed_product"] = False
            validated_row["active"] = True  # Make product active

            # data treatment for numbers
            validated_row["purchase_price"] = validated_row["purchase_price"].lstrip("$ ").replace(".", "")
            validated_row["sale_price"] = validated_row["sale_price"].lstrip("$ ").replace(".", "")
            validated_row["wholesale_price"] = validated_row["wholesale_price"].lstrip("$ ").replace(".", "")
            validated_row["discount_surcharge"] = validated_row["discount_surcharge"].strip("%")

            return validated_row
        return None

    def create_or_modify_product(self, valid_row):
        try:
            # try to update product
            result = 1  # Updated product
            product = Product.objects.get(id_product=valid_row["id_product"])

            # mantain data native to our app, since list will have invalid data
            valid_row["stock"] = product.stock
            valid_row["composed_product"] = product.composed_product
            valid_row["entry_stock_unit"] = product.entry_stock_unit

            if not self.is_changed(valid_row, product):
                return 0  # No Changes
            serializer = ProductSerializer(product, data=valid_row, partial=True)

        except Product.DoesNotExist:
            # if no product exists with id, create product
            serializer = ProductSerializer(data=valid_row)
            result = 2  # Created product

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return result
        print("INVALID SERIALIZED ROW: " + str(valid_row))
        return -1  # Invalid product

    def is_changed(self, row, product):
        category = product.category
        if category is None:
            category = ""
        supplier = product.supplier
        if supplier is None:
            supplier = ""
        return (str(row["id_product"]) != str(product.id_product) or
                str(row["description"]) != str(product.description) or
                Decimal(row["purchase_price"]) != product.purchase_price or
                Decimal(row["sale_price"]) != product.sale_price or
                Decimal(row["wholesale_price"]) != product.wholesale_price or
                Decimal(row["wholesale_quantity"]) != product.wholesale_quantity or
                Decimal(row["discount_surcharge"]) != product.discount_surcharge or
                Decimal(row["critical_stock"]) != product.critical_stock or
                str(row["exit_stock_unit"]) != str(product.exit_stock_unit) or
                str(row["category"]) != str(category) or
                str(row["supplier"]) != str(supplier))


"""
    post:
    Procesa un archivo PDF con una tabla de categorías. Extrae filas válidas para crear o actualizar categorías.

    Cada fila debe tener exactamente 3 columnas: código, nombre, y posiblemente otra columna no usada. Solo se valida código y nombre.

    Entradas (multipart/form-data):
        - file (File): Archivo PDF que contiene una o más tablas de categorías.

    Proceso:
        - Crea categorías si no existen.
        - Actualiza categorías si han cambiado.
        - Ignora categorías sin cambios.
        - Registra errores de validación si los datos no son válidos.

    Salida (JSON):
        - message (str): Estado general del procesamiento.
        - total_count (int): Total de filas procesadas.
        - update_count (int): Categorías actualizadas.
        - create_count (int): Categorías creadas.
        - invalid_count (int): Filas inválidas.
        - no_change_count (int): Categorías que no necesitaban cambios.
"""
class CategoriesPDFProcessingView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['file']
            update_count = 0
            create_count = 0
            invalid_count = 0
            no_change_count = 0

            try:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        for table in page.extract_tables():
                            for row in table:
                                valid_row = self.get_validated_category_row(row)
                                if valid_row is not None:
                                    created = self.create_or_modify_category(valid_row)
                                    if created == -1:
                                        invalid_count += 1
                                    elif created == 0:
                                        no_change_count += 1
                                    elif created == 1:
                                        update_count += 1
                                    elif created == 2:
                                        create_count += 1
                        page.flush_cache()
                        page.get_textmap.cache_clear()
                del pdf_file
                gc.collect()

                return Response({
                    "message": "PDF processed successfully.",
                    "total_count": update_count + create_count + invalid_count + no_change_count,
                    "update_count": update_count,
                    "create_count": create_count,
                    "invalid_count": invalid_count,
                    "no_change_count": no_change_count
                })
            except Exception as e:
                return Response({"error": f"Failed to process PDF: {str(e)}"}, status=400)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_validated_category_row(self, row):
        validated_row = {}
        if isinstance(row, list) and len(row) == 3:
            if (row[0] is None or
                    row[1] is None or
                    not row[0].isdigit() or
                    row[1] == ''):  # if code is invalid, or name is empty
                print("EXCLUDING INVALID ROW: " + str(row))
                return None

            # row dictionary creation
            validated_row["id_category"] = row[0]
            validated_row["name"] = row[1]

            return validated_row
        return None

    def create_or_modify_category(self, valid_row):
        result = 1  # Updated category
        try:
            category = Category.objects.get(id_category=valid_row["id_category"])
            if not self.is_changed(valid_row, category):
                return 0  # No Changes
            serializer = CategorySerializer(category, data=valid_row)  # UPDATE
        except Category.DoesNotExist:
            serializer = CategorySerializer(data=valid_row)  # CREATE
            result = 2  # Created category

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return result
        print("INVALID SERIALIZED ROW: " + str(valid_row))
        return -1  # Invalid category

    def is_changed(self, row, category):
        return (str(row["id_category"]) != str(category.id_category) or
                str(row["name"]) != str(category.name))


class SuppliersPDFProcessingView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['file']
            update_count = 0
            create_count = 0
            invalid_count = 0
            no_change_count = 0

            try:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        for table in page.extract_tables():
                            for row in table:
                                valid_row = self.get_validated_supplier_row(row)
                                if valid_row is not None:
                                    created = self.create_or_modify_supplier(valid_row)
                                    if created == -1:
                                        invalid_count += 1
                                    elif created == 0:
                                        no_change_count += 1
                                    elif created == 1:
                                        update_count += 1
                                    elif created == 2:
                                        create_count += 1
                        page.flush_cache()
                        page.get_textmap.cache_clear()
                del pdf_file
                gc.collect()

                return Response({
                    "message": "PDF processed successfully.",
                    "total_count": update_count + create_count + invalid_count + no_change_count,
                    "update_count": update_count,
                    "create_count": create_count,
                    "invalid_count": invalid_count,
                    "no_change_count": no_change_count
                })
            except Exception as e:
                return Response({"error": f"Failed to process PDF: {str(e)}"}, status=400)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_validated_supplier_row(self, row):
        validated_row = {}
        if isinstance(row, list) and len(row) == 9:
            if (row[0] is None or
                    row[1] is None or
                    row[1] == '' or
                    row[1] == ''):  # if code or name is empty
                print("EXCLUDING INVALID ROW: " + str(row))
                return None

            # row dictionary creation
            validated_row["rut"] = row[0]
            validated_row["name"] = row[1]
            validated_row["line"] = row[2]
            validated_row["address"] = row[3]
            validated_row["commune"] = row[4]
            validated_row["city"] = row[5]
            validated_row["telephone"] = row[6]
            validated_row["cellphone"] = row[7]
            validated_row["email"] = row[8]

            return validated_row
        return None

    def create_or_modify_supplier(self, valid_row):
        result = 1  # Updated supplier
        try:
            supplier = Supplier.objects.get(rut=valid_row["rut"])
            if not self.is_changed(valid_row, supplier):
                return 0  # No Changes
            serializer = SupplierSerializer(supplier, data=valid_row)  # UPDATE
        except Supplier.DoesNotExist:
            serializer = SupplierSerializer(data=valid_row)  # CREATE
            result = 2  # Created supplier

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return result
        print("INVALID SERIALIZED ROW: " + str(valid_row))
        return -1  # Invalid supplier

    def is_changed(self, row, supplier):
        return (str(row["rut"]) != str(supplier.rut) or
                str(row["name"]) != str(supplier.name) or
                str(row["line"]) != str(supplier.name) or
                str(row["address"]) != str(supplier.name) or
                str(row["commune"]) != str(supplier.name) or
                str(row["city"]) != str(supplier.name) or
                str(row["telephone"]) != str(supplier.name) or
                str(row["cellphone"]) != str(supplier.name) or
                str(row["email"]) != str(supplier.name))