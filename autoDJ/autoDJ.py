import json
from typing import overload
import requests
import time
import math
from threading import Timer

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import Client_ID, Client_Secret

scope = "user-read-playback-state,user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=Client_ID, client_secret=Client_Secret, redirect_uri='http://localhost'))


def main():

    newSongFlag = False
    currentSongID = ''
    idList = []

    f = open("songEffects.json", "r")
    songEffects = json.load(f)
    f.close()

    songList = list(songEffects)
    for i in range(0, len(songEffects)):
        idList.append(songEffects[songList[i]]['id'])
    print(idList)

    while(True):
        if(checkForSong(idList) == True):
            currentPlayer = spotify.currently_playing()
            print(currentPlayer)
            currentSongID = currentPlayer['item']['id']
            for i in range(0, len(idList)):
                if(currentSongID == idList[i]):
                    currentSongDuration = currentPlayer['item']['duration_ms']
                    currentSongTimestamp = currentPlayer['progress_ms']
                    currentSongSceneList = list(songEffects[songList[i]]['scenes'])
                    timeStamps = []

                    for j in range(0, len(currentSongSceneList)):
                        timeStamps.append(songEffects[songList[i]]['scenes'][currentSongSceneList[j]])
                    
                    hasPlayed = list(timeStamps)
                    
                    prevTime = int(time.time()*1000)
                    while(int(time.time()*1000) - prevTime) <= (currentSongDuration - currentSongTimestamp):
                        for i in range(0, len(timeStamps)):
                            if((int(time.time()*1000) - prevTime + currentSongTimestamp) > timeStamps[i]):
                                if(hasPlayed[i] != True):
                                    changeScene(currentSongSceneList[i])
                                    hasPlayed[i] = True
                    print("finished")
        time.sleep(5)

def changeScene(sceneName):
    url = "http://127.0.0.1:8888/api/scenes"
    payload = json.dumps({
        "id": sceneName,
        "action": "activate"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)

def checkForSong(idList):
    currentPlayer = spotify.currently_playing()
    currentSongID = currentPlayer['item']['id']
    print(currentSongID)
    for i in range(0, len(idList)):
        print(idList[i])
        if(currentSongID == idList[i]):
            return(True)
        else:
            pass
    return(False)
    #print("Spotify is not playing anyting right now")

main()