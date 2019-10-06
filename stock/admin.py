from django.contrib import admin

# Register your models here.
from .models import Stock, Shares, Market, Transaction_History

class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_name','stock_ticker','stock_gics','stock_price',
    'stock_dayChange','stock_max','stock_sold','stock_hasValidInfo',)
    search_fields = ['stock_name','stock_ticker', 'stock_gics']

class SharesAdmin(admin.ModelAdmin):
    list_display = ('getUser', 'getTradingName', 'getStockName', 'shares_amount')

admin.site.register(Stock, StockAdmin)
admin.site.register(Shares, SharesAdmin)
admin.site.register(Transaction_History)
