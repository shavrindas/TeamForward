# fos_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('setting/', views.setting_view, name='setting'),
]