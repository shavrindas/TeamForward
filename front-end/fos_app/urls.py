# fos_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login.html/', views.login_view, name='login'),
    path('login.html/signup.html/', views.signup_view, name='signup'),
    path('login.html/forgotpassword.html/', views.forgotpassword_view, name='forgotpassword'),
    path('setting.html/', views.setting_view, name='setting'),
]