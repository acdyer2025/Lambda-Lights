# Welcome to Lambda Lights
The Lambda Lights are a large LED strip installation designed to provide dancing, music-reactive lightshows in the basement of our house during social functions. This repository is intended as documentation and reference for the current users of this installation on how the strips are connected, powered, and controlled. The goal is that this installation should last for years to come, even if the original installer (Adam Dyer) is no longer around, which is why this repo was created. 

Please note that this installation is still in its infanacy, and many changes are expected to happen in the future before a final design is reached. Likewise, this repo is still very much a work in progress.

# General Overview
Lambda Lights consists of 2000 WS2815 individually addressable LED pixels connected in four distinct sections. basementRender.png shows how these four sections are arranged. Each section consists of a dedicated ESP32 microcontroller running a program called WLED. Each of those ESP32's is connected through WLED to software called LedFx running on a dedicated computer or laptop. This allows for each section to be set to a different music reactive effect, all based on the sound input on the dedicated computer or laptop. 

This repository also contains a Python script that runs on the laptop on startup that starts all the required programs and sets the network configuration on the laptop automatically. During the lightshows, it also periodically checks to make sure everything is still connected and functioning as expected, taking steps if necessary to fix issues that may come up without the user having to intervene at all.

# Installation Steps
* Clone this repository
* Create a new python virtual enviroment (Optional, but highly recommended)
    * Install required packages

* Flash WLED onto each ESP32 - see https://kno.wled.ge/
    * Configure WLED with the correct network settings
    * set the static ip address to whatever you want the the ip address for each device to be

* Install LedFx (I use a fork of the original LedFx software called BladeMod. It has a better user interface and some slighty different effect settings) - https://github.com/YeonV/LedFx-Frontend-v2
    * **Note: Currently tested to work with release Beta46 - https://github.com/YeonV/LedFx-Frontend-v2/releases/tag/2.0.0-beta46**
    * **From that release, navigate to assets then download and run LedFx_CC-beta46--win-setup.exe**

* Configure LedFx
    * set up all devices in LedFx with ip addresses you set in WLED

* Fill in config.json
    * replace hotspotAddress with your hotspot's ip address (Note: Must be a 2.4 Ghz hotspot)
    * add to device addresses the names and ip address's of your WLED devices (name can be anything). The ip must match the ip of the device in LedFx and WLED
    * replace ledFxPath with the path to your ledFx executable

* Install a virtual audio cable - I use https://vb-audio.com/Cable/
    * This allows you to send the audio to both ledFx and your speakers. Make sure you set the audio input in LedFx accordinly.
    You might have to go to Control Panel - Sound - Recording - Cable Output Properties - Listen and check the 'listen' box as
    well as select Speakers in the playback through device menu

# Integrations

My related project, LedFx-autoDJ, was designed for this installation as a way to easily program the strips to change their effect based on timestamps in Spotify songs.

# DOCUMENTATION TODO

* Add detailed schematics of main power distribution box
* Add detailed schematics of underBar setup
* Add screenshots of each WLED config page for each WLED instance
* Update README with much more detailed explanations, troubleshooting, etc

