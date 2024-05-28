# fos_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import CustomUser

def home(request):
    return render(request, 'fos_app/home.html')

def login_view(request):
    return render(request, 'fos_app/login.html')

#def signup_view(request):
#    return render(request, 'fos_app/signup.html') 

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        # 비밀번호와 비밀번호 확인이 일치하는지 확인합니다.
        if password == confirm_password:
            # 비밀번호를 해시화하여 저장합니다.
            hashed_password = make_password(password)
            # 사용자를 생성합니다.
            user = CustomUser.objects.create_user(email=email, password=hashed_password)
            # 회원가입이 완료되면 로그인 페이지로 리디렉션합니다.
            return redirect('login')  # 'login'은 로그인 페이지의 URL name입니다.
        else:
            # 비밀번호가 일치하지 않는 경우에 대한 처리를 추가할 수 있습니다.
            pass
    
    # GET 요청이면 회원가입 폼을 반환합니다.
    return render(request, 'fos_app/signup.html')


def forgotpassword_view(request):
    return render(request, 'fos_app/forgotpassword.html') 

def setting_view(request):
    return render(request, 'fos_app/setting.html')


def temp_fine_view(request):
    user = request.user
    return render(request, 'fos_app/temp_fine.html', {'user': user})

@login_required
def forgot_password_remake_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        if password == confirm_password:
            # 비밀번호 재설정 로직을 여기에 추가
            # 예를 들어, request.user의 비밀번호를 새로운 비밀번호로 업데이트하고 성공 메시지를 표시할 수 있습니다.
            request.user.set_password(password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # 세션의 인증 해시 갱신
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')

    return render(request, 'fos_app/forgotpasswordremake.html')

