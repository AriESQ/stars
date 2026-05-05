# FRANK Genesis

Sega Genesis / Mega Drive emulator for Raspberry Pi Pico 2 (RP2350) with HDMI output, SD card, NES/SNES gamepad, and I2S audio.

## Supported Boards

This firmware is designed for the following RP2350-based boards with integrated HDMI, SD card, and PSRAM:

- **[FRANK](https://rh1.tech/projects/frank?area=about)** — A versatile development board based on RP Pico 2, HDMI output, and extensive I/O options.
- **[Murmulator](https://murmulator.ru)** — A compact retro-computing platform based on RP Pico 2, designed for emulators and classic games.

Both boards provide all necessary peripherals out of the box (no additional wiring required).

## Features

- Native 320×240 HDMI video output via PIO
- Full YM2612 FM synthesis and SN76489 PSG sound emulation
- 8MB QSPI PSRAM support for ROM and emulator state
- SD card support for ROM files and save states
- NES and SNES gamepad support (directly connected)
- USB gamepad support (via native USB Host)
- Runtime settings menu (CPU/PSRAM frequency, audio, display options)
- CRT scanline effect for authentic retro look
- Configurable frameskip for performance tuning

## Hardware Requirements

- **Raspberry Pi Pico 2** (RP2350) or compatible board
- **8MB QSPI PSRAM** (mandatory!)
- **HDMI connector** (directly connected via resistors, no HDMI encoder needed)
- **SD card module** (SPI mode)
- **NES or SNES gamepad** (directly connected) — OR —
- **USB gamepad** (via native USB port)
- **I2S DAC module** (e.g., TDA1387, PCM5102) for audio output

> **Note:** When USB HID is enabled, the native USB port is used for gamepad input. USB serial console (CDC) is disabled in this mode; use UART for debug output.

### PSRAM Options

FRANK Genesis requires 8MB PSRAM to run. You can obtain PSRAM-equipped hardware in several ways:

1. **Solder a PSRAM chip** on top of the Flash chip on a Pico 2 clone (SOP-8 flash chips are only available on clones, not the original Pico 2)
2. **Build a [Nyx 2](https://rh1.tech/projects/nyx?area=nyx2)** — a DIY RP2350 board with integrated PSRAM
3. **Purchase a [Pimoroni Pico Plus 2](https://shop.pimoroni.com/products/pimoroni-pico-plus-2?variant=42092668289107)** — a ready-made Pico 2 with 8MB PSRAM

## Board Configurations

Two GPIO layouts are supported: **M1** and **M2**. The PSRAM pin is auto-detected based on chip package:

- **RP2350B**: GPIO47 (both M1 and M2)
- **RP2350A**: GPIO19 (M1) or GPIO8 (M2)

### HDMI (via 270Ω resistors)

| Signal | M1 GPIO | M2 GPIO |
|--------|---------|---------|
| CLK-   | 6       | 12      |
| CLK+   | 7       | 13      |
| D0-    | 8       | 14      |
| D0+    | 9       | 15      |
| D1-    | 10      | 16      |
| D1+    | 11      | 17      |
| D2-    | 12      | 18      |
| D2+    | 13      | 19      |

### SD Card (SPI mode)

| Signal  | M1 GPIO | M2 GPIO |
|---------|---------|---------|
| CLK     | 2       | 6       |
| CMD     | 3       | 7       |
| DAT0    | 4       | 4       |
| DAT3/CS | 5       | 5       |

### NES/SNES Gamepad (directly connected)

| Signal | M1 GPIO | M2 GPIO |
|--------|---------|---------|
| CLK    | 14      | 20      |
| LATCH  | 15      | 21      |
| DATA 1 | 16      | 26      |
| DATA 2 | 17      | 27      |

> **Note:** Gamepad 2 uses the same CLK and LATCH as Gamepad 1, only the DATA pin differs.

### I2S Audio

| Signal | M1 GPIO | M2 GPIO |
|--------|---------|---------|
| DATA   | 26      | 9       |
| BCLK   | 27      | 10      |
| LRCLK  | 28      | 11      |

### PS/2 Keyboard (directly connected)

| Signal | M1 GPIO | M2 GPIO |
|--------|---------|---------|
| CLK    | 0       | 2       |
| DATA   | 1       | 3       |

## Controller Support

### NES Gamepad (3-button mode)

| NES Button | Genesis Button | Notes |
|------------|---------------|-------|
| D-pad      | D-pad         | Direct mapping |
| A          | A             | |
| B          | B             | |
| A + B      | C             | Button combo required |
| Start      | Start         | |
| Select + Start | Settings  | Opens settings menu |

### SNES Gamepad (6-button mode)

The emulator automatically detects SNES controllers and provides full 6-button support.

| SNES Button | Genesis Button | Notes |
|-------------|---------------|-------|
| D-pad       | D-pad         | Movement |
| B (bottom)  | A             | Jump |
| A (right)   | B             | Primary action |
| Y (left)    | C             | Secondary action |
| X (top)     | C             | Secondary action (alternate) |
| L (shoulder)| A             | Jump (alternate) |
| R (shoulder)| B             | Primary action (alternate) |
| Start       | Start         | Pause/Menu |
| Select + Start | Settings   | Opens settings menu |

### USB Gamepad

When built with USB HID support, standard USB gamepads are supported with automatic button mapping.

### PS/2 Keyboard

PS/2 keyboards are supported for direct gameplay without a gamepad.

| Keyboard Key | Genesis Button | Notes |
|--------------|----------------|-------|
| Arrow keys   | D-pad          | Movement |
| A            | A              | |
| S            | B              | |
| D            | C              | |
| Q            | X              | 6-button mode |
| W            | Y              | 6-button mode |
| E            | Z              | 6-button mode |
| Enter        | Start          | |
| Space        | Select         | |
| Alt          | Mode           | 6-button mode toggle |
| ESC          | Settings       | Opens settings menu |

### USB Keyboard

When built with USB HID support (`-DUSB_HID_ENABLED=1`), USB keyboards are also supported with the same key mappings as PS/2 keyboards (see table above).

## Building

### Prerequisites

1. Install the [Raspberry Pi Pico SDK](https://github.com/raspberrypi/pico-sdk) (version 2.0+)
2. Set environment variable: `export PICO_SDK_PATH=/path/to/pico-sdk`
3. Install ARM GCC toolchain

### Build Steps

```bash
# Clone the repository with submodules
git clone --recursive https://github.com/mmatveev/frank-genesis.git
cd frank-genesis

# Or if already cloned, initialize submodules
git submodule update --init --recursive

# Build for M1 layout with NES/SNES gamepad (default)
mkdir build && cd build
cmake -DBOARD_VARIANT=M1 ..
make -j$(nproc)

# Build for M2 layout
cmake -DBOARD_VARIANT=M2 ..
make -j$(nproc)

# Build with USB gamepad support (instead of NES/SNES)
cmake -DBOARD_VARIANT=M1 -DUSB_HID_ENABLED=1 ..
make -j$(nproc)
```

### Build Options

| Option | Description |
|--------|-------------|
| `-DBOARD_VARIANT=M1` | Use M1 GPIO layout (default) |
| `-DBOARD_VARIANT=M2` | Use M2 GPIO layout |
| `-DUSB_HID_ENABLED=1` | Enable USB gamepad (disables USB serial) |
| `-DCPU_SPEED=504` | CPU overclock in MHz (252, 378, 504) |
| `-DPSRAM_SPEED=166` | PSRAM speed in MHz (100, 133, 166) |
| `-DZ80_CORE=OLD` | Z80 core: OLD (ASM optimized, default) or GPX (Genesis-Plus-GX) |
| `-DM68K_CORE=OLD` | M68K core: OLD (ASM optimized, default) or GPX (Genesis-Plus-GX) |
| `-DFRAMESKIP_LEVEL=3` | Frameskip level: 0-4 (0=60fps, 3=30fps default, 4=20fps) |

Or use the build script (builds M1 by default):

```bash
./build.sh
```

### Release Builds

To build both M1 and M2 variants at multiple clock speeds:

```bash
./release.sh
```

This creates versioned UF2 files in the `release/` directory:
- `frank-genesis_m1_504_166_X_XX.uf2` — M1 layout, 504MHz CPU, 166MHz PSRAM
- `frank-genesis_m2_378_133_X_XX.uf2` — M2 layout, 378MHz CPU, 133MHz PSRAM
- etc.

### Flashing

```bash
# With device in BOOTSEL mode:
picotool load build/frank-genesis.uf2

# Or with device running:
picotool load -f build/frank-genesis.uf2
```

Or use the flash script:

```bash
./flash.sh
```

## SD Card Setup

1. Format an SD card as FAT32
2. Create a `genesis/` directory in the root
3. Copy ROM files (.bin, .md, .gen) to the `genesis/` directory
4. Save states and settings are stored automatically in `genesis/`

## Settings Menu

Press **Select + Start** during gameplay to open the settings menu. Available options:

- **CPU Frequency**: 378 / 504 MHz
- **PSRAM Frequency**: 133 / 166 MHz
- **Z80**: Enable/Disable the Z80 sound CPU
- **Audio**: Master audio enable/disable
- **FM Sound**: Enable/Disable YM2612 FM synthesis
- **Channels**: Per-channel audio mute (FM1-6, PSG)
- **CRT Effect**: Scanline effect on/off
- **CRT Dim**: Scanline brightness (10-90%)
- **Frameskip**: None / Low / Medium / High / Extreme
- **Gamepad 2**: NES / Keyboard / USB / Disabled

Settings are saved to `genesis/settings.ini` and persist across reboots.

### Gamepad 2 Modes

The **Gamepad 2** setting controls how the second player input is handled:

| Mode | Description |
|------|-------------|
| **NES** (default) | Second NES/SNES gamepad controls Player 2, keyboard controls Player 1 |
| **Keyboard** | Keyboard controls Player 2 instead of Player 1 |
| **USB** | USB gamepad controls Player 2, NES/SNES gamepad controls Player 1 |
| **Disabled** | Player 2 input is disabled |

## Troubleshooting

### Device won't boot after changing settings

If you configure settings that prevent the device from booting (e.g., incompatible CPU/PSRAM frequencies), remove the `genesis/settings.ini` file from the SD card to restore defaults.

## License

GNU Affero General Public License v3. See [LICENSE](LICENSE) for details.

This project is primarily based on [Gwenesis](https://github.com/bzhxx/gwenesis) by bzhxx.

Additional code or concepts are incorporated from:

| Project | Author(s) | License | Used For |
|---------|----------|---------|----------|
| [Gwenesis](https://github.com/bzhxx/gwenesis) | bzhxx | AGPL v3 | Core emulator |
| [pico-megadrive](https://github.com/xrip/pico-megadrive) | xrip | AGPL v3 | I2S audio driver |
| [Z80 Emulator](https://fms.komkon.org/EMUL8/) | Marat Fayzullin | Non-commercial | Z80 CPU core |
| [Genesis-Plus-GX](https://github.com/ekeeke/Genesis-Plus-GX) | Charles MacDonald, Eke-Eke | Non-commercial | Reference, optional CPU cores |
| [ClownMDEmu](https://github.com/Clownacy/clownmdemu) | Clownacy | AGPL v3 | Reference |
| [ARMZ80](https://github.com/FluBBaOfWard/ARMZ80) | Fredrik Ahlström (FluBBa) | Custom | Reference for ARM assembly |
| [jgenesis](https://github.com/jsgroth/jgenesis) | James Groth | MIT | Reference |
| [yaze-ag](https://www.mathematik.uni-ulm.de/users/ag/yaze-ag/) | Frank D. Cringle, Andreas Gerlich | GPL v2 | Z80 reference |
| [Raspberry Pi Pico SDK](https://github.com/raspberrypi/pico-sdk) | Raspberry Pi Foundation | BSD 3-Clause | Hardware abstraction |

## Author

Mikhail Matveev <<xtreme@rh1.tech>>

## Acknowledgments

- @bzhxx for Gwenesis emulator
- @xrip and @dncraptor for pico-megadrive and I2S audio driver
- Marat Fayzullin for the Z80 emulator core
- Charles MacDonald for the foundational Genesis emulation work
- Eke-Eke for Genesis-Plus-GX and extensive documentation
- SEGA for the original Genesis/Mega Drive hardware
- The Raspberry Pi Foundation for the RP2350 and Pico SDK
- The Murmulator community for hardware designs and testing
