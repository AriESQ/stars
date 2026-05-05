# MIDI UART USB converter

Bi-directional converter between MIDI USB and MIDI UART. There are many pages
that describe how to connect a UART port to DIN connectors so it is not covered
here.

Maximum System Exclusive size is 1024 bytes. This can be bigger on SAMD boards
which have more RAM.

Install MIDI Library (version 4.3.1) and MIDIUSB libraries using the Arduino IDE library
manager. MIDI Library version 5 and newer do not work with large SysEx.

Tested in 32u4 boards such as Arduino Leonardo, SparkFun Pro Micro, and Adafuit
Itsy Bitsy 32u4.

Tested on Arduino Zero, Adafruit Trinket M0, and Adafruit QT Py. It might work
on other SAMD21 boards. Either Arduino or TinyUSB stack can be used.

Tested on Raspberry Pi Pico using the TinyUSB stack and the [Earle Philhower
Arduino Core for RP2040](https://github.com/earlephilhower/arduino-pico). It might
work on other RP2040 boards.

## Testing

Tested in with hardware loop back on UART Tx/Rx using SendMIDI and ReceiveMIDI.

In one command line window run receivemidi like this:

$ receivemidi dev arduino

In another command line window run sendmidi with the test script
receivemidi.txt like this:

$ sendmidi dev arduino file receivemidi.txt

Compare the output of receivemidi (redirect output to a file) with the
receivemidi.txt test script.

## Hardware

All of the following run MIDIUARTUSB.

Arduino Leonardo (32u4) with SparkFun MIDI shield. The buttons and pots are not
used in this program.

![Arudino Leonardo with SparkFun MIDI shield](https://github.com/gdsports/MIDIUARTUSB/blob/master/images/leonardo_midi.jpg)

Pro Micro (32u4) 5V with MIDI breakout board.

![Pro Micro 5V with MIDI breakout board](https://github.com/gdsports/MIDIUARTUSB/blob/master/images/promicro_midi.jpg)

Adafruit Trinket M0 (SAMD21) 3.3V with MIDI breakout board. Note the different
resistor values on the MIDI board for 3.3V operation.

![Trinket M0 3.3V with MIDI breakout board](https://github.com/gdsports/MIDIUARTUSB/blob/master/images/trinketm0_midi.jpg)

## Options

Ground pin 2 to enable MIDI pass thru.

## Trinket M0 firmware

Compiled programs can be burned into the Trinket M0 just by dragging and
dropping a UF2 file on to the Trinket M0 USB drive. There is no need to install
the Arduino IDE, source code, or USB serial device driver.

* Download the UF2 file.
* Plug in the Trinket M0 to the computer.
* Double tap the Trinket M0 reset button.
* When the TRINKETBOOT USB drive appears, drop the UF2 file on to the drive.
* Wait until the Trinket M0 reboots.

## References

https://www.midi.org/specifications/

http://www.usb.org/developers/docs/devclass_docs/midi10.pdf

https://github.com/gbevin/ReceiveMIDI

https://github.com/gbevin/SendMIDI
