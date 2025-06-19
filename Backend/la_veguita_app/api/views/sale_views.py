from django.shortcuts import render
import os
from datetime import datetime
import re
import xml.etree.ElementTree as ET
from decimal import Decimal
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics
from rest_framework.views import APIView
from ..models import Sale, SaleDetail, Product, Batch, LastProcessedReceipt
from ..serializers import SaleSerializer


class SaleListCreate(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class SaleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    lookup_field = "id_sale"


class DailyStockUpdate(APIView):
    # Path to the folder synced with Google Drive
    FOLDER_PATH = r"C:\Users\User\Desktop\test_xmls"

    def post(self, request, *args, **kwargs):

        # Match filenames like "printer_A_123.txt"
        pattern = re.compile(r"^(\d+)_(\d+)\.xml$")

        try:
            # Get or create singleton row
            last_record, created = LastProcessedReceipt.objects.get_or_create(id=1)
            last_num = last_record.last_num

            new_files = []

            # Get relevant file names after last_num
            for filename in os.listdir(self.FOLDER_PATH):
                match = pattern.match(filename)
                if match:
                    file_num = int(match.group(2))
                    if file_num > last_num:
                        full_path = os.path.join(self.FOLDER_PATH, filename)
                        new_files.append((file_num, full_path))

            new_files.sort()  # Sort by file_num

            # Process files
            for file_num, filepath in new_files:
                self.process_receipt(filepath)
                print(f"Processed file {file_num}: {filepath}")

            # Update last_num in DB if new files were processed
            if new_files:
                max_file_num = max(file_num for file_num, _ in new_files)
                with transaction.atomic():
                    last_record.last_num = max_file_num
                    last_record.save()

            return JsonResponse({
                "status": "success",
                "processed_files": [os.path.basename(f[1]) for f in new_files],
                "new_last_num": last_record.last_num
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    def process_receipt(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                xml_content = file.read()
        except Exception as e:
            raise Exception("Receipt file could not be opened")

        mod_timestamp = os.path.getmtime(filepath)
        fecha_emision = datetime.fromtimestamp(mod_timestamp)
        products = []
        try:
            root = ET.fromstring(xml_content)

            # Extract basic fields
            total = root.findtext('total')

            # Extract sale detail list
            for sale_detail in root.findall('./detalle_articulos/producto'):
                # Extracting relevant data
                desc = sale_detail.findtext('descripcion')
                quantity = int(sale_detail.findtext('cantidad'))
                subtotal = Decimal(sale_detail.findtext('subtotal'))

                # Obtaining product and removing stock
                product = Product.objects.get(description=desc.strip())
                self.discount_stock(product, quantity, subtotal)

                # Put correct quantity value if unit is kilo
                if product.exit_stock_unit == 'kilo':
                    kilo_quantity = self.kilo_quantity_calc(product, subtotal)
                    if kilo_quantity is not None:
                        quantity = kilo_quantity

                # Adding product data
                product_data = {
                    'product': product,
                    'quantity': quantity,
                    'unit': product.exit_stock_unit,
                    'unit_price': product.sale_price,
                    'subtotal': subtotal,
                }
                products.append(product_data)
        except Exception as e:
            raise Exception(f"File does not match Receipt format: {str(e)}")

        if fecha_emision is None or total is None or len(products) == 0:
            raise Exception("File does not match Receipt format")

        sale_data = {
            'datetime': fecha_emision,
            'total_amount': total,
        }

        # Printing results
        #print("Fecha de emisión:", fecha_emision)
        #print("Total:", total)
        #print("Productos:")
        #for p in products:
        #    print(p)

        with transaction.atomic():
            sale = Sale.objects.create(**sale_data)

            for detail in products:
                try:  # if multiple sales with the same product, acumulate quantity and subtotal
                    sale_detail = SaleDetail.objects.get(sale=sale, product=detail['product'])
                    sale_detail.quantity += detail['quantity']
                    sale_detail.subtotal += detail['subtotal']
                    sale_detail.save()
                except SaleDetail.DoesNotExist:
                    SaleDetail.objects.create(sale=sale, **detail)

    def discount_stock(self, product, quantity, subtotal):
        # Product stock update
        if product.exit_stock_unit == "kilo":
            quantity = self.kilo_quantity_calc(product, subtotal)
            if quantity is None:
                print("WARNING: Product has sale price 0 and unit kilo, cannot calculate quantity, skipping...")
                return
            product.stock = max(0, product.stock - quantity)
        elif product.exit_stock_unit == "unit":
            product.stock = max(0, product.stock - quantity)
        product.save()

        # Batch stock update
        try:
            while quantity > 0:  # If there is leftover after discounting batch, get next batch and discount
                batch = Batch.objects.filter(product=product).filter(quantity__gte=0).earliest("entry_date")  # Gets oldest non-empty batch of product
                current_batch_quantity = batch.quantity
                batch.quantity = max(0, batch.quantity - quantity)  # Assumes product unit == batch unit
                quantity = quantity - current_batch_quantity
                batch.save()
            return
        except Batch.DoesNotExist:
            print(f"WARNING: Product {str(product.description)} does not have non empty batch available. Batch quantity discarded: {str(quantity)}")

    def kilo_quantity_calc(self, product, subtotal):
        if product.sale_price == 0:
            return None
        return subtotal / (product.sale_price * (1 + product.discount_surcharge))