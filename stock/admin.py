from django.contrib import admin

# Register your models here.
from .models import Stock, Shares, Market

admin.site.register(Stock)
admin.site.register(Shares)
admin.site.register(Market)
