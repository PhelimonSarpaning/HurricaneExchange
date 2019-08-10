from django.urls import path
from .views import (
    trading_create_view,
    trading_list_view
)

app_name = 'trading'
urlpatterns = [
    path('', trading_list_view, name='list'),
    path('create/', trading_create_view, name='create')
]
