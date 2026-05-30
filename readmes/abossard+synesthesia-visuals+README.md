# Synesthesia Visuals

A VJ performance toolkit built around **VirtualDJ** (DJ + phrasing), **Magic Music Visuals** (audio analysis + visuals), **QLC+5** (DMX lighting), **LedFX** (LED strips), and **SwiftVJApp** (central hub). MIDI controllers (Launchpad, MIDImix) tie everything together for live performance.

## Live Rig Architecture

```
┌──────────┐                    ┌──────────────┐
│VirtualDJ │──OS2L (TCP:9997)──▶│  SwiftVJApp  │──Syphon──▶ Magic Music Visuals
│          │──OSC  (UDP:9010)──▶│  (central    │              │         │
│          │                    │   hub)       │              │         │
│          │──OS2L (TCP:9996)──▶│              │              ▼         │
│          │   (beat, cues      │              │──REST──▶  LedFX       │
│          │    direct to QLC+) │              │          (LED strips)  │
└──────────┘                    └──────────────┘              │         │
                                                              │    OSC  │
┌──────────┐                                                  │    from │
│  QLC+5   │◀── OS2L from VDJ (beat sync, cue actions) ──────┘   Magic │
│  (DMX)   │◀── OSC  from Magic (audio-reactive lighting) ◀──────────┘
│          │──▶ DMX fixtures, ArtNet → WLED
└──────────┘
```

### Signal Flow

| Signal | From | To | Protocol | Port |
|--------|------|----|----------|------|
| Beat, cue actions, phrasing | VirtualDJ | QLC+5 (direct) | OS2L (TCP) | 9996 |
| Beat, cue actions, phrasing | VirtualDJ | SwiftVJApp | OS2L (TCP) | 9997 |
| Track info, BPM, deck state | VirtualDJ | SwiftVJApp | OSC (UDP) | 9010 |
| Cue events → shader control | SwiftVJApp | Magic | OSC (UDP) | 11111 |
| Lyrics + song info overlay | SwiftVJApp | Magic | Syphon | — |
| Audio levels (bass/mid/high) | Magic | QLC+5 | OSC (UDP) | configurable |
| LedFX playlist triggers | SwiftVJApp | LedFX | HTTP REST | 8888 |
| LedFX scene select | QLC+5 | sACN_ledfx_bridge → LedFX | sACN (E1.31) | 5568 |
| DMX → fixtures | QLC+5 | lights/WLED | DMX/ArtNet | — |

### What Each App Does

| App | Role | Receives | Sends |
|-----|------|----------|-------|
| **VirtualDJ** | DJ + musical structure (phrasing, cue points) | — | OS2L (beat/cues), OSC (track info) |
| **SwiftVJApp** | Central hub: lyrics, Syphon output, LedFX triggers | OS2L from VDJ, OSC from VDJ | Syphon to Magic, OSC to Magic, REST to LedFX |
| **Magic** | Visuals + audio analysis | Syphon from SwiftVJApp, audio input | OSC to QLC+ (audio-reactive lighting) |
| **QLC+5** | DMX lighting show control | OS2L from VDJ (beat), OSC from Magic (audio) | DMX/ArtNet to fixtures, sACN to LedFX bridge |
| **LedFX** | LED strip effects | REST from SwiftVJApp, REST from sACN bridge | LED data to WLED |
| **sACN_ledfx_bridge** | QLC+ → LedFX scene bridge | sACN (E1.31) from QLC+ | REST to LedFX (scene activate/deactivate) |

## Setup Checklist

### Ports to configure

| Port | App that listens | Configure in | What to set |
|------|-----------------|--------------|-------------|
| **9996** | QLC+5 | QLC+ → Input/Output → OS2L plugin | Enable, default port |
| **9997** | SwiftVJApp | SwiftVJApp → Settings or bridge config | OS2L listen port |
| **9010** | SwiftVJApp | SwiftVJApp → Settings | VDJ OSC receive port |
| **11111** | Magic | Magic → OSC input module | Listen port for SwiftVJApp |
| **8888** | LedFX | LedFX config | REST API port (default) |
| **5568** | sACN_ledfx_bridge | Bridge config.json / TUI | E1.31 sACN port (default); bridge + QLC+ must match universe |
| **OS2L target** | — | VirtualDJ → Settings → OS2L | Set to `127.0.0.1` (both 9996 for QLC+ and 9997 for SwiftVJApp) |

### Quick start checklist

1. **VirtualDJ**: Settings → OS2L → enable, target IP `127.0.0.1`
2. **QLC+5**: Input/Output → enable OS2L plugin on Universe 2
3. **Magic**: Add OSC input module, set listen port (for QLC+ audio OSC)
4. **Magic**: Add Syphon input, select SwiftVJApp's Syphon servers (Lyrics, SongInfo, Shader)
5. **LedFX**: Start LedFX (`ledfx`), verify API at `http://127.0.0.1:8888`
6. **SwiftVJApp**: Launch, verify Hub Dashboard shows green status for OSC Hub + OS2L

### VDJ cue points for lighting

In VirtualDJ's POI Editor, add **Action POIs** at key moments:
- Drop: `os2l_button "drop"`
- Chorus: `os2l_button "chorus"`
- Strobe: `os2l_button "strobe"`
- Blackout: `os2l_button "blackout"`

These fire as OS2L → SwiftVJApp translates to OSC for Magic + REST for LedFX. QLC+ receives them directly for DMX.

## Repository Structure

```
├── swift-vj/               # macOS VJ control app (SwiftUI + Metal rendering)
│   ├── Sources/
│   │   ├── SwiftVJApp/     # SwiftUI application
│   │   │   ├── Rendering/  # Metal-based shader/text/image rendering
│   │   │   └── Views/      # Master control, Hub dashboard, shader browser
│   │   ├── SwiftVJCore/    # Core library
│   │   │   ├── Modules/    # Playback, Lyrics, AI, Shaders, Pipeline
│   │   │   ├── Adapters/   # OSCHub, VDJMonitor, OS2LAdapter, LedFXClient
│   │   │   ├── Domain/     # Pure data types (OS2LTypes, HubMessage, BridgeConfig)
│   │   │   └── Launchpad/  # MIDI controller support
│   │   └── OscRestBridge/  # Generic OSC → REST translation engine
│   └── Tests/              # Behavior + E2E integration tests
├── magic/                  # ISF shaders for Magic Music Visuals
├── synesthesia-shaders/    # Synesthesia .synScene directories (GLSL + JSON + JS)
├── docs/                   # Documentation (setup, operation, reference)
└── archive/                # Deprecated code (Python-VJ, Processing-VJ)
```

## Quick Start

**→ [Quick Start: Magic Music Visuals + QLC+](docs/setup/quickstart-magic-to-qlcplus.md)** — Get the full audio-visual-lighting pipeline running.

### Swift-VJ Control Application
The `swift-vj/` folder contains a native macOS application serving as the central hub.

**Features:**
- **Hub Dashboard** — Unified view of all OSC, OS2L, and REST traffic with live filtering
- **Playback Monitoring** — VirtualDJ (OSC) and Spotify (AppleScript) support
- **Lyrics System** — LRCLIB API + AI refrain detection, rendered as Syphon overlay for Magic
- **OS2L Bridge** — Receives VDJ cue point actions, translates to OSC (Magic) + REST (LedFX)
- **LedFX Integration** — Trigger playlists/scenes from VDJ cue points via REST API
- **App Launcher** — Start/Stop DJ Rig (VDJ + QLC+ + Magic + LedFX) with one button
- **Shader Engine** — Metal-based rendering with 300+ GLSL shaders
- **MIDI Control** — Launchpad Mini Mk3 support with learn mode
- **Syphon Output** — 6 servers (Shader, Mask, Lyrics, Refrain, SongInfo, Image)

**Requirements:**
- macOS 14.0+ (Sonoma)
- Xcode 15+ / Swift 5.9+

**Installation:**
```bash
cd swift-vj
swift build
swift run SwiftVJApp
```

See [swift-vj/README.md](swift-vj/README.md) for detailed documentation.

## Audio Analysis

**Primary Engine**: [Magic Music Visuals](https://magicmusicvisuals.com/) provides audio analysis with:
- Per-band energy (bass, mid, high) via dual-envelope ISF shaders
- Beat detection and BPM estimation
- Spectral features (centroid, flux)
- OSC output to QLC+5 for audio-reactive DMX lighting

### MIDI Controllers
This project uses:
- **Akai MIDImix** - VJ/lighting control (faders, knobs)
- **Launchpad Mini Mk3** - Interactive control (pad grid, learn mode)

Swift-VJ includes full Launchpad support via CoreMIDI with:
- 4 pad modes (SELECTOR, TOGGLE, ONE_SHOT, PUSH)
- Button groups with radio behavior
- LED control (10 colors × 3 brightness levels)
- Learn mode for interactive pad mapping
- Beat-synced LED blinking

## Documentation

**[📚 Complete Documentation](docs/)** — Organized by purpose: Setup, Operation, Reference, Development

### Quick Links

**🚀 Setup**
- [Quick Start: Magic → QLC+](docs/setup/quickstart-magic-to-qlcplus.md) — Full audio → lighting pipeline
- [Magic Music Visuals Setup](docs/setup/magic-detailed-setup.md) — Audio analysis, globals, dual-envelope
- [QLC+ Setup](docs/setup/qlcplus-detailed-setup.md) — DMX, OS2L input, OSC from Magic
- [MIDI Controller Setup](docs/setup/midi-controller-setup.md) — Launchpad + MIDImix

**🎮 Using the System**
- [Swift-VJ Documentation](swift-vj/README.md) — Central hub app
- [Magic Music Visuals Guide](docs/operation/magic-music-visuals-guide.md) — MMV operations

**📚 Technical Reference**
- [OSC Architecture](OSC.md) — Current OSC communication system
- [ISF to Synesthesia Migration](docs/reference/isf-to-synesthesia-migration.md) — Shader conversion
- [Magic Dual Envelope Audio](docs/reference/magic-dual-envelope-audio-analysis.md) — Audio analysis reference

## Controller Roles

| Controller | Primary Use | Integration |
|------------|-------------|-------------|
| Akai MIDImix | VJ / lighting faders & knobs | Magic Music Visuals |
| Launchpad Mini Mk3 | Scene triggering, pad control | SwiftVJApp (CoreMIDI, learn mode, 8 banks) |

See [OSC.md](OSC.md) for the full OSC message format reference.

## License

See individual shader files for licensing. Original shader credits are preserved in scene metadata.
