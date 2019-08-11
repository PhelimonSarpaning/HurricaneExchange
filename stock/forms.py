from django import forms
from .models import Stock_Amount
from django.db import models
from django.forms import ModelForm
from trading.models import Trading_Account

class StockForm(ModelForm):
    class Meta:
        model = Stock_Amount
        fields = ('stock_name', 'stock_amount')
