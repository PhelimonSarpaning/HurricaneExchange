from django.urls import path
from .views import (
    trading_create_view
)

app_name = 'trading'
urlpatterns = [
    path('', trading_create_view, name='create'),
]
