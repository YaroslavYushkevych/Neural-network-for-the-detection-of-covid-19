import random
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

import method

method.photo_path_add()

model = load_model(r'E:\Neuro\pneumo_C_dence.h5')

predict_dir = r"E:\Neuro\archive\Predict"

train_datagen_ones_photo = ImageDataGenerator(
    horizontal_flip=True,
    rescale=1/255,
    width_shift_range=0.10,
    height_shift_range=0.10,
    shear_range=0.1,
    fill_mode='nearest',
    rotation_range=20
)
predict_generator = train_datagen_ones_photo.flow_from_directory(
    predict_dir,
    class_mode='binary',
    color_mode='rgb',
    batch_size= 16,
    target_size=(1000,1000,3)[:2]
)

predictions = model.predict(predict_generator)
marker_true, marker_false = 0, 0
predict_1 = predictions > 0.5

for i in range(0, len(predict_1)):
    #print(f"{i+1}-predictions: {predictions[i][0]} = {predict_1[i][0]}")
    if predict_1[i][0] == True:
        marker_true += 1
    elif predict_1[i][0] == False:
        marker_false += 1
print(f'1N===== \nTrue: {marker_true} \nFalse: {marker_false}')

if marker_false < marker_true:
    result_num_pneumo = 1
    print("Pneumonia \n")
    method.clear_dir()
else:
    result_num_pneumo  = 0
    print("no Pneumonia \n")
    method.clear_dir()
    #method.clear_eval()



random_num_covid = random.randint(0, 1)
#print(random_num_covid)