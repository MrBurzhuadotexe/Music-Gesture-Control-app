from flask import Flask, request
import requests
from flask_cors import CORS
from tokens import *

app = Flask(__name__)
CORS(app)

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


@app.route('/')
def home():
    return "BLANK"


@app.route("/auth", methods=['POST'])
def auth():
    data = request.json
    code = data.get('code')

    if not code:
        return {"error": "Code is required"}, 400  # Ensure access is always a boolean

    api_response = fetch_access_token(code)  # Fetch token from Spotify API
    print(api_response)

    if 'access_token' in api_response:
        return {"access": True}

    return { "error": api_response.get("error", "Unknown error")}, 400 #responce

if __name__ == '__main__':
    app.run(debug=True)
