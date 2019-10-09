from django.contrib import admin

# Register your models here.
from .models import Trading_Account
from stock.models import Shares

class InlineShares(admin.TabularInline):
    model = Shares

class TradingAdmin(admin.ModelAdmin):
    list_display = ('trading_name', 'user_id', 'user_id')
    inlines = [InlineShares]


admin.site.register(Trading_Account, TradingAdmin)
