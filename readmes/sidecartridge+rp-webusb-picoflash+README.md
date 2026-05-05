# rp-webusb-picoflash

A single-file WebUSB UF2 flasher for RP2040 and RP2350 devices in BOOTSEL mode.

This project runs fully in the browser (Chromium-based only) and uses the ROM vendor protocol (picotool-style), not the mass-storage UF2 drag & drop path.

## Features

- Load UF2 in the browser (no helper app).
- Optional erase before write.
- Progress feedback with color phases: load (blue), erase (red), write (green).
- Simple UI and plain JavaScript (no build step).

## Requirements

- A Chromium-based browser: Chrome, Edge, or Brave.
- A RP2040 or RP2350 device in BOOTSEL mode.
- WebUSB enabled (default on desktop Chromium).

## Usage

1. Open `sidecartridge-firmware-installer.html` in a Chromium-based browser.
2. Click **Select UF2** and choose your file.
3. Put the device into BOOTSEL mode and plug it in.
4. Click **Flash** and select the device in the WebUSB dialog.
5. Watch the progress log and bar.

## Notes

- BOOTSEL mode is required for ROM flashing.
- The flasher uses the ROM vendor interface (not MSC), so it streams commands directly.
- If reboot fails at the end, unplug/replug the device.

## Development

Everything is in a single file:

- `sidecartridge-firmware-installer.html`

No build or dependencies required.

## License

See `LICENSE`.
