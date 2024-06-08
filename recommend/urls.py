# recommend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.recommend_algorithm, name='recommend_algorithm'),  # 추천 알고리즘 페이지
    path('save_recommendation/', views.save_recommendation, name='save_recommendation'),
]


