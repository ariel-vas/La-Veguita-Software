from django.shortcuts import render
import os
import re
from decimal import Decimal
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics
from rest_framework.views import APIView
from ..models import Sale, SaleDetail, Product, LastProcessedReceipt
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
    FOLDER_PATH = r"C:\Users\User\Desktop\test_prt"

    def post(self, request, *args, **kwargs):

        # Match filenames like "printer_A_123.txt"
        pattern = re.compile(r"^printer_A_(\d+)\.out$")

        try:
            # Get or create singleton row
            last_record, created = LastProcessedReceipt.objects.get_or_create(id=1)
            last_num = last_record.last_num

            new_files = []

            # Get relevant file names after last_num
            for filename in os.listdir(self.FOLDER_PATH):
                match = pattern.match(filename)
                if match:
                    file_num = int(match.group(1))
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
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [line.strip().strip('"') for line in f if line.strip()]
        except Exception as e:
            raise Exception("Receipt file could not be opened")

        total = None
        fecha_emision = None
        hora = None
        sale_details_data = []

        product_section = False
        product_line_pattern = re.compile(r'^\s*(\d+)\s+(.+?)\s+(\d+)\s+(\d+)$')

        try:
            for line in lines:
                if "Fecha de emision" in line:
                    fecha_emision = line.split(":")[-1].strip()
                elif "Hora:" in line:
                    hora = line.split(":")
                    hora = ":".join(hora[1:4]).strip()
                elif line.startswith("TOTAL"):
                    match = re.search(r"\$ *([\d\.]+)", line)
                    if match:
                        total = Decimal(match.group(1).replace('.', ''))
                elif line.startswith("Ctd."):
                    product_section = True
                elif product_section:
                    if "____" in line or "TOTAL" in line:
                        product_section = False
                    else:
                        match = product_line_pattern.match(line)
                        if match:
                            ctd, desc, precio, subtotal = match.groups()
                            product = Product.objects.filter(description=desc.strip())
                            sale_details_data.append({
                                'product': product,
                                'quantity': int(ctd),
                                'unit': product.exit_stock_unit,
                                'unit_price': product.sale_price,
                                'precio': Decimal(precio),
                                'subtotal': Decimal(subtotal)
                            })
        except Exception as e:
            raise Exception("File does not match Receipt format")

        if fecha_emision is None or hora is None or total is None or len(sale_details_data) == 0:
            raise Exception("File does not match Receipt format")

        sale_data = {
            'datetime': fecha_emision,
            'total_amount': total,
        }

        # Printing results
        print("Fecha de emisión:", fecha_emision)
        print("Hora:", hora)
        print("Total:", total)
        print("Productos:")
        for p in sale_details_data:
            print(p)

        with transaction.atomic():
            sale = Sale.objects.create(**sale_data)

            for detail in sale_details_data:
                SaleDetail.objects.create(sale=sale, **detail)