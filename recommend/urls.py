# recommend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #path('recommend/', views.recommend_algorithm, name='recommend_algorithm'),  # 추천 알고리즘 페이지
    path('recommendation/', views.recommend_clothes, name='recommend_clothes'),
    path('recommend_clothes/', views.recommend_clothes, name='recommend_clothes'),
    path('save-recommendation/', views.save_recommendation, name='save_recommendation'),
    #path('save_recommendation/', views.save_recommendation, name='save_recommendation'),
]


