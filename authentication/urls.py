from django.urls import path
from django.contrib.auth import views as authv

from . import views

urlpatterns = [
    path('login/', authv.LoginView.as_view(), name='auth-login'),
    path('logout/', authv.logout_then_login, name='auth-logout')
]
