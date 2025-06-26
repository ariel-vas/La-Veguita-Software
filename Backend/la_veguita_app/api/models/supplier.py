from django.db import models


class Supplier(models.Model):
    rut = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    line = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    commune = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20, blank=True)
    cellphone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name