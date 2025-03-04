from flask import Flask, request
import requests
from flask_cors import CORS
from tokens import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "BLANK"


@app.route("/auth", methods=['POST'])
def auth():
    data = request.json
    code = data['code']
    req_body = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REACT_APP_REDIRECT_URI,
        'client_id': REACT_APP_CLIENT_ID,
        'client_secret': REACT_APP_CLIENT_SECRET
    }
    api_response = requests.post(REACT_APP_REDIRECT_URI, data=req_body).json()
    return api_response['access_token']


if __name__ == '__main__':
    app.run(debug=True)
