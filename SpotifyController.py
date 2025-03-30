import requests
from tokens import *


class SpotifyController:
    def __init__(self):
        self.header = None
        self.device_id = None
        self.access_token = None
        self.paused = True
        self.methods = None


    def fetch_access_token(self, code):
        """Fetches the access token from Spotify."""
        payload = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REACT_APP_REDIRECT_URI,
            'client_id': REACT_APP_CLIENT_ID,
            'client_secret': REACT_APP_CLIENT_SECRET
        }

        response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
        print('RESPONSE:', response.json())
        data = response.json
        response_access_token = data.access_token


        self.access_token = response_access_token
        self.header = {
            'Authorization': f'Bearer { self.access_token}',
            'Content-Type': 'application/json'
        }
        return response.json()

    def fetch_device_id(self):
        print('AAAAA', self.header)
        """Fetches the active device ID from Spotify."""
        response = requests.get(f"{SPOTIFY_PLAYER_API_URL}devices", headers=self.header)
        data = response.json()

        self.device_id = data["devices"][0]["id"]

    def update_access_token(self, access_token):
        self.access_token = access_token
        self.header = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def next_song(self):
        response = requests.post(f"{SPOTIFY_PLAYER_API_URL}next?device_id={self.device_id}", self.header)
        return response

    def prev_song(self):
        response = requests.post(f"{SPOTIFY_PLAYER_API_URL}previous?device_id={self.device_id}", self.header)
        return response

    def pause(self):
        self.paused = True
        response = requests.put(f"{SPOTIFY_PLAYER_API_URL}pause?device_id={self.device_id}", self.header)
        return response

    def play(self):
        self.paused = False
        response = requests.put(f"{SPOTIFY_PLAYER_API_URL}play?device_id={self.device_id}", self.header)
        return response

    def call_method(self, code):
        if code == 'play':
            self.play()
        elif code == 'pause':
            self.pause()
        elif code == 'next':
            self.next_song()
        elif code == 'previous':
            self.prev_song()

