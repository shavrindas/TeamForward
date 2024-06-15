from django.urls import path
from . import views


urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/add_event/', views.add_event, name='add_event'),
    path('calendar/day/<str:date>/', views.day_view, name='day_view'),
]
