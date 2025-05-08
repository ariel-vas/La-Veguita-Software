from django.db import models

class SubCategory(models.Model):
    id_subcategory = models.AutoField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name