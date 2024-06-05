# add_clothes/views.py
import os
import sys
import json
import numpy as np
from PIL import Image
from io import BytesIO
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages
from .models import UserData, UserPicture
from .forms import UserPictureForm
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# 모델 로드
model_path = os.path.join(os.path.dirname(__file__), 'model/clothes_classification_model.h5')
model = load_model(model_path)

# 클래스 인덱스 로드
class_indices_path = os.path.join(os.path.dirname(__file__), 'model/class_indices.json')
with open(class_indices_path, 'r') as f:
    class_indices = json.load(f)
class_labels = {v: k for k, v in class_indices.items()}

def predict_clothes(img):
    img = img.resize((50, 50), Image.LANCZOS)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    
    predicted_label = class_labels[predicted_class[0]]
    
    return predicted_label



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
            
            # 이미지 이름을 예측된 레이블로 저장합니다.
            predicted_label = predict_clothes(img)
            picture.picture_name = predicted_label
            
            # 이미지를 BytesIO에 저장하고 InMemoryUploadedFile로 변환합니다.
            img = img.resize((50, 50), Image.LANCZOS)
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

def delete_picture(request, picture_id):
    picture = get_object_or_404(UserPicture, id=picture_id)
    
    # 이미지 파일을 삭제합니다.
    if os.path.exists(picture.picture.path):
        os.remove(picture.picture.path)
    
    picture.delete()
    return HttpResponseRedirect(reverse('add_and_show'))
