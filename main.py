import cv2
import tensorflow as tf
import numpy as np
import time
gesture_val = None

gestures = ['Fist', 'One finger', 'Palm', 'Three fingers']


interpreter = tf.lite.Interpreter(model_path="converted_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)
print(output_details)

print("Loading camera...")
cam = cv2.VideoCapture(0)
beforeFrame = None
i=0
prev_Hand = None
while True:
    ret, img = cam.read()
    frame = cv2.resize(img, (224,224))
    input_data = frame.reshape(1,224,224,3)
    input_data = input_data.astype("float32")
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    sm_preferred = tf.nn.softmax(output_data).numpy()
    if np.max(sm_preferred)>=0.9925 and beforeFrame == str(np.argmax(output_data)):
       i+=1
    else:
       i=0
       gesture_val=None
    beforeFrame = str(np.argmax(output_data))
    if i>10:
       gesture_val = int(np.argmax(output_data))
       if gesture_val != prev_Hand:
           print(gestures[gesture_val])
           prev_Hand = gesture_val

    k = cv2.waitKey(1)
    if k != -1:
        break
cam.release()
cv2.destroyAllWindows()