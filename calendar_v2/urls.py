from django.urls import path
from . import views

app_name = 'cal2'

urlpatterns = [
    path('calendar_v2/', views.CalendarView.as_view(), name='calendar_v2'),  # 캘린더 페이지
    path('event2/new/', views.event_new2, name='event_new2'),  # 새 이벤트 생성 페이지
    path('event2/edit/<int:event_id>/', views.event_edit2, name='event_edit2'),  # 이벤트 수정 페이지
    path('event2/delete/<int:event_id>/', views.event_delete2, name='event_delete2'),  # 이벤트 삭제 처리
    path('event2/<int:event_id>/', views.event_page2, name='event_page2'),  # 이벤트 상세 페이지
    path('event2/view/', views.event_view2, name='event_view2'),  # 이벤트 보기 페이지
    path('weather2/', views.weather2, name='weather2'),  # 날씨 정보 가져오기

]
