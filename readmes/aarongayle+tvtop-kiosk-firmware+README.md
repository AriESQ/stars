# TV-Top Kiosk firmware

Firmware that turns a Raspberry Pi Pico 2 W into an HDMI games console for
[TV-Top Games](https://play.tvtop.games), a board game platform where the TV is the board and
everyone plays from their own phone. The kiosk joins your Wi-Fi, pairs with the TV-Top server, and
draws whatever the current game sends it.

![A television showing a Frontier Island reference screen, driven by the Pico on the stand below](docs/images/kiosk-on-tv.jpg)

It outputs **1920x1080 at 30 Hz in full 8-bit-per-channel colour**, with no framebuffer and no
external video hardware. A 1080p frame at 24 bit is almost 6 MB and the RP2350 has 520 KB, so there
is no frame in memory at all. Each scanline is built as a run-length HSTX command stream just
before the beam reaches it, six lines ahead, out of vector geometry cached in flash.

The RP2350's HSTX serialiser is rated for 300 Mbit/s per pin. 1080p30 needs 744, so it runs at
372 MHz with the core regulator at 1.30 V. See [docs/HARDWARE.md](docs/HARDWARE.md) for the clock
tables, the overclock, and the Wi-Fi interference problem that comes with it.

## Build your own

You do not need custom hardware. A Raspberry Pi Pico 2 W, some way to get eight of its GPIOs onto
an HDMI connector, and a TV.

There are two configurations, matching the two revisions of the custom board:

| | Radio | Extra parts |
|---|---|---|
| **Option 1** | the Pico 2 W's on-board cyw43 | none |
| **Option 2** | an ESP32 over a UART | an ESP32-C3 DevKitM-1 |

Option 1 is the simpler build. Option 2 moves Wi-Fi, the IP stack and TLS onto the ESP32, which is
what the v3 board does and what the 1080p work is developed on. Wiring and the ESP-IDF build are
in [docs/MODEM.md](docs/MODEM.md).

![A Pico 2 W wired to an ESP32-C3 DevKitM-1, with an HDMI cable between them](docs/images/bring-up-rig.jpg)

*Option 2 on the bench: a Pico 2 W and an ESP32-C3 DevKitM-1, with the HSTX DVI breakout between the Pico and the HDMI cable.*

A Pico W (RP2040) also runs this firmware, driving DVI from PIO instead of HSTX, but it tops out
well below 1080p.

### Getting HDMI off the board

Four differential pairs, eight GPIOs. The positive line of each pair is the lower GPIO, so nothing
needs inverting:

| Signal | + | − |
|---|---|---|
| D0, blue | GPIO12 | GPIO13 |
| Clock | GPIO14 | GPIO15 |
| D2, red | GPIO16 | GPIO17 |
| D1, green | GPIO18 | GPIO19 |

This is the same pinout as libdvi's `pico_sock_cfg`, which most Pico DVI breakouts follow, so any
of them will work: an HSTX to DVI adapter, a Pico DVI Sock, a plain HDMI breakout board, or
soldered wires. Pick whatever is in stock.

Optionally, DDC on GPIO4 (SDA) and GPIO5 (SCL) lets the `edid` console command read what modes
your display actually claims to support, which is the fastest way to work out why a TV is refusing
a mode. Video works without it.

**On wiring quality.** At 1080p each lane carries 744 Mbit/s out of 3.3 V CMOS pins. Jumper wires
on a breadboard are fine for getting a picture at `480p60` and will probably manage `720p60`, but
1080p wants short, tightly paired connections and a short HDMI cable. Start at `480p60`, confirm
you have a picture, then work up.

## Quick start

Install the [Pico SDK](https://github.com/raspberrypi/pico-sdk) (2.2.0 or later), the Arm GNU
toolchain, cmake, ninja and picotool. Then, for option 1:

```bash
cmake -S . -B build -G Ninja -DPICO_BOARD=pico2_w -DKIOSK_TLS=ON -DKIOSK_VIDEO_MODE=1080p30
cmake --build build
picotool load -f build/tvtop_kiosk.uf2 && picotool reboot
```

Or for option 2, where the ESP32 terminates TLS so this firmware does not need mbedTLS:

```bash
cmake -S . -B build -G Ninja -DPICO_BOARD=pico2_w -DKIOSK_MODEM=ON -DKIOSK_VIDEO_MODE=1080p30
cmake --build build
picotool load -f build/tvtop_kiosk.uf2 && picotool reboot
```

Option 1 at 1080p with TLS is the tightest configuration there is: it links with about 48 KB of
the RP2350's 520 KB left for the heap, and an mbedTLS handshake wants 30 to 40 KB of that. It
builds, but it has not been run on hardware. If it will not reach the server, drop to
`-DKIOSK_VIDEO_MODE=720p60` (which frees roughly 140 KB of line pool) or use option 2, where TLS
lives on the ESP32 and there is about 79 KB spare.

On first boot the kiosk has no Wi-Fi credentials, so it starts an open access point called
`TVTOP-xxxx` and shows that name on the TV. Join it from your phone, the setup page opens by
itself, pick your network and press Save. Full details in
[docs/PROVISIONING.md](docs/PROVISIONING.md).

The kiosk then registers itself with the server and shows a pairing code on the TV to enter in the
app.

## Video modes

Set with `-DKIOSK_VIDEO_MODE=` at build time, or `mode <name>` on the USB serial console followed
by a reboot. The setting persists in flash.

On the Pico 2 W (RP2350, HSTX):

| Mode | Output | clk_sys | Notes |
|---|---|---|---|
| `720p60` | 1280x720, CEA VIC 4 | 372 MHz | the safe default |
| `1080p30` | 1920x1080, CEA VIC 34 | 372 MHz | needs a sink that accepts a 33.8 kHz line rate |
| `1080p25` | 1920x1080, CEA VIC 33 | 372 MHz | for TVs that will not go above 30 kHz |
| `1080p24` | 1920x1080, CEA VIC 32 | 372 MHz | likewise |
| `960x540p60` | 960x540 | 351-372 MHz | fall back here if a cable or chip lacks the margin |
| `480p60` | 640x480 | 252 MHz | gentlest overclock, widest compatibility |

The refresh rate being low costs nothing here: the kiosk only redraws when the game state changes,
so 30 Hz and 60 Hz look identical in use.

No picture? [docs/HARDWARE.md](docs/HARDWARE.md) has a checklist. The usual causes are a TV that
rejects the timing, or a long HDMI cable at 744 Mbit/s from 3.3 V pins.

## Pointing it somewhere else

The kiosk talks to `https://kiosk.tvtop.games` by default. Override it at build time with
`-DKIOSK_SERVER_BASE=`, on the setup page, or with `server <url>` on the serial console. The drawing
ops the kiosk implements are documented in [docs/RENDERING.md](docs/RENDERING.md). The protocol
specification and the server itself are not open source.

## Docs

| | |
|---|---|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | how the pieces fit together, and the constraints behind it |
| [BUILD.md](docs/BUILD.md) | build options and flashing |
| [HARDWARE.md](docs/HARDWARE.md) | wiring, video modes, the overclock, Wi-Fi interference |
| [RENDERING.md](docs/RENDERING.md) | the drawing ops and how frames are rasterised |
| [NETWORK.md](docs/NETWORK.md) | the long poll, backoff and TLS |
| [PROVISIONING.md](docs/PROVISIONING.md) | first boot, the setup portal, serial console |
| [MODEM.md](docs/MODEM.md) | the ESP32 Wi-Fi modem used by the custom board |
| [FONTS.md](docs/FONTS.md) | text rendering |

## Built on

- [PicoDVI](https://github.com/Wren6991/PicoDVI) by Luke Wren, vendored as `vendor/libdvi`, which
  does the video on the RP2040 path and showed that any of this was possible.
- [pico-examples](https://github.com/raspberrypi/pico-examples) for the DHCP server used by the
  setup portal.
- [stb](https://github.com/nothings/stb) for font rasterisation.

## License

[MIT](LICENSE), which covers everything here except the vendored and generated pieces below. They
keep their own terms, all of them permissive and compatible with it.

| | |
|---|---|
| `vendor/libdvi` | BSD 3-Clause, Luke Wren |
| `vendor/pico-examples` | BSD 3-Clause, Raspberry Pi (Trading) Ltd |
| `vendor/stb` | MIT or public domain, Sean Barrett |
| `tools/fonts/*.ttf` | Apache 2.0, Google. `src/common/font_blob.c` and `assets/fonts.bin` are generated from them (`tools/fonts/NOTICE`) |
