import streamlit as st

import tensorflow as tf
from tensorflow.keras.preprocessing import image

import numpy as np

import time

from PIL import Image

classes = ['Covid-19','normal','pneumonia']


def loadmodel():
    interpreter = tf.lite.Interpreter(model_path="covidcnn_161.tflite")
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.allocate_tensors()
    return interpreter,input_details,output_details


def make_prediction(image_buf,interpreter,input_details,output_details):
    img=Image.open(image_buf)
    img = img.convert('RGB')
    #resize image
    img = img.resize((256,256))
    
    #Converting to float32 and normalizing 
    img = image.img_to_array(img)
    #img = np.expand_dims(img,axis=0)
    img/=255
    start = time.time()
    
    #predict
    interpreter.set_tensor(input_details[0]['index'], [img])

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    end = time.time()
    #set results
    result = classes[np.argmax(output_data[0])]

    return output_data, result,(end-start)


def main():
    st.markdown("# Covid Scanner")
    
    st.header('Scan x-ray to detect covid-19')
    
    image_file = st.file_uploader("upload a X-ray image file",type=['png','jpg','jpeg'])
    if image_file is not None:
        image = Image.open(image_file)
        st.image(image,use_column_width=True)    
        scan = st.button('Scan')
        if scan:
            interpreter,input_details,output_details = loadmodel()
            pred,result,inference_time = make_prediction(image_buf=image_file,interpreter=interpreter,input_details=input_details,output_details=output_details)
            st.subheader("Result: "+result)
            st.write("Confidence %.2f" %(np.max(pred[0])*100)+"%")
            st.info('Inference took %.2f ms'%((inference_time)*1000))
    st.sidebar.markdown("# Warning")
    st.sidebar.markdown("*This is model is not reliable to use and it is just for Research purposes")
    
    


#del(model)
if __name__ == "__main__":
    main()
