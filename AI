import cv2
import tensorflow as tf
import numpy as np


class Processor:
    def __init__(self, interpreter):
        self.prev_prediction = None
        self.counter = 0
        self.interpreter = interpreter


    def process_single_frame(self, frame):

        frame = cv2.imdecode(frame, cv2.IMREAD_GRAYSCALE)
        frame = cv2.resize(frame, (224, 224))
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

        input_data = frame.reshape(1, 224, 224, 3)

        input_data = input_data.astype("float32")
        self.interpreter.set_tensor(0, input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(265)
        output_data = tf.nn.softmax(output_data).numpy()
        predicted_value = np.argmax()

        if np.max(output_data) >= 0.99 and self.prev_prediction == predicted_value:
            self.counter += 1
        else:
            self.counter = 0

        self.prev_prediction = predicted_value

        if self.counter == 10:
            return predicted_value
        else:
            return None

