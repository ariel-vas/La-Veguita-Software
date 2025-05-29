from django.utils.timezone import make_aware
from datetime import datetime
from django.db import models
from .batch import Batch

class Notification(models.Model):
    id_notification = models.AutoField(primary_key=True)
    state = models.CharField(max_length=50, default='pending')
    date_of_completion = models.DateTimeField(null=True, blank=True)
    id_batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, related_name='notifications', null=True, blank=True)
    expiration_date = models.DateTimeField(editable=False, null=True, blank=True)
    name_product = models.CharField(max_length=150, editable=False)

    def save(self, *args, **kwargs):
        if self.id_batch:
            self.name_product = self.id_batch.product.name

            expiration = self.id_batch.expiration_date
            # Si expiration es solo date, conviértelo a datetime
            if isinstance(expiration, datetime):
                self.expiration_date = expiration
            else:
                self.expiration_date = make_aware(datetime.combine(expiration, datetime.min.time()))

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Notification {self.id_notification} - {self.name_product}"
