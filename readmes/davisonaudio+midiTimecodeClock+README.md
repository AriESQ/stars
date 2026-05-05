# midiTimecodeClock
MIDI timecode parser library with Arduino program to display timecode or time of day (using an RTC) on an 8 digit 7 segment display

The provided Arduino sketch uses USB MIDI with an Arduino Micro board, though this could be altered easily to use a Serial UART connection for traditional MIDI input.

## Future additions:

- Add ability to set RTC time with a MIDI SysEx message.
- Add a timeout feature to turn off display a certain amount of time after last receiving a MIDI message.

## Hardware
The clock uses 2 [Adafruit 1.2" 4-Digit 7-Segment Displays](https://www.adafruit.com/product/1270). The enclosure is made from MDF. a signal pole, dual throw (SPDT) latching switch is used to switch between time of day mode and MIDI timecode mode.

![mtc_clock](https://github.com/davisonaudio/midiTimecodeClock/assets/54866265/b38b930e-7625-4e86-8053-99d89ac97366)
