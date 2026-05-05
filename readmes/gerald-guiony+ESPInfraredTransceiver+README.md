# ESPInfraredTransceiver

[![ESP8266](https://img.shields.io/badge/ESP-8266-000000.svg?longCache=true&style=flat&colorA=CC101F)](https://www.espressif.com/en/products/socs/esp8266)

ESPInfraredTransceiver is a C++ library for the Arduino Core designed for the ESP8266 board, allowing the transmission and reception of any InfraRed signals.

This library is compatible with any infrared signal because it simply records and replays infrared signals, 
there is no protocol analysis like with [this other library](https://github.com/Arduino-IRremote/Arduino-IRremote/tree/master)

## Getting started

To use ESPInfraredTransceiver, you will need:

* An ESP8266 board
* The Arduino IDE configured for ESP8266 (version 2.3.2 or later)
* [Arduino core for the ESP8266](https://github.com/esp8266/Arduino) version 3.1.2
* A basic understanding of the Arduino environment (e.g., uploading sketches, importing libraries, etc.)

## Installing ESPInfraredTransceiver

1. Download the latest master source code as a [.zip](https://github.com/gerald-guiony/ESPInfraredTransceiver/archive/master.zip) file
2. In the Arduino IDE, import the `.zip` file by navigating to **Sketch → Include Library → Add .ZIP Library**

## Prerequisites

To build this library you must have the latest version of [ESPCoreExtension library](https://github.com/gerald-guiony/ESPCoreExtension)

## Example

Universal IR remote control : [IrRemoteControl](https://github.com/gerald-guiony/ESPInfraredTransceiver/blob/master/examples/IrRemoteControl)
