import cv2

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import numpy as np

import argparse

import time

# Argparser
ap = argparse.ArgumentParser()
ap.add_argument("-m","--model",type=str,required=True,help="path to model")
ap.add_argument("-i","--image",type=str,required=True,help="path to input image")
args = vars(ap.parse_args())

classes = ['Covid-19','normal','pneumonia']

#load model
print("[info] Loading model...")
model = load_model(args['model'])
print("[info] model loaded...")
print(f"[info] Model Summary")
print(model.summary())


#read image
img = cv2.imread(args['image'])

#resize image
img = cv2.resize(img,(256,256))

#Converting to float32 and normalizing 
img = image.img_to_array(img)
img = np.expand_dims(img,axis=0)
img/=255

start = time.time()
#predict
pred = model.predict(img)
end = time.time()
result = classes[np.argmax(pred[0])]
print(result)
print("Confidence",np.max(pred[0])*100)

print(f'[info] Inference took {(end-start)*1000} ms')

del(model)
