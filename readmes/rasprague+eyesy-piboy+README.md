# eyesy-piboy

The operating system for the EYESY video synthesizer device - remixed. Then re-remixed for use on
- PiBoy DMG
  - Tested on Raspberry Pi 4 B with the official [PiBoy DMG Image](https://experimentalpi.com/downloads.html).
- WaveShare Game HAT
  - Tested on Raspberry Pi 3 B+ with RetroPie v4.8.
- a plain old Raspberry Pi 3 B+ with RetroPie v4.8.

Adaptation of the Critter&Guitari Eyesy video synth in order to run it on a regular Raspberry Pi

Eyesy Manual : https://www.critterandguitari.com/manual?m=EYESY_Manual#eyesy%E2%84%A2-user-manual

### Notable changes
- [add command-line argument support for sound device, rate, and period](https://github.com/rasprague/eyesey-piboy/commit/a640d715b3b469e6a3f973992e64beeec6938cbf)
- [add start_python_foreground.sh to start python video in foreground](https://github.com/rasprague/eyesey-piboy/commit/7edb6ddf3b73518912475c6f1862e6e80f524363)
- [add list-pcms.py utility to list available sound cards](https://github.com/rasprague/eyesey-piboy/commit/98bd0b147c0dbe6e897164b15b3fb9db83462efd)
- [add /quit OSC message, create controller-osc.py to translate gamepad controller presses to OSC messages](https://github.com/rasprague/eyesey-piboy/commit/4f8dc3119ef0065946df1a9d0a6ccee58265c5e5)
- [add controller mapping file support, add mapping files for piboy and gamehat](https://github.com/rasprague/eyesy-piboy/commit/eae1708e8e9cb8db1901d44f0f766a95962f1582)
- [add joy-test.py to discover controller buttons](https://github.com/rasprague/eyesy-piboy/commit/b2f58d58e75b2bd9e9cab657c21d9009cea360d8)
- [sync OSC value changes to controller-osc.py](https://github.com/rasprague/eyesy-piboy/commit/e6749d7559480240c5e7739a6fb403c5192c48ea)
- [add support for "dummy" alsa sound capture device](https://github.com/rasprague/eyesy-piboy/commit/98427a621791b2ea767e2b31218a364e04cec4fb)
- [Add option to disable double-buffering](https://github.com/rasprague/eyesy-piboy/commit/ccbcfd584a001f4f9d48cd8aef8e7f5689afb6ae)
- [add eyesy-choose.sh startup script](https://github.com/rasprague/eyesy-piboy/commit/c56c8a807bbd707720399c4f125a1b950605054a)
- [change midi values for scene / mode change, new assignments reflect arturia knob default Relative 1 mode, also better for  korg cc keys, 0,64=ignored, 61-63=prev, 65-67=next](https://github.com/rasprague/eyesy-piboy/commit/42ff29c75b9e5e5ab5aaabec05b33751e6bcbd81)
- [let max gain go to 10](https://github.com/rasprague/eyesy-piboy/commit/5c023c8ba7c78441e99cca0c03420a69c45b540f)
- [keyboard support](https://github.com/rasprague/eyesy-piboy/commit/597810ea52835ecc2044511bc437fb50a8e1de50)

# Thanks to
- [okyeron](https://github.com/okyeron) for doing the hard work of [porting Eyesy to Raspberry Pi](https://github.com/okyeron/EYESY_OS_for_RasPi)
- [Critter & Guitari](https://www.critterandguitari.com/) for the amazing work with the [Eyesy Video Synthesizer](https://www.critterandguitari.com/eyesy) (suport Critter & Guitari, go buy their products!)
- The great and wonderful [Pygame](https://www.pygame.org/) on top of which this is all built

# Requirements
- A working Raspberry Pi / Retropie setup on one of the following handheld hardware:
  - PiBoy DMG, see [the PiBoy DMG Getting Started guide](https://resources.experimentalpi.com/the-complete-piboy-dmg-getting-started-guide/)
  - Waveshare Game HAT, see [the Game HAT Wiki](https://www.waveshare.com/wiki/Game_HAT) and [manual](https://www.waveshare.com/w/upload/2/22/Game_HAT_user_manual_en.pdf)
  - a plain old Raspberry Pi 3 B+
  - other systems may work but will need additional support, e.g. you get it working and share your findings with us, or you can send me some hardware so I might get is working =]

# Installation

The instructions assume that you already have a working Retropie installation with an internet connection.

**Open Terminal or SSH into you Pi and run the following commands:**

### Download source code, build
```
git clone https://github.com/rasprague/eyesy-piboy.git Eyesy
cd Eyesy
./deploy.sh
 ```

### Make scripts user executable
```
chmod u+x *.sh *.py
chmod u+x controller/controller-osc.py
```

# Adding m8c to EmulationStation

### Install eyesy 'ROMs'
#### create rom driectory
```
mkdir -p /home/pi/RetroPie/roms/eyesy
```
#### Install stock startup scripts
```
ln -s /home/pi/Eyesy/eyesy-choose.sh /home/pi/RetroPie/roms/eyesy/eyesy-choose.sh
```
You can use the eyesy-choose.sh script to choose your settings when starting up Eyesy, but better to create a custom startup script for your hardware configuration

#### find your sound hardware
- attach your sound hardware (USB or otherwise) to your PiBoy
- run ```./list-pcms.py -a | sort```, you'll see something like
```
default:CARD=Headphones
default:CARD=CODEC
...
```
  in this example, my Behringer u-Control USB audio interface is "default:CARD=CODEC" (the "Headphones" entry is the audio on-board the RaspberryPi, which doesn't support audio capture)

#### make a custon startup script
in this example I'll create a custom startup script for my u-Control audio interface, change names as appropriate

- run
```
cp eyesy-piboy-example.sh /home/pi/RetroPie/roms/eyesy/eyesy-ucontrol.sh
```
if you're on a PiBoy  

or
```
cp eyesy-gamehat-example.sh /home/pi/RetroPie/roms/eyesy/eyesy-ucontrol.sh
```
if you're on a Game HAT

or
```
cp eyesy-raspi-example.sh /home/pi/RetroPie/roms/eyesy/eyesy-ucontrol.sh
```
if you're on a plain old Raspberry Pi

- now edit your script
```
nano /home/pi/RetroPie/roms/eyesy/eyesy-ucontrol.sh
```
- replace the DEVICE value with your harware's name, in this example "default:CARD=CODEC"
- replace the RATE value with the bitrate your hardware supports (usually 44100 or 48000)
- OPTIONAL set DOUBLEBUF=0 if Eyesy crashes (e.g. segmentation faults) on your particular hardware setup
- save and quit

#### or use Eyesy with a "dummy" sound capture device (useful for just MIDI / OSC control, or during testing / development)

- run
```
cp eyesy-piboy-dummy.sh /home/pi/RetroPie/roms/eyesy/eyesy-dummy.sh
```
if you're on a PiBoy  

or
```
cp eyesy-gamehat-dummy.sh /home/pi/RetroPie/roms/eyesy/eyesy-dummy.sh
```
if you're on a Game HAT

or
```
cp eyesy-raspi-dummy.sh /home/pi/RetroPie/roms/eyesy/eyesy-dummy.sh
```
if you're on a plain old Raspberry Pi

#### custom controller support
if you're using a differnt gamepad controller you can create a custom mapping file
- in the ```controller``` folder, you'll find some preset mapping python files, copy one of these as a starting point
- run ```joy-test.py``` from a ssh / terminal to discover what buttons / hats / axes your controller sends out
- make sure to save your controller mapping python file to the ```controller``` folder
- in your custom startup script, set the CONTROLLER_MAPPING value

### Add eyesy system entry
- go to /home/pi/.emulationstation/
- append the contents of this repo's file es_systems.cfg.eyesy.paste.txt to the bottom of es_systems.cfg (just before the ```</systemList>``` line) in that folder (/home/pi/.emulationstation/es_systems.cfg)

If you don't already have an es_systems.cfg file in /home/pi/.emulationstation/, first copy the es_systems.cfg file that's in /etc/emulationstation/ into /home/pi/.emulationstation/.

- restart EmulationStation

This adds "eyesy" to your EmulationStation game console selection menu.

# Usage:
 - Boot up your PiBoy / Game HAT / Raspberry Pi
 - From the EYESY EmulationStation entry, launch your custom startup script

   In order to control Eyesy you
   will have to use the TouchOSC Android (or iOS) app (see below), a MIDI controller, a game controller, or a keyboard.

### Control:

**Control via TouchOSC:**
- Download and install the TouchOSC app for your iOS or Android device (it is not free; nevertheless, this app is well developed and it's also nice to support this kind of effort I believe)
- Download the fitting TouchOSC template from [here](https://github.com/rasprague/eyesy-piboy/tree/master/touchosc_templates) to your device and import it via the app (in Layout).
- In the OSC setting of the app set Host to the ip adress of your pi (your device and your pi must be on the same network)
- Set the outgoing port to `4000` and incoming to `4001`
- You're `Done`!
 
 
**Control via midi in messages (should be plug and play):**
- if MIDI isn't plug-and-play, I highly recommend installing [amidiminder](https://github.com/mzero/amidiminder)

  | Midi CC    | 21,22,23,24 | 25               | 26               | 27               | 28                | 29                | 30              | 31        | 32           | 33              | 34                         | 35       |
  |-------|-------------|------------------|----------------------|-------------------|---------------------|-----------|--------------|-----------------|----------------------------|----------|------------|----------------|
  | Control | Mode Params | Background Color | Scene selection | Save or delete (long hold) | Auto Clear Toggle | Mode Selection | Take Screenshot | Info Disp | Send Trigger | ShiftKey | Input Gain | Trigger Source |

For Scene and Mode Select (CC 26 and 29), send a value between 61-63 for previous, send a value between 65-67 for next

**Control via PiBoy built-in controller:**
- press and hold a face button, then use the dpad Left or Right to change the value slowly, or Up or Down to change the value quickly
  - Z = **Knob1**
  - Y = **Knob2**
  - X = **Knob3**
  - C = **Knob4**
  - B = **Knob5**
- press and hold A, then use the dpad Left or Right to change **Mode**, or Up or Down to change **Scene**
- press and hold the Start button to access secondary functions:
  - Z = **OSD**
  - X = **Persist**
  - C = **Save Scene**
  - B = **Sceenshot**
  - A = **Trgger**
- press Select to toggle shift mode. While in shift mode, press and hold a face button, then use the dpad Left or Right to change the value slowly, or Up or Down to change the value quickly
  - Z = **Input Gain**
  - Y = **Trigger Source**
  - X = **MIDI Channel**
- press Select, B, and Down simultaneously to **Quit** Eyesy

**Control via Game HAT built-in controller:**
- **note**: I consider the Select button to be on the left side of the console, and the Start button to be on the right side, despite what the front-panel labeling suggests
- press and hold a face button, then use the joystick Left or Right to change the value slowly, or Up or Down to change the value quickly
  - Y = **Knob1**
  - X = **Knob2**
  - B = **Knob3**
  - A = **Knob4**
  - RT = **Knob5**
- press and hold LT, then use the joystick Left or Right to change **Mode**, or Up or Down to change **Scene**
- press and hold the Start button to access secondary functions:
  - Y = **OSD**
  - X = **Persist**
  - B = **Save Scene**
  - A = **Sceenshot**
  - RT = **Trgger**
- press Select to toggle shift mode. While in shift mode, press and hold a face button, then use the joystick Left or Right to change the value slowly, or Up or Down to change the value quickly
  - Y = **Input Gain**
  - X = **Trigger Source**
  - A = **MIDI Channel**
- press Select, B, and Down simultaneously to **Quit** Eyesy

**Control via keyboard:**
- press and hold a number key, then use the arrow keys Left or Right to change the value slowly, or Up or Down to change the value quickly
  - 1 = **Knob1**
  - 2 = **Knob2**
  - 3 = **Knob3**
  - 4 = **Knob4**
  - 5 = **Knob5**
  - 6 = **Input Gain**
  - 7 = **Trigger Source**
  - 8 = **MIDI Channel**
- press a key for other functions
  - q = **Previous Scene**
  - w = **Next Scene**
  - e = **Previous Mode**
  - r = **Next Mode**
  - a = **Save Scene**
  - s = **Screenshot**
  - d = **Trigger**
  - z = **OSD**
  - x = **Persist**
  - shift = **toggle shift mode**
- press ESC or Ctrl-C to **Quit** Eyesy

### Web Editor
The web editor lets you edit the pygame scripts that generate the visuals on the fly. It should be accessible at http://raspberrypi.local:8080/ (or IP:8080 where IP is the current ip adress of your Pi)

See the Eyesy manual for more details on using the web editor.

### Uninstall:
Simply run: `./uninstall.sh`

### Rem:

- You can use the stereo input in your Modes, in Python there are accessible via `etc.audio_left` and `etc.audio_right` in the scripts, `etc.audio_in` remains L+R



---
# orignal EYESY_OS_RasPi README below
# EYESY_OS_RasPi

The operating system for the EYESY video synthesizer device - remixed.

Adaptation of the Critter&Guitari Eyesy video synth in order to run it on a regular Raspberry Pi
Eyesy Manual : https://www.critterandguitari.com/manual?m=EYESY_Manual#eyesy%E2%84%A2-user-manual



### Installation :

```
git clone https://github.com/okyeron/EYESY_OS_for_RasPi.git Eyesy
cd Eyesy
./deploy.sh
 ```
  
### Usage:
 - Connect a display to the first hdmi out
 - Boot up your RasPi
 - (Via SSH) Run the `~/Eyesy/start_web.sh` script to start the web services. Then you can start/stop the video engine from the web editor - see below.

   In order to control Eyesy you
   will have to use the TouchOSC Android (or iOS) app (see below) or a MIDI controller.
   
   You will also need a sound card. Sound card setup is beyond the scope of this readme and will depend on your specific device.
   
   Note - EYESY is looking for your sound card to be the "default" device.
   
### Control:

**Control via TouchOSC:**
- Download and install the TouchOSC app for your iOS or Android device (it is not free, I've been looking for free/open-source alternatives, please let me know if you know one; nevertheless, this app is well developed and it's also nice to suppot this kind of effort I believe)
- Download the fitting TouchOSC template from [here](https://www.dropbox.com/sh/l5bhlr3li820olc/AAD399Ej1-16u7qgEB3BTCQ1a?dl=0) to your device and import it via the app (in Layout).
- In the OSC setting of the app set Host to the ip adress of your pi (your device and your pi must be on the same network)
- Set the outgoing port to `4000` and ingoing to `4001`
- You're `Done`!
 
 
**Control via midi in messages (should be plug and play):**
  | Midi CC    | 21,22,23,24 | 25               | 26               | 27               | 28                | 29                | 30              | 31        | 32           | 33              | 34                         | 35       |
  |-------|-------------|------------------|----------------------|-------------------|---------------------|-----------|--------------|-----------------|----------------------------|----------|------------|----------------|
  | Control | Mode Params | Background Color | Scene selection | Save or delete (long hold) | Auto Clear Toggle | Mode Selection | Take Screenshot | Info Disp | Send Trigger | ShiftKey | Input Gain | Trigger Source |


### Web Editor
The web editor lets you edit the pygame scripts that generate the visuals on the fly. It should be accessible at http://raspberrypi.local:8080/ (or IP:8080 where IP is the current ip adress of your Pi)

See the Eyesy manual for more details on using the web editor.

### Uninstall:
Simply run: `./uninstall.sh`

### Rem:

- You can use the stereo input in your Modes, in Python there are accessible via `etc.audio_left` and `etc.audio_right` in the scripts, `etc.audio_in` remains L+R

