from flask import Flask, request
import requests
from flask_cors import CORS
from tokens import *
import time

app = Flask(__name__)
CORS(app)
api_response = None

def fetch_access_token(code):
    #separated fetching function
    req_body = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REACT_APP_REDIRECT_URI,
        'client_id': REACT_APP_CLIENT_ID,
        'client_secret': REACT_APP_CLIENT_SECRET
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=req_body)
    return response.json()


def fetch_next_track(token, deviceId):
    req_header = build_header(token)
    url_with_device_id = f"{SPOTIFY_PLAYER_NEXT}?device_id={deviceId}"
    response = requests.post(url_with_device_id, headers=req_header)
    print(response.json())
    return response.json()


def fetch_device_id(token):
    req_header = build_header(token)
    response = requests.post(SPOTIFY_PLAYER_NEXT, headers=req_header)
    print(response.json())
    return response.json()


def build_header(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    return headers

@app.route("/nexttrack", methods=['POST'])
def nexttrack():
    global api_response
    print(api_response)
    deviceId = fetch_device_id(api_response["access_token"])
    print(deviceId)
    response = fetch_next_track(api_response["access_token"], deviceId["device_id"])
    return response


@app.route("/auth", methods=['POST'])
def auth():
    data = request.json
    code = data.get('code')

    if not code:
        return {"error": "Code is required"}, 400  # Ensure access is always a boolean
    
    
    global api_response
    api_response = fetch_access_token(code)  # Fetch token from Spotify API
    time_stamp = time.time()
    api_response['time stamp'] = time_stamp
    print(api_response)

    if 'access_token' in api_response:
        return {"access": True}

    return { "error": api_response.get("error", "Unknown error")}, 400 #responce

if __name__ == '__main__':
    app.run(debug=True)
