from django.db import models
from trading.models import Trading_Account


# Create your models here.
class Stock(models.Model):
    stock_name = models.CharField(max_length=255)
    stock_max = models.FloatField()

class Market(models.Model):
    stockID = models.ForeignKey(Stock, on_delete=models.CASCADE)
    market_amount = models.FloatField()
    market_sold = models.FloatField()

class Shares(models.Model):
    tradingID = models.ForeignKey(Trading_Account, on_delete=models.CASCADE)
    stockID = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares_amount = models.FloatField()