# recommend/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('recommendation/'      , views.recommend_clothes,      name='recommend_clothes'),
    path('recommend_clothes/'   , views.recommend_clothes,      name='recommend_clothes'),
    path('save-recommendation/' , views.save_recommendation,    name='save_recommendation'),

]


