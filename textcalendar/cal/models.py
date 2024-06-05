# cal/models.py

from django.db import models
from django.urls import reverse
from datetime import datetime

# 파일 업로드 경로 설정
def get_upload_to(instance, filename):
    return f'{datetime.now().strftime("%Y%m%d")}_{filename}'

# 이벤트 모델
class Event(models.Model):
    title = models.CharField(max_length=200)  # 일정
    description = models.TextField(blank=True)  # 일정 설명
    start_time = models.DateTimeField(null=True, blank=True)  # 일정 시작 시간
    end_time = models.DateTimeField(null=True, blank=True)  # 일정 종료 시간
    outer_clothes = models.ImageField(upload_to=get_upload_to, blank=True, null=True)  # 외투 이미지
    top_clothes = models.ImageField(upload_to=get_upload_to, blank=True, null=True)  # 상의 이미지
    bottom_clothes = models.ImageField(upload_to=get_upload_to, blank=True, null=True)  # 하의 이미지
    image_editable = models.BooleanField(default=True)  # 이미지 편집 가능 여부
    latitude = models.FloatField(null=True, blank=True)  # 위도
    longitude = models.FloatField(null=True, blank=True)  # 경도
    
    # 이벤트 페이지 URL 가져오기
    @property
    def get_html_url(self):
        url = reverse('cal:event_page', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a> <br> {self.outer_clothes} <br> {self.top_clothes} <br> {self.bottom_clothes}'