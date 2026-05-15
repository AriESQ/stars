# RustJay Delta

A GPU-accelerated motion extraction VJ tool based on **Posy's RGB delay technique**. Feed it any video source and it produces vivid, colourful motion trails by assigning temporally-delayed copies of the input to the R, G, and B channels independently.

## How It Works

RustJay Delta keeps a ring buffer of up to 16 past frames entirely on the GPU. Each frame, the shader samples three points in that history — one for red, one for green, one for blue — and differences adjacent pairs to extract motion energy:

```
Input frame  ──► GPU ring buffer (up to 16 frames)
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
         frame[R]   frame[G]   frame[B]   ← per-channel delays
              │         │         │
              └────── diff ───────┘
                        │
                 motion signal
                        │
              blend modes, gains, threshold, smoothing
                        │
                     output
```

Static areas produce near-zero motion signal and remain dark or neutral. Moving objects leave trails coloured by the delay spread — with the default 0/2/4 frame offsets, motion trails from red to green to blue.

## Features

### Motion Extraction

- **Per-channel frame delays** — Red, Green, Blue each independently 0–16 frames back
- **Grayscale input mode** — Convert to luminance before channel assignment for cleaner trails
- **Per-channel gain** — Negative values invert the channel signal
- **Intensity** — Blend between extracted motion and original input
- **Blend modes** — Replace, Add, Multiply, Screen, Difference, Overlay, Lighten, Darken
- **Threshold** — Suppress slow-moving areas; remaining range is renormalised
- **Trail fade** — Gamma-like boost that lifts darker trail areas
- **Spatial smoothing** — 5-tap neighbourhood sampling to soften noisy edges

### Built-in Presets

| Preset | Red | Green | Blue | Notes |
|---|---|---|---|---|
| Classic Posy | 0 | 2 | 4 | Grayscale input, Replace blend |
| Reverse | 4 | 2 | 0 | Trails run B→G→R |
| Subtle | 0 | 1 | 2 | Half intensity, Add blend |
| Extreme | 0 | 4 | 8 | Colour input, Add blend |
| RGB Trails | 0 | 3 | 6 | Colour input, Screen blend |
| Strobe | 0 | 0 | 1 | One-frame diff, Difference blend |

### GPU Frame Buffer

- Ring buffer of up to 16 frames stored as BGRA8 GPU textures
- GPU-to-GPU copies only — no CPU readback
- History size auto-scales with resolution to manage VRAM:
  - 720p / 1080p: 8 frames
  - 1440p: 7 frames
  - 4K: 6 frames

### Modulation

- **LFO** — 3 banks with Sine, Triangle, Ramp, Saw, Square waveforms; tempo sync; targets any motion parameter
- **Audio routing** — 8-band FFT routed to any parameter with per-route attack/release envelopes; beat detection
- **MIDI** — CC mapping with learn mode
- **OSC** — UDP server (port 9000)
- **Web remote** — WebSocket interface (port 8080)

### Presets

- Save/load full parameter snapshots including motion, LFO, and audio routing settings
- 8 quick-access slots for live performance
- Backward-compatible JSON format — older presets load with default LFO/routing values

### Inputs / Outputs

| | Sources |
|---|---|
| **In** | Webcam, NDI, Syphon (macOS), Spout (Windows), V4L2 (Linux) |
| **Out** | NDI, Syphon (macOS), Spout (Windows), V4L2 (Linux), screen |

## Install

Pre-built binaries are available on the [Releases](https://github.com/BlueJayLouche/rustjay-delta/releases) page.

| Platform | Format | Notes |
|----------|--------|-------|
| macOS Apple Silicon | `.dmg` | Ad-hoc signed. Right-click → Open on first launch. |
| macOS Intel | `.dmg` | Ad-hoc signed. Right-click → Open on first launch. |

Download the `.dmg`, open it, and drag RustJay Delta to your Applications folder.

> NDI and Syphon are not included in release builds. For NDI/Syphon support, build from source with `cargo build --release`.

## Building from Source

### Requirements

#### macOS
- macOS 11+ (Big Sur or later)
- Xcode Command Line Tools
- Rust 1.75+

#### Windows
- Windows 10/11 (64-bit)
- [Rust](https://rustup.rs/) 1.75+ with the `x86_64-pc-windows-msvc` toolchain
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (C++ workload)
- [LLVM](https://github.com/llvm/llvm-project/releases) (optional — only needed if building with `webcam` or `ndi` features)

#### Linux
- Vulkan-capable GPU
- Rust 1.75+

### Clone and Build

```bash
cd rustjay-delta
cargo build --release
```

The default build includes webcam support and works on all platforms with no extra dependencies beyond the Rust toolchain and platform build tools.

### NDI Support (Optional)

NDI is not included in the default build. To enable:

```bash
cargo build --release --features ndi
```

Download and install the NDI SDK from [ndi.video](https://ndi.video). On macOS the build system finds it automatically in `/usr/local/lib` or `/Library/NDI SDK for Apple/lib/macOS`. LLVM must also be installed (NDI's build script uses `bindgen`).

### Syphon Support (macOS Only)

Syphon is enabled automatically on macOS. The build system finds the framework at `../syphon-rs/syphon-lib/Syphon.framework`.

**Requirements:** The `syphon-rs` repo must be present as a sibling directory:

```
developer/rust/
├── syphon-rs/          ← must exist
└── rustjay-delta/
```

If your layout differs, set `SYPHON_FRAMEWORK_DIR` before building:

```bash
SYPHON_FRAMEWORK_DIR=/path/to/syphon-rs/syphon-lib cargo build --release
```

### Spout Support (Windows Only)

Spout is enabled automatically on Windows. No extra dependencies are required — the Spout sender protocol is implemented directly using the Windows D3D11 and DXGI APIs (via the `windows` crate).

```powershell
cargo build --release
cargo run --release
```

Open Resolume Arena, OBS (with [OBS-Spout2-Plugin](https://github.com/Off-World-Live/obs-spout2-plugin)), or any Spout-capable app on the same machine to receive the output.

### V4L2 Support (Linux Only)

On Linux, video I/O uses Video4Linux2 (V4L2):

- **V4L2 Input** — real webcams and any `/dev/video*` capture node are enumerated natively in the **Input** tab.
- **V4L2 Output** — frames are written to a virtual camera device created by the [`v4l2loopback`](https://github.com/umlaeute/v4l2loopback) kernel module. Other apps (OBS, ffplay, Chromium, Firefox) then read from the virtual camera as if it were a real webcam.

#### 1. Install `v4l2loopback`

```bash
# Arch / Manjaro
sudo pacman -S v4l2loopback-dkms v4l-utils

# Debian / Ubuntu
sudo apt install v4l2loopback-dkms v4l-utils
```

#### 2. Load the kernel module with a virtual device

```bash
sudo modprobe v4l2loopback devices=1 video_nr=10 \
    card_label="RustJay Output" exclusive_caps=1
```

- `video_nr=10` — the virtual node, so it appears as `/dev/video10`. Pick any free number.
- `card_label="RustJay Output"` — the name consumer apps (OBS, browsers) will display.
- `exclusive_caps=1` — required for Chromium/Firefox to recognize the device as a webcam.

Verify it worked:

```bash
v4l2-ctl --list-devices
# → RustJay Output (platform:v4l2loopback-000):
#       /dev/video10
```

Make it persist across reboots:

```bash
echo "v4l2loopback" | sudo tee /etc/modules-load.d/v4l2loopback.conf
echo "options v4l2loopback devices=1 video_nr=10 card_label=\"RustJay Output\" exclusive_caps=1" \
  | sudo tee /etc/modprobe.d/v4l2loopback.conf
```

#### 3. Start the stream

```bash
cargo run --release
```

In the control window → **Output** tab:
1. The "V4L2 Loopback Output" section lists all detected virtual cameras in a combo box.
2. Select `RustJay Output (/dev/video10)` and click **Start V4L2 Output**.
3. The status indicator turns green when streaming.

Consume the stream from any webcam-aware app:

```bash
ffplay /dev/video10
```

Or in OBS: **Sources → Video Capture Device → Device: RustJay Output**.
Or in a browser: open any webcam test site and pick "RustJay Output" from the camera list.

#### Format notes

- Frames are written as **YUYV 4:2:2** — the most compatible format across browsers, OBS, and ffmpeg-based tools.
- BGRA→YUYV conversion is done on the CPU with a pre-allocated scratch buffer (no per-frame allocation) using BT.601 limited-range coefficients.
- If the render resolution changes while the output is running, the V4L2 device is automatically reopened at the new size.

## Running

```bash
cargo run --release
```

## Controls

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `Esc` | Exit |
| `Space` | Toggle output fullscreen |
| `F` | Toggle fullscreen |

### GUI Tabs

#### Input Tab
- Select video source (Webcam, NDI, Syphon on macOS, Spout on Windows, V4L2 on Linux)
- Refresh device lists
- Input status and resolution display

#### Motion Tab
- Enable/disable motion extraction
- Per-channel delay sliders (Red 0–16, Green 0–16, Blue 0–16)
- Per-channel gain (−2.0 to 2.0; negative inverts)
- Intensity, blend mode dropdown
- Grayscale input toggle
- Input mix, trail fade, threshold, smoothing
- Preset buttons
- Open LFO window — 3 independent LFOs with waveform preview, tempo sync, and per-LFO target assignment

#### Audio Tab
- Device selection
- Amplitude, smoothing, normalization
- 8-band FFT display
- Audio routing matrix — map any FFT band to any motion parameter with independent attack/release envelopes
- Beat detection, tap tempo

#### Output Tab
- NDI output name and toggle
- Syphon output name and toggle (macOS)
- Spout output name and toggle (Windows)
- V4L2 loopback device selector + toggle (Linux)
- Resolution preset (720p / 1080p / 1440p / 4K)
- Fullscreen toggle

#### Settings Tab
- MIDI, OSC, Web remote controls
- UI scale

## Configuration

Settings are auto-saved to `~/.config/rustjay/settings.json`. You can also use `config.toml` in the project root:

```toml
[video]
internal_width = 1280
internal_height = 720
surface_format = "Bgra8Unorm"
vsync = true

[audio]
sample_rate = 48000
buffer_size = 1024
fft_size = 2048
```

## Technical Details

### Frame History Memory

At 1080p with 8 frames of history: 8 × 1920 × 1080 × 4 bytes ≈ **66 MB VRAM**. History size is automatically reduced at higher resolutions.

### Color Format

Native `Bgra8Unorm` throughout — matches macOS surface format and Syphon's native format, eliminating conversion overhead.

### Audio Processing

- `realfft` 3.4 with lock-free `AtomicU32` sharing — no mutex on the real-time audio thread
- 8-band FFT (20 Hz – 16 kHz), optional pink noise shaping
- Beat detection with energy history

## Troubleshooting

### "Library not loaded: Syphon.framework"

1. Verify the framework exists: `ls ../syphon-rs/syphon-lib/Syphon.framework`
2. Rebuild after setting the path: `SYPHON_FRAMEWORK_DIR=/path/to/syphon-rs/syphon-lib cargo build --release`

### NDI source not found

- Install the NDI Runtime from [ndi.video](https://ndi.video)
- Ensure source and receiver are on the same subnet
- Check firewall — NDI uses ports 5960–5969

### Performance

- Use `cargo run --release` — debug builds are significantly slower
- Lower the resolution preset in the Output tab to reduce VRAM usage
- Disable smoothing if CPU-bound

## License

MIT License — see LICENSE for details

## Credits

Motion extraction technique by [Posy](https://www.youtube.com/@Posy).

Built with:
- [wgpu](https://github.com/gfx-rs/wgpu) — GPU rendering
- [imgui-rs](https://github.com/imgui-rs/imgui-rs) — immediate mode GUI
- [grafton-ndi](https://crates.io/crates/grafton-ndi) — NDI support
- [nokhwa](https://github.com/l1npengtul/nokhwa) — webcam capture
- [realfft](https://github.com/HEnquist/realfft) — FFT analysis
- [syphon-rs](https://github.com/BlueJayLouche/syphon-rs) — Syphon integration (macOS)
