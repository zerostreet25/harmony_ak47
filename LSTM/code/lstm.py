from tensorflow.keras.models import load_model
from tensorflow.keras.initializers import Orthogonal
import tensorflow.keras.backend as K

def get_f1(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2 * (precision * recall) / (precision + recall + K.epsilon())
    return f1_val

custom_objects = {'Orthogonal': Orthogonal, 'get_f1': get_f1}
model = load_model('./test.h5', custom_objects=custom_objects)

import mysql.connector
import numpy as np
import tensorflow as tf
import time

# MySQL 데이터베이스 연결 설정
db_config = {
    'user': 'ysn',
    'password': 'aaaa',
    'host': '127.10.20.12',
    'database': 'test'
}

# MySQL 데이터베이스 연결
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 모델 로드
model = tf.keras.models.load_model('./TEST1.h5', custom_objects={'get_f1': get_f1})

# 데이터 버퍼 초기화
window_size = 5  # 모델에 입력으로 사용할 시퀀스 길이
data_buffer = []

# 데이터 전처리 함수
def preprocess_data(data_buffer, window_size):
    if len(data_buffer) >= window_size:
        return np.array(data_buffer[-window_size:]).reshape(1, window_size, 6)
    else:
        return None

# 실시간 데이터 수집 및 예측
while True:
    # 데이터베이스에서 최신 데이터 가져오기
    query = "SELECT A, B, C, D, E, F FROM imu_data ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        data_buffer.append(result)
        input_data = preprocess_data(data_buffer, window_size)
        
        if input_data is not None:
            prediction = model.predict(input_data)
            print(f"Prediction: {prediction}")
    
    time.sleep(1)  # 1초마다 데이터 갱신
