# add_clothes/views.py
import os
import sys
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from .models import UserData, UserPicture
from .forms import UserPictureForm
from django.contrib import messages

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
            img = img.resize((50, 50), Image.LANCZOS)
            
            # 이미지를 BytesIO에 저장하고 InMemoryUploadedFile로 변환합니다.
            output = BytesIO()
            img.save(output, format='JPEG', quality=100)
            output.seek(0)
            picture.picture = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % picture.picture.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
            
            # 이미지 이름을 저장합니다.
            picture.picture_name = picture.picture.name

            picture.user = user  # 현재 로그인한 사용자를 할당합니다.
            picture.save()
            return redirect('add_and_show')
    else:
        # GET 요청일 때는 새로운 이미지 폼을 생성합니다.
        form = UserPictureForm()
    
    # 현재 사용자의 모든 이미지를 가져옵니다.
    pictures = UserPicture.objects.filter(user=user)
    return render(request, 'add_clothes/addandshow.html', {'form': form, 'pictures': pictures, 'user': user})

def delete_picture(request, picture_id):
    picture = get_object_or_404(UserPicture, id=picture_id)
    
    # 이미지 파일을 삭제합니다.
    if os.path.exists(picture.picture.path):
        os.remove(picture.picture.path)
    
    picture.delete()
    return HttpResponseRedirect(reverse('add_and_show'))