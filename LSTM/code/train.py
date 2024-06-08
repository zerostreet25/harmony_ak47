import keras
import numpy as np
#import matplotlib.pyplot as plt
import tensorflow as tf

#from keras.utils import np_utils
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
# import tensorflow.keras.backend as K
import pandas as pd

# def get_f1(y_true, y_pred): #taken from old keras source code
#     true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
#     possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
#     predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
#     precision = true_positives / (predicted_positives + K.epsilon())
#     recall = true_positives / (possible_positives + K.epsilon())
#     f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
#     return f1_val

filename = "./IMU.xlsx"
data =  pd.read_excel(filename, header= None ,engine='openpyxl', names = ['A','B','C','D','E','F','G'])

seq = data[['A','B','C','D','E','F']].to_numpy()  #,'D','E','F'
seq2 = data[['G']].to_numpy()


def seq2dataset(seq,seq2, window, horizon):
    X = []; Y = []
    for i in range(len(seq)-(window+horizon)+1):
        x = seq[i:(i+window)]
        y = seq2[i:i+window+horizon-1].max()
        X.append(x); Y.append(y)
    return np.array(X), np.array(Y)

w = 5
h = 1
X,Y = seq2dataset(seq,seq2, w, h)
Y = np.delete(to_categorical(Y),0,axis =1)

filename_2 = "./imu_data1.xlsx"
data_test =  pd.read_excel(filename_2, header= None ,engine='openpyxl', names = ['A','B','C','D','E','F','G'])

seq_test = data_test[['A','B','C','D','E','F']].to_numpy()  #
seq2_test = data_test[['G']].to_numpy()


def seq2dataset_1(seq_test,seq2_test, window, horizon):
    X_test = []; Y_test = []
    for i in range(len(seq_test)-(window+horizon)+1):
        x_1 = seq_test[i:(i+window)]
        y_1 = seq2_test[i:i+window+horizon-1].max()
        X_test.append(x_1); Y_test.append(y_1)
    return np.array(X_test), np.array(Y_test)

w_test = 5
h_test = 1
X_test,Y_test = seq2dataset_1(seq_test,seq2_test, w_test, h_test)
Y_test = np.delete(to_categorical(Y_test),0,axis =1)


x_train = X
y_train = Y
x_test = X_test
y_test = Y_test


model = Sequential()
model.add(LSTM(units = 256, activation = 'relu', input_shape = x_train[0].shape))
model.add(Dense(256, activation = "relu"))
model.add(Dense(128, activation = "relu"))
model.add(Dense(64, activation = 'relu'))
model.add(Dense(2, activation = 'softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam') #, metrics = ['accuracy',get_f1]
hist = model.fit(x_train, y_train, epochs = 3, batch_size = 128,
                 validation_data = (x_test,y_test),verbose = 1)

ev = model.evaluate(x_test,y_test,verbose = 0)
#print("손실 함수: ",ev[0],"accuracy",ev[1])

model.save( "./TEST1.h5")
