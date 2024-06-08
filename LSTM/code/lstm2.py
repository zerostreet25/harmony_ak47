from tensorflow.keras.models import load_model
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

cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

# 모델 로드
model = tf.keras.models.load_model('./lstm_model_binary.h5')

# 데이터 버퍼 초기화
window_size = 3  # 모델에 입력으로 사용할 시퀀스 길이
data_buffer = []

# 데이터 전처리 함수
def preprocess_data(data_buffer, window_size):
    if len(data_buffer) >= window_size:
        # 버퍼에서 시퀀스를 추출
        seq_data = np.array(data_buffer[-window_size:])
        return seq_data.reshape(1, window_size, 6)
    else:
        return None

# 실시간 데이터 수집 및 예측
while True:
    cursor.execute("START TRANSACTION")
    # 데이터베이스에서 최신 데이터 3개 가져오기
    query = "SELECT ax, ay, az, gx, gy, gz FROM imu_data ORDER BY id DESC LIMIT 3"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.execute("COMMIT")
    print(results)

    if results:
        data_buffer.extend(results)
        data_buffer = data_buffer[-window_size:]  # 버퍼 크기를 window_size로 유지
        input_data = preprocess_data(data_buffer, window_size)
        
        if input_data is not None:
            prediction = model.predict(input_data)
            prediction_binary = (prediction > 0.5).astype(int) + 1  # 0과 1을 1과 2로 변환
            print(f"Prediction: {prediction_binary[0][0]}")
    time.sleep(1)  # 1초마다 데이터 갱신

# MySQL 연결 닫기
cursor.close()
conn.close()
