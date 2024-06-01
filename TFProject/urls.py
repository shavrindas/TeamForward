# TFProject/urls.py
from django.contrib import admin
from django.urls import include, path #include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(''             , views.main_page,  name='main_page'),
    path('', include('accounts.urls')), # 일일이 추가하는대신 accounts.urls 포함해줬습니다.
    #path('signup/'      , views.signup,     name='signup'),
    #path('login/'       , views.login,      name='login'),
    #path('logout/'      , views.logout,     name='logout'),
    #path('user_session/', views.user_session, name='user_session'),  # URL 패턴 수정
    #path('find_account/', views.find_account, name='find_account'),
    #path('edit_account/', views.edit_account, name='edit_account'),
    #path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    # 일단 테스트로 add_clothes/urls.py 파일 경로 설정. 나중에 해당 파일 수정하자.
    path('add_clothes/', include('add_clothes.urls')),
    # 일단 테스트로 recommendation_clothes/urls.py 파일 경로 설정. 나중에 해당 파일 수정하자.
    path('recommendation_clothes/', include('recommendation_clothes.urls')),
]
