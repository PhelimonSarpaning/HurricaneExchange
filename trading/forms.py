from django import forms
from .models import Trading_Account
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class TradingForm(ModelForm):
    class Meta:
        model = Trading_Account
        fields = [
            'trading_name'
        ]
