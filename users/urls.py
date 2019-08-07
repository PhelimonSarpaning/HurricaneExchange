from django.urls import path
from .views import (
    users_signup_view,
    users_login_view,
    users_logout_view
)

app_name = 'users'
urlpatterns = [
    path('signup/', users_signup_view, name='signup'),
    path('', users_login_view, name='login'),
    path('logout/', users_logout_view, name="logout")
]
