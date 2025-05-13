from django.db import models
from .product import Product


class SubCategory(models.Model):
    id_subcategory = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(Product, related_name='subcategories', blank=True)

    def __str__(self):
        return self.name