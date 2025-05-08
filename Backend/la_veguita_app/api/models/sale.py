from django.db import models


class Sale(models.Model):

    id_sale = models.AutoField(primary_key=True)
    datetime = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    #user = ManyToMany

    def __str__(self):
        return self.id_sale