import json
from pathlib import Path
from django.conf import settings
import os

import os


def read_class_indices_clothesdata():
    file_path = settings.BASE_DIR / 'add_clothes' / 'model' / 'class_indices.json'
    with open(file_path, 'r') as f:
        class_indices = json.load(f)
    return class_indices

import os

def get_user_clothes():
    current_directory = os.getcwd()
    pictures_directory = os.path.join(current_directory, 'media', 'user_pictures')
    #pictures_directory = 'C:/TeamForward-recommendation/media/user_pictures'  # 사용자 사진이 저장된 디렉토리 경로
    user_pictures = []

    # 사용자 사진 디렉토리의 모든 파일에 대해 반복
    for filename in os.listdir(pictures_directory):
        # 파일 확장자가 이미지인 경우에만 리스트에 추가
        if filename.endswith('.jpg'):
            user_pictures.append(filename)
        else:
            continue
    return user_pictures
