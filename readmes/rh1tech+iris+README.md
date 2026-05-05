# IRIS

IRIS is a versatile DIY serial terminal software based on the excellent work by [David Hansel](https://github.com/dhansel) on the original [VersaTerm](https://github.com/dhansel/VersaTerm) project. IRIS extends and adapts this foundation while maintaining respect for the original design principles and feature completeness, and is specially designed for [Protea](https://github.com/rh1tech/protea) development board. Following the Greek mythology naming convention, IRIS (the messenger goddess who connects heaven and earth via rainbow bridges) serves as the communication bridge in this terminal implementation, while running on the Protea hardware platform.

This project maintains full compatibility with the original VersaTerm feature set while incorporating specific optimizations and additions tailored to the Protea devboard’s capabilities.

IRIS is open source and licensed under [GPL v3](LICENSE).

Documentation: [rh1.tech](https://rh1.tech/projects/IRIS)

## Features

### Core Functionality:
- Native HDMI output
- USB keyboard support including keyboards with integrated USB hubs
- Wide baud rate range from 50 to 921,600 baud with both presets and custom rates
- Flow control support for both hardware (RTS/CTS) and software (XOn/XOff) protocols
- USB power compatibility for convenient operation

### Terminal Capabilities:

- Highly configurable with support for user-uploadable bitmap fonts
- Complete VT100 attribute support including bold, underline, blink, inverse, double width, and double height
- 16 ANSI color support for enhanced visual output
- Robust VT100 control sequence implementation - passes VTTest validation for 80-column VT52/VT100/VT102 terminals
- PETSCII mode with full PETSCII character set and control character support, including authentic C64 font

## Hardware Platform

IRIS is specifically designed for the [Protea](https://github.com/rh1tech/protea) development board (powered by RP2040 micro controller), a custom hardware platform that provides the necessary interfaces and processing power for professional serial terminal operations. The Protea board integrates seamlessly with the software to deliver reliable, instant-access terminal functionality.