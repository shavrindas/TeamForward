# add_clothes/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views  # add_clothes.views에서 가져옵니다
from .views import add_and_show, delete_picture

urlpatterns = [
    path('yet/', views.yet, name='yet'),
    path('add/', views.add_and_show, name='add_and_show'),
    path('delete/<int:picture_id>/', views.delete_picture, name='delete_picture'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
