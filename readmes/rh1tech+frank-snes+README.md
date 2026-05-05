# FRANK SNES

SNES (Super Nintendo) emulator for Raspberry Pi Pico 2 (RP2350) with HDMI output, SD card ROM browser, NES/SNES gamepad, USB gamepad, PS/2 keyboard, and I2S audio support.

Based on [Snes9x](https://github.com/snes9xgit/snes9x) / [snes9x2010](https://github.com/libretro/snes9x2010).

## Screenshots

| Contra III | Prince of Persia |
|:---:|:---:|
| ![Contra III](screenshots/screen1.png) | ![Prince of Persia](screenshots/screen2.png) |
| **Lion King** | **ROM Selector** |
| ![Lion King](screenshots/screen3.png) | ![ROM Selector](screenshots/screen4.png) |

## Supported Boards

This firmware supports two board layouts (**M1** and **M2**) on RP2350-based boards with integrated HDMI, SD card, and PSRAM:

- **[FRANK](https://rh1.tech/projects/frank?area=about)** — RP Pico 2 development board with HDMI and additional I/O
- **[Murmulator](https://murmulator.ru)** — RP Pico 2 board with HDMI, SD card, and PSRAM

Both boards have the required peripherals built in — no additional wiring needed.

## Features

- Native 640x480 HDMI video output (doubled from 256x224 SNES resolution)
- SNES sound emulation (SPC700 + DSP) over I2S
- CRT scanline effect (toggle on/off)
- 8MB QSPI PSRAM for ROM loading and metadata
- SD card ROM browser with cover art, game info, animated SNES cartridge carousel, and plain file-browser view (Select+Start or Tab to toggle)
- Typing search in the ROM browser (PS/2 and USB keyboards)
- On-demand ROM loading (ROMs loaded from SD when selected, not at boot)
- NES and SNES gamepad support, auto-detected per port (NES pads map A/B; SNES pads get A/B/X/Y/L/R)
- USB gamepad support via native USB Host, with HID and XInput (Xbox 360) controllers
- First-connect menu A/B calibration wizard for unknown USB pads (learned bits saved to SD and reused on future boots)
- PS/2 and USB keyboard support
- SNES Mouse support over PS/2 or USB, routable to controller port 1 or port 2
- Configurable input routing (map any input device to Player 1 or Player 2)
- Master volume control with gain scaling
- Configurable frameskip (none / low / medium / high / extreme)
- Video layer toggles (BG1-4, sprites, transparency, HDMA)
- Audio settings (echo, interpolation)
- Runtime settings menu with persistence to SD card
- Welcome screen with animated SNES controller logo
- Visible "NO SD CARD DETECTED" screen when the SD is missing or fails to mount

## Hardware Requirements

- **Raspberry Pi Pico 2** (RP2350) or compatible board
- **8MB QSPI PSRAM** (mandatory)
- **HDMI connector** (directly connected via resistors, no HDMI encoder needed)
- **SD card module** (SPI mode)
- **NES or SNES gamepad** (directly connected) - OR -
- **USB gamepad** (via native USB port)
- **I2S DAC module** (e.g., TDA1387, PCM5102) for audio output
- **PS/2 keyboard** (optional)

> **Note:** When USB HID is enabled (default), the native USB port is used for gamepad input. USB serial console is disabled; UART TX (GPIO 0) is used for debug output.

### PSRAM

FRANK SNES requires 8MB PSRAM to run. You can obtain PSRAM-equipped hardware in several ways:

1. **Solder a PSRAM chip** on top of the Flash chip on a Pico 2 clone (SOP-8 flash chips are only available on clones, not the original Pico 2)
2. **Build a [Nyx 2](https://rh1.tech/projects/nyx?area=nyx2)** - a DIY RP2350 board with integrated PSRAM
3. **Purchase a [Pimoroni Pico Plus 2](https://shop.pimoroni.com/products/pimoroni-pico-plus-2?variant=42092668289107)** - a ready-made Pico 2 with 8MB PSRAM

## Pin Assignment

Two GPIO layouts are supported: **M1** and **M2**. The PSRAM pin is auto-detected based on chip package:

- **RP2350B**: GPIO47 (both M1 and M2)
- **RP2350A**: GPIO19 (M1) or GPIO8 (M2)

### HDMI (via 270 Ohm resistors)

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

### NES/SNES Gamepad

| Signal | M1 GPIO | M2 GPIO |
|--------|---------|---------|
| CLK    | 14      | 20      |
| LATCH  | 15      | 21      |
| DATA 1 | 16      | 26      |

> **Note:** Gamepad 2 uses the same CLK and LATCH as Gamepad 1, only the DATA pin differs.

### I2S Audio

| Signal | M1 GPIO | M2 GPIO |
|--------|---------|---------|
| DATA   | 26      | 9       |
| BCLK   | 27      | 10      |
| LRCLK  | 28      | 11      |

### PS/2 Keyboard

| Signal | M1 GPIO | M2 GPIO |
|--------|---------|---------|
| CLK    | 0       | 2       |
| DATA   | 1       | 3       |

## How to Use

### SD Card Setup

1. Format an SD card as **FAT32**
2. Create a `snes` directory in the root
3. Copy `.smc`, `.sfc`, or `.fig` ROM files into the `snes/` directory
4. (Optional) Copy game metadata for cover art and game info - extract `sdcard/metadata.zip` to your SD card's `snes/` directory
5. Insert the SD card and power on the device

The emulator also uses the SD card for:

- `snes/settings.ini` — runtime settings
- `snes/.crc_cache` — cached ROM checksums
- `snes/gamepads/gamepad_VVVV_PPPP.txt` — per-pad menu A/B layouts learned by the USB HID calibration wizard

If the SD card is missing or fails to mount, the emulator now displays a visible **"NO SD CARD DETECTED"** error screen on boot instead of dropping into a silent LED-blink loop.

### First Boot and Caching

On the **first boot**, FRANK SNES scans all ROM files in `snes/` and computes a CRC32 checksum for each one. This is used to look up cover art and game metadata. This can take a few seconds per file depending on ROM size.

The checksums are cached in `snes/.crc_cache` so subsequent boots are fast. The cache is automatically updated when new ROMs are added.

> **Tip:** Keep the number of ROMs on your SD card reasonable (under 50). The ROM selector loads cover art on-the-fly as you browse.

### Welcome Screen

On boot, a welcome screen is displayed with the FRANK SNES logo, version, and author information. Press **A** or **Start** to continue (or wait 10 seconds for auto-continue).

### ROM Selector

After the welcome screen, the ROM selector displays your game library as animated SNES cartridges with cover art. There are two views: the cartridge **carousel** and a plain **file browser**.

Carousel:

- **Left / Right** - Browse ROMs
- **Up** - Show game info panel (year, genre, players, description)
- **Down** - Hide game info panel
- **A** - Load selected ROM and start playing
- **Select + Start** / **Tab** - Toggle between carousel and file browser
- **Select + Start + A** / **F12** - Open settings

File browser:

- **Up / Down** - Navigate entries
- **A** - Open directory / launch ROM (Start is reserved for combos)
- **B** - Go up a directory
- Type on a PS/2 or USB keyboard to open incremental search
- **Select + Start** / **Tab** - Back to carousel
- **Select + Start + A** / **F12** - Open settings

The last selected ROM is remembered across reboots.

### During Gameplay

- **Select + Start + A** (gamepad), **F12** or **ESC** (keyboard) - Open settings menu

> **Why the A?** Bare **Select + Start** is reserved for toggling the carousel / file browser in the ROM selector and is therefore also reserved in-game for consistency.

### Game Metadata

For cover art and game info in the ROM selector, place metadata files on the SD card:

```
snes/metadata/images/{X}/{CRC32}.555   - Cover art (RGB555 format)
snes/metadata/descr/{X}/{CRC32}.txt    - Game info (XML format)
```

Where `{X}` is the first hex digit of the CRC32, and `{CRC32}` is the 8-digit uppercase hex checksum (computed from ROM data, skipping the 512-byte copier header if present).

A pre-built metadata pack is included in `sdcard/metadata.zip`.

## Controller Support

### SNES Gamepad

| SNES Button         | Action                                       |
|---------------------|----------------------------------------------|
| D-pad               | Movement                                     |
| A / B / X / Y       | Buttons                                      |
| L / R               | Shoulder                                     |
| Start               | Start                                        |
| Select              | Select                                       |
| Select + Start      | Toggle ROM browser carousel / file view      |
| Select + Start + A  | Settings menu                                |

### NES Gamepad

NES controllers are auto-detected per port on first use. A and B are routed to the SNES A and B buttons respectively; X/Y/L/R are unmapped (no source). Switching between NES and SNES pads on the same port requires a power cycle (detection is sticky).

### USB Gamepad

USB HID and XInput (Xbox 360) gamepads are supported over the native USB port (USB HID enabled by default).

- Pads with a known VID/PID work out of the box (a growing list of captures lives in `gamepads/`).
- The first time an unknown pad is connected, a short on-screen wizard prompts you to press **A**, then **B**. The learned layout is saved to `snes/gamepads/gamepad_VVVV_PPPP.txt` on the SD card and reused from then on. In-game button mapping is unaffected — the wizard only teaches menu A/B.
- Settings → **Button Mapping** → **Clean USB Cache** deletes those files and re-arms the wizard.

### SNES Mouse

PS/2 and USB mice are supported as an SNES mouse. When a mouse is detected, the **Mouse Port** setting becomes available to route it to controller **Port 1** or **Port 2** (replacing the old on/off toggle). Mouse emulation engages automatically whenever a mouse is connected.

### PS/2 / USB Keyboard

| Key               | Action                                              |
|-------------------|-----------------------------------------------------|
| Arrow keys        | D-pad                                               |
| X                 | A                                                   |
| Z                 | B                                                   |
| S                 | X                                                   |
| A                 | Y                                                   |
| Q                 | L                                                   |
| W                 | R                                                   |
| Enter             | Start                                               |
| Space             | Select                                              |
| Tab               | Toggle ROM browser carousel / file view             |
| F12 / ESC         | Settings menu                                       |
| F11               | Restart current game                                |
| Ctrl + Alt + Del  | Restart current game                                |
| Any printable key | Start typing search in the ROM file browser        |

## Settings Menu

Press **Select + Start + A** during gameplay (or **F12** / **ESC** on keyboard) to open the settings menu:

| Setting        | Options                                                     |
|----------------|-------------------------------------------------------------|
| Volume         | OFF, 10% - 100% (10% steps)                                 |
| CRT Effect     | ON / OFF                                                    |
| Frameskip      | None, Low, Medium, High, Extreme                            |
| Mouse Port     | Gamepad 1 / Gamepad 2 (hidden when no mouse is connected)   |
| Gamepad 1      | Any, NES 1, NES 2, USB 1, USB 2, Keyboard                   |
| Gamepad 2      | NES 1, NES 2, USB 1, USB 2, Keyboard, Disabled              |
| Button Mapping | Per-input button remap + **Clean USB Cache** (re-arm wizard) |
| Video Settings | BG1-4, Sprites, Transparency, HDMA toggles                  |
| Audio Settings | Echo, Interpolation toggles                                 |
| Restart Game   | Reload current ROM from SD                                  |
| Change ROM     | Return to ROM browser                                       |
| Back to Game   | Resume gameplay                                             |

Settings are saved to `snes/settings.ini` and persist across reboots.

## Building

### Prerequisites

1. Install the [Raspberry Pi Pico SDK](https://github.com/raspberrypi/pico-sdk) (version 2.0+)
2. Set environment variable: `export PICO_SDK_PATH=/path/to/pico-sdk`
3. Install ARM GCC toolchain

### Development Build

```bash
git clone https://github.com/rh1tech/frank-snes.git
cd frank-snes
./build.sh M2    # or M1 for M1 layout
```

Output: `build/frank-snes.uf2`

### Release Build

```bash
./release.sh
```

Builds both M1 and M2 variants with USB HID enabled. Output files in `release/`:
- `frank-snes_m1_A_BB.uf2`
- `frank-snes_m2_A_BB.uf2`

### Flashing

Hold BOOTSEL and plug in the Pico 2 via USB, then copy the `.uf2` file to the mounted drive. Or use picotool:

```bash
picotool load build/frank-snes.uf2
```

## Troubleshooting

### No HDMI signal

Make sure your board matches the correct firmware variant (M1 or M2). The HDMI pins are different between layouts.

### ROM selector shows no cover art

Make sure the metadata files are in the correct directory structure on the SD card. See [Game Metadata](#game-metadata) above.

### First boot is slow

This is normal - CRC32 checksums are being computed for all ROMs. Subsequent boots will be fast thanks to the cache file.

### Settings got corrupted

Delete `snes/settings.ini` from the SD card to restore defaults.

### USB gamepad buttons feel wrong in the menu

Power-cycle with the pad connected and run through the on-screen A / B calibration wizard that appears on first connect. If you already dismissed it or want to redo it, open **Settings → Button Mapping → Clean USB Cache** — this removes the learned `snes/gamepads/gamepad_VVVV_PPPP.txt` file and re-arms the wizard on next connect.

### Mouse does nothing

Open the settings menu and confirm **Mouse Port** is set to the controller port the game expects (most SNES mouse titles use port 1). The **Mouse Port** entry is hidden until a PS/2 or USB mouse is detected.

### NES pad face buttons are swapped

NES vs. SNES pad detection is sticky per port and only flips from NES to SNES once SNES-only bits are seen. If you swap pads on the same port, power-cycle the device.

## License

Copyright (c) 2026 Mikhail Matveev <<xtreme@rh1.tech>>

Original FRANK SNES code is licensed under the GNU General Public License v3.0. The Snes9x emulator core has its own license that restricts commercial use. See [LICENSE](LICENSE) for full details.

## Acknowledgments

| Project | Author(s) | License | Used For |
|---------|-----------|---------|----------|
| [Snes9x](https://github.com/snes9xgit/snes9x) / [snes9x2010](https://github.com/libretro/snes9x2010) | Gary Henderson, Jerremy Koot, et al. | Snes9x freeware | SNES emulation core |
| [pico-snes](https://github.com/xrip/pico-snes) | xrip | — | Initial RP2350 port |
| [FatFS](http://elm-chan.org/fsw/ff/) | ChaN | Custom permissive | FAT32 filesystem |
| [pico_fatfs_test](https://github.com/elehobica/pico_fatfs_test) | Elehobica | BSD-2-Clause | SD card PIO-SPI driver |
| [PS/2 keyboard driver](https://github.com/mrmltr) | mrmltr | GPL-2.0 | PS/2 keyboard PIO driver |
| [TinyUSB](https://github.com/hathach/tinyusb) | Ha Thach | MIT | USB HID host driver |
| [Raspberry Pi Pico SDK](https://github.com/raspberrypi/pico-sdk) | Raspberry Pi Foundation | BSD-3-Clause | Hardware abstraction layer |

Special thanks to:
- [Gavin](https://t.me/DynaMight1124) — SNES metadata and support
- [Murmulator community](https://murmulator.ru) — USB HID, HDMI, PSRAM, and audio drivers

## Author

Mikhail Matveev <<xtreme@rh1.tech>>

[https://rh1.tech](https://rh1.tech) | [GitHub](https://github.com/rh1tech/frank-snes)
