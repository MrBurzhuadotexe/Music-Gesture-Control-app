from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from tokens import *
import time
import uuid
from flask_socketio import SocketIO
import tensorflow as tf
from AI import Processor
from SpotifyController import SpotifyController

import base64
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


interpreter = tf.lite.Interpreter(model_path="my_model.tflite")
interpreter.allocate_tensors()

ai = Processor(interpreter)
controller = SpotifyController()




@app.route("/auth", methods=['POST'])
def auth():
    """Handles authentication and stores the access token."""
    data = request.json
    code = data.get('code')

    if not code:
        return jsonify({"error": "Code is required"}), 400

    api_response = controller.fetch_access_token(code)

    if 'access_token' in api_response:
        token_api = api_response['access_token']
        api_response['timestamp'] = time.time()
        api_response['id'] = str(uuid.uuid4())
        return jsonify({"access": True, "id": api_response["id"]})

    return jsonify({"error": api_response.get("error", "Unknown error")}), 400


@socketio.on('videoframe')
def handle_video(data):

    try:
        # Decode the base64 image
        image_data = base64.b64decode(data.split(',')[1])
        frame = np.frombuffer(image_data, np.uint8)
        gesture_code = ai.process_single_frame(frame)
        if gesture_code is not None:
            controller.call_method(gesture_code)

    except Exception as e:
        print(f"Error processing frame: {e}")


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, allow_unsafe_werkzeug=True)

