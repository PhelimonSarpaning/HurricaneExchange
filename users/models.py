from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserFund(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    fund = models.FloatField(default=1000000)
