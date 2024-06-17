from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
import calendar
import requests
from .models import Event2
from accounts.models import UserData
from .forms import EventForm
from django import forms
from recommend.models import RecommendedClothes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(date__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li><a href="#" class="date" data-date="{event.date}" data-event-id="{event.id}">{event.title}</a></li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatmonth(self, withyear=True):
        events = Event2.objects.filter(date__year=self.year, date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar_v2">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += self.formatweek(week, events)
        return cal

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'


class CalendarView(generic.ListView):
    model = Event2
    template_name = 'calendar_v2/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event_new2(request):
    user_id = request.COOKIES.get('user_id')  # 쿠키에서 사용자 ID 읽기
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # 폼 데이터를 저장하기 전에 사용자 ID를 설정하여 저장
            event = form.save(commit=False)
            event.user_id = user_id
            event.save()
            return HttpResponseRedirect(reverse('cal2:calendar_v2'))
    else:
        form = EventForm()
    return render(request, 'calendar_v2/event.html', {
        'form': form,
        'event_exists': False  # 새 이벤트 생성 시
    })

def event_page2(request, event_id):
    event = get_object_or_404(Event2, pk=event_id)
    user_cookie = request.COOKIES.get('user_cookie')
    
    if user_cookie:
        try:
            user = UserData.objects.get(email=user_cookie)  # Assuming user_cookie contains email
            recommended_clothes = RecommendedClothes.objects.filter(user_email=user.email, date=event.date)
        except UserData.DoesNotExist:
            user = None
            recommended_clothes = []
    else:
        user = None
        recommended_clothes = []

    recommended_clothes_data = []
    for rc in recommended_clothes:
        recommended_clothes_data.append({
            'top_url': f"/media/{rc.top}",
            'bottom_url': f"/media/{rc.bottom}",
            'outer_url': f"/media/{rc.outer}",
        })

    return render(request, 'calendar_v2/event_detail.html', {
        'event': event,
        'user': user,  # Pass the user object for context in the template if needed
        'recommended_clothes': recommended_clothes_data,
    })

def event_delete2(request, event_id):
    event = get_object_or_404(Event2, pk=event_id)
    event.delete()
    return redirect('cal2:calendar_v2')

def event_view2(request):
    event_exists = Event2.objects.exists()
    return render(request, 'calendar_v2/event_view.html', {'event_exists2': event_exists})

def event_edit2(request, event_id):
    event = get_object_or_404(Event2, pk=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            # 현재 로그인한 사용자의 쿠키에서 사용자 ID를 가져옵니다.
            user_id = request.COOKIES.get('user_id')
            
            # 해당 사용자 ID를 가진 UserData를 가져옵니다.
            try:
                user_data = UserData.objects.get(id=user_id)
            except UserData.DoesNotExist:
                user_data = None
            
            # 사용자가 존재하면 이벤트의 user 필드를 업데이트합니다.
            if user_data:
                event.user = user_data
                form.save()
                return redirect('cal2:event_page2', event_id=event.id)
            else:
                # 사용자가 존재하지 않는 경우 예외 처리합니다.
                pass
    else:
        form = EventForm(instance=event)
    
    return render(request, 'calendar_v2/event_edit.html', {'event': event, 'form': form})

@api_view(['GET'])
def weather2(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    weather_data = get_weather_data(lat, lon)
    response_data = {
        'temp': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description'],
        'icon': weather_data['weather'][0]['icon'],
    }
    return JsonResponse(response_data)

def get_weather_data(lat, lon):
    api_key = 'cbd3023a75f5f25f7c80897189cbe42a'  # OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()
