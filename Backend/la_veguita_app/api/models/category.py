from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):

    id_category = models.DecimalField(primary_key=True, max_digits=50, decimal_places=0, validators=[MinValueValidator(0)])
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name