from django.db import models


class Product(models.Model):
    class StockUnit(models.TextChoices):
        UNIT = 'unit'
        KILO = 'kilo'

    id_product = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price_unit = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price_kilo = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_quantity = models.DecimalField(max_digits=12, decimal_places=4)
    discount_surcharge = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.DecimalField(max_digits=12, decimal_places=4)
    critical_stock = models.DecimalField(max_digits=12, decimal_places=4)
    stock_unit = models.CharField(max_length=4, choices=StockUnit.choices)
    composed_product = models.BooleanField()

    def __str__(self):
        return self.name