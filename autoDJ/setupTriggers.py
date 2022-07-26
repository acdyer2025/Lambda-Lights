import json
import requests

#Spotipy is a python library that makes it very easy to work with the spotify API
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import Client_ID, Client_Secret #stored in secrets.py - this file is ignored by GIT

scope = "user-read-playback-state,user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=Client_ID, client_secret=Client_Secret, redirect_uri='http://localhost'))

#load current song effects configuration
f = open('.\\songEffects.json','r')
songEffects = json.load(f)
f.close()

data = {
        'id': 'testID',
        'name': 'testName',
        'scenes': {
            'testName000': 0,
            'testName010': 10000,
            'testName020': 20000,
            'testName030': 30000
        }
}

songEffects.append(data)
print(songEffects)

f = open('.\\songEffects.json','w')
json.dump(songEffects, f, indent=4)
f.close()





