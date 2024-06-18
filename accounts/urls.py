from django.contrib import admin
from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(''             , views.main_page,  name='main_page'),
    path('signup/'      , views.signup,     name='signup'),
    path('login/'       , views.login,      name='login'),
    path('logout/'      , views.logout,     name='logout'),
    path('user_session/', views.user_session, name='user_session'),
    path('find_account/', views.find_account, name='find_account'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
   
]   

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)