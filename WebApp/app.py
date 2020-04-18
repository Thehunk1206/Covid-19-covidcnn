import cv2

import streamlit as st

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import numpy as np

import time

classes = ['Covid-19','normal','pneumonia']


@st.cache(suppress_st_warning=True)
def loadmodel():
    #st.info("Loading model for the firt time")
    model =  load_model('covid-19_161.h5')
    return model

def make_prediction(image,model):
    img = cv2.imread(image)
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

    return pred, result,(end-start)


def main():
    st.title('Covid Scanner')
    st.subheader('A webapp to scan x-ray to detect covid-19')
    model = loadmodel()
    st.success("model loaded Successfully")
    image_file = st.file_uploader("upload a X-ray image file",type=['png','jpg','jpeg'])
    if image_file is not None:
        scan = st.button('Scan')
        pred,result,inference_time = make_prediction(image=image_file,model=model)
        st.write(result)
        st.write("Confidence",np.max(pred[0])*100)
        st.info(f'[info] Inference took {(inference_time)*1000} ms')




#del(model)
main()
