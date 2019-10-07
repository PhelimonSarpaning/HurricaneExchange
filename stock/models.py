from django.db import models
from django.contrib.auth.models import User
from trading.models import Trading_Account


TRANSACTION_TYPE = (
    ('P', 'Purchased'),
    ('S', 'Sold')
)


# Create your models here.
class Stock(models.Model):
    stock_name = models.CharField(max_length=255)
    stock_ticker = models.CharField(max_length=10, default="NLL")
    stock_gics = models.CharField(max_length=255, default="NULL")
    stock_price = models.FloatField(default=200.0)
    stock_dayChange = models.FloatField(default=10.0)
    stock_dayChangePercent = models.CharField(max_length=20, default='10.0')
    stock_max = models.BigIntegerField(default=1000.0)
    stock_sold = models.BigIntegerField(default=0)
    stock_hasValidInfo = models.BooleanField(default=False)
    stock_rating = models.FloatField(default=0.0)

    def __str__(self):  # __unicode__ for py2
        return self.stock_name

class Market(models.Model):
    stockID = models.ForeignKey(Stock, on_delete=models.CASCADE)
    market_amount = models.FloatField()
    market_sold = models.FloatField()

class Shares(models.Model):
    tradingID = models.ForeignKey(Trading_Account, on_delete=models.CASCADE)
    stockID = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares_amount = models.FloatField()

    def getUser(self):
        return self.tradingID.user_id
    def getTradingName(self):
        return self.tradingID.trading_name
    def getStockName(self):
        return self.stockID.stock_name



class Transaction_History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trading_name = models.CharField(max_length=100, blank=True)
    stock_name = models.CharField(max_length=100)
    stock_gics = models.CharField(max_length=100)
    stock_price = models.FloatField()
    no_of_shares = models.FloatField()
    funds = models.FloatField()
    transaction = models.CharField(choices=TRANSACTION_TYPE, max_length=1)
    date_of_transaction = models.DateTimeField(auto_now_add=True)
