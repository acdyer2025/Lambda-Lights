# This is the main script to automate the setup and configuration for Lambda Lights
# A shortcut should be placed to the batch file initLambdaLights.bat in the startup folder if this script should run at startup
# Created by Adam Dyer, summer 2022

import subprocess
import time
import requests
import json

headers = requests.utils.default_headers()

f = open("config.json", "r")
config = json.load(f)
f.close()

deviceList = list(config['deviceAddresses'])

def main():

    #test if built in mobile hotspot is turned on, if not turn it on
    
    try:
        if(ping(config['hotspotAddress'], 1) == False):
            print("Starting Hotspot...")
            subprocess.Popen([r'.\batchFiles\hotspot.bat'])
        else:
            print("Hotspot Connected")
    except:
        print("Hotspot could not be started, or is already turned on. Please check batchFiles\hotspot.bat")
    
    pingCheck = 0
    connectedDevices = 0
    while(pingCheck < config['initialConnectionTimeout'] and connectedDevices != len(config['deviceAddresses'])):
        for i in range(len(config['deviceAddresses'])):    
            if(ping(config['deviceAddresses'][deviceList[i]], 1) == False):
                print(deviceList[i] + " is not connected.\n")
            else:
                print(deviceList[i] + "Successfully Connected")
                connectedDevices += 1
        pingCheck += 1
            
    if(connectedDevices == 0):
        print('Error: All devices timed out on the initial connection attempt. Please make sure devices are turned on and IP addresses are set correctly')
        print('Contiuing to ping for devices in background')
        while(connectedDevices == 0):
            if(ping(config['hotspotAddress'], 1) == False):
                print("The hotspot is no longer connected")
            else:
                for i in range(len(config['deviceAddresses'])):    
                    if(ping(config['deviceAddresses'][deviceList[i]], 1) == True):
                        print(deviceList[i]+ "Successfully Connected. Verifying LedFx...")
                        connectedDevices += 1

    elif(connectedDevices == len(config['deviceAddresses'])):
        print('All Devices connected. Verifying LedFx connection...')
    else:
        print('Warning: Some devices timed out on the initial connection attempt. Check IP Addresses for those particular devices.')
        print('Verifying LedFx connection...')

    #Check to make sure that LedFx started correctly
    #Also restarts LedFx in the event of a crash (Somewhat common)

    while(True):
        if(ping(config['hotspotAddress'], 1) == False):
            print("The hotspot is no longer connected")
        else:
            for i in range(len(config['deviceAddresses'])):
                try:
                    response = requests.get("http://" + config['deviceAddresses'][deviceList[i]] + "/json/info")
                    responseObject = json.loads(response.content)
                except Exception as e:
                    print("unable to connect to " + deviceList[i] + ". Exception")
                    print(e)
                    print(deviceList[i] + " has disconnected from the network")
                else:
                    if(responseObject["live"] == False):
                        print(deviceList[i] + " has disconnected from LedFx. Restarting LedFx")
                        subprocess.Popen([r'.\batchFiles\stopLedFx.bat'])
                        subprocess.Popen([r'.\batchFiles\startLedFx.bat'])
                        time.sleep(10)
                    else:
                        print("Connected to hotspot, devices, and LedFx")

def ping(host, packets):
    command = [r'.\batchFiles\ping.bat ', str(packets), host]
    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0


if __name__ == "__main__":
    main()