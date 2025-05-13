from django.db import models
from .product import Product


class Batch(models.Model):
    class Unit(models.TextChoices):
        UNIT = 'unit'
        KILO = 'kilo'
    
    id_batch = models.AutoField(primary_key=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.CharField(max_length=4, choices=Unit.choices)
    entry_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batches')

    def __str__(self):
        return self.name