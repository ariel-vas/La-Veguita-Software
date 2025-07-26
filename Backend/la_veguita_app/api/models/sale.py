from django.db import models
from .product import Product


class Sale(models.Model):

    id_sale = models.AutoField(primary_key=True)
    receipt_number = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    datetime = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, through='SaleDetail', related_name='sales')

    def __str__(self):
        return self.id_sale