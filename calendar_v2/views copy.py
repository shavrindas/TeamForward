
def event_new2(request, event_id=None):
    event = get_object_or_404(Event2, pk=event_id) if event_id else None
    form = EventForm(request.POST or None, instance=event)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal2:calendar_v2'))
    return render(request, 'calendar_v2/event.html', {
        'form': form,
        'event_exists': bool(event_id),
        'event': event
    })



# views.py
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
import calendar, requests
from .models import Event2
from calendar import HTMLCalendar

from django import forms


class EventForm(forms.ModelForm):
    description = forms.CharField(required=False)  # 설명 필드 (필수 아님)
    time = forms.DateTimeField(  # 시작 시간 필드 (필수 아님)
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), 
        required=False
    )

    class Meta:
        model = Event2
        fields = ['title', 'description', 'time']
        labels = {
            'title': '일정',
            'description': '설명',
            'time': '시작 시간',
        }
        error_messages = {
            'title': { 
                'required': "일정을 입력해주세요.", 
            }
        }
        

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time is None:
            return self.fields['time'].initial or datetime.now()
        return time




class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatmonthname(self, theyear, themonth, withyear=True):
        month_names = ['', '1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
        s = f'{theyear}년 {month_names[themonth]}' if withyear else f'{month_names[themonth]}'
        return f'<tr><th colspan="7" class="month">{s}</th></tr>'

    def formatweekday(self, day):
        weekday_names = ['월', '화', '수', '목', '금', '토', '일']
        return f'<th class="{self.cssclasses[day]}">{weekday_names[day]}</th>'

    def formatday(self, day, events):
        events_per_day = events.filter(date__day=day)
        d = ''
        for event in events_per_day:
            event_time = event.time.strftime('%H:%M')
            d += f'<li>{event_time} - {event.title}</li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        return f'<tr> {" ".join([self.formatday(d, events) for d, weekday in theweek])} </tr>'

    def formatmonth(self, withyear=True):
        events = Event2.objects.filter(date__year=self.year, date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar_v2">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        cal += ''.join([f'{self.formatweek(week, events)}\n' for week in self.monthdays2calendar(self.year, self.month)])
        return cal




class Calendar:
    def __init__(self, events):
        self.events = events

    def formatmonth(self, year=None, month=None):
        if year is None or month is None:
            import datetime
            now = datetime.datetime.now()
            year = now.year
            month = now.month

        cal2 = calendar.HTMLCalendar(calendar.SUNDAY)
        month_str = cal2.formatmonth(year, month)
        return month_str




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


def event2(request, event_id=None):
    instance = get_object_or_404(Event2, id=event_id) if event_id else None
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal2:calendar_v2'))
    return render(request, 'calendar_v2/event.html', {'form': form, 'event_exists2': bool(instance)})


def event_view2(request):
    event_exists = Event2.objects.exists()

    return render(request, 'event.html', {'event_exists2': event_exists})


def event_delete2(request, event_id):
    event = get_object_or_404(Event2, pk=event_id)
    event.delete()
    return redirect('cal2:calendar_v2')

def event_page2(request, event_id):
    print("event_page2")
    event = get_object_or_404(Event2, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cal2:calendar_v2'))
    else:
        form = EventForm(instance=event)
    return render(request, 'cal2/event.html', {'form': form, 'event_exists2': True, 'event2': event})

@csrf_exempt
def event_new2(request, event_id=None):
    print("event_new2")
    event = get_object_or_404(Event2, pk=event_id) if event_id else None
    form = EventForm(request.POST or None, instance=event)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal2:calendar_v2'))
    return render(request, 'calendar_v2/event.html', {
        'form': form,
        'event_exists': bool(event_id),
        'event': event
    })

api_key = 'cbd3023a75f5f25f7c80897189cbe42a';  # OpenWeatherMap에서 발급받은 API 키

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
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()
