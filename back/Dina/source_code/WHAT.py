import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# 저장된 모델 불러오기
model = tf.keras.models.load_model("D:/unsafe_code/TeamForward/back/Dina/resource/model/clothing_classification_model.h5")

# 클래스 레이블 정의
class_names = ["옷1", "옷2", "옷3", "옷4", "옷5", "옷6", "옷7", "옷8", "옷9", "옷10", "옷11", "옷12"]

# 예측할 이미지 폴더 경로
image_folder_path = r"D:/unsafe_code/TeamForward/back/Dina/resource/set_pic"

# 폴더 내의 모든 이미지 파일에 대해 예측 수행 및 결과 출력
for filename in os.listdir(image_folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # 이미지 파일인 경우에만
        img_path = os.path.join(image_folder_path, filename)
        img = image.load_img(img_path, target_size=(50, 50))  # 이미지를 모델 입력 크기에 맞게 로드
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가
        img_array /= 255.  # 이미지를 0과 1 사이의 값으로 스케일링
        prediction = model.predict(img_array)
        predicted_class_index = np.argmax(prediction)
        predicted_class_name = class_names[predicted_class_index]
        print(f"이미지 '{filename}'의 예측 결과: {predicted_class_name}")
