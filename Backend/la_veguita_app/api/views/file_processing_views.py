import pdfplumber
import gc
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import PDFUploadSerializer, ProductSerializer, CategorySerializer
from ..models import Product, Category


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
            if (row[1] is None or
                    row[2] is None or
                    not row[1].isdigit() or
                    row[2] == ''):  # if code is invalid, or name is empty
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
            validated_row["category"] = row[8]
            validated_row["supplier"] = row[9]

            # added defaults
            validated_row["stock"] = "0"
            validated_row["entry_stock_unit"] = "unit"
            validated_row["exit_stock_unit"] = "unit"
            validated_row["composed_product"] = False


            # data treatment for numbers
            validated_row["purchase_price"] = validated_row["purchase_price"].lstrip("$ ").replace(".", "")
            validated_row["sale_price"] = validated_row["sale_price"].lstrip("$ ").replace(".", "")
            validated_row["wholesale_price"] = validated_row["wholesale_price"].lstrip("$ ").replace(".", "")
            validated_row["discount_surcharge"] = validated_row["discount_surcharge"].strip("%")
            return validated_row
        return None

    def create_or_modify_product(self, valid_row):
        result = 1  # Updated product
        try:
            product = Product.objects.get(id_product=valid_row["id_product"])
            if not self.is_changed(valid_row, product):
                return 0  # No Changes
            serializer = ProductSerializer(product, data=valid_row, partial=True)  # UPDATE
        except Product.DoesNotExist:
            serializer = ProductSerializer(data=valid_row)  # CREATE
            result = 2  # Created product

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return result
        print("INVALID SERIALIZED ROW: " + str(valid_row))
        return -1  # Invalid product

    def is_changed(self, row, product):
        return (row["id_product"] != product.id_product or
                row["description"] != product.description or
                row["purchase_price"] != product.purchase_price or
                row["sale_price"] != product.sale_price or
                row["wholesale_price"] != product.wholesale_price or
                row["wholesale_quantity"] != product.wholesale_quantity or
                row["discount_surcharge"] != product.discount_surcharge or
                row["critical_stock"] != product.critical_stock or
                row["category"] != product.category or
                row["supplier"] != product.supplier)


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
        result = 1  # Updated product
        try:
            category = Category.objects.get(id_category=valid_row["id_category"])
            if not self.is_changed(valid_row, category):
                return 0  # No Changes
            serializer = CategorySerializer(category, data=valid_row)  # UPDATE
        except Category.DoesNotExist:
            serializer = CategorySerializer(data=valid_row)  # CREATE
            result = 2  # Created product

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return result
        print("INVALID SERIALIZED ROW: " + str(valid_row))
        return -1  # Invalid product

    def is_changed(self, row, category):
        return (row["id_category"] != category.id_category or
                row["name"] != category.name)