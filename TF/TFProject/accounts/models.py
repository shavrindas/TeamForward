from django.db import models

class UserData(models.Model):
    id          = models.AutoField(primary_key=True)
    email       = models.EmailField(max_length=254)
    password    = models.CharField(max_length=128)
    is_active   = models.BooleanField(default=True)  # 기본값 설정
    date_joined = models.DateTimeField(auto_now_add=True)  # auto_now_add 옵션 추가

    class Meta:
        db_table = 'user_data'
        managed  = True    # Django가 이 테이블을 관리하지 않도록 설정
