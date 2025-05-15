from django.db import models
from django.core.validators import MinValueValidator
from .sale import Sale
from .product import Product


class SaleDetail(models.Model):
    class Unit(models.TextChoices):
        UNIT = 'unit'
        KILO = 'kilo'

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=4, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=4, choices=Unit.choices)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sale', 'product'], name='unique_sale_product')
        ]

    def __str__(self):
        return "{}_{}".format(self.sale.__str__(), self.product.__str__())