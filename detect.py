import cv2

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import numpy as np

classes = ['Covid-19','normal','pneumonia']

#load model
model = load_model('model/trained_model/covid-19_161.h5')

#read image
img = cv2.imread('model/samples/pbact1.jpeg')

#resize image
img = cv2.resize(img,(256,256))

#Converting to float32 and normalizing 
img = image.img_to_array(img)
img = np.expand_dims(img,axis=0)
img/=255

#predict
pred = model.predict(img)
result = classes[np.argmax(pred[0])]
print(result)
print("Confidence",np.max(pred[0])*100)

del(model)
