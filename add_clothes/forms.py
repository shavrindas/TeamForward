from django import forms
from .models import UserPicture

class UserPictureForm(forms.ModelForm):
    class Meta:
        model = UserPicture
        fields = ['picture'] 