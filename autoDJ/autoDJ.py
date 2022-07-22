import json
import requests
import time
from threading import Timer

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import Client_ID, Client_Secret

scope = "user-read-playback-state,user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=Client_ID, client_secret=Client_Secret, redirect_uri='http://localhost'))

songStatus = ['','','',0,0]
idList = []

f = open('C:\\Users\\EY Zeta\\scripts\\lambdaLights\\autoDJ\\songEffects.json','r')
songEffects = json.load(f)
f.close()

songList = list(songEffects)
for i in range(0, len(songEffects)):
    idList.append(songEffects[songList[i]]['id'])
print(idList)

def main():

    t = Timer(5, checkForSong, [idList, True])
    t.start()

    while(True):
        global songStatus
        #print(songStatus)
        if(songStatus[0] == 'inList'):
            print('found song in list')
            currentSong = songStatus[2]
            currentSongDuration = songStatus[3]
            currentSongTimestamp = songStatus[4]
            currentSongSceneList = list(songEffects[currentSong]['scenes'])
            timeStamps = []
            for j in range(0, len(currentSongSceneList)):
                timeStamps.append(songEffects[currentSong]['scenes'][currentSongSceneList[j]])
            
            hasPlayed = list(timeStamps)
            
            prevTime = time.time()*1000
            prevID = songStatus[1]

            while((time.time()*1000 - prevTime) <= (currentSongDuration - currentSongTimestamp)):
                #print("Running custom song effects")
                if(songStatus[1] != prevID):
                    print("song changed")
                    break
                for i in range(0, len(timeStamps)):
                    if(time.time()*1000 - prevTime + currentSongTimestamp > timeStamps[i]):
                        if(hasPlayed[i] != True):
                            changeScene(currentSongSceneList[i])
                            hasPlayed[i] = True
            
            print("finished with current song")
            time.sleep(0.5)
            checkForSong(idList, False)

        elif(songStatus[0] == 'none'):
            print('found song not present in list')
            currentSongDuration = songStatus[3]
            currentSongTimestamp = songStatus[4]
            prevTime = time.time()*1000
            prevID = songStatus[1]

            while((time.time()*1000 - prevTime) <= (currentSongDuration - currentSongTimestamp)):
                #print("Running custom song effects")
                if(songStatus[1] != prevID):
                    print("song changed")
                    break

            print("finished with current song")
            time.sleep(1)
            checkForSong(idList, False)
        elif(songStatus[0] == 'spotifyUnavailable'):
            print("Spotify Client Unavaiable")
            break
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

    try:
        currentPlayer = spotify.currently_playing()
        songStatus[1] = currentPlayer['item']['id']
        songStatus[3] = currentPlayer['item']['duration_ms']
        songStatus[4] = currentPlayer['progress_ms']
    except Exception as e:
        print(e)
        songStatus = ['spotifyUnavailable', 'empty', 'empty', 0, 0]
        return

    t = Timer(5, checkForSong, [idlist, True])
    t.start()

    for i in range(0, len(idlist)):
        if(songStatus[1] == idlist[i]):
            songStatus = ['inList', songStatus[1], songList[i], currentPlayer['item']['duration_ms'], currentPlayer['progress_ms']]
            return 
        else:
            pass
    songStatus = ['none', songStatus[1], songStatus[2], currentPlayer['item']['duration_ms'], currentPlayer['progress_ms']]

    return

main()