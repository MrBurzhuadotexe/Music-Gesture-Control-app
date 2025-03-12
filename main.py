from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from tokens import *
import time
import uuid
from flask_socketio import SocketIO

import base64
import cv2
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

token_api = None
api_response = None


def fetch_access_token(code):
    """Fetches the access token from Spotify."""
    payload = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REACT_APP_REDIRECT_URI,
        'client_id': REACT_APP_CLIENT_ID,
        'client_secret': REACT_APP_CLIENT_SECRET
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
    return response.json()


def fetch_device_id(token):
    """Fetches the active device ID from Spotify."""
    headers = build_header(token)
    response = requests.get(f"{SPOTIFY_PLAYER_API_URL}devices", headers=headers)
    data = response.json()

    if "devices" in data and data["devices"]:
        return data["devices"][0]["id"]

    return None


def build_header(token):
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@app.route("/auth", methods=['POST'])
def auth():
    """Handles authentication and stores the access token."""
    global token_api, api_response
    data = request.json
    code = data.get('code')

    if not code:
        return jsonify({"error": "Code is required"}), 400

    api_response = fetch_access_token(code)

    if 'access_token' in api_response:
        token_api = api_response['access_token']
        api_response['timestamp'] = time.time()
        api_response['id'] = str(uuid.uuid4())
        return jsonify({"access": True, "id": api_response["id"]})

    return jsonify({"error": api_response.get("error", "Unknown error")}), 400


@app.route("/postcommand", methods=['POST'])
def post_to_spotify():  # list of commands: next, previous, pause, play...
    data = request.json
    command = data.get('command')
    global token_api

    if not token_api:
        return jsonify({"error": "No active session. Please authenticate."}), 401

    device_id = fetch_device_id(token_api)

    if not device_id:
        return jsonify({"error": "No active device found. Please play music on a device."}), 400

    headers = build_header(token_api)
    url = f"{SPOTIFY_PLAYER_API_URL}{command}?device_id={device_id}"
    if command in ['next', 'previous']:
        response = requests.post(url, headers=headers)
    else:
        response = requests.put(url, headers=headers)

    return response.json()


def get_from_spotify():
    pass


@socketio.on('videoframe')
def handle_video(data):
    try:
        # Decode the base64 image
        image_data = base64.b64decode(data.split(',')[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        print(frame)
        if frame is not None:
            # Create a new window for display
            cv2.namedWindow("Received Frame", cv2.WINDOW_NORMAL)
            cv2.imshow("Received Frame", frame)
            cv2.waitKey(1)
        else:
            print("Failed to decode frame")
    except Exception as e:
        print(f"Error processing frame: {e}")


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, allow_unsafe_werkzeug=True)
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from tokens import *
import time
import uuid

app = Flask(__name__)
CORS(app)

token_api = None
api_response = None


def fetch_access_token(code):
    """Fetches the access token from Spotify."""
    payload = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REACT_APP_REDIRECT_URI,
        'client_id': REACT_APP_CLIENT_ID,
        'client_secret': REACT_APP_CLIENT_SECRET
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
    return response.json()


def fetch_device_id(token):
    """Fetches the active device ID from Spotify."""
    headers = build_header(token)
    response = requests.get(f"{SPOTIFY_PLAYER_API_URL}devices", headers=headers)
    data = response.json()

    if "devices" in data and data["devices"]:
        return data["devices"][0]["id"]

    return None


def build_header(token):
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@app.route("/auth", methods=['POST'])
def auth():
    """Handles authentication and stores the access token."""
    global token_api, api_response
    data = request.json
    code = data.get('code')

    if not code:
        return jsonify({"error": "Code is required"}), 400

    api_response = fetch_access_token(code)

    if 'access_token' in api_response:
        token_api = api_response['access_token']
        api_response['timestamp'] = time.time()
        api_response['id'] = str(uuid.uuid4())
        return jsonify({"access": True, "id": api_response["id"]})

    return jsonify({"error": api_response.get("error", "Unknown error")}), 400


@app.route("/postcommand", methods=['POST'])
def post_to_spotify(): #list of commands: next, previous, pause, play...
    data = request.json
    command = data.get('command')
    global token_api

    if not token_api:
        return jsonify({"error": "No active session. Please authenticate."}), 401

    device_id = fetch_device_id(token_api)

    if not device_id:
        return jsonify({"error": "No active device found. Please play music on a device."}), 400

    headers = build_header(token_api)
    url = f"{SPOTIFY_PLAYER_API_URL}{command}?device_id={device_id}"
    if command in ['next', 'previous']:
        response = requests.post(url, headers=headers)
    else:
        response = requests.put(url, headers=headers)

    return response.json()

def get_from_spotify():
    pass

if __name__ == '__main__':
    app.run(debug=True)
