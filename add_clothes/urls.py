# add_clothes/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views  # add_clothes.views에서 가져옵니다

urlpatterns = [
    path('yet/', views.yet, name='yet'),
    path('add/', views.add_and_show, name='add_and_show'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
