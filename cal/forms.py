# cal/forms.py

from django import forms
from .models import Event
from datetime import datetime

# 이벤트 폼
class EventForm(forms.ModelForm):
    description = forms.CharField(required=False)  # 설명 필드 (필수 아님)
    start_time = forms.DateTimeField(  # 시작 시간 필드 (필수 아님)
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), 
        required=False
    )
    end_time = forms.DateTimeField(  # 종료 시간 필드 (필수 아님)
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), 
        required=False
    )
    outer_clothes = forms.ImageField(required=False)  # 외투 이미지 필드 (필수 아님)
    top_clothes = forms.ImageField(required=False)  # 상의 이미지 필드 (필수 아님)
    bottom_clothes = forms.ImageField(required=False)  # 하의 이미지 필드 (필수 아님)

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'outer_clothes', 'top_clothes', 'bottom_clothes']
        labels = {
            'title': '일정',
            'description': '설명',
            'start_time': '시작 시간',
            'end_time': '종료 시간',
            'outer_clothes': '아우터',
            'top_clothes': '상의',
            'bottom_clothes': '하의',
        }
        error_messages = {
            'title': { 
                'required': "일정을 입력해주세요.",  # 제목 필드가 비어있을 때의 에러 메시지
            }
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        # 이미지 편집이 불가능한 경우, 해당 필드를 비활성화
        if instance and not instance.image_editable:
            for field in ['outer_clothes', 'top_clothes', 'bottom_clothes']:
                self.fields[field].widget.attrs['disabled'] = 'disabled'

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time is None:
            return self.fields['start_time'].initial or datetime.now()
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        start_time = self.cleaned_data.get('start_time')
        if end_time is None:
            end_time = start_time.replace(hour=23, minute=59)
        elif end_time < start_time:
            raise forms.ValidationError("종료 시간은 시작 시간 이후여야 합니다.")
        return end_time