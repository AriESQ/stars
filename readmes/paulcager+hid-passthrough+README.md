# HID Pass: Raspberry Pi Pico USB HID Passthrough

A Raspberry Pi Pico firmware project that implements a USB HID passthrough device, acting as a man-in-the-middle between a USB HID device (e.g., keyboard, mouse) and a host PC. This allows for inspection, logging, and modification of HID reports in real-time.

## Features

- **Man-in-the-Middle**: Intercepts USB HID reports between a physical device and a host PC
- **Dual-Core Operation**: Utilizes both RP2040 cores for efficient USB device and host stack management
- **Composite USB Device**: Presents as both HID and CDC (serial) interfaces to the host PC
- **PIO-USB Host**: GPIO-based USB host functionality for connecting physical HID devices
- **Debug Logging**: Real-time logging of all HID reports via UART and USB CDC serial
- **Bidirectional Communication**: Supports host-to-device reports (e.g., keyboard LED control)
- **Multiple Device Support**: Can handle up to 4 HID devices simultaneously

## Hardware Requirements

### Components
- Raspberry Pi Pico (RP2040)
- USB cable (for connecting Pico to host PC)
- USB-A female breakout board or connector (for connecting HID device)
- Breadboard and jumper wires (for prototyping)

### Wiring

Connect a USB-A female connector to the Pico as follows:

| USB Signal | Pico GPIO |
|------------|-----------|
| D+ (Data+) | GPIO2     |
| D- (Data-) | GPIO3     |
| VCC (5V)   | VBUS      |
| GND        | GND       |

**Note**: The PIO-USB library automatically handles D- on GPIO3 when D+ is configured on GPIO2.

## Software Prerequisites

- [Pico SDK](https://github.com/raspberrypi/pico-sdk) installed at `~/pico/pico-sdk` (or set `PICO_SDK_PATH` environment variable)
- CMake 3.13 or higher
- ARM cross-compiler toolchain (`gcc-arm-none-eabi`)
- Git (for cloning submodules)

### Installing Prerequisites (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib git
```

## Building

### Clone the Repository

```bash
git clone https://github.com/yourusername/hid-passthrough.git
cd hid-passthrough
git submodule update --init --recursive
```

### Build the Firmware

```bash
mkdir -p build
cd build
cmake ..
make -j$(nproc)
```

The output binary will be `build/hid_pass.uf2`.

### Clean Build

If you need to rebuild from scratch:

```bash
cd build
rm -rf *
cmake ..
make -j$(nproc)
```

## Installation

### Flashing the Pico

1. Hold down the BOOTSEL button on the Pico while connecting it to your computer via USB
2. The Pico will appear as a USB mass storage device (named `RPI-RP2`)
3. Copy `build/hid_pass.uf2` to the Pico drive
4. The Pico will automatically reboot and start running the firmware

## Usage

### Basic Operation

1. Flash the firmware to your Pico as described above
2. Connect your USB HID device (keyboard, mouse, etc.) to the USB-A connector wired to GPIO2/3
3. Connect the Pico to your computer via its USB port
4. The Pico will enumerate as a composite USB device with:
   - HID interface (your keyboard/mouse will work normally)
   - CDC serial interface (for debug output)

### Viewing Debug Output

Debug messages are available on two interfaces:

#### USB CDC Serial Port

```bash
# On Linux
sudo screen /dev/ttyACM0 115200

# On macOS
screen /dev/cu.usbmodem* 115200

# On Windows, use PuTTY or similar terminal program
```

#### UART (GPIO0/GPIO1)

Connect a USB-to-serial adapter to GPIO0 (TX) and GPIO1 (RX) at 115200 baud.

### Example Debug Output

```
USB HID proxy
HID device mounted: addr 1, instance 0
HID report from device 1, instance 0, len 8
00 00 04 00 00 00 00 00
HID SET_REPORT from host PC: report_id 0, type 2, len 1
02
```

## Architecture

### Dual-Core Design

The project leverages both cores of the RP2040:

- **Core 0**: Runs the TinyUSB device stack (`tud_task()`) to present as a USB device to the host PC
- **Core 1**: Runs the TinyUSB host stack with PIO-USB (`tuh_task()`) to communicate with the physical HID device

### USB Stack Configuration

- **Device Mode (RHPORT0)**: Uses native RP2040 USB hardware (HID + CDC composite device)
- **Host Mode (RHPORT1)**: Uses PIO-USB (GPIO-based USB implementation) on GPIO2/3

### HID Passthrough Flow

1. Physical HID device connects to Pico GPIO2/3 (USB host port)
2. `tuh_hid_mount_cb()` called when device is detected
3. `tuh_hid_report_received_cb()` receives HID reports from physical device
4. Reports are forwarded via `tud_hid_report()` to host PC
5. Host PC can send reports back via `tud_hid_set_report_cb()` (e.g., keyboard LEDs)
6. All reports are logged via `printf()` to CDC serial port

### TinyUSB Direct Usage

This project uses TinyUSB directly (not through `pico_stdlib`):

- Standard `pico_enable_stdio_usb()` is disabled
- USB stdio provided by `cdc_stdio_lib` instead
- All USB descriptors manually defined in `main.c`
- Must call `tusb_init()` before `cdc_stdio_lib_init()`

## Project Structure

```
hid-passthrough/
├── main.c              # Main firmware code
├── tusb_config.h       # TinyUSB configuration
├── CMakeLists.txt      # Build configuration
├── pio_usb/            # PIO-USB submodule (GPIO-based USB host)
├── cdc_stdio_lib/      # CDC stdio bridge submodule
└── build/              # Build output directory
```

## Configuration

### tusb_config.h

Defines TinyUSB configuration:
- Enables both device and host stacks
- 1 HID device interface + 1 CDC device interface
- Supports up to 4 HID host interfaces
- Configures endpoint buffer sizes

### CMakeLists.txt

- Links against `tinyusb_device` and `tinyusb_host`
- Includes `pico_pio_usb` for GPIO-based USB host
- Includes `cdc_stdio_lib` for USB CDC stdio support
- Enables UART stdio on UART0 (GP0/GP1)

## Troubleshooting

### HID device not detected
- Check wiring connections (especially D+/D- and power)
- Verify the device works when connected directly to a PC
- Check debug output for mount/unmount messages

### No debug output on USB CDC
- Device may not have enumerated yet
- Try using UART debug output instead (GPIO0/GPIO1)
- Check that you're connecting to the correct serial port

### Keyboard/mouse not working on host PC
- Check that reports are being received (view debug output)
- Verify the device is presenting the correct HID descriptors
- Some devices may require specific handling not implemented yet

### Build errors
- Ensure Pico SDK is properly installed and `PICO_SDK_PATH` is set
- Update submodules: `git submodule update --init --recursive`
- Try a clean build: `cd build && rm -rf * && cmake .. && make`

## Dependencies

This project uses the following libraries as Git submodules:

- [**pio_usb**](https://github.com/sekigon-gonnoc/Pico-PIO-USB): GPIO-based USB host implementation
- [**cdc_stdio_lib**](https://github.com/Pioreactor/cdc_stdio_lib): CDC stdio bridge for TinyUSB

The Raspberry Pi [Pico SDK](https://github.com/raspberrypi/pico-sdk) is also required.

## Use Cases

- **Security Research**: Analyze USB HID traffic for security vulnerabilities
- **Input Monitoring**: Log keyboard and mouse activity for debugging or analysis
- **USB Protocol Learning**: Understand how HID devices communicate
- **Custom Input Filtering**: Modify or filter HID reports in real-time
- **Input Device Development**: Test and debug custom HID devices

## License

This project is provided as-is for educational and research purposes. Please check individual dependencies for their respective licenses.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Potential Improvements

- Support for more HID device types (gamepads, joysticks, etc.)
- Report modification/filtering capabilities
- Configuration via runtime commands
- Web interface for monitoring
- Non-volatile storage of settings

## Acknowledgments

- [TinyUSB](https://github.com/hathach/tinyusb) - USB stack implementation
- [Pico-PIO-USB](https://github.com/sekigon-gonnoc/Pico-PIO-USB) - GPIO-based USB host
- Raspberry Pi Foundation for the Pico SDK

## References

- [Raspberry Pi Pico Documentation](https://www.raspberrypi.com/documentation/microcontrollers/)
- [TinyUSB Documentation](https://docs.tinyusb.org/)
- [USB HID Specification](https://www.usb.org/hid)
