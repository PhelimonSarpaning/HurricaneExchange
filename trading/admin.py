from django.contrib import admin

# Register your models here.
from .models import Trading_Account, Stock_Amount

admin.site.register(Trading_Account)
admin.site.register(Stock_Amount)