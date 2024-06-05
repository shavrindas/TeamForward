# add_clothes/forms.py

from django import forms
from .models import UserPicture

class UserPictureForm(forms.ModelForm):
    class Meta:
        model = UserPicture
        fields = ['picture']  # 사용자 필드 제거
