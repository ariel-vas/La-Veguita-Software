from django.db import models


class SaleDetail(models.Model):
    class Unit(models.TextChoices):
        UNIT = 'unit'
        KILO = 'kilo'

    id_sale_detail = models.AutoField(primary_key=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.CharField(max_length=4, choices=Unit.choices)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    #sale = ManyToOne
    #product = ManyToOne

    def __str__(self):
        return self.id_sale_detail