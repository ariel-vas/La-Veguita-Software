from django.db import models
from datetime import date, datetime


class LastProcessedReceipt(models.Model):

    last_num = models.IntegerField(default=0)
    last_date = models.DateField(default=date(2000, 1, 1))

    def __str__(self):
        return f"last_num: {str(self.last_num)}, last_date: {str(self.last_date)}"