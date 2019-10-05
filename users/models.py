from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserFund(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fund = models.FloatField(default=1000000)
    totalAssetValue = models.FloatField(default=1000000)

class FirstTime(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isFirstTime = models.BooleanField(default=True)

class UserAssetValue(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    totalAssetValue = models.FloatField(default=1000000)
    date_tracked = models.DateTimeField(auto_now_add=True)