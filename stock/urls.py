from django.urls import path
from .views import (
    stock_create_view,
    stock_detail_view,
    stock_list_view,
    stock_sell,
    stock_buy
)

app_name = 'stock'
urlpatterns = [
    path('create/<int:id>/', stock_create_view, name='create'),
    path('<int:id>/', stock_detail_view, name='detail'),
    path('stocklist', stock_list_view, name='list'),
    path('sell/<int:id>/', stock_sell, name='detail'),
    path('buy/<int:id>/', stock_buy, name='detail')
]
