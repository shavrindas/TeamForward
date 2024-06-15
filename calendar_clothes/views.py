from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .utils import get_weather  # utils에서 get_weather 함수 import
from .calendar import Calendar  # 캘린더 클래스 import (calendar.py 파일 필요)

@login_required
def calendar_view(request):
    events = Event.objects.filter(user=request.user)

    # 날씨 정보 가져오기
    weather = get_weather()

    cal = Calendar(events).formatmonth(request.GET.get('year'), request.GET.get('month'))
    
    return render(request, 'calendar_clothes/calendar.html', {'calendar': cal, 'weather': weather})

@login_required
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        Event.objects.create(user=request.user, title=title, description=description, date=date, time=time)
        return redirect('calendar')
    return render(request, 'calendar_clothes/add_event.html')

@login_required
def day_view(request, date):
    events = Event.objects.filter(user=request.user, date=date)

    # 날씨 정보 가져오기
    weather = get_weather()

    return render(request, 'calendar_clothes/day_view.html', {'events': events, 'weather': weather})
