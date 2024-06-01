# recommendation_clothes/urls.py # 일단 테스트로 임시로 저장한거니까 나중에 수정하자.
from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path(''             , views.main_page,  name='main_page'),
    path('signup/'      , views.signup,     name='signup'),
    path('login/'       , views.login,      name='login'),
    path('logout/'      , views.logout,     name='logout'),
    path('user_session/', views.user_session, name='user_session'),  # URL 패턴 수정
    path('find_account/', views.find_account, name='find_account'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
   
]