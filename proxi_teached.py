import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist         # библиотека базы выборок Mnist
from tensorflow import keras

from tensorflow.keras.models import load_model

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# стандартизация входных данных
x_train = x_train / 255
x_test = x_test / 255

y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

x_train = np.expand_dims(x_train, axis=3)
x_test = np.expand_dims(x_test, axis=3)

#print( x_train.shape )

model = load_model('proxi_mnist_dence.h5')

model.evaluate(x_test, y_test)

predict = model.predict(x_test)

print (predict[0])

#for i in range(0, 10):
#    print(np.argmax(predict[i]))
#    print(np.argmax(y_test[i]))

scores = model.evaluate(x_test, y_test, verbose=0)
print("Score : %.2f%%" % (scores[1]*100))

