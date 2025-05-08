from django.db import models


class User(models.Model):
    class RolTypes(models.TextChoices):
        ADMIN = 'admin'
        vendor = 'vendor'

    id = models.AutoField(primary_key=True)
    username = models.TextField()
    email = models.EmailField(max_length=254)
    password = models.TextField()
    rol = models.CharField(max_length=6, choices=RolTypes.choices)

    def __str__(self):
        return self.username