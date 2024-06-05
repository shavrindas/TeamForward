# cal/urls.py

from django.urls import path
from . import views

app_name = 'cal'

urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),  # 캘린더 페이지
    path('event/new/', views.event_new, name='event_new'),  # 새 이벤트 생성 페이지
    path('event/edit/<int:event_id>/', views.event_new, name='event_edit'),  # 기존 이벤트 편집 페이지
    path('event/delete/<int:event_id>/', views.event_delete, name='event_delete'),  # 이벤트 삭제 처리
    path('event/<int:event_id>/', views.event_page, name='event_page'),  # 이벤트 상세 페이지
    path('event/view/', views.event_view, name='event_view'),  # 이벤트 보기 페이지
    path('weather/', views.weather, name='weather'),  # 날씨 정보 가져오기
]