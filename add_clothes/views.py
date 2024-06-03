# add_clothes/views.py
import sys  # sys 모듈 import 추가

from django.shortcuts import render, redirect, get_object_or_404
from .models import UserData, UserPicture  # 필요한 모델을 import 해야합니다.
from .forms import UserPictureForm  # 이미지 폼을 import 해야합니다.
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image

def yet(request):
    return render(request, 'add_clothes/yet.html')
# add_clothes/views.py


def add_and_show(request):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        # 로그인이 필요한 경우 로그인 페이지로 리디렉션합니다.
        messages.error(request, '로그인이 필요합니다.')
        return redirect('login')
    
    user = get_object_or_404(UserData, id=user_id)

    if request.method == 'POST':
        # POST 요청일 때는 이미지를 추가합니다.
        form = UserPictureForm(request.POST, request.FILES)
        if form.is_valid():
            # 이미지를 업로드하고 사이즈를 조정합니다.
            picture = form.save(commit=False)
            image_file = picture.picture
            img = Image.open(image_file)
            img = img.resize((50, 50), Image.LANCZOS)  # Image.ANTIALIAS 대신 Image.LANCZOS 사용
            
            # 이미지를 BytesIO에 저장하고 InMemoryUploadedFile로 변환합니다.
            output = BytesIO()
            img.save(output, format='JPEG', quality=100)
            output.seek(0)
            picture.picture = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % picture.picture.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
            
            picture.user = user  # 현재 로그인한 사용자를 할당합니다.
            picture.save()
            return redirect('add_and_show')
    else:
        # GET 요청일 때는 새로운 이미지 폼을 생성합니다.
        form = UserPictureForm()
    
    # 현재 사용자의 모든 이미지를 가져옵니다.
    pictures = UserPicture.objects.filter(user=user)
    return render(request, 'add_clothes/addandshow.html', {'form': form, 'pictures': pictures, 'user': user})