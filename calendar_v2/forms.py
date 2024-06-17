from django import forms
from .models import Event2

class EventForm(forms.ModelForm):
    description = forms.CharField(required=False, label='설명')
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='날짜'
    )

    class Meta:
        model = Event2
        fields = ['title', 'description', 'date']
        labels = {
            'title': '일정',
        }
        error_messages = {
            'title': {
                'required': "일정을 입력해주세요.",
            }
        }
