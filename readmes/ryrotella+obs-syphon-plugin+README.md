# obs-syphon

A macOS plugin for OBS Studio that sends video to other applications via [Syphon](https://github.com/Syphon/Syphon-Framework). Share your OBS output with TouchDesigner, Resolume, MadMapper, VDMX, or any Syphon-compatible application in real time over IOSurface — zero-copy on the GPU path.

## Features

- **Syphon Output** — broadcasts the full OBS program canvas as a Syphon server (accessible from the Tools menu)
- **Syphon Filter** — attach to any individual source to share just that source's video
- **Native settings panel** — configure server name, auto-start, and vertical flip from an AppKit UI (no Qt dependency)
- **GPU and CPU paths** — the filter uses `gs_copy_texture` for zero-copy GPU sharing; the output uses a raw video callback for backend-agnostic compatibility
- **Universal binary** — builds for both Apple Silicon (arm64) and Intel (x86_64)

## Install via Homebrew

```bash
brew tap ryrotella/obs-syphon-plugin https://github.com/ryrotella/obs-syphon-plugin
brew install obs-syphon
```

This requires OBS Studio to be installed (`brew install --cask obs` if needed). The plugin is symlinked into the OBS plugins directory automatically. Restart OBS to load it.

## Requirements

- macOS 12.0+
- [OBS Studio](https://obsproject.com/) installed at `/Applications/OBS.app`
- CMake 3.28+
- [Syphon.framework](https://github.com/Syphon/Syphon-Framework) (can be copied from OBS.app or built from source)
- [simde](https://github.com/simd-everywhere/simde) — install via `brew install simde`

## Building

```bash
# Clone the repo
git clone https://github.com/ryrotella/obs-syphon-plugin.git
cd obs-syphon-plugin

# Fetch OBS source headers (needed for the local-deps fallback)
cd deps
git clone --depth 1 --branch 32.1.1 https://github.com/obsproject/obs-studio.git obs-studio-src
cd ..

# Place Syphon.framework in deps/ (if not already present)
# Option A: copy from OBS.app
cp -R /Applications/OBS.app/Contents/Frameworks/Syphon.framework deps/
# Option B: build from source (see https://github.com/Syphon/Syphon-Framework)

# Build
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

## Installing

```bash
cmake --install build
```

This copies `obs-syphon.plugin` to `~/Library/Application Support/obs-studio/plugins/`. Restart OBS to load the plugin.

## Usage

### Syphon Output (full canvas)

1. In OBS, go to **Tools > Syphon Output**
2. Set a server name (default: "OBS Studio")
3. Optionally enable **Start automatically when OBS launches**
4. Click **Start**

The full program output is now available as a Syphon source in any receiving application.

### Syphon Filter (per-source)

1. Right-click a source in OBS and select **Filters**
2. Click **+** under Effect Filters and add **Syphon Output**
3. Optionally set a custom server name (defaults to the source name)
4. The filter broadcasts whenever the source is visible in the active scene

## Project Structure

```
src/
  plugin-main.m          Entry point — registers output, filter, and Tools menu item
  syphon-obs-server.h/m  SyphonServerBase subclass bridging OBS textures to IOSurface
  syphon-output.m        Output type — sends full OBS canvas via Syphon (CPU path)
  syphon-filter.m        Filter type — sends individual source via Syphon (GPU path)
  syphon-settings.m      Native AppKit settings panel
  plugin-support.h       Version defines and logging macro
data/
  locale/en-US.ini       UI strings
deps/
  Syphon.framework/      Syphon framework (not checked in)
```

## License

GPL-2.0-or-later. See source file headers for details.

Copyright (C) 2024-2026 Ryan Rotella
