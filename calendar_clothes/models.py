from django.db import models
from accounts.models import UserData  

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE) 
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        db_table = 'event'
