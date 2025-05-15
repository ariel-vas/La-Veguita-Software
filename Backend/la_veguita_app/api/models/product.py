from django.db import models
from django.core.validators import MinValueValidator
from .category import Category
from .supplier import Supplier


class Product(models.Model):
    class StockUnit(models.TextChoices):
        UNIT = 'unit'
        KILO = 'kilo'

    id_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price_unit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price_kilo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    wholesale_quantity = models.DecimalField(max_digits=12, decimal_places=4, validators=[MinValueValidator(0)])
    discount_surcharge = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.DecimalField(max_digits=12, decimal_places=4, validators=[MinValueValidator(0)])
    critical_stock = models.DecimalField(max_digits=12, decimal_places=4, validators=[MinValueValidator(0)])
    entry_stock_unit = models.CharField(max_length=4, choices=StockUnit.choices)
    exit_stock_unit = models.CharField(max_length=4, choices=StockUnit.choices)
    composed_product = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    def __str__(self):
        return self.name