# DRUM_2025_VSAMPLER
ESP32 DRUM SAMPLER MACHINE (JC4827W543 C BOARD)
![drum_2025_vsampler](https://github.com/user-attachments/assets/3fb7114c-5d6b-4e27-aafa-b983e639490f)

This is my DRUM SAMPLER HIFI MACHINE for Guition ESP32 JC4827W543 (Capacitive touch model)

44100 Hz, 16 Bit, 16 polyphony.

Sounds are stored on flash as const arrays.

50 selectable samples with different size.

16 sounds/tracks. 16 patterns. 16 memories (16 pattern each)

Random pattern/sound generator

Sample parameters: Begin, End, Pitch, Reverse, Vol, Pan, Filter

# HARDWARE:

Guition JC4827W543 C (ESP32-S3 N4R8, LCD ILI9488, touch panel GT911) https://s.click.aliexpress.com/e/_EzVhSEH

PCM5102A I2s DAC

Optional:
No ADS (pots) and no rotary by default. If you want to use ADS and rotary uncomment line 17
//#define ads_ok

![MODULO](https://github.com/user-attachments/assets/4a1d3dbe-8290-43cb-9718-73bc6ba3658f)

ADS1115 (I2c ADC)

4 pots (B10k)

1 Rotary encoder

![SCHEMATICS](https://github.com/user-attachments/assets/767dedda-4bc9-43dc-ac95-ab5210c8e54d)

Gerber file attached into file ads1115 module.rar

# SOFTWARE:

IDE: Arduino 2.3.5

Boards: Expressif Systems 3.2.0
Board: ESP32S3 Dev module
Partition: Huge APP 3MB or custom CSV

Libraries:

Sequencer Timer - Modified version of uClock. ([macsbug solution](https://github.com/midilab/uClock/issues/48)). I'm testing an alternative. Commented funcs included. Random boot :(

TFT - Arduino_GFX_Library

Select "Huge APP 3MB" partition.

If samples don't fit into flash you can use custom partition included to get 3.5MB 
You can replace the sounds changing code "easily".
To get .c from sound files I use wavtocode (windows) https://colinjs.com/software.htm#t_WAVToCode
Sounds specs: 44100hz, 16Bit, Mono

# VIDEO:

https://www.youtube.com/watch?v=HiQ_GUZait4&t=1s&ab_channel=zcarloszc

# TODO:

- Add sample files names instead of sample number (code is ready)
- MIDI. Not tested.
- MIDI BLE. Waiting update. Now can't compile.
- Add a reverb code (I tried a lot but no good result) or some other audio FX.
- Solve issues
- Finish this read me.

# NEXT VERSION:
Target is to use SD card instead of flash.
- Use 8MB PSRAM
- Wav file explorer
- PSRAM manager

