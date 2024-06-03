from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(''    , include('accounts.urls')),
    path('' , include('add_clothes.urls')),  # URL 패턴 추가



]


'''

    path('yet/'         , views.yet, name='yet'),
    path('add/'         , views.add_and_show, name='add_and_show'),
    
    path(''             , views.main_page,  name='main_page'),
    path('signup/'      , views.signup,     name='signup'),
    path('login/'       , views.login,      name='login'),
    path('logout/'      , views.logout,     name='logout'),
    path('user_session/', views.user_session, name='user_session'),  # URL 패턴 수정
    path('find_account/', views.find_account, name='find_account'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
'''
