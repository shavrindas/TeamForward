import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# GPU 디바이스 사용 설정
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 데이터 경로 설정
train_data_dir = "E:\\Data\\H1000"
validation_data_dir = "E:\Data\Testset"
img_width, img_height = 50, 50
batch_size = 32

# 이미지 데이터 생성기 설정
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

# 모델 구성
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(12, activation='softmax')
])

# 모델 컴파일
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# 모델 학습
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator)

# 모델 평가
loss, accuracy = model.evaluate(validation_generator)
print("Validation Loss:", loss)
print("Validation Accuracy:", accuracy)

# 모델 저장
model.save("D:/unsafe_code/TeamForward/back/Dina/resource/model/clothing_classification_model.h5")
