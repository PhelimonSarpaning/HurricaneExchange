from django.contrib import admin

# Register your models here.
from .models import Stock, Shares, Market, Transaction_History

admin.site.register(Stock)
admin.site.register(Shares)
admin.site.register(Market)
admin.site.register(Transaction_History)