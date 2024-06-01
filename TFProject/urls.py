from django.contrib import admin
from django.urls import include, path #include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')), # 일일이 추가하는대신 accounts.urls 포함해줬습니다.
    #path(''             , views.main_page,  name='main_page'),
    #path('signup/'      , views.signup,     name='signup'),
    #path('login/'       , views.login,      name='login'),
    #path('logout/'      , views.logout,     name='logout'),
    #path('user_session/', views.user_session, name='user_session'),  # URL 패턴 수정
    #path('find_account/', views.find_account, name='find_account'),
    #path('edit_account/', views.edit_account, name='edit_account'),
    #path('edit_profile/', views.edit_profile, name='edit_profile'),
   

]
