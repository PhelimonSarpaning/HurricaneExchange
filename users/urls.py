from django.urls import path
from .views import (
    users_signup_view,
)

app_name = 'users'
urlpatterns = [
    path('', users_signup_view, name='users-signup-view')
]
