import requests
from tokens import *


class SpotifyController:
    def __init__(self):
        self.device_id = None
        self.access_token = None
        self.paused = True
        self.header = {}
        self.methods = {
            0: self.play,
            1: self.pause,
            2: self.next_song,
            3: self.prev_song
        }

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
        return response.json()

    def fetch_device_id(self):
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
        calling_method = self.methods.get(code)
        if calling_method:
            calling_method()
        else:
            print("Error calling the method")




