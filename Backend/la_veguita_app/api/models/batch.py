from django.db import models


class Batch(models.Model):
    class Unit(models.TextChoices):
        UNIT = 'unit'
        KILO = 'kilo'
    
    id_batch = models.AutoField(primary_key=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    unit = models.CharField(max_length=4, choices=Unit.choices)
    entry_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    #id_product = models.ManyToOneRel('product')


    def __str__(self):
        return self.name