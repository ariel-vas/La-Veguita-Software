from django.db import models
from django.core.validators import MinValueValidator


class WrongSaleDetail(models.Model):    # TODO: FINISH SERIALIZER AND VIEWS

    id_wrong_sale_detail = models.AutoField(primary_key=True)
    receipt_number = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    name = models.CharField(max_length=100, unique=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=4, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name