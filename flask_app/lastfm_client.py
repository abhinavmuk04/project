import requests
from flask_login import current_user


class LastFmClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://ws.audioscrobbler.com/2.0/'

    def search_album(self, search_string):
        params = {
            'method': 'album.search',
            'album': search_string,
            'api_key': self.api_key,
            'format': 'json'
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()['results']['albummatches']['album']
            print("API Data:", data)
            return response.json()['results']['albummatches']['album']
        else:
            print("Request URL:", response.url)
            print("Failed to retrieve data:", response.status_code, response.json())
            return None
        
    def search_art(self, search_string):
        params = {
            'method': 'artist.search',
            'artist': search_string,
            'api_key': self.api_key,
            'format': 'json'
        }
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            response_data = response.json()
            print("Full API Response:", response_data)

            try:
                artists = response_data['results']['artistmatches']['artist']
                print("API Data:", artists)
                return artists
            except KeyError:
                print("KeyError: Could not find the expected keys in the response.")
                return None
        else:
            print("Request URL:", response.url)
            print("Failed to retrieve data:", response.status_code, response.json())
            return None


    def get_top_albums(self, period='overall', limit=50, page=1):
        if not current_user.is_authenticated:
            return []
        username = current_user.username
        params = {
        'method': 'chart.getTopTracks',
        'user': username,
        'period': period,
        'limit': limit,
        'page': page,
        'api_key': self.api_key,
        'format': 'json'
        }
        response = requests.get(self.base_url, params=params)
        print("Request URL:", response.url)
        print("Response Content:", response.content)
        if response.status_code == 200:
            data = response.json().get('tracks', {}).get('track', [{}])
            print("API Data:", data)
            return data
        elif response.status_code == 404:
            print("User not found:", response.json())
            return []
        else:
             print("Failed to retrieve data:", response.status_code, response.json())
             return []
