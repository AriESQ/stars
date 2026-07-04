# recur-recur

A cyberboy666 r_e_c_u_r - inspired live video instrument for the **Raspberry Pi 5**.
cobbled together by dirge and claude code, mainly claude code.

**→ See [MANUAL.md](MANUAL.md) for all controls, workflows, and operation.**

## Architecture

A single mpv process is the sole renderer — it owns the HDMI output (DRM on
`/dev/dri/card1`) at all times and is driven over a JSON IPC socket
(`/tmp/recur-mpv.sock`). GLSL shaders are hot-swapped via mpv's
`glsl-shaders` property; temporal effects (trail, V-overlay) are lavfi
video-filter chains. Status and the menu UI render on a 3.5" ILI9486 SPI
display via a direct spidev driver (`control/display.py`) — no fbtft.

```
main.py (RecurInstrument)
├── engine/sampler.py   mpv lifecycle + IPC, clips, play modes, vf chains
├── engine/shader.py    GLSL param substitution → unique tmp paths → mpv
├── engine/mixer.py     ffmpeg kmsgrab recording
└── control/            keyboard (numpad), menu, display, midi, gpio, osd
```

Three modes — **SAMPLER** (clips + FX), **SHADER** (generative GLSL,
optionally blended with clip/camera), **LIVE** (CSI/USB camera) — cycled with
the numpad **Enter** key. State persists in `prefs.json`.

## Install

### Requirements

- **Raspberry Pi 5** (Pi 4 is untested — the mpv DRM path targets `/dev/dri/card1`)
- **Raspberry Pi OS Bookworm 64-bit** (lite or desktop both work; lite is cleaner)
- HDMI display connected before boot
- Internet connection for package install

### 1 — Flash and first boot

Flash Raspberry Pi OS **Bookworm 64-bit** with the Raspberry Pi Imager. In
Imager's advanced settings, set a username, enable SSH, and configure Wi-Fi if
you need it. Insert the card and boot the Pi until you can SSH in or open a
terminal.

### 2 — Clone the repo

```bash
cd ~
git clone https://github.com/thedirgemedia/recur-recur.git
cd recur-recur
```

### 3 — Run setup

```bash
./setup.sh
```

This script does the following (safe to re-run):

- `apt install` — mpv, ffmpeg, picamera2, python3-lgpio, python3-spidev,
  python3-evdev, pillow, numpy, libasound2/libjack (for MIDI), pmount, git
- `pip install` — python-rtmidi, gpiozero (not in apt on Bookworm)
- Adds your user to the `input`, `video`, and `render` groups (needed for
  numpad evdev, DRM KMS, and V3D respectively — takes effect after reboot)
- Switches the boot target to **console autologin** (`raspi-config B2`) so the
  desktop doesn't hold DRM master and block mpv
- Enables `dtparam=spi=on` in `/boot/firmware/config.txt` for the SPI display
- Sets `v3d_freq_min=500` to prevent GPU frequency scaling from causing frame
  drops under load
- Runs `install-service.sh` automatically (see step 4)

### 4 — Service install (also called by setup.sh)

`install-service.sh` writes `/etc/systemd/system/recur.service` and enables it.
The service:

- Runs as your user on `tty1`, exclusively (conflicts with `getty@tty1`)
- Gets `CAP_SYS_NICE` (mpv scheduler priority) and `CAP_SYS_ADMIN` (USB import
  mount helper, ffmpeg kmsgrab recording)
- Restarts automatically on failure (`RestartSec=3`)

To change the startup mode or output, edit `ExecStart` in the service file:

```bash
sudo nano /etc/systemd/system/recur.service
# change --mode SAMPLER|SHADER|LIVE or --output hdmi|composite
sudo systemctl daemon-reload
sudo systemctl restart recur
```

### 5 — HDMI hotplug (required if display isn't detected)

If the HDMI output is black or the display was plugged in after boot, add to
`/boot/firmware/config.txt`:

```
hdmi_force_hotplug=1
```

This forces the HDMI port active even if no display is detected at boot — needed
with most monitors and HDMI capture cards.

```bash
sudo nano /boot/firmware/config.txt
# add the line above, then reboot
```

### 6 — Add clips

Copy your video files into `clips/` before the first run. Supported formats:
`.mp4 .mov .mkv .avi .webm`

```bash
cp /path/to/video.mp4 ~/recur-recur/clips/
```

You can also import from USB drives at runtime via the **IMPORT** menu page
(see step 8).

### 7 — Reboot

```bash
sudo reboot
```

The instrument launches automatically on `tty1`. The SPI display shows the
status. HDMI outputs pure video — no UI.

### 8 — USB import helper (optional)

To copy video files off USB sticks via the IMPORT menu page, install the mount
helper once:

```bash
sudo ./tools/install-usb-import.sh
sudo systemctl restart recur
```

This installs a small root helper (`/usr/local/sbin/recur-usb`) and a
passwordless sudoers rule so the recur service can mount removable drives
read-only on demand. The helper refuses to touch anything that isn't a removable
USB partition, so granting it passwordless sudo is safe.

Without this, the IMPORT page shows `RUN install-usb-import.sh`.

### Day-to-day commands

```bash
sudo systemctl restart recur   # restart after config changes
sudo systemctl stop recur      # stop the instrument
journalctl -u recur -f         # watch live logs
```

### Debugging without the service

Stop the service first (it holds tty1 and the numpad), then run directly:

```bash
sudo systemctl stop recur
cd ~/recur-recur
python3 main.py -v             # verbose; Ctrl-C to quit
# options: --output hdmi|composite  --mode SAMPLER|SHADER|LIVE
#          --clips-dir clips/  --shaders-dir shaders/
#          --no-midi  --no-gpio  --resolution 1280x720
```

Error logs: mpv → `/tmp/mpv.err`, camera → `/tmp/rpicam.err`.

## Writing shaders

Shaders live in `shaders/` and use mpv's hook format with four live-tunable
parameters. The `/* comment */` after each define becomes the UI label:

```glsl
//!DESC my shader
//!HOOK MAIN
//!BIND HOOKED

#define PARAM_1 0.5    /* speed */
#define PARAM_2 0.5    /* scale */
#define PARAM_3 0.5    /* warp  */
#define PARAM_4 0.5    /* mix   */

vec4 hook() {
    vec4 c = HOOKED_texOff(vec2(0.0));
    return c * vec4(PARAM_1, PARAM_2, PARAM_3, 1.0);
}
```

FX shaders (process video) are picked up automatically. Generative shaders
(ignore the input, draw from scratch) are classified by their `//!DESC` line —
include `(generative)` in it and the shader appears in SHADER mode instead of
the FX list. Omit it and it lands in the FX list.

When a knob moves, the engine rewrites the `PARAM_N` values and writes the
shader to a **new unique temp path** before handing it to mpv — mpv 0.40
caches compiled shaders by path and will not recompile a reused path.
Changes are debounced 100 ms to avoid recompile storms.

## Credits

**Big Buck Bunny** sample clip included under the
[Creative Commons Attribution 3.0 license](https://creativecommons.org/licenses/by/3.0/).  
© 2008 Blender Foundation / www.bigbuckbunny.org
