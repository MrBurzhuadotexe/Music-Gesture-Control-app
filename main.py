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


def fetch_next_track(token, device_id):
    """Skips to the next track on the given device."""
    headers = build_header(token)
    url = f"{SPOTIFY_PLAYER_API_URL}next?device_id={device_id}"
    response = requests.post(url, headers=headers)
    return response.json()


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


@app.route("/nexttrack", methods=['POST'])
def next_track():
    """Skips to the next track on the user's active Spotify device."""
    global token_api

    if not token_api:
        return jsonify({"error": "No active session. Please authenticate."}), 401

    device_id = fetch_device_id(token_api)
    if not device_id:
        return jsonify({"error": "No active device found. Please play music on a device."}), 400

    response = fetch_next_track(token_api, device_id)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)