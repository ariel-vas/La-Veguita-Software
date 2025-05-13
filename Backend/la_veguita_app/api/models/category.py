from django.db import models


class Category(models.Model):

    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name