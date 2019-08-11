from django.db import models
from trading.models import Trading_Account


# Create your models here.
class Stock_Amount(models.Model):
    trading_id = models.ForeignKey(Trading_Account, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=100)
    stock_amount = models.FloatField()

