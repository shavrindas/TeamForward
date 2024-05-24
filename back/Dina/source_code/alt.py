import tensorflow as tf
from tensorflow.keras import layers, models

# 데이터 경로 설정
train_data_dir = "E:\Data\H1000"
validation_data_dir = "D:\\unsafe_code\\TeamForward\\back\\Dina\\resource\\data_get_pic"
img_width, img_height = 50, 50
batch_size = 32

# 모델 구성
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(12, activation='softmax')  # 12개의 클래스에 대한 softmax 출력
])

# 모델 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 모델 요약 확인
model.summary()

# 데이터 전처리 후 모델 훈련
# 이 부분은 실제 데이터와 함께 코드를 실행해야 하므로 생략합니다.


# 모델 저장
model.save('my_model.h5')
