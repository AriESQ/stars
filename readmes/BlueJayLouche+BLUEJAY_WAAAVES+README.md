# DRAGON_WAAAVES v2.0

## Disclaimer

**This is NOT an official port of Gravity Waaaves.** The original creator, **Andrei Jay**, will not provide any support whatsoever for this software.

This source code is distributed AS-IS, there is no guaranteed continuing support. Please contact ElectronFlow on discord with any questions, please have a clear and concise description of the problem.

---

## Special Thanks to Andrei Jay

This project would not exist without the incredible work of **Andrei Jay**, who created the original VSEJET GRAVITY_WAAAVES and generously open-sourced his work. His contributions to the video synthesis community through open-source projects, educational resources, and creative tools have enabled countless artists and developers to explore the world of analog-style video feedback and synthesis.

**Please support Andrei:**
- Patreon: https://www.patreon.com/c/andrei_jay
- Ko-fi: https://ko-fi.com/andreijay
- Website: https://videosynthecosphere.com
- Alternative Website: https://andreijaycreativecoding.com

You can download WPDSK and GW-DSK from his website - **please go support him!**

---

## What It Is

An updated/modified port of the original VSEJET GRAVITY_WAAAVES from Andrei Jay, featuring a complete modular architecture rewrite, OSC control, NDI/Spout integration, GPU texture sharing, video file input, a built-in preview window with color picker, and many other enhancements.

A dual-channel, 2 input video effects processor and synthesizer built with openFrameworks.

---

## Major Upgrades in v2.0

### 🏗️ Complete Modular Architecture Refactor
The codebase has been completely restructured into a clean, modular architecture:

```
src/
├── Core/               # SettingsManager - Centralized JSON configuration
├── Inputs/             # InputManager - Unified webcam/NDI/Spout/VideoFile handling
├── ShaderPipeline/     # PipelineManager - 3-block shader processing
├── Output/             # OutputManager - Async NDI/Spout output with PBO transfer
├── Geometry/           # GeometryManager - Lissajous, Hypercube, and pattern generators
├── Parameters/         # ParameterManager - OSC/MIDI parameter system
├── Presets/            # PresetManager - Bank-based preset system
├── Preview/            # PreviewPanel - Real-time preview with color picker
├── Audio/              # AudioAnalyzer - FFT-based audio visualization
└── Tempo/              # TempoManager - BPM sync and tempo-based modulation
```

### ✨ New Features

- **Video File Input** - Load and loop video files as input sources
- **Preview Window with Color Picker** - Real-time preview of any shader block (B1/B2/B3) with click-to-pick color sampling for chroma-keying
- **Audio Visualization & Reactivity** - Real-time FFT analysis with 8 frequency bands (Sub Bass to Presence) for audio-reactive visuals
- **Tempo Sync (BPM)** - Tap tempo, beat-synchronized LFOs, and BPM-based parameter modulation
- **Runtime Settings Reload** - Edit `config.json` while the app is running - changes sync automatically
- **Cross-Platform Shader Loader** - Automatic GL3.2/GL4/GLES2 shader detection and loading
- **Async PBO Transfer** - Non-blocking GPU→CPU transfer for better NDI performance
- **JSON-Based Configuration** - Modern JSON settings (with automatic XML migration)

### 🔧 Technical Improvements

- **GPU-Only FBOs** - No CPU backing where not needed
- **Lazy Initialization** - Resources created on-demand
- **Shared Input Sources** - Webcam/NDI/Spout instances reused across inputs
- **Unified Shader Uniforms** - Batch uniform updates
- **Type-Safe Parameters** - Template-based parameter system with automated OSC addressing

### 🎛️ OSC & MIDI

- **700+ addressable parameters** for full automation
- Preserved original OSC addressing scheme (`/gravity/block1/ch1/xDisplace`, etc.)
- MIDI macro mapping (16 macros per parameter group) with latching

### 📺 Input/Output

- **Multiple input sources:** Webcam, NDI, Spout (Windows), Video Files
- **Streaming output:** NDI and Spout (Windows) with async sending
- **Dual feedback loops** in 3-block video processing chain

### 🎵 Audio & Tempo

- **8-Band FFT Analysis:** Sub Bass (20-60Hz), Bass (60-120Hz), Low Mid, Mid, High Mid, High, Very High, Presence (8k-16kHz)
- **Audio Modulation:** Map any FFT band to any parameter with adjustable amount, attack, release, and smoothing
- **Tap Tempo:** Click to set BPM based on your music
- **Beat-Synced LFOs:** All LFOs can sync to BPM with divisions (1/16, 1/8, 1/4, 1/2, 1, 2, 4, 8 beats)
- **Waveform Types:** Sine, Triangle, Saw, Square, Random
- **Per-Parameter Modulation:** Each parameter can have independent audio and/or BPM modulation

---

## Features

- 3-block video processing chain with dual feedback loops
- Multiple input sources: webcam, NDI, Spout (Windows), video files
- OSC control with 700+ addressable parameters for automation
- MIDI macro mapping (16 macros per parameter group)
- Streaming output via NDI and Spout
- Preset bank system with save/load functionality
- Built-in geometric pattern generators (Lissajous, Hypercube, Seven Star, Spiral Ellipse, Line)
- Real-time preview window with color picker for chroma-keying
- **Audio visualization with 8-band FFT and audio-reactive parameter modulation**
- **BPM tempo sync with tap tempo and beat-synchronized LFOs**
- Runtime configuration reloading
- Cross-platform support (Windows, macOS, Linux/Jetson)

---

## Requirements

- NewTek NDI: https://ndi.video
- Spout2: https://spout.zeal.co (Windows only)

!! Follow install instructions closely !!

- openFrameworks 0.12+ - https://github.com/openframeworks/openFrameworks.git

!! Follow install instructions closely !!

- Required addons (see `addons.make`):
  - ofxImGui - https://github.com/jvcleave/ofxImGui.git
  - ofxMidi - https://github.com/danomatika/ofxMidi.git
  - ofxNDI - https://github.com/leadedge/ofxNDI.git
  - ofxOsc - Packaged with openFrameworks
  - ofxSpout - https://github.com/ElectronFlowVJ/ofxSpout.git (Windows only)

---

## Usage

- The application runs with two windows: a control window (GUI) and an output window, but can also be used on single display (not recommended)
- FPS is variable from 1-60 (affects GUI as well for now)
- The output window can be set to fullscreen for production using **F11**
- Window decorations can be toggled with **F10**
- Presets are stored in `bin/data/presets/`

### Runtime Configuration

Settings are stored in `bin/data/config.json`. Edit this file while the app is running and changes will sync automatically:

- Display settings (resolution, FPS) - synced to GUI, click "Apply Resolution" to apply
- Input sources - synced to GUI, click "Reinitialize Inputs" to apply (safety feature)
- OSC/MIDI settings - auto-applied
- UI scale - auto-applied

---

## OSC Reference

See `bin/data/OSC_Parameters_Reference.txt` for complete OSC address documentation.

Common addresses:
```
/gravity/block1/ch1/xDisplace      - Channel 1 X displacement
/gravity/block1/ch2/mixAmount      - Channel 2 mix amount
/gravity/block1/fb1/delayTime      - FB1 delay time
/gravity/block2/input/zDisplace    - Block2 input Z displacement
/gravity/block3/matrix/mixBgRed    - Matrix mixer
/gravity/preset/save               - Save preset trigger
/gravity/preset/load               - Load preset trigger
/gravity/audio/enabled             - Enable audio analysis
/gravity/audio/fftBand0            - Sub Bass (20-60Hz) level
/gravity/audio/amplitude           - Global audio amplitude
/gravity/tempo/bpm                 - BPM tempo
/gravity/tempo/tap                 - Tap tempo trigger
/gravity/tempo/play                - Play/pause tempo
```

---

## MIDI

MIDI works with macro mapping (16 macros per parameter group). For posterity's sake, MIDI still works with the original implementation, though you can change your device now.

**Note:** Currently only works on Windows, crashes on Jetson when you try to refresh devices.

---

## Configuration

Settings are stored in `bin/data/config.json`:

```json
{
    "display": {
        "input1Width": 640,
        "input1Height": 480,
        "input2Width": 640,
        "input2Height": 480,
        "internalWidth": 1280,
        "internalHeight": 720,
        "outputWidth": 1280,
        "outputHeight": 720,
        "ndiSendWidth": 1280,
        "ndiSendHeight": 720,
        "targetFPS": 30
    },
    "osc": {
        "enabled": false,
        "receivePort": 7000,
        "sendIP": "127.0.0.1",
        "sendPort": 7001
    },
    "midi": {
        "selectedPort": -1,
        "deviceName": "",
        "enabled": false
    },
    "inputSources": {
        "input1SourceType": 1,
        "input2SourceType": 1,
        "input1DeviceID": 0,
        "input2DeviceID": 1,
        "input1NdiSourceIndex": 0,
        "input2NdiSourceIndex": 0
    },
    "audio": {
        "enabled": false,
        "inputDevice": 0,
        "sampleRate": 44100,
        "bufferSize": 512,
        "fftSize": 1024,
        "numBins": 128,
        "smoothing": 0.5,
        "normalization": true,
        "amplitude": 1.0,
        "peakDecay": 0.95
    },
    "tempo": {
        "bpm": 120.0,
        "enabled": true,
        "tapHistorySize": 8,
        "minBpm": 20.0,
        "maxBpm": 300.0,
        "autoResetTap": true,
        "tapTimeout": 2.0
    },
    "uiScaleIndex": 0
}
```

---

## Distribution

This software is only to be distributed as source code or on a Jetson disk image. Do not redistribute compiled binaries.

---

## Known Issues

- Scaling weirdness on Jetson around 300%
- Openbox window config on Jetson
- FPS slider behavior is a bit hit or miss
- touchOSC file still needs some (read: lots of) work
- OSC reference needs updated
- MIDI device refresh crashes on Jetson

---

## Support

If you like the work I've done here, please consider supporting electronFlow on Ko-fi: https://ko-fi.com/electronflow

**ElectronFlow's Website:** https://electronflow.tv

---

## Architecture Details

For detailed information about the modular architecture, see `AGENTS.md`.

For preview window integration details, see `PREVIEW_INTEGRATION_GUIDE.md`.

For shader loading updates, see `README_SHADER_UPDATE.md`.

---

## License

This project is based on the original VSEJET GRAVITY_WAAAVES by Andrei Jay. Please respect the original author's work and support him through the links above.
