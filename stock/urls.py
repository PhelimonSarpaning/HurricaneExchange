from django.urls import path
from .views import (
    stock_create_view
)

app_name = 'stock'
urlpatterns = [
    path('create/<int:id>/', stock_create_view, name='create')
]
