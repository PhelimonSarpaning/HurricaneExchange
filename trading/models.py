from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Trading_Account(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    trading_name = models.CharField(max_length=20)
    trading_amount = models.FloatField(default=1000000)

    # def get_absolute_url(self):
    #     return reverse("trading:list", kwargs={"id": self.pk})
    

class Stock_Amount(models.Model):
    trading_id = models.ForeignKey('Trading_Account', on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=100)
    stock_amount = models.FloatField()
