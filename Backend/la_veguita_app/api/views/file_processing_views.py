import pdfplumber
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

            try:
                tables = []
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        # Extract tables from each page
                        page_tables = page.extract_tables()
                        for table in page_tables:
                            tables.append(table)

                # Product generation or updating
                for table in tables:
                    for row in table:
                        valid_row = self.get_validated_product_row(row)
                        if valid_row is not None:
                            self.create_or_modify_product(valid_row)

                return Response({
                    "message": "PDF processed successfully.",
                    "tables": tables[:2]  # Only show the first 2 tables for preview
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
            #validated_row["category"] = row[8]
            #validated_row["supplier"] = row[9]

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
        try:
            product = Product.objects.get(id_product=valid_row["id_product"])
            serializer = ProductSerializer(product, data=valid_row, partial=True)  # UPDATE
            print("UPDATING ROW: " + str(valid_row))
        except Product.DoesNotExist:
            serializer = ProductSerializer(data=valid_row)  # CREATE

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return
        print("INVALID SERIALIZED ROW: " + str(valid_row))


class CategoriesPDFProcessingView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['file']

            try:
                tables = []
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        # Extract tables from each page
                        page_tables = page.extract_tables()
                        for table in page_tables:
                            tables.append(table)

                # Product generation or updating
                for table in tables:
                    for row in table:
                        valid_row = self.get_validated_category_row(row)
                        if valid_row is not None:
                            self.create_or_modify_category(valid_row)

                return Response({
                    "message": "PDF processed successfully.",
                    "tables": tables
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
        try:
            category = Category.objects.get(id_category=valid_row["id_category"])
            serializer = CategorySerializer(category, data=valid_row)  # UPDATE
            print("UPDATING ROW: " + str(valid_row))
        except Category.DoesNotExist:
            serializer = CategorySerializer(data=valid_row)  # CREATE

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return
        print("INVALID SERIALIZED ROW: " + str(valid_row))