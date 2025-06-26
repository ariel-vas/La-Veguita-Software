from django.shortcuts import render
import os
from datetime import datetime
import re
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics
from rest_framework.views import APIView
from ..models import Sale, SaleDetail, Product, Batch, LastProcessedReceipt, Category, WrongSaleDetail
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
                self.process_journal_file(filepath)
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

    # TODO: PROCESS Journals now :C, SAVE wrong products in receipt for visualization
    def process_journal_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
        except Exception as e:
            raise Exception(f"Receipt file could not be opened: {e}")

        # Split into sections using separator line
        sections = content.split("------------------------------------------------------------")

        for section in sections:
            if "Nº BOLETA" not in section:
                continue  # Skip non-receipts

            receipt = self.extract_receipt_data(section)
            if receipt:
                self.process_receipt(receipt)
        return

    def extract_receipt_data(self, text):
        receipt = {
            "receipt_number": None,
            "datetime": None,
            "total_amount": None,
            "products": []
        }

        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

        # 1. Get receipt number
        for line in lines:
            if "Nº BOLETA" in line:
                match = re.search(r'Nº BOLETA\s*:\s*(\d+)', line)
                if match:
                    receipt["receipt_number"] = int(match.group(1))
                break  # assume only one per block

        # 2. Get first timestamp after boleta
        for line in lines:
            ts_match = re.search(r'\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}', line)
            if ts_match:
                receipt["datetime"] = datetime.strptime(ts_match.group(), '%d-%m-%Y %H:%M:%S')
                break

        # 3. Get total
        for line in lines:
            if line.startswith("TOTAL :"):
                match = re.search(r'TOTAL\s*:\s*\$?\s*([\d.,]+)', line)
                if match:
                    total_str = match.group(1).replace('.', '').replace(',', '')
                    receipt["total_amount"] = int(total_str)
                break

        # 4. Get product lines
        products = []
        for i in range(len(lines) - 1):
            qty_line = lines[i]
            prod_line = lines[i + 1]

            # Match quantity line like "1 X", "3 X"
            qty_match = re.match(r'^(\d+)\s+X\b', qty_line)
            if not qty_match:
                continue

            quantity = int(qty_match.group(1))

            # Match product line: BARCODE (no spaces), then NAME, then PRICE at end
            match = re.match(r'^\s*(\S+)\s+(.+?)\s+(\d+)$', prod_line)
            if match:
                barcode = match.group(1)
                name = match.group(2).strip()
                price = int(match.group(3).replace(',', '').replace('.', ''))

                products.append({
                    "id_product": barcode,
                    "name": name,
                    "quantity": quantity,
                    "subtotal": price
                })

        receipt["products"] = products

        # Validate receipt
        if receipt["receipt_number"] and receipt["datetime"] and receipt["total_amount"] and receipt["products"]:
            return receipt
        return None

    def process_receipt(self, receipt):
        products = []
        # Extract sale detail list
        for sale_detail in receipt["products"]:
            product = None
            invalid = False
            invalid_name = False
            # Obtaining product and handling errors
            try:
                product = Product.objects.get(id_product=sale_detail["id_product"].strip())
                if product.description.strip() != sale_detail["name"]:
                    invalid_name = True
            except Product.DoesNotExist:
                invalid = True

            if invalid or invalid_name:  # Suspicion of wrong_sale_detail
                try:
                    category = Category.objects.get(id_category=sale_detail[
                        "id_product"].strip())  # Check if receipt is wrongly made (Category as product)
                    if category.name.strip() == sale_detail["name"]:  # Confirm wrongly made receipt
                        self.register_wrong_sale_detail(receipt["receipt_number"], sale_detail)
                        continue
                except Category.DoesNotExist:
                    if invalid:
                        continue

            if product:
                self.discount_stock(product, sale_detail["quantity"])

                # Adding product data
                product_data = {
                    'product': product,
                    'quantity': sale_detail["quantity"],
                    'unit': product.exit_stock_unit,
                    'unit_price': product.sale_price,
                    'subtotal': sale_detail["subtotal"],
                }
                products.append(product_data)

        if receipt["receipt_number"] is None or receipt["total_amount"] is None or len(receipt["products"]) == 0:
            raise Exception("Data does not match Receipt format")

        sale_data = {
            'receipt_number': receipt["receipt_number"],
            'datetime': receipt["datetime"],
            'total_amount': receipt["total_amount"],
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

    def discount_stock(self, product, quantity):
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

    def register_wrong_sale_detail(self, receipt_number, sale_detail):
        wrong_sale_data = {
            'receipt_number': receipt_number,
            'name': sale_detail["name"],
            'quantity': sale_detail["quantity"],
            'subtotal': sale_detail["subtotal"]
        }

        try:  # if multiple wrong sales in same receipt acumulate quantity and subtotal
            wrong_sale = WrongSaleDetail.objects.get(receipt_number=receipt_number)
            wrong_sale.quantity += sale_detail['quantity']
            wrong_sale.subtotal += sale_detail['subtotal']
            wrong_sale.save()
        except WrongSaleDetail.DoesNotExist:
            WrongSaleDetail.objects.create(receipt_number=receipt_number, **wrong_sale_data)
