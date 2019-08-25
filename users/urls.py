from django.urls import path
from django.conf.urls.static import static
from HurricaneExchange import settings
from .views import (
    users_signup_view,
    users_login_view,
    users_logout_view
)

app_name = 'users'
urlpatterns = [
    path('', users_login_view, name='login'),
    path('signup/', users_signup_view, name='signup'),
    path('logout/', users_logout_view, name='logout')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)