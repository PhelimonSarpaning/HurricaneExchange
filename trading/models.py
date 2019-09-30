from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here.
class Trading_Account(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    trading_name = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):  # __unicode__ for py2
        return self.trading_name
