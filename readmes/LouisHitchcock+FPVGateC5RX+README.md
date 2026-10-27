# FPVGateC5RX

**Use an ESP32-C5 in place of the RX5808 receiver in an
[FPVGate](https://github.com/LouisHitchcock/FPVGate) lap timer.**

The ESP32-C5 has a 5 GHz radio that can receive most 5.8 GHz FPV channels. This
firmware makes it behave exactly like an RX5808 module: FPVGate tunes it over
the usual three-wire bus, and it sends the signal strength back as a voltage on
the RSSI pin. FPVGate needs no changes.

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)

![FPVGate's live RSSI graph with the C5 as its receiver](docs/images/rssi-power-cycles.png)

*FPVGate detecting repeated passes with the C5 as its receiver. The shaded
green regions mark detections; the horizontal lines show the gate thresholds.*

## Status

Working on the bench with a **Waveshare ESP32-C5-Zero** and an FPVGate timer
built on a Seeed XIAO ESP32-S3.

| | Result |
|---|---|
| Picks up the tuned channel | With a VTX on R4 at 50 cm: -12 to -24 dBm on R4, -93 to -97 dBm on other channels, and -76 dBm with the VTX off |
| Response | Sharp rises and falls on FPVGate's graph |
| Stability | A steady reading, within 3 dB, with the VTX left on for a minute |
| Tuning from FPVGate | FPVGate's channel changes arrive and the C5 follows them |
| Unit tests | About 1,300 checks, all passing |

Still to do: compare lap times with an RX5808 over many real passes, and test
more ESP32-C5 boards.

## Features

- **Behaves like an RX5808:** takes RX5808 tuning commands, answers FPVGate's
  frequency check, and handles power-down and reset.
- **Analog RSSI output**, and the RSSI can also be read digitally over the bus.
- **Fast, clean RSSI:** a live signal-strength reading from the radio, with
  short Wi-Fi bursts filtered out and the VTX's own short dips bridged, without
  smoothing off the edges.
- **Calibration and a soft ceiling:** fit your real signal levels to FPVGate's
  0 to 255 scale, and optionally make strong signals bunch together like a
  saturating RX5808.
- **Serial console:** scan channels, watch the signal live, calibrate and save,
  over USB with no FPVGate needed.
- **Channels:** all of Raceband (R8 included), bands A, B and F, and E1-E5.
  Channels outside the Wi-Fi bands (R8, E6-E8, L) are tuned directly in the
  radio; see [Extended tuning](docs/EXTENDED_TUNING.md).

## Quick start

```powershell
git clone https://github.com/LouisHitchcock/FPVGateC5RX.git
cd FPVGateC5RX\firmware
pio run -e waveshare_c5_zero -t upload --upload-port COM29
```

Then follow [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) to test the
radio over USB, wire it to FPVGate and calibrate it.

## Documentation

| Document | Contents |
|---|---|
| [Getting started](docs/GETTING_STARTED.md) | **Start here.** Flashing, testing, wiring to FPVGate, calibration, troubleshooting. |
| [Console](docs/CONSOLE.md) | Every serial console command |
| [Hardware](docs/HARDWARE.md) | Wiring, and why each resistor and capacitor is needed |
| [How it works](docs/SPEC.md) | The design: the bus, the radio, the RSSI pipeline |
| [Extended tuning](docs/EXTENDED_TUNING.md) | R8 and other channels outside the Wi-Fi bands, the live signal-RSSI reading, and the bench results |
| [Licensing](docs/LICENSING.md) | The licence, commercial licensing, and why it isn't GPL |
| [Provenance](docs/PROVENANCE.md) | Where each technical fact came from |

## Repository layout

```
firmware/   PlatformIO project: core/ (portable C++, unit-tested) and src/ (ESP32-C5 code)
test/       Unit tests that run on a PC: bash test/run.sh (needs g++)
tools/      c5cmd.py, for sending console commands from a script
docs/       Documentation
```

## Licence

Free for non-commercial use under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), the
same licence as FPVGate.

Commercial use, such as selling hardware or firmware or running a paid service,
needs a commercial licence. To ask, email louishitchcock@gmail.com.

This firmware was written from scratch and isn't GPL: no code from the GPL
projects that use the ESP32-C5's radio for FPV was used. The reasoning, and the
licences of the third-party parts (Arduino-ESP32 core: LGPL-2.1; ESP-IDF:
Apache-2.0), are in [docs/LICENSING.md](docs/LICENSING.md).

---

Copyright 2026 Louis Hitchcock
