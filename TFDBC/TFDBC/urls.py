"""
URL configuration for TFDBC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required  # login_required 임포트
from django.contrib import admin
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('admin/', admin.site.urls),
    
    path(''             , views.main_page,  name='main_page'),
    path('signup/'      , views.signup,     name='signup'),
    path('login/'       , views.login,      name='login'),
    path('logout/'      , views.logout,     name='logout'),
    path('user_session/', views.user_session, name='user_session'),  # URL 패턴 수정
    path('find_account/', views.find_account, name='find_account'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
   
]


'''
    path('admin/', admin.site.urls),
    
    path('', views.main_page, name='main_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:user_id>/user_session/', login_required(views.user_session), name='user_session'),  # URL 패턴 수정
    path('find_account/', views.find_account, name='find_account'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
'''