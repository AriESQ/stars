# Prettyscope

Prettyscope is a modern OpenGL oscilloscope and signal visualizer. The goal is a
beautiful, musical scope that can grow from a standalone visual demo into a
reusable visualization layer for generated signals, audio buffers, and eventual
`soemdsp-sandbox` runtime output.

Longer-term, Prettyscope should also be able to publish its rendered GPU output
to visual-performance and projection workflows. The desired targets are
[Syphon](https://syphon.info/) on macOS, for realtime frame sharing between
creative applications, and [Spout](https://spout.zeal.co/) on Windows, for
low-latency realtime video routing between graphics tools.

This repository still contains PrettyScope Graveyard material at the root. New
work lives in `src/` and should stay small, direct, and runnable.

## Current Demo

- Native Win32 window
- OpenGL rendering through the vendored GLAD 3.2 loader
- Animated Gaussian beam waveform trace
- Small `SignalBuffer`, `TestSignalGenerator`, and `VisualParams` abstraction
- `SignalSource` interface for test signals now, and future audio/plugin input
- `ExternalSignalSource` prototype bridge for copied host/audio buffers
- `ScopeEngine` host boundary that owns params, signal advancement, and rendering
- `prettyscope.hpp` umbrella header for future host/plugin integrations
- Shared visual parameter descriptors, normalized automation helpers, and named
  palettes for future UI/plugin binding
- Keyboard controls for fast visual testing

## Roadmap

- Keep the standalone OpenGL renderer as the visual reference and development
  lab.
- Preserve the current phosphor XY look as the first golden preset.
- Build a clean input path for mono, stereo, and eventual external audio buffers.
- Prepare for future plugin/runtime integration, including `soemdsp-sandbox`.
- Prepare a future CLAP plugin path using the Architect-selected
  `baconpaul/sidequest-startingpoint` JUCE foundation. See
  `docs/PLUGIN_ROADMAP.md`.
- Add optional GPU frame-sharing outputs:
  - Syphon sender support on macOS.
  - Spout sender support on Windows.

## Build

```powershell
cmake -S . -B build-ninja -G Ninja
cmake --build build-ninja
.\build-ninja\prettyscope.exe
```

Run those commands from a Visual Studio Developer PowerShell or Developer
Command Prompt so MSVC is on `PATH`.

Press `Esc` or close the window to quit.

Run tests with:

```powershell
ctest --test-dir build-ninja --output-on-failure
```

## Controls

- `1` / `2`: decrease / increase waveform gain
- `Mouse wheel`: decrease / increase waveform gain
- `3` / `4`: decrease / increase glow strength
- `5` / `6`: decrease / increase trace width
- `7` / `8`: decrease / increase glow width
- `9` / `0`: coarse decrease / increase screen decay
- `[` / `]`: fine decrease / increase screen decay
- `T` / `Y`: decrease / increase phosphor fast decay
- `-` / `=`: decrease / increase phosphor tail burn
- `P`: toggle persistence
- `D`: toggle classic / phosphor decay style
- `F`: toggle FPS counter
- `G`: toggle graticule grid
- `X`: toggle 1D / XY vectorscope mode
- `Space`: cycle test signal
- `C`: cycle color palette
- `S`: save current default preset to `presets/default.prettyscope.json`
- `L`: load `presets/default.prettyscope.json`
- `R`: reset visual parameters

## Salvage Policy

The old JUCE plugin project, presets, color maps, and installer files are
reference material only unless a piece is intentionally adapted. Any salvaged
code or assets should be documented in `docs/SALVAGE.md` with source and reason.
