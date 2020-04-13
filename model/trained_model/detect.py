import cv2

import tensorflow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import numpy as np


model = load_model('covid-19_161.h5')

classes = ['Covid-19','normal','pneumonia']

img = cv2.imread('pbact1.jpeg')


img = cv2.resize(img,(256,256))

img = image.img_to_array(img)

img = np.expand_dims(img,axis=0)
img/=255

pred = model.predict(img)
print(pred[0])
result = classes[np.argmax(pred[0])]

print(result)


del(model)
