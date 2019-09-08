from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here.
class Trading_Account(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    trading_name = models.CharField(max_length=20)

