import numpy as np
import tensorflow as tf
import cv2

from tensorflow.keras.preprocessing import image

label = ['covid-19','normal','puemonia']

#create interpreter object
interpreter = tf.lite.Interpreter(model_path="./model/trained_model/lite model/covidcnn_161.tflite")

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# initialize model
interpreter.allocate_tensors()


print(input_details,output_details)
img = cv2.imread('./model/samples/covid.jpg')

new_img = cv2.resize(img, (256, 256))   
img = image.img_to_array(new_img)
#img = np.expand_dims(img,axis=0)
img/=255

#inferencing
interpreter.set_tensor(input_details[0]['index'], [img])

interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])

print(label[np.argmax(output_data[0])])

