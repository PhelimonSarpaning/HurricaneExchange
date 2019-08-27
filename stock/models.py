from django.db import models
from trading.models import Trading_Account



# Create your models here.
class Stock(models.Model):
    stock_name = models.CharField(max_length=255)
    stock_ticker = models.CharField(max_length=10, default="NLL")
    stock_gics = models.CharField(max_length=255, default="NULL")
    stock_price = models.FloatField(default=200.0)
    stock_dayChange = models.FloatField(default=10.0)
    stock_max = models.BigIntegerField(default=1000.0)
    stock_sold = models.BigIntegerField(default=0)
    stock_hasValidInfo = models.BooleanField(default=False)

class Market(models.Model):
    stockID = models.ForeignKey(Stock, on_delete=models.CASCADE)
    market_amount = models.FloatField()
    market_sold = models.FloatField()

class Shares(models.Model):
    tradingID = models.ForeignKey(Trading_Account, on_delete=models.CASCADE)
    stockID = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares_amount = models.FloatField()
