from django.db import models

class Supplier(models.Model):
    id_supplier = models.AutoField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name