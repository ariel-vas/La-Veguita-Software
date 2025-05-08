from django.db import models


class Category(models.Model):

    id_category = models.AutoField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name