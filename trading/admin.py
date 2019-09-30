from django.contrib import admin

# Register your models here.
from .models import Trading_Account

class TradingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'trading_name')


admin.site.register(Trading_Account, TradingAdmin)
