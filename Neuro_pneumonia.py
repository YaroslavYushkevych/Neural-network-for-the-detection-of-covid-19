'''
import os
for dirname, _, filenames in os.walk('/archive/chest_xray'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils.np_utils import to_categorical
import cv2
import glob
import gc
import pathlib

def lire_images(img_dir, xdim, ydim, nmax=5000) :
    label = 0
    label_names = []
    X = []
    y=[]
    for dirname in os.listdir(img_dir):
        print(dirname)
        label_names.append(dirname)
        data_path = os.path.join(img_dir + "/" + dirname,'*g')
        files = glob.glob(data_path)
        n=0
        for f1 in files:
            if n>nmax : break
            img = cv2.imread(f1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (xdim,ydim))
            X.append(np.array(img))
            y.append(label)
            n=n+1
        #print(n,' images lues')
        label = label+1
    X = np.array(X)
    y = np.array(y)
    gc.collect()
    return X,y, label, label_names

def plot_scores(train) :
    accuracy = train.history['accuracy']
    val_accuracy = train.history['val_accuracy']
    epochs = range(len(accuracy))
    plt.plot(epochs, accuracy, 'b', label='Score apprentissage')
    plt.plot(epochs, val_accuracy, 'r', label='Score validation')
    plt.title('Scores')
    plt.legend()
    plt.show()

train_path = pathlib.Path("E:/Neuro/archive/chest_xray/train")
test_path = pathlib.Path("E:/Neuro/archive/chest_xray/test")
val_path = pathlib.Path("E:/Neuro/archive/chest_xray/val")


X_train,y_train,Nombre_classes,Classes = lire_images("E:/Neuro/archive/chest_xray/train", 224, 224, 1000)
X_test,y_test,Nombre_classes,Classes = lire_images("E:/Neuro/archive/chest_xray/test", 224, 224, 1000)
X_val,y_val,Nombre_classes,Classes = lire_images("E:/Neuro/archive/chest_xray/val", 224, 224, 1000)

x_train = X_train / 255
x_test = X_test / 255
x_val = X_val / 255
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
y_val = tf.keras.utils.to_categorical(y_val)

model = Sequential()
model.add(Conv2D(32, (5, 5), padding='same', input_shape=(224, 224, 3), activation='relu'))
model.add(MaxPooling2D((2, 2), strides=2))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D((2, 2), strides=2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(Nombre_classes, activation='softmax'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

train = model.fit(x_train,
                  y_train,
                  validation_data=(x_val, y_val),
                  epochs=40,
                  batch_size=256,
                  verbose=1)

model.save('pneumo_B_dence.h5')

model.summary()

scores = model.evaluate(x_test, y_test, verbose=0)
print("Score : %.2f%%" % (scores[1]*100))

plot_scores(train)
'''

import numpy as np
import pandas as pd
import seaborn as sns
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Flatten,MaxPooling2D,Conv2D,Dropout,Activation,BatchNormalization
from tensorflow.keras.preprocessing import image
from sklearn.metrics import classification_report,confusion_matrix
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

train_dir = (r"E:/Neuro/archive/chest_xray/train")
test_dir = (r"E:/Neuro/archive/chest_xray/test")
classes_train =os.listdir(train_dir)
classes_test =os.listdir(test_dir)
print(classes_train)

train_datagen=ImageDataGenerator(
    #zoom_range=0.2, #the amount of zooming u need
    horizontal_flip=True, # Make a horizontal copy of image
    rescale=1/255, # Normalize the new images
    width_shift_range=0.10, # The percentage of Width shifitning
    height_shift_range=0.10, # The percentage of height shifitning
    shear_range=0.1, #Shear angle in counter-clockwise direction in degrees
    fill_mode='nearest',
    rotation_range=20,
)
train_generator=train_datagen.flow_from_directory(
    train_dir,
    class_mode='binary',
    color_mode='rgb',
    batch_size= 16,
    target_size=(1000,1000,3)[:2]
)

test_datagen=ImageDataGenerator(rescale=1/255)
test_generator=test_datagen.flow_from_directory(
    test_dir,
    class_mode='binary',
    color_mode='rgb',
    batch_size=16,
    target_size=(1000,1000,3)[:2]
)

earlystop=EarlyStopping(patience=6)
learning_rate_reduction=ReduceLROnPlateau(
    monitor='val_acc',
    patience= 3,
    verbose=1,
    factor=0.5,
    min_lr=0.00001
)
callbacks = [earlystop, learning_rate_reduction]

model=Sequential()

model.add(Conv2D(32,(2,2),activation='relu',input_shape=(1000,1000,3)))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(64,(2,2),activation='relu'))
model.add(MaxPooling2D(3,3))

model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(3,3))

model.add(Flatten())
model.add(Dropout(0.4))
model.add(Dense(128, activation='relu'))

model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam' ,loss='binary_crossentropy',metrics=['accuracy'])

model.summary()

model.fit(
    train_generator,
    epochs=3,
    validation_data=test_generator,
    callbacks=callbacks
)

losses = pd.DataFrame(model.history.history)
losses[['accuracy','val_accuracy']].plot()

losses[['loss','val_loss']].plot()

model.evaluate(test_generator)

real = test_generator.classes
print(real)

predictions = model.predict_generator(test_generator) > 0.5
print(predictions)

con = confusion_matrix(real, predictions)
print(sns.heatmap(con,cmap="coolwarm" ,annot=True,fmt="d",linewidths=1 ,square= True))
print('report :',classification_report(real, predictions ))

predict_path=r'E:\Neuro\archive\chest_xray\val\NORMAL\NORMAL2-IM-1430-0001.jpeg'
my_image = image.load_img(predict_path,target_size=(1000,1000,3))

my_image = np.expand_dims(my_image,axis = 0)

np.argmax(model.predict(my_image))

model.save('pneumo_C_dence.h5')