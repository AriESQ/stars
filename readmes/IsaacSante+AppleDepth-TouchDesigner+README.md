# Apple Depth for TouchDesigner

A native C++ TOP plugin for TouchDesigner that runs [Depth Anything V2](https://depth-anything-v2.github.io/) (Apple's CoreML build) on live video, entirely in-process via Vision/CoreML. Any TOP in → 32-bit float depth map out, in real time on Apple Silicon.

The model is **bundled automatically at build time** — there is nothing to download or configure. Clone, build, done.

## Requirements

*   **macOS on Apple Silicon** (arm64).
*   **TouchDesigner** 2023+ (built against the 2025 SDK headers).
*   **CMake** (`brew install cmake`) and the Xcode Command Line Tools.

## Building

```bash
# prerequisite (skip if you already have CMake)
brew install cmake

git clone https://github.com/IsaacSante/AppleDepth-TouchDesigner.git
cd AppleDepth-TouchDesigner

# run these from inside the project folder
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
cmake --install build
```

The first configure downloads the CoreML model (~50 MB, one time) from Hugging Face and bakes it into the plugin bundle. `cmake --install` copies the finished plugin to `~/Library/Application Support/Derivative/TouchDesigner099/Plugins/`, where TouchDesigner finds it at startup.

Restart TouchDesigner — the plugin appears in the OP Create dialog under **Custom → Apple Depth**.

## Features

*   **Real-time monocular depth:** ~30 fps inference on an Apple Silicon Mac while TouchDesigner keeps rendering at 60 fps.
*   **Asynchronous inference:** processing runs on a background queue; one inference in flight, stale frames dropped, the node never stutters the timeline.
*   **Frame-perfect synchronization:** a second output carries the original RGB image time-aligned to the depth result, so downstream compositing never ghosts.
*   **32-bit float output:** full-precision depth (`Mono32Float`) at the model's native resolution — no 8-bit banding in point clouds.
*   **Self-contained:** the CoreML model ships inside the plugin bundle. No model files, no paths, no Python.
*   **Diagnostic Info CHOP channels:** latency, queue state, model status, and the per-frame depth range.

## Usage

Wire any TOP (webcam, movie, NDI…) into the node. The first model load compiles CoreML for ~10 seconds (asynchronous — watch the Textport for `[AppleDepth] model ready`), after which depth streams continuously.

### Outputs

1.  **Output 0 (main):** the depth map, `Mono32Float`, at the model's native resolution.
2.  **Output 1:** the original RGB frame, delayed to match the depth result exactly. Access it with a **Render Select TOP** pointed at the node, **Color Buffer Index = 1**.

### The output is disparity, not distance

Depth Anything outputs *inverse* depth: larger = closer, normalized per frame. Two consequences:

*   **Normalize with a smoothed range.** The per-frame min/max shifts as objects enter the frame. Read `depth_min` / `depth_max` from an **Info CHOP**, smooth with a **Lag CHOP** (~0.5 s), and normalize in a Math or GLSL TOP. Normalization is deliberately left out of the plugin so it stays visible and tunable.
*   **For metric-ish depth or point clouds**, convert with `z = 1 / (a·d + b)` and tune `a`, `b` by eye. Feeding `z` into a **TOP to POP** in Depth mode (with your camera's FOV) yields a correctly unprojected point cloud.

### Info CHOP channels

*   `latency_frames` — frames between current input and the displayed result
*   `queue_size` — internal delay-line depth
*   `model_ready` — 1 once CoreML compilation is done
*   `depth_min` / `depth_max` — the current frame's raw disparity range

## Parameters

*   **Compute Units:** All / CPU+GPU / CPU+Neural Engine. Leave on **All**.
*   **Process Every N Frames:** skip inference frames to save power.
*   **Sync Frames:** extra delay on output 1 for manual alignment.
*   **Reload Model:** re-initialize CoreML.

## Credits & Licenses

*   Plugin code: MIT (see `LICENSE`).
*   Architecture adapted from [AppleVisionMask-TouchDesigner](https://github.com/aaronmylespereira/AppleVisionMask-TouchDesigner) by Aaron Myles Pereira (MIT).
*   Model: [Depth Anything V2 Small](https://huggingface.co/apple/coreml-depth-anything-v2-small), Apple's CoreML conversion — Apache 2.0. The build downloads and redistributes it inside the plugin bundle under that license.
*   `TOP_CPlusPlusBase.h` / `CPlusPlus_Common.h` are Derivative's TouchDesigner SDK headers, included as shipped with TouchDesigner's C++ samples.
