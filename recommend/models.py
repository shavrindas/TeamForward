from django.db import models
from datetime import date

class RecommendedClothes(models.Model):
    date = models.DateField(default=date.today) 
    top = models.CharField(max_length=100)
    bottom = models.CharField(max_length=100)
    outer = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.date} - {self.top}, {self.bottom}, {self.outer}"
