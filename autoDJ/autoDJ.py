import json
import requests
import time
from threading import Timer

#Spotipy is a python library that makes it very easy to work with the spotify API
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import Client_ID, Client_Secret #stored in secrets.py - this file is ignored by GIT

scope = "user-read-playback-state,user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=Client_ID, client_secret=Client_Secret, redirect_uri='http://localhost'))

#load song effects list
f = open('.\\songEffects.json','r')
songEffects = json.load(f)
f.close()

#songStatus = ['state', 'spotify_song_id', duration_ms, progress_ms]
songStatus = ['',0,0,0]
idList = []

for i in range(0, len(songEffects)):
    idList.append(songEffects[i]['id'])

print(idList)

def main():

    #start timer to poll spotify every 5 seconds to get current song
    t = Timer(5, checkForSong, [idList, True])
    t.start()

    while(True):
        global songStatus
    
        if(songStatus[0] == 'inList'): #the song spotify is currently playing is one that effects exist for
            print('found song in list')
            currentSong = songStatus[1]
            currentSongDuration = songStatus[2]
            currentSongTimestamp = songStatus[3]
            currentSongSceneList = list(songEffects[currentSong]['scenes'])
            timeStamps = []
            for i in range(0, len(currentSongSceneList)):
                timeStamps.append(songEffects[currentSong]['scenes'][currentSongSceneList[i]])
            
            hasPlayed = list(timeStamps)
            
            prevTime = time.time()*1000
            prevSong = songStatus[1]

            while((time.time()*1000 - prevTime) <= (currentSongDuration - currentSongTimestamp)):
                #print("Running custom song effects")
                if(songStatus[1] != prevSong):
                    print("song changed")
                    break
                for i in range(0, len(timeStamps)):
                    if(time.time()*1000 - prevTime + currentSongTimestamp > timeStamps[i]):
                        if(hasPlayed[i] != True):
                            changeScene(currentSongSceneList[i])
                            hasPlayed[i] = True
            
            print("finished with current song")
            time.sleep(1)
            checkForSong(idList, False)

        elif(songStatus[0] == 'none'):
            print('found song not present in list')
            currentSongDuration = songStatus[2]
            currentSongTimestamp = songStatus[3]
            prevTime = time.time()*1000
            prevSong = songStatus[1]

            while((time.time()*1000 - prevTime) <= (currentSongDuration - currentSongTimestamp)):
                #print("Running custom song effects")
                if(songStatus[1] != prevSong):
                    print("song changed")
                    break

            print("finished with current song")
            time.sleep(1)
            checkForSong(idList, False)
        elif(songStatus[0] == 'spotifyUnavailable'):
            print("Spotify Client Unavaiable")
        else:
            pass

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

def checkForSong(idlist, startTimer):
    
    global songStatus
    print("checking for song")

    if(startTimer == True):
        t = Timer(5, checkForSong, [idlist, True])
        t.start()

    try:
        currentPlayer = spotify.currently_playing()
        songID = currentPlayer['item']['id']
        songStatus[2] = currentPlayer['item']['duration_ms']
        songStatus[3] = currentPlayer['progress_ms']
        print(songStatus)
    except Exception as e:
        print(e)
        songStatus = ['spotifyUnavailable', -1, -1, -1]
        return

    for songIndex in range(0, len(idlist)):
        if(songID == idlist[songIndex]):
            songStatus[0] = 'inList'
            songStatus[1] = songIndex
            return 
        else:
            pass
    songStatus[0] = 'none'
    songStatus[1] = -1
    return

main()