# VideoSynthEngine

[![openFrameworks](https://img.shields.io/badge/openFrameworks-0.12+-purple)](https://openframeworks.cc)
[![Addons](https://img.shields.io/badge/addons-1-blueviolet)](addons.make)
[![Platform](https://img.shields.io/badge/platform-macOS%20|%20RPi%20|%20Linux-lightgrey)]()

A reusable openFrameworks video synthesis engine combining the best abstractions from **Channel0**, **Mantis**, and **NTSC-Player** into a single plug-and-play foundation.

Designed for live video performance: camera input, USB video playback, multi-pass GPU shader processing, MIDI control, and optional Raspberry Pi GPIO — all cleanly separated into independent, reusable classes.

---

## Quick Start

```bash
# Requires openFrameworks 0.12+ with ofxMidi addon installed
cd /Applications/openFrameworks/apps/myApps/VideoSynthEngine
make -j$(sysctl -n hw.logicalcpu)
make RunRelease
```

No camera? The app falls back to a procedural test pattern. No MIDI controller? Keyboard and (on RPi) GPIO work identically.

---

## Architecture

```
                    ┌──────────────┐
  Camera ──────────▶│    Video     │
                    │   Source     ├──▶ ┌───────────────┐     ┌──────────────┐
  Video File ──────▶│              │    │  FrameBuffer  │     │  Shader      │
  (USB hotplug)     └──────────────┘    │  (optional    │────▶│  Manager     │──▶ Screen
                                        │   ring buf)   │     │  (multi-pass)│
  Test Pattern ───▶ (fallback)          └───────────────┘     └──────────────┘
                                                                    ▲
                                                               ┌────┴────┐
                                                               │  MIDI   │
                                                               │  GPIO   │
                                                               └─────────┘
```

The pipeline is a directed graph managed by `ofApp` through a `SourceMode` enum:

| Mode | Description |
|---|---|
| `SOURCE_CAMERA` | Live camera grabber via `VideoInputManager` |
| `SOURCE_PLAYBACK` | Video file playback via `VideoPlayer` |
| `SOURCE_TEST_PATTERN` | Procedural color bars when no camera/playback |

The source → `ShaderManager` chain → screen. `FrameBuffer` is available as a standalone ring buffer for frame-accurate capture (used in downstream projects).

---

## Components

All 10 core abstractions extracted from the three predecessor projects:

| Class | Origin | Purpose | File |
|---|---|---|---|
| `MidiController` | NTSC-Player / Channel0 | Named MIDI binding (`bindContinuous`/`bindTrigger`), threshold activation, `getByCC()` for ShaderManager interop, thread-safe message queue, port cycling | `src/MidiController.h/.cpp` |
| `ShaderManager` | NTSC-Player | Multi-pass FBO ping-pong chain, cross-platform GL version injection (`#version 300 es` on RPi, `#version 150` on desktop), standard uniforms (`uFrameCount`, `iTime`, `iResolution`, `uSourceSize`, `uOutputSize`), MIDI param mapping | `src/ShaderManager.h/.cpp` |
| `ShaderPresets` | NTSC-Player (extracted) | Named preset system with automatic MIDI remapping per preset. Demonstrates single-pass and multi-pass (sharpen→colourise) chains | `src/ShaderPresets.h/.cpp` |
| `ShaderParam` | NTSC-Player | Struct: name/value/min/max/defaultValue. Used by both ShaderManager and ShaderPresets for parameter definition | `src/ShaderParam.h` |
| `FrameBuffer` | Mantis | Header-only ring buffer of `ofPixels`. `addFrame()`, `removeFirstFrame()`, `getFrame()`, `getAllFrames()`, `setFrames()`, `resize()` | `src/FrameBuffer.h` |
| `VideoInputManager` | Mantis | Auto-detects suitable capture devices (filters `bcm2835` ISP devices on RPi), periodic polling for hotplug, device cycling | `src/VideoInputManager.h/.cpp` |
| `VideoPlayer` | Channel0 | Wraps `ofVideoPlayer` with retry logic (4 attempts, 250ms backoff) for USB storage latency. Simplified to a single backend (no HAP dependency) | `src/VideoPlayer.h/.cpp` |
| `DriveWatcher` | Channel0 | Polls `/Volumes` (macOS) / `/media` (Linux) every 1s for hotplug detection. Callback-based with `simulateEvent()` for initial enumeration | `src/DriveWatcher.h/.cpp` |
| `ButtonController` | Mantis | Threaded GPIO button with edge detection. Uses `wiringPiSetupGpio()` (BCM pin numbering). Adds `getPinNum()` for multi-button identification. Compiles to no-op on non-RPi platforms | `src/ButtonController.h/.cpp` |
| `RotaryEncoderController` | Mantis | Interrupt-driven rotary encoder with lookup table (`dirTable[4][4]`) and detent detection (both pins HIGH). Fixed ISR wrapper: handles both rising and falling edges correctly. Compiles to no-op on non-RPi platforms | `src/RotaryEncoderController.h/.cpp` |

---

## Presets

| # | Name | Passes | Params | MIDI Map |
|---|---|---|---|---|
| 0 | passthrough | 1 | — | — |
| 1 | colourise | 1 | uHue, uSaturation, uContrast, uBrightness | CC 0-3 |
| 2 | sharpen | 1 | uAmount | CC 0 |
| 3 | mix | 1 | uMix | CC 0 |
| 4 | sharpen+colour | 2 | sharpen(uAmount) → colourise(uHue/uSat/uCon/uBri) | CC 0-5 |

Presets are defined in `ShaderPresets::setup()`. Each param maps to a MIDI CC (sliders CC 0-7, knobs CC 16-23). Switching presets automatically remaps MIDI bindings.

### Adding a New Preset

In `src/ShaderPresets.cpp`:

```cpp
presets.push_back({"my-effect", {{"my-effect", "shaders/passthru.vert", "shaders/my_effect.frag",
    {
        {"uParam1", 0.5f, 0.0f, 1.0f, 0.5f},
        {"uParam2", 1.0f, 0.0f, 5.0f, 1.0f},
    }
}}});
```

Then create `bin/data/shaders/my_effect.frag` — it receives all standard uniforms plus your custom params.

---

## Controls

### Keyboard

| Key | Action |
|---|---|
| `[` / `]` or `P` / `N` | Previous / Next preset |
| `D` | Toggle debug HUD |
| `M` | Cycle MIDI input port |
| `F` | Toggle fullscreen |
| `R` | Reset to passthrough preset |
| `0` | Test pattern source |
| `1` | Camera source (falls back to test pattern) |
| `2` | Video playback source (requires USB drive) |
| `3` — `7` | Direct preset select by index |

### MIDI

| CC | Binding | Range |
|---|---|---|
| 0-7 | slider0-7 (param mapping per preset) | -1.0 – 1.0 → mapped to param min/max |
| 16-23 | knob0-7 (param mapping per preset) | -1.0 – 1.0 → mapped to param min/max |
| 41 | prevPreset (trigger) | edge |
| 42 | nextPreset (trigger) | edge |
| 43 | debug (trigger) | edge |
| 44 | prev (file index) | edge |
| 45 | next (file index) | edge |
| 62 | reset (trigger) | edge |

MIDI controller values are normalized to -1.0 – 1.0. A threshold filter prevents accidental activation from resting controller positions.

### GPIO (Raspberry Pi only)

Auto-detected at compile time — no wiringPi on macOS or Linux desktop.

| Pin (BCM) | Type | Action |
|---|---|---|
| 26 | Button | Next preset |
| 19 | Button | Previous preset |
| 13 | Button | Toggle debug |
| 6 | Button | Reserved |
| 1 | Button | Reserved |
| 5, 0 | Rotary Encoder | Buffer select (reserved for FrameBuffer) |
| 16, 12 | Rotary Encoder | Window size (reserved for FrameBuffer) |
| 21, 20 | Rotary Encoder | Window position (reserved for FrameBuffer) |

Uses BCM pin numbering (`wiringPiSetupGpio()`). Button pins have internal pull-up resistors enabled.

---

## GPIO Platform Detection

GPIO controllers use `__has_include(<wiringPi.h>)` (C++17) for compile-time auto-detection:

| Platform | `__linux__` | `__has_include(<wiringPi.h>)` | GPIO enabled |
|---|---|---|---|
| macOS | ❌ | — | ❌ |
| Raspberry Pi (Raspbian) | ✅ | ✅ | ✅ |
| Linux desktop | ✅ | ❌ | ❌ |

Defined in `src/PlatformConfig.h`:

```cpp
#pragma once
#if defined(__linux__) && __has_include(<wiringPi.h>)
    #define VSE_HAS_GPIO
    #include <wiringPi.h>
#endif
```

On non-RPi platforms, `ButtonController` and `RotaryEncoderController` compile to stub objects with empty method bodies — no linker errors, no missing symbols.

---

## Shader Authoring

### Standard Uniforms (set by ShaderManager)

| Uniform | Type | Description |
|---|---|---|
| `uFrameCount` | `float` | Elapsed frames since app start |
| `iFrame` | `int` | Elapsed frames (integer) |
| `iTime` | `float` | Approximate seconds (`frameNum / 60.0`) |
| `iResolution` | `vec3` | Output width, height, 0 |
| `uSourceSize` | `vec2` | Source texture width, height |
| `uOutputSize` | `vec2` | Output FBO width, height |

### Texture Sampler

```glsl
uniform sampler2D src;
```

Your fragment shader receives the source texture through `src`. Coordinates are normalized (0.0 – 1.0). The texture target is always `GL_TEXTURE_2D` (`ofDisableArbTex()` is called at setup).

### Multi-pass Chaining

When a preset has multiple passes, each pass receives the previous pass's output as its `src`. Passes are processed left-to-right in the FBO ping-pong chain:

```
passthrough.vert             passthrough.vert
sharpen.frag      ───▶      colourise.frag      ───▶ screen
                  FBO A                      FBO B
```

### Example: Simple Invert

```glsl
uniform sampler2D src;

in vec2 vTexCoord;
out vec4 fragColor;

void main()
{
    vec4 col = texture(src, vTexCoord);
    fragColor = vec4(1.0 - col.rgb, col.a);
}
```

Save as `bin/data/shaders/invert.frag` and add a preset in `ShaderPresets.cpp`.

---

## Dependencies

**Required:**
- [openFrameworks](https://openframeworks.cc/download/) 0.12+ (tested on macOS 10.15+, requires C++17)
- `ofxMidi` addon (included with OF by default)

**Optional (Raspberry Pi only):**
- `wiringPi` library (`sudo apt install wiringpi`)

No other addons. No vendored binaries. Clone, configure `OF_ROOT` in `config.make`, and build.

---

## Project Structure

```
VideoSynthEngine/
├── src/
│   ├── main.cpp                      # Window setup (720×480, GL 3.2)
│   ├── ofApp.h / ofApp.cpp           # Pipeline orchestrator, mode routing
│   ├── PlatformConfig.h              # VSE_HAS_GPIO detection
│   ├── MidiController.h / .cpp       # Named MIDI binding
│   ├── ShaderManager.h / .cpp        # Multi-pass FBO chain
│   ├── ShaderPresets.h / .cpp        # Preset definitions & loading
│   ├── ShaderParam.h                 # Param struct (header-only)
│   ├── FrameBuffer.h                 # Pixel ring buffer (header-only)
│   ├── VideoInputManager.h / .cpp    # Camera auto-detect & hotplug
│   ├── VideoPlayer.h / .cpp          # Unified video player with retry
│   ├── DriveWatcher.h / .cpp         # USB volume hotplug
│   ├── ButtonController.h / .cpp     # GPIO button (RPi, stubs elsewhere)
│   └── RotaryEncoderController.h / .cpp  # GPIO encoder (RPi, stubs elsewhere)
├── bin/data/
│   ├── shaders/
│   │   ├── passthru.vert             # Vertex shader (used by all presets)
│   │   ├── passthru.frag             # No-op fragment shader
│   │   ├── test_pattern.frag         # Procedural color bars + grid
│   │   ├── colouriser.frag           # Hue/saturation/contrast/brightness
│   │   ├── sharpen.frag              # Unsharp mask (uses uSourceSize)
│   │   └── mixer.frag               # Mirror crossfade
│   └── fonts/
│       └── VCR_OSD_MONO_1.001.ttf    # Screen-optimized monospace font
├── addons.make                       # ofxMidi
├── config.make                       # OF_ROOT, C++17
└── Makefile                          # OF standard makefile
```

---

## Cross-Platform Notes

- **macOS**: Primary development target. Window mode at 720×480, GL 3.2 core profile, `#version 150` shaders.
- **Raspberry Pi**: Set `TARGET_RASPBERRY_PI` for GLES 3.0 shader version (`#version 300 es`). GPIO controllers auto-enable when wiringPi is detected.
- **Linux desktop**: Same shader path as macOS. GPIO controllers compile to no-ops. Ensure `ofxMidi` is installed.
- **Video playback**: Standard `.mov`/`.mp4` via `ofVideoPlayer`. Use H.264 or PhotoJPEG for reliable seeking on embedded devices.
- **USB storage**: `DriveWatcher` polls `/Volumes` (macOS) or `/media` (Linux). Video files are discovered recursively per volume.

---

## Class Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                             ofApp                            │
│  ┌─────────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │  MidiController │  │ ShaderManager │  │  ShaderPresets │  │
│  └─────────────────┘  └───────────────┘  └────────────────┘  │
│  ┌─────────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │  VideoInputMgr  │  │  VideoPlayer  │  │  DriveWatcher  │  │
│  └─────────────────┘  └───────────────┘  └────────────────┘  │
│  ┌─────────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │  BtnController  │  │  EncoderCtrl  │  │   FrameBuffer  │  │
│  │      (RPi)      │  │     (RPi)     │  │   (optional)   │  │
│  └─────────────────┘  └───────────────┘  └────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Origin Projects

VideoSynthEngine consolidates patterns from three video synthesis projects:

| Project | Purpose | Key Contributions |
|---|---|---|
| [Channel0](https://github.com/petehaughie/Channel0) | 60fps HAP video player | MidiController pattern, DriveWatcher, retry logic, dual video player abstraction |
| [Mantis](https://github.com/petehaughie/mantis) | 5-bank frame buffer | FrameBuffer, VideoInputManager, BufferWindowState, GPIO controllers (improved) |
| [NTSC-Player](https://github.com/petehaughie/NTSC-Player) | Shader-based video processor | ShaderManager, ShaderPresets, ShaderParam, extended MidiController (getByCC) |

Each class is tagged with its origin in this README. Improvements made during consolidation are noted in commit messages.

---

## License

MIT
