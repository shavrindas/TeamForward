# utils.py

from calendar import HTMLCalendar
from django.urls import reverse
from .models import Event
from datetime import datetime


# HTML 캘린더 클래스
class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# 월 이름을 테이블 행으로 반환
	def formatmonthname(self, theyear, themonth, withyear=True):
		month_names = ['', '1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
		s = f'{theyear}년 {month_names[themonth]}' if withyear else f'{month_names[themonth]}'
		return f'<tr><th colspan="7" class="month">{s}</th></tr>'

	# 요일 이름을 테이블 헤더로 반환
	def formatweekday(self, day):
		weekday_names = ['월', '화', '수', '목', '금', '토', '일']
		return f'<th class="{self.cssclasses[day]}">{weekday_names[day]}</th>'

	# 일자별 이벤트를 포맷팅
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		d = ''.join([f'<li> {event.get_html_url} </li>' for event in events_per_day])
		for event in events_per_day:
			if event.outer_clothes or event.top_clothes or event.bottom_clothes:
				url = reverse('cal:event_page', args=(event.id,))
				for clothes_type in ['outer_clothes', 'top_clothes', 'bottom_clothes']:
					clothes = getattr(event, clothes_type)
					if clothes:
						d += f'<a href="{url}"><img src="{clothes.url}" alt="{clothes_type.replace("_", " ").capitalize()}"></a>'
						d += f'<p>Image editable: {event.image_editable}</p>'
		return f"<td><span class='date' data-date='{self.year}-{self.month}-{day}'>{day}</span><ul> {d} </ul></td>" if day != 0 else '<td></td>'

	# 주별 이벤트를 포맷팅
	def formatweek(self, theweek, events):
		return f'<tr> {" ".join([self.formatday(d, events) for d, weekday in theweek])} </tr>'

	# 월별 이벤트를 포맷팅
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		cal += ''.join([f'{self.formatweek(week, events)}\n' for week in self.monthdays2calendar(self.year, self.month)])
		return cal