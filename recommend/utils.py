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

def get_user_clothes():
    current_directory = os.getcwd()
    pictures_directory = os.path.join(current_directory, 'media', 'user_pictures')
    user_pictures = []

    for filename in os.listdir(pictures_directory):
        if filename.endswith('.jpg'):
            user_pictures.append(filename)
        else:
            continue
    return user_pictures
