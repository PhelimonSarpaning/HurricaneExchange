from django.urls import path
from .views import (
    trading_create_view,
    trading_list_view,
    trading_detail_view,
    trading_delete_view
)

app_name = 'trading'
urlpatterns = [
    path('', trading_list_view, name='list'),
    path('create/', trading_create_view, name='create'),
    path('<int:id>/', trading_detail_view, name='detail'),
    path('delete/<int:id>/', trading_delete_view, name='delete')
]
