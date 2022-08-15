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
                pingStatus = ping(config['hotspotAddress'], 1)
                if(pingStatus == 0):
                    print("Starting Hotspot...")
                    subprocess.Popen([r'.\batchFiles\\hotspot.bat'])
                elif(pingStatus == 1):
                    print("Hotspot Connected")
                    state = 1
                else:
                    print("Invalid hotspot IP address. Check config.json")
            except Exception as e:
                print(e)

        while(state == 1): 
            for i in range(len(config['deviceAddresses'])):   
                try:
                    pingStatus = ping(config['deviceAddresses'][deviceList[i]], 1)
                    if(pingStatus == 0):
                        print(deviceList[i] + " is not connected to hotspot.\n")
                        connectedDevices[i] = False
                    elif(pingStatus == 1):
                        print(deviceList[i] + " is connected to hotspot")
                        connectedDevices[i] = True
                    else:
                        print("Invalid " +deviceList[i]+ " IP address. Check config.json")
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
                pingStatus = ping(config['hotspotAddress'], 1)
                if(pingStatus != 1):
                    state = 0
            except Exception as e:
                print(e)
                state = 0
           

def ping(host, packets):
    command = [r'.\batchFiles\ping.bat ', str(packets), host]
    try:    
        returnValue = subprocess.call(command)
        return returnValue
    except Exception as e:
        print(e)
        return 3


if __name__ == "__main__":
    main()