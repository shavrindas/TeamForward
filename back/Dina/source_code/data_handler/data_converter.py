import os
import hashlib
from PIL import Image
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime

def resize_images():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    # 작업할 폴더의 상대 경로 설정
    input_folder = os.path.join(parent_dir, 'resource', 'temp_pic')
    output_folder = os.path.join(parent_dir, 'resource', 'set_pic')

            
    for filename in os.listdir(input_folder):
        input_filepath = os.path.join(input_folder, filename)
        if os.path.isfile(input_filepath) and \
                (filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png')):
            with Image.open(input_filepath) as img:
                resized_img = img.resize((540, 480))
                current_time = time.strftime("%Y%m%d%H%M%S")
                new_filename = f"{current_time}_{filename}"
                output_filepath = os.path.join(output_folder, new_filename)
                resized_img.save(output_filepath)

                try:
                    print(f"이미지 {filename}이(가) {output_filepath}로 저장되었습니다.")
                    os.remove(input_filepath)  # 원본 이미지 파일 삭제
                except Exception as e:
                    print(f"이미지 {filename} 저장에 실패했습니다: {e}")



