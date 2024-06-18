from django.db import models

class UserData(models.Model):
    id          = models.AutoField(primary_key=True)
    email       = models.EmailField(max_length=254)
    password    = models.CharField(max_length=128)
    is_active   = models.BooleanField(default=True) 
    date_joined = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'user_data'
        managed  = True    
