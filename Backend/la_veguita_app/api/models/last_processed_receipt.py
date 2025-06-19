from django.db import models


class LastProcessedReceipt(models.Model):

    last_num = models.IntegerField(default=0)

    def __str__(self):
        return str(self.last_num)