# fos_app/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'fos_app/home.html')

def login_view(request):
    return render(request, 'fos_app/login.html')

def signup_view(request):
    return render(request, 'fos_app/signup.html') 

def forgotpassword_view(request):
    return render(request, 'fos_app/forgotpassword.html') 

def setting_view(request):
    return render(request, 'fos_app/setting.html')