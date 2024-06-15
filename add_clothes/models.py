# add_clothes/models.py

from django.db import models
from accounts.models import UserData  
class UserPicture(models.Model):
    
    
    user        = models.ForeignKey(UserData, on_delete=models.CASCADE)
    picture     = models.ImageField(upload_to='user_pictures/')
    upload_date = models.DateTimeField(auto_now_add=True)
    picture_name= models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'user_picture'
        managed = True
