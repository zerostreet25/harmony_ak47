import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split

# 데이터 로드
filename = "./IMU.xlsx"
data = pd.read_excel(filename, header=None, engine='openpyxl', names=['A', 'B', 'C', 'D', 'E', 'F', 'G'])

seq = data[['A', 'B', 'C', 'D', 'E', 'F']].to_numpy()
seq2 = data[['G']].to_numpy() - 1  # 1과 2를 0과 1로 변환

filename_2 = "./imu_data1.xlsx"
data_test = pd.read_excel(filename_2, header=None, engine='openpyxl', names=['A', 'B', 'C', 'D', 'E', 'F', 'G'])

seq_test = data_test[['A', 'B', 'C', 'D', 'E', 'F']].to_numpy()
seq2_test = data_test[['G']].to_numpy() - 1  # 1과 2를 0과 1로 변환

# 시퀀스 데이터 생성 함수
def create_sequences(data, target, time_steps=1):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps)])
        y.append(target[i + time_steps])
    return np.array(X), np.array(y)

time_steps = 3
X, y = create_sequences(seq, seq2, time_steps)
X_test, y_test = create_sequences(seq_test, seq2_test, time_steps)

# 데이터 분할
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# LSTM 모델 정의
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_steps, X.shape[2])))
model.add(LSTM(50))
model.add(Dense(1, activation='sigmoid'))  # 활성화 함수는 sigmoid로 유지

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 모델 학습
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_val, y_val))

# 모델 저장
model.save('lstm_model_binary.h5')
print("Model saved to lstm_model_binary.h5")

# 모델 평가
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}")

# 예측 수행
predictions = model.predict(X_test)
predictions_binary = (predictions > 0.5).astype(int) + 1  # 0과 1을 1과 2로 변환

# 예측 결과 출력
print(predictions_binary[:])  # 처음 10개 예측 결과 출력
