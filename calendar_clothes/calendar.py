# calendar.py

import calendar

class Calendar:
    def __init__(self, events):
        self.events = events

    def formatmonth(self, year=None, month=None):
        if year is None or month is None:
            import datetime
            now = datetime.datetime.now()
            year = now.year
            month = now.month

        cal = calendar.HTMLCalendar(calendar.SUNDAY)
        month_str = cal.formatmonth(year, month)
        return month_str
