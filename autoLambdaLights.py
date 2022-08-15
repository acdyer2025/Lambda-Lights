# This is the main script to automate the setup and configuration for Lambda Lights
# A shortcut should be placed to the batch file initLambdaLights.bat in the startup folder if this script should run at startup
# Created by Adam Dyer, summer 2022

import subprocess
import time
import requests
import json

headers = requests.utils.default_headers()

f = open(".\\config.json", "r")
config = json.load(f)
f.close()

deviceList = list(config['deviceAddresses'])

def main():

    state = 0
    connectedDevices = list()
    for i in range(len(config['deviceAddresses'])):
        connectedDevices.append(False)

    while(True):
        while(state == 0):#test if built in mobile hotspot is turned on, if not turn it on    
            try:
                if(ping(config['hotspotAddress'], 1) == False):
                    print("Starting Hotspot...")
                    subprocess.Popen([r'.\batchFiles\\hotspot.bat'])
                else:
                    print("Hotspot Connected")
                    state = 1
            except:
                print("Hotspot could not be started, or is already turned on. Please check batchFiles\hotspot.bat")

        while(state == 1): 
            print(state)   
            for i in range(len(config['deviceAddresses'])):   
                try: 
                    if(ping(config['deviceAddresses'][deviceList[i]], 1) == False):
                        print(deviceList[i] + " is not connected to hotspot.\n")
                        connectedDevices[i] = False
                    else:
                        print(deviceList[i] + " is connected to hotspot")
                        connectedDevices[i] = True
                except Exception as e:
                    print(e)
            
            for i in range(len(connectedDevices)):
                if(connectedDevices[i] == True):
                    try:
                        url = 'http://' + config['deviceAddresses'][deviceList[i]] + '/json/info'
                        response = requests.request('GET', url)
                        responseObject = json.loads(response.content)
                        if(response.status_code != 200):
                            connectedDevices[i] = False
                            print(deviceList[i]+ 'Disconnected')
                    except Exception as e:
                        print("unable to connect to " + deviceList[i] + ". Exception")
                        print(e)
                    else:
                        if(responseObject["live"] == False):
                            print('LedFx has disconneced. Restarting LedFx')
                            try:
                                subprocess.Popen([r'.\batchFiles\stopLedFx.bat'])
                            except Exception as e:
                                print(e)
                            try:
                                subprocess.Popen([r'.\batchFiles\startLedFx.bat', config['ledFxPath']])
                            except Exception as e:
                                print(e)
                            else:
                                time.sleep(10)
                        else:
                            print(deviceList[i]+' is connected to LedFx')
                else:
                    pass
            try:
                if(ping(config['hotspotAddress'], 1) == False):
                    state = 0
            except:
                state = 0

def ping(host, packets):
    command = [r'.\batchFiles\ping.bat ', str(packets), host]
    try:    
        return subprocess.call(command, stdout=subprocess.DEVNULL) == 0
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    main()