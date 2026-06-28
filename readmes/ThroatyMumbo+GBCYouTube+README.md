# YouTube on Game Boy Color

Ever wanted to watch your favorite comedy podcast on a 160x144 screen with no backlight?
Well now you can! Introducing the (unofficial, of course) YouTube for Game Boy Color app!
All you need is a microcontroller, a cartridge breakout board, and a bunch of other crap
soldered together to make this nightmare a reality!

Featured in https://youtu.be/_GlYnN9JK1k

You browse and pick a video on the Game Boy itself. A host PC resolves that video from
YouTube and streams it, in real time, into a cartridge that doesn't actually contain a
ROM — it's a microcontroller *pretending* to be one, filling in "ROM" data on the fly as
the console reads it. No clip is ever baked into a file or copied to an SD card; the picture
and audio you see are being fetched from YouTube and pushed onto the console as they play.

This repo is the streaming cart and its host stack. (Several earlier, self-contained
"bake a clip into a `.gbc` ROM" playback engines also live here under `experiments/` — see
the bottom — but the active project is the live stream.)

---

## What actually happens

```
  ┌──────────┐   YouTube    ┌─────────────┐   TCP/WiFi   ┌────────────┐   SPI    ┌──────────┐   cart bus   ┌─────────┐
  │ YouTube  │ ───video───▶ │   Host PC   │ ───────────▶ │  ESP32-C6  │ ───────▶ │ RP2350B  │ ───────────▶ │ Game Boy│
  │          │              │ (host/ pkg) │              │ (WiFi modem)│          │ ("cart") │              │  Color  │
  └──────────┘              └─────────────┘              └────────────┘          └────┬─────┘              └─────────┘
        ▲                          ▲                                                  │ I2S
        │   videoId (what to play) │                                                  ▼
        └──────────────────────────┴──────────────── GB → server uplink ◀──── [MAX98357 amp → speaker]
```

1. **You search and pick a video on the Game Boy.** The on-cartridge GUI (`gui/`) is a
   little YouTube front-end: a landing page, an on-screen keyboard, a results list, and a
   thumbnail gallery — all rendered on the GBC. Searching and the thumbnails are served
   live from the host over the same WiFi link.

2. **The Game Boy tells the host what to play.** When you select a result, the console
   sends that video's `videoId` *up* to the host (the GB drives the PC, not the other way
   around). This reverse channel reuses the existing wires — no extra cabling.

3. **The host resolves and streams it from YouTube, live.** The host (`host/`, one
   in-process Python package) hands the `videoId` to `yt-dlp` to get a directly-streamable
   144p media URL — **no download**, nothing hits disk — then runs `ffmpeg` straight off
   that URL, encodes each frame into the player's cartridge-bank format, and streams the
   bytes over WiFi. Audio is decoded in parallel and **muxed onto the same socket** as the
   video.

4. **The microcontroller pretends to be the cartridge.** An **RP2350B** sits on the
   console's cartridge bus and answers every memory read in lockstep with the Game Boy's
   clock, serving video out of "ROM" banks it's filling in real time from the incoming
   stream. A small player ROM running on the GB just keeps reading the next bank and
   displaying it — it's a blind, cycle-exact decoder; all the cleverness is in the cart
   keeping the right bytes ready exactly when the console reaches for them.

5. **The cart plays the soundtrack itself.** The Game Boy CPU has no spare cycles for
   audio, so the RP2350 demuxes the audio out of the stream and clocks it to an I2S amplifier
   on its own, kept loosely lip-synced to the video.

The result, on real hardware: pick a video → it plays with sound → press **B** to drop
back to the menu and pick another, all with no resets and no files.

---

## The hardware

| Part | Role |
|---|---|
| **Catridge breakout board** | Allows you to tap into the edge connector |
| **Pimoroni PGA2350 (RP2350B)** | Pretends to be the cartridge. Drives the console's data bus in sync with its clock and serves the live video stream. |
| **ESP32-C6 (XIAO)** | WiFi modem. Bridges TCP from the host to a fast SPI link into the RP2350. |
| **MAX98357 I2S amp** | The RP2350 plays the soundtrack through this, independent of the Game Boy. |

The host PC connects over WiFi to the C6, which connects over SPI to the RP2350, which
connects to the Game Boy over the cartridge bus. One TCP socket carries video + audio +
control records, multiplexed together.

**NOTE**: The ESP32-C6 is enough of a power hog that you're likely not going to get away with powering it solely off the GBC.
I worked around this issue with a secondary battery. It ain't ideal, but it gets the job done.

---

## Two video engines

You pick the engine in the menu; both stream over the exact same path:

- **hiframe** — full-frame **160×144 at 30 fps**. This is a streaming-specific port of [LIJI32's GBVideoPlayer](https://github.com/LIJI32/GBVideoPlayer).
- **hicolor** — far more on-screen color via per-scanline palette streaming, at **128×128, ~5.45 fps**. Ported from [Jeff Frohwein's Hicolor Animation Engine](https://www.devrs.com/gb/files/software.html).

---

## Quick start

You'll need the toolchains in **[Prerequisites](#prerequisites)** set up first. Then, from
the repo root:

```bash
# 1. One-time: give the WiFi modem your network
cd streaming_common/c6_modem
cp creds.env.example creds.env      # then edit creds.env with your 2.4 GHz SSID/password
./build.sh /dev/ttyACM1 flash       # the C6 joins your AP and prints its DHCP IP
cd ../..

# 2. Build + flash the cartridge firmware (GUI + both players, one image)
./run.sh flash-gui

# 3. Power-cycle the Game Boy once — it boots to the GBCTube landing page

# 4. Start the streaming server (uses $GBCYT_C6_IP, or pass --ip <C6-address>)
./run.sh serve
```

Now, **on the Game Boy**: press **A** to open the keyboard and search, pick a result, and
press **A** to play it. The console sends the chosen video up to the host, which resolves
and streams it live. **B** in a player returns to the menu; **START** pauses/resumes;
the d-pad seeks.

> Streaming a local file instead of YouTube (e.g. a test pattern), outside the menu:
> `python3 -m host.play --player hiframe <video>`

---

## Repository layout

| Path | What it is |
|---|---|
| `gui/` | The on-cartridge **GBCTube front-end** (GBDK): landing page, search keyboard, results list, thumbnail gallery. |
| `player/hiframe/` | The full-frame 30 fps player ROM (`video.asm`) + its encoder. |
| `player/hicolor/` | The high-color player ROM (`player.asm`) + its encoder. |
| `player/firmware/` | CMake build for the RP2350 firmware + the repo-root `run.sh` build/flash/serve driver. |
| `streaming_common/` | The shared **RP2350 cartridge firmware** (`main.c`, `serve.pio`), the WiFi/SPI transport, the **ESP32-C6 modem** firmware (`c6_modem/`), the I2S audio output, and the GB→host uplink. |
| `host/` | The **PC-side streaming stack** (one Python package): YouTube search + resolve, ffmpeg/encode, the WiFi transport, and the menu-driven daemon. |
| `experiments/` | Earlier, standalone "bake a clip into a ROM" playback engines and hardware bring-up tests (background, not the active work). |
| `CLAUDE.md` | Deep technical notes on the architecture and the hard-won design decisions. |

The host package, run as `python3 -m host.<module>`: `daemon` (the menu-driven server),
`youtube`/`search` (live search by scraping the public results page), `ytstream` (videoId →
streamable URL via yt-dlp), `convert` (ffmpeg → cartridge-bank format), `engine`/`transport`
(the streaming + muxed WiFi link), `thumbs` (gallery thumbnails).

---

## Prerequisites

- **`PICO_SDK_PATH`** pointing at a pico-sdk checkout, plus **RGBDS** (`rgbasm`/`rgblink`/
  `rgbfix`), **GBDK-2020**, and **`picotool`** on `PATH` (for the RP2350 + Game Boy ROMs).
- **ESP-IDF** for the ESP32-C6 modem firmware.
- **Python 3** with **`ffmpeg`**, **Pillow**, **numpy**, and **`yt-dlp`** (a `.venv` is
  the easy path). `run.sh` invokes `python3`, so run it with the venv active.
- WiFi credentials are injected at build time and never committed — copy
  `streaming_common/c6_modem/creds.env.example` → `creds.env` (gitignored) and fill in your
  **2.4 GHz** network.

---

## Credits & licensing

This project builds on prior art:

- [**GBVideoPlayer**](https://github.com/LIJI32/GBVideoPlayer) by Lior Halphon (LIJI32) — the basis of the hiframe player.
- [**Hicolor Animation Engine**](https://www.devrs.com/gb/files/software.html) by Jeff Frohwein — the basis of the hicolor player.
- [**Croco Cartridge**](https://github.com/shilga/rp2350-gameboy-cartridge-firmware/) firmware by Sebastian Quilitz (GPLv3) — the cartridge-bus PIO responder and DMA scheme the serve path is derived from.
