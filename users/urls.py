from django.urls import path
from .views import (
    users_signup_view,
    users_login_view,
)

app_name = 'users'
urlpatterns = [
    path('signup/', users_signup_view, name='users-signup-view'),
    path('', users_login_view, name='users_login_view')
]
