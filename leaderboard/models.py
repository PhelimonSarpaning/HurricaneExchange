from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Leaderboard(models.Model):
    user_id = models.IntegerField(default=100.0)
    fund = models.BigIntegerField(default=1000.0)