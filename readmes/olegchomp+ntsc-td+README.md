# ntsc-td

<img width="720" height="480" alt="Image" src="https://github.com/user-attachments/assets/08bbd91c-267d-417f-b314-485d5b810793" />


A TouchDesigner Custom TOP that runs [ntsc-rs](https://github.com/valadaptive/ntsc-rs) on the CPU. It shows up in the OP Create dialog as **NTSC** (type `Ntscrs`).

The effect is the same signal chain as the ntsc-rs standalone app: composite encoding, VHS, head switching, ringing, and the rest. Frames are processed as 8-bit BGRA. Put a Resolution TOP at **720×480** (or 480×720) in front of the node — the plugin does not resample.

This is a heavy CPU process, not a GPU shader. Even at 720×480 the cook can take a full frame or more, so project FPS may drop below 60. Larger resolutions make that worse. Info CHOP `process_ms` / `cook_ms` show where the time goes.

Built against **TOP API 12** (TouchDesigner 2025.31760) on Windows x64.

## Install

1. Copy `Plugins/Ntsc.dll` into a `Plugins` folder next to your `.toe`, or into `Documents/Derivative/Plugins`.
2. Fully quit TouchDesigner and open the project again. Custom operators are scanned only at startup.
3. Tab → Custom → **NTSC**. Wire one TOP into it.

If TouchDesigner asks whether to trust the plugin, allow it.

## Parameters

The `Ntsc Plugin` page is the host:

| Parameter | What it does |
|---|---|
| Bypass | Pass the input through unchanged |
| Frame Source | Timeline frame or frames-since-startup (seeds the noise) |
| Cook Every Frame | Keep cooking on a still input so the noise moves |
| Low Latency (Stall) | Process the current frame immediately; otherwise the node stays one frame behind |
| Threads | `0` uses every physical core |
| Use Preset File | Load a JSON preset saved from the ntsc-rs app |

Every other page is generated from ntsc-rs itself (`Ntsc`, `VHS emulation`, `Head switching`, and so on), so the settings match the reference application.

Info CHOP channels: `process_ms`, `wait_ms`, `memcpy_ms`, `cook_ms`, `width`, `height`, `threads`.

## Build

Needs Rust (stable), CMake, and Visual Studio 2022 with the C++ workload. TouchDesigner 2025.31760 must be installed so the C++ TOP headers are on disk.

```bat
cd td_plugin
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
```

The finished `Ntsc.dll` is copied to `Plugins/`. Point `-DTD_SDK_DIR` at another TouchDesigner `Samples/CPlusPlus` folder if the default path does not match your install.

`vendor/ntscrs` is the ntsc-rs processing crate, vendored so the plugin builds without the rest of that project.

## License

Plugin sources in this repository are MIT. The signal processing comes from ntsc-rs (`crates/ntscrs`), which is MIT OR ISC OR Apache-2.0. See `LICENSE` and `NOTICE`. The GUI crate of ntsc-rs is GPL-3.0 and is **not** included.
