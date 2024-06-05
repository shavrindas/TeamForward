# cal/views.py
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
import calendar, requests
from .models import Event
from .utils import Calendar
from .forms import EventForm

api_key = 'cbd3023a75f5f25f7c80897189cbe42a';  # OpenWeatherMap에서 발급받은 API 키

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

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


def event(request, event_id=None):
    instance = get_object_or_404(Event, id=event_id) if event_id else None
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form, 'event_exists': bool(instance)})


def event_view(request):
    event_exists = Event.objects.exists()

    return render(request, 'event.html', {'event_exists': event_exists})


def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('cal:calendar')

def event_page(request, event_id):
    print("event_page")
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cal:calendar'))
    else:
        form = EventForm(instance=event)
    return render(request, 'cal/event.html', {'form': form, 'event_exists': True, 'event': event})

@csrf_exempt
def event_new(request, event_id=None):
    print("event_new")
    event = get_object_or_404(Event, pk=event_id) if event_id else Event()
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form, 'event_exists': bool(event_id), 'event': event})

def weather(request):
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