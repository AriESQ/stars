# TinyWifiDongle

[![Arduino Library](https://img.shields.io/badge/Arduino-Library-blue.svg)](https://www.arduino.cc/reference/en/libraries/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A __header-only C++ Arduino library__ that turns a microcontroller into a __USB WiFi dongle__: the MCU joins a WiFi network and appears to your PC as a USB network adapter (CDC-NCM).

- No driver needed on the PC: Linux, macOS and Windows 11 have a CDC-NCM driver built in
- Ethernet frames are bridged unchanged between USB and WiFi, so the PC is a normal client of your WiFi network and gets its address from your router's DHCP server. The MCU itself has no IP address
- Speed is limited by the full-speed USB (12 Mbit/s) of these chips: about 600 KB/s on the ESP32-S3 and about 250 KB/s on the Pico 2 W in the tests. Fine for browsing and downloads, but much slower than a PC's own WiFi ([details](https://github.com/pschatzmann/TinyWifiDongle/wiki/Status))
- Messages go to any `Print` the sketch passes to `TWD_LOGGER`, e.g. a UART or a USB serial port ([details](https://github.com/pschatzmann/TinyWifiDongle/wiki/Logging))
- Credentials can be hard-coded or entered in a browser on a setup page the board opens itself ([details](https://github.com/pschatzmann/TinyWifiDongle/wiki/Setup)), with no additional library

## Supported platforms

| Platform | Arduino core | State |
|---|---|---|
| __ESP32-S3__, __ESP32-S2__ | arduino-esp32 3.x (tested 3.3.12) | works, tested on an ESP32-S3 |
| __Raspberry Pi Pico 2 W__ (RP2350), __Pico W__ (RP2040) | arduino-pico (tested 6.3.1) | works, tested on a Pico 2 W; the Pico W is untested |
| __ESP32-P4__ | arduino-esp32 3.x | compiles, WiFi side tested; the USB side needs a board with a USB-OTG connector |

Not supported: the original ESP32, ESP32-C3/C6 and other chips without a USB device controller that can carry a network class, the Raspberry Pi Pico without WiFi, and the Arduino mbed cores. Details and test results are in [Status](https://github.com/pschatzmann/TinyWifiDongle/wiki/Status).

### Example

```cpp
#include "TinyWifiDongle.h"

TinyWifiDongle dongle;

void setup() {
  dongle.begin("ssid", "password");
}

void loop() {}
```

Board settings (the board is then connected to the PC with its USB connector):

- __ESP32-S2/S3:__ board option __USB Mode: USB-OTG (TinyUSB)__, connect the USB-OTG port
- __Raspberry Pi Pico W / Pico 2 W:__ the default option __USB Stack: Pico SDK__, connect the USB connector of the board

## Documentation

- [Examples](https://github.com/pschatzmann/TinyWifiDongle/wiki/Examples)
- [WiFi setup in a browser](https://github.com/pschatzmann/TinyWifiDongle/wiki/Setup) (`TinyWifiDongleSetup`)
- [Configuration](https://github.com/pschatzmann/TinyWifiDongle/wiki/Configuration)
- [Logging](https://github.com/pschatzmann/TinyWifiDongle/wiki/Logging) (`TWD_LOGGER`: output, log levels)
- [How it behaves](https://github.com/pschatzmann/TinyWifiDongle/wiki/Behaviour) (addresses, status line, stall watchdog)
- [Host setup tips](https://github.com/pschatzmann/TinyWifiDongle/wiki/Host-Setup) (route priority, NetworkManager, MTU, reading the counters, Wake-on-LAN)
- [Status](https://github.com/pschatzmann/TinyWifiDongle/wiki/Status) (per platform, throughput) and [Known issues](https://github.com/pschatzmann/TinyWifiDongle/wiki/Known-Issues) (the ESP32 USB stall, the Pico)
- [Architecture](https://github.com/pschatzmann/TinyWifiDongle/wiki/Architecture) (classes, bridge rules, analysis of the USB stall)
- [Class documentation](https://pschatzmann.github.io/TinyWifiDongle/annotated.html) (Doxygen, generated from the sources; to build it yourself run `doxygen Doxyfile`, the HTML goes to `html-out/html/`)

## Installation in Arduino

You can download the library as zip and call Sketch -> Include Library -> Add .ZIP Library. Or you can git clone this project into the Arduino libraries folder e.g. with

```
cd  ~/Documents/Arduino/libraries
git clone https://github.com/pschatzmann/TinyWifiDongle.git
```

I recommend to use git because you can easily update to the latest version just by executing the ```git pull``` command in the project folder.

Requirements:

- __ESP32:__ ESP32 board package (arduino-esp32) 3.x, tested with 3.3.12. It must include the TinyUSB NCM class, which is on in the prebuilt libraries. Board option __USB Mode: USB-OTG (TinyUSB)__, with the USB-OTG port of the board connected to the PC
- __Raspberry Pi Pico W / Pico 2 W:__ the arduino-pico core (Raspberry Pi Pico/RP2040/RP2350), tested with 6.3.1, board "Raspberry Pi Pico W" or "Raspberry Pi Pico 2W" with the default option __USB Stack: Pico SDK__. The board's single USB connector carries the adapter
- Include `TinyWifiDongle.h` from the sketch only, because the header defines the USB driver callbacks (both platforms)

Host support for CDC-NCM: Linux and macOS native, Windows 11 native (Windows 10 needs a driver).

## License

MIT, see [LICENSE](LICENSE).
