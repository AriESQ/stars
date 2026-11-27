<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="Assets/RAYS-wordmark-white.svg">
    <img src="Assets/RAYS-wordmark-black.svg" alt="RAYS" width="320">
  </picture>
</p>

<h3 align="center">Your lights, locked to the DJ's beat.</h3>

<p align="center">
  Free, open-source DMX lighting for DJs on macOS.<br>
  It follows Ableton Link, Pioneer Pro DJ Link or MIDI Clock and plays choreographies on real fixtures, on the downbeat.
</p>

<p align="center">
  <a href="https://github.com/gasparoff/rays/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/gasparoff/rays/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="macOS 14+" src="https://img.shields.io/badge/macOS-14%2B-black">
  <img alt="Swift 6" src="https://img.shields.io/badge/Swift-6-orange">
  <a href="CONTRIBUTING.md"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen"></a>
</p>

<p align="center">
  <a href="../../releases/latest"><b>Download</b></a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#supported-hardware">Hardware</a> ·
  <a href="docs/manual.md">User guide</a> ·
  <a href="#faq">FAQ</a> ·
  <a href="docs/architecture.md">Architecture</a> ·
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

<p align="center">
  <img src="docs/images/hero.gif" alt="RAYS opens paused; Play starts the show and the stage preview follows the beat as scenes change" width="800">
  <br><sub>No lights connected: the stage preview shows exactly the DMX that RAYS sends.</sub>
</p>

<p align="center">
  <img src="docs/images/real-rig.gif" alt="Three LED triangle fixtures on a table changing colour on the beat, driven by RAYS during a test session" width="480">
  <br><sub>And on a real rig: RAYS driving LED fixtures during a test session.</sub>
</p>

RAYS turns a Mac into a lighting console that **follows the music by itself**. Plug in an
Art-Net node, sACN receiver or USB DMX interface, start your set, and the lights move with the
tempo and phase of your DJ software or CDJs. No lighting desk, no timeline to program, no
subscription.

If you know SoundSwitch or Lightkey: RAYS is the free and open-source take on beat-synced
lighting, native on the Mac and built around the DJ's clock.

## Why RAYS

- **Locks to the beat, not to a microphone.** Tempo and phase come from Ableton Link (Traktor,
  rekordbox, djay, Ableton Live…), straight from Pioneer CDJ/XDJ consoles over Pro DJ Link, or from
  MIDI Clock. Scenes land on the downbeat.
- **Choreographies, not chases.** Twelve built-in scenes in two banks (House, Club 130–138), plus
  your own, edited on a shared rhythm grid with per-track step, cycle, envelopes and timing.
- **A preview that tells the truth.** The stage view decodes the very same DMX bytes that go out
  on the wire. It also runs with no light connected, so you can design scenes on the train.
- **Hands on.** Full Allen & Heath Xone:K2 layout with LED feedback, Akai APC40 mkII layout,
  MIDI Learn for anything else, Build → Drop gesture, Flash, Blackout.
- **Made for real gigs.** Auto-discovery of Art-Net nodes and consoles, automatic reconnection,
  safe blackout on Esc, no App Nap while lights are on.
- **Your rig, as data.** Around 320 fixture modes from 112 lights and 12 brands, and controller
  layouts, all in plain JSON. Adding yours takes one file and no Swift.

## Quick start

**Download, free.** Get `RAYS-<version>-macOS-arm64.zip` from the
[latest release](../../releases/latest) (Apple silicon, macOS 14+), unzip it and move RAYS.app to
Applications. No account, no sign-up, no licence key. From 0.2.0 the app is signed with a Developer ID
and notarized by Apple, so it opens with a double click, and Pro DJ Link is built in: you don't need
Beat Link Trigger or anything else.

**No lights yet?** Launch the app anyway: the stage preview runs without any hardware, and the
internal clock or Tap gives it a tempo.

New to RAYS? The [user guide](docs/manual.md) goes from install to your first show.

### Build from source

Requirements: macOS 14+, Xcode 16 or a Swift 6 toolchain.

```sh
git clone --recursive https://github.com/gasparoff/rays.git
cd rays
make bootstrap   # Ableton Link submodule (+ Beat Link helper, see below)
make test        # 300+ tests, no hardware needed
make build       # builds dist/RAYS.app (without Beat Link Trigger: no Pro DJ Link)
open dist/RAYS.app
```

Building from source needs Beat Link Trigger installed only for Pro DJ Link: `make bootstrap` takes
its runtime to make the helper. Without it the app builds and runs, with Ableton Link and MIDI Clock.
Users of the released app never need it.

## Supported hardware

| Type | Supported | Status |
|---|---|---|
| Art-Net nodes | ENTTEC ODE MK3 | ✅ tested on hardware |
| Art-Net nodes | Any Art-Net 4 node | 🟡 should work, [report it](../../issues/new?template=hardware-report.yml) |
| sACN (E1.31) | Any E1.31 receiver, multicast or unicast | 🟡 implemented from the spec |
| USB DMX | ENTTEC DMX USB Pro and compatibles (DMXking ultraDMX Pro/Micro) | 🟡 implemented from the protocol |
| Fixtures | Varytec Retro Blinder TRI 180 / TRI 380 | ✅ verified profiles |
| Fixtures | Generic RGB, RGBW, Dimmer+RGB, Dimmer+RGBW | ✅ built in |
| Fixtures | ~320 modes of PARs, bars and washes from Chauvet DJ, ADJ, Cameo, Eurolite, Stairville, Showtec, BeamZ, Martin, Elation and more | 🟡 converted from the [Open Fixture Library](https://open-fixture-library.org) |
| Fixtures | Varytec Event Par, LED Pad 7 and generic RGBA / RGBWA / UV profiles | 🟡 from the manuals |
| Controllers | Allen & Heath Xone:K2 (Classic and Live v2 layouts) | ✅ |
| Controllers | Akai APC40 mkII | 🟡 from Akai's published protocol |
| Controllers | Any MIDI controller | ✅ via MIDI Learn |
| Tempo | Ableton Link, Pioneer Pro DJ Link (CDJ/XDJ) | ✅ |
| Tempo | MIDI Clock (opt-in) | 🟡 |

🟡 means implemented from public specifications and covered by tests, but not yet confirmed on
the device. Full matrix, including what is not supported and why: [docs/hardware.md](docs/hardware.md).

**Your light or controller is missing?** Adding it takes one JSON file:
see [Add a fixture](docs/adding-a-fixture.md) and [Add a controller](docs/adding-a-controller.md).
Every new profile is a welcome first PR.

## How it works

```
 Pro DJ Link ─┐                                                 ┌─► Stage preview
 Ableton Link ┼─► Tempo ─► Scene sequencer ─► DMX composer ─────┤
 MIDI Clock ──┘           (choreographies)    (patch+profiles)  └─► Art-Net / sACN / USB DMX ─► lights
 MIDI controllers ─► Router ─┘
```

The engine runs at 30 Hz on its own queue and never waits for the UI. Everything except the app
target is Foundation-only and fully unit-tested without hardware.

| Module | What lives there |
|---|---|
| `Sources/RaysOutput` | Art-Net, sACN and DMX USB Pro drivers, node discovery, the `OutputDriver` protocol. |
| `Sources/RaysTempo` | Tempo snapshots, internal clock, tap tempo, Pro DJ Link beats, MIDI Clock, the `TempoSource` registry. |
| `Sources/RaysCore` | Fixtures, patch, profiles, scenes, choreography, sequencer, DMX composer, stage geometry. |
| `Sources/RaysControl` | MIDI decoding, controller layouts, the router (Learn, soft takeover). |
| `Sources/RaysEngine` | The 30 Hz `LightEngine` and the JSON config store. |
| `Sources/RaysApp` | The SwiftUI macOS app. |
| `Profiles/`, `Controllers/` | Fixture profiles and controller layouts (JSON), bundled into the app. |

More in [docs/architecture.md](docs/architecture.md) and the [design decisions](docs/adr/README.md).

## FAQ

**Do I need Pioneer gear?** No. Any app with Ableton Link works (Traktor, rekordbox, djay, Ableton
Live and many more), and so does MIDI Clock. Without any of them, use the internal clock and Tap.

**Which DMX interface should I buy?** Any Art-Net node is the most tested path (ENTTEC ODE MK3 is
the reference). sACN receivers and ENTTEC DMX USB Pro compatibles are supported too.
ENTTEC Open DMX USB is not, [and here is why](docs/hardware.md#dmx-outputs).

**Windows or Linux?** Not today. The engine modules are Foundation-only Swift, so a port is
possible: open a Discussion if you want to work on it.

**Which languages does the app speak?** English and Italian. RAYS follows the macOS language; you can pick another one in Setup › Advanced › Language.
Adding a language takes one translation file: see [Localization/README.md](Localization/README.md).

## Contributing

RAYS grows with the people who use it on stage. The easiest ways in:

1. **Add a fixture profile** for a light you own ([guide](docs/adding-a-fixture.md)).
2. **Add a controller layout** ([guide](docs/adding-a-controller.md)).
3. **Report hardware** that works, or doesn't ([form](../../issues/new?template=hardware-report.yml)).
4. **Share a scene idea** in [Discussions](../../discussions).

Read [CONTRIBUTING.md](CONTRIBUTING.md) and look for
[`good first issue`](../../issues?q=is%3Aopen+label%3A%22good+first+issue%22).

## Safety

RAYS can drive strobes and high-power blinders. Built-in scenes never trigger fixtures' internal
strobe programs, and Esc always means blackout. Respect photosensitivity guidelines when you
design your own scenes.

## Author

RAYS is created and maintained by **Manuel Gasparini** ([@gasparoff](https://github.com/gasparoff)),
born from real club nights and tested on real rigs. If RAYS lights up your set, a ⭐ helps other
DJs find it.

## License

RAYS source code is [MIT](LICENSE). Built apps include Ableton Link (GPLv2+) and run Beat Link
(EPL-2.0) as a helper: see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). RAYS is not
affiliated with Ableton, Pioneer DJ, AlphaTheta, inMusic, Lightkey, ENTTEC, Varytec or Allen & Heath.
