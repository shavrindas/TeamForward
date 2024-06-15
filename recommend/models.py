from django.db import models
from datetime import date
from accounts.models import UserData
from add_clothes.models import UserPicture
from django.db import models

class RecommendedClothes(models.Model):
    id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=254)  # 사용자 이메일 필드 추가
    bottom = models.CharField(max_length=100)
    outer = models.CharField(max_length=100)
    date = models.DateField()
    top = models.CharField(max_length=100)
    style = models.CharField(max_length=100)

    class Meta:
        db_table = 'recommended_clothes'