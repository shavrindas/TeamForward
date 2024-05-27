# fos_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login.html/', views.login_view, name='login'),
    #path('login.html/signup.html/', views.signup_view, name='signup'),
    path('signup/',       views.signup, name='signup'),
    path('login.html/forgotpassword.html/', views.forgotpassword_view, name='forgotpassword'),
    path('setting.html/', views.setting_view, name='setting'),
    path('temp-fine/',    views.temp_fine_view, name='temp_fine'),
    path('login.html/forgotpassword.html/forgotpasswordremake/', views.forgot_password_remake_view, name='forgot_password_remake'),
]