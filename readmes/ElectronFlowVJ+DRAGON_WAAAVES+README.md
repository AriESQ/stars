known issues: 
- GUI scaling weirdness, will probably just make this a user input field
- Openbox window config on jetson
- FPS slider behavior is a bit hit or miss
- touchOSC file still needs some (read: lots of) work
- OSC reference needs updated

# DRAGON_WAAAVES v1.0

## Disclaimer

**This is NOT an official port of Gravity Waaaves.** The original creator, Andrei Jay, will not provide any support whatsoever for this software. 

This source code is distributed AS-IS, there is no guaranteed continuing support. Please contact ElectronFlow on discord with any questions, please have a clear and concise description of the problem.


**An updated/modified port of the original VSEJET GRAVITY_WAAAVES from Andrei Jay, Adding OSC, NDI, GPU texture sharing (in progress), and a couple other things to discover**

If you like the work I've done here, please consider supporting me on Ko-fi @ https://ko-fi.com/electronflow. 

Please also consider supporting Andrei either on Patreon @ https://www.patreon.com/c/andrei_jay, or his Ko-fi @ https://ko-fi.com/andreijay as this would not have been possible without the amazing groundwork he has laid out, and his willingness to open source his projects.

**Andrei's website:** [https://videosynthecosphere.com](https://videosynthesisecosphere.com)

You can download WPDSK here, which is a good introduction to the concepts present in this application, you can also buy GW-DSK there, which you should do. PLEASE GO SUPPORT HIM.

**Andrei's other website:** https://andreijaycreativecoding.com

A wealth of knowledge and resources about video synthesis, feedback, and programming these sorts of things.

**ElectronFlow's Website:** https://electronflow.tv

my art mostly

## Distribution

This software is only to be distributed as source code or on a Jetson disk image. Do not redistribute compiled binaries.

---

## What It Is

A dual-channel, 2 input video effects processor and synthesizer built with openFrameworks. Ported and expanded from the original VSEJET linux source.

## Features

- 3-block video processing chain with dual feedback loops
- Multiple input sources: webcam, NDI, Spout (Windows)
- OSC control with 700+ addressable parameters for automation
- MIDI macro mapping (16 macros per parameter group)
- Streaming output via NDI and Spout
- Preset bank system with save/load functionality
- Built in Lissajous Shape Generator

## Requirements

- NewTek NDI: ndi.video
- Spout2: spout.zeal.co

!!follow install instructions closely!!
- openFrameworks 0.12+ - https://github.com/openframeworks/openFrameworks.git

!!follow install instructions closely!!


- Required addons (see `addons.make`):
  - ofxImGui - https://github.com/jvcleave/ofxImGui.git
  - ofxMidi - https://github.com/danomatika/ofxMidi.git
  - ofxNDI - https://github.com/leadedge/ofxNDI.git
  - ofxOsc - Packaged with openFrameworks
  - ofxSpout - https://github.com/ElectronFlowVJ/ofxSpout.git (Windows only)


## Stuff

- The application runs with two windows: a control window (GUI) and an output window, but can also be used on single display, not recommended though.
- FPS is variable from 1-60 (affects GUI as well for now) 
- The output window can be set to fullscreen for production using F11, deocrations can be toggled with F10
- Presets are stored in `bin/data/presets/`

## OSC Reference

See `bin/data/OSC_Parameters_Reference.txt` for complete OSC address documentation.

## MIDI

For posterity's sake MIDI does still work with the original implementation, though you can change your device now. Might change this later tp be able to map CCs, but given the OSC implementation that isn't going to be any sort of priority for me.

Currently on works on Windows, crashes on jetson when you try to refresh devices. 
