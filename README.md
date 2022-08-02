# Welcome to Lambda Lights
The Lambda Lights are a large LED strip installation designed to provide dancing, music-reactive lightshows in the basement of our house during social functions. This repository is intended as documentation and reference for the current users of this installation on how the strips are connected, powered, and controlled. The goal is that this installation should last for years to come, even if the original installer (Adam Dyer) is no longer around, which is why this repo was created. 

Please note that this installation is still in its infanacy, and many changes are expected to happen in the future before a final design is reached. Likewise, this repo is still very much a work in progress.

# General Overview
Lambda Lights consists of 2000 WS2815 individually addressable LED pixels connected in four distinct sections. basementRender.png shows how these four sections are arranged. Each section consists of a dedicated ESP32 microcontroller running software called WLED (see https://kno.wled.ge/ for more information). Each of those WLED instances is connected to software running on a dedicated laptop called LedFx (see https://www.ledfx.app/ for more information). This allows for each section to be set to a different music reactive effect, all based on the sound input on the dedicated laptop. 

This repository also contains a Python script that runs on the laptop on startup that starts all the required programs and sets the network configuration on the laptop automatically. During the lightshows, it also periodically checks to make sure everything is still connected and functioning as expected, taking steps if necessary to fix issues that may come up without the user having to intervene at all.

# DOCUMENTATION TODO

* Add detailed schematics of main power distribution box
* Add detailed schematics of underBar setup
* Add screenshots of each WLED config page for each WLED instance
* Update README with much more detailed explanations, troubleshooting, etc

