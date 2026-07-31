# Syphon Server OBS Plugin

A high-performance macOS OBS plugin that provides a video filter to output frames to a Syphon server. This allows for seamless video sharing between OBS and other macOS applications like Resolume, MadMapper, or custom creative coding tools.

## Overview

The **Syphon Server Plugin** acts as a "bridge" out of OBS. Unlike the built-in Syphon *source* in OBS (which brings video in), this plugin provides a *filter* that sends video **out**. 

It is designed for modern macOS workflows, utilizing the **Metal** API and the **Accelerate** framework for efficient, low-latency video processing and scaling.

### Key Features
- **Flexible Output**: Send video from any specific source, scene, or nested group.
- **On-the-fly Scaling**: Automatically resize frames to a target width (default 256px) while maintaining aspect ratio.
- **Metal Backend**: Uses `SyphonMetalServer` for compatibility with modern OBS (v28+) and Apple Silicon.
- **High-Quality Resampling**: Uses the `vImage` library for professional-grade scaling.
- **Broad Format Support**: Handles common OBS formats including NV12, I420, UYVY, BGRA, and RGBA.

## How to Use

### Installation
1. Navigate to the plugin directory:
   ```bash
   cd syphon-server-plugin
   ```
2. Run the build and deploy script:
   ```bash
   ./build_and_deploy.sh
   ```
   *Note: This script will build the plugin, bundle dependencies, fix library paths, and copy it to your OBS plugins directory (`~/Library/Application Support/obs-studio/plugins`).*

### Configuration in OBS
1. Open OBS and right-click on any **Source** or **Scene**.
2. Select **Filters**.
3. Click the **+** button under **Video Filters** and select **Syphon Server Output**.
4. **Channel Name**: Enter the name you want other apps to see (e.g., "My OBS Feed").
5. **Scale Width**: Enter the desired output width in pixels. The height will be calculated automatically.

## Technical Details

### Architecture
The plugin follows the standard OBS video filter architecture but bridges into the macOS native environment:
- **Frontend (C++)**: Handles OBS module registration, UI properties, and the filter lifecycle.
- **Backend (Objective-C++)**: Interfaces with macOS-specific frameworks (`Metal`, `Syphon`, `CoreVideo`).

### Processing Pipeline
1. **Frame Capture**: Receives `obs_source_frame` from the OBS filter pipeline.
2. **Color Space Conversion**: 
   - YUV formats (**NV12**, **I420**, **UYVY**) are converted to RGB using hardware-accelerated `vImage` functions.
   - Channel permutation ensures the correct Red/Blue order for Metal.
3. **Scaling**: The frame is scaled to the target width using `vImageScale_ARGB8888` with high-quality resampling.
4. **Texture Upload**: The processed CPU data is uploaded to an `MTLTexture`.
5. **Syphon Publication**: The texture is published to the `SyphonMetalServer`. Orientation is corrected (`flipped:YES`) to match the standard expectation of Syphon clients.

## Developer Overview

### Project Structure
- `src/syphon-server-plugin.cpp`: OBS Boilerplate and UI logic.
- `src/SyphonProcessor.h`: C++ interface for the Syphon processor.
- `src/SyphonProcessor.mm`: Objective-C++ implementation of the Metal/Syphon logic.
- `CMakeLists.txt`: Build configuration, handles framework linking.
- `build_and_deploy.sh`: Deployment automation script.

### Dependencies
- **libobs**: The OBS Studio core library.
- **Syphon.framework**: Bundled within the plugin.
- **System Frameworks**: Metal, Accelerate, CoreVideo, Foundation, QuartzCore.

### Building Manually
If you prefer not to use the deploy script, you can build using standard CMake:
```bash
mkdir build && cd build
cmake ..
make
```

### Known Considerations
- **Format Support**: Optimized for BGRA, RGBA, NV12, I420, and UYVY.
- **Performance**: While highly optimized, scaling very large frames (e.g., 4K) to small sizes on the CPU still incurs some overhead.
- **Orientation**: Standardized to `flipped:YES` to accommodate common Syphon client expectations.
