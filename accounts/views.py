from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import UserData
import hashlib

def main_page(request):
    return render(request, 'accounts/main_page.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if UserData.objects.filter(email=email).exists():
            messages.error(request, '이미 사용 중인 이메일입니다.')
            return render(request, 'accounts/signup.html')
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        UserData.objects.create(email=email, password=hashed_password, is_active=True, date_joined=timezone.now())
        
        messages.success(request, '회원가입이 완료되었습니다.')
        return redirect('login')
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            user = UserData.objects.get(email=email, password=hashed_password)
            response = redirect('user_session')
            response.set_cookie('user_id', user.id)
            return response
        except UserData.DoesNotExist:
            messages.error(request, '유효하지 않은 이메일 또는 비밀번호입니다.')
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')

def user_session(request):
    user_id = request.COOKIES.get('user_id')
    if user_id:
        user = get_object_or_404(UserData, id=user_id)
        return render(request, 'accounts/user_session.html', {'username': user.email})
    else:
        return redirect('login')
    
def find_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if UserData.objects.filter(email=email).exists():
            user = UserData.objects.get(email=email)
            return render(request, 'accounts/edit_account.html', {'user_id': user.id})
        else:
            messages.error(request, '해당 이메일로 가입된 계정을 찾을 수 없습니다.')
            return render(request, 'accounts/find_account.html')
    else:
        return render(request, 'accounts/find_account.html')

def edit_account(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(UserData, id=user_id)
        
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and new_password == confirm_password:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            user.password = hashed_password
            user.save()
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('login')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'accounts/edit_account.html', {'user_id': user_id})
    else:
        return redirect('main_page')


def edit_profile(request):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        messages.error(request, '로그인이 필요합니다.')
        return redirect('login')
    
    user = get_object_or_404(UserData, id=user_id)

    if request.method == 'POST':
        if 'change_email' in request.POST:
            new_email = request.POST.get('new_email')
            if new_email:
                if UserData.objects.filter(email=new_email).exists():
                    messages.error(request, '이미 사용 중인 이메일입니다.')
                else:
                    user.email = new_email
                    user.save()
                    messages.success(request, '이메일이 성공적으로 변경되었습니다.')
            else:
                messages.error(request, '유효한 이메일을 입력해주세요.')
        
        elif 'change_password' in request.POST:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password and new_password == confirm_password:
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                user.password = hashed_password
                user.save()
                messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')

        elif 'delete_account' in request.POST:
            user.delete()
            messages.success(request, '계정이 성공적으로 삭제되었습니다.')
            return redirect('signup')

    return render(request, 'accounts/edit_profile.html', {'username': user.email})

def logout(request):
    response = redirect('login')
    response.delete_cookie('user_id')
    return response
