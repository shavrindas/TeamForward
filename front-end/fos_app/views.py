# fos_app/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'fos_app/home.html')

def login_view(request):
    return render(request, 'fos_app/login.html')