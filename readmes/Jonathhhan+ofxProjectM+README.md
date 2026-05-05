# ofxProjectM

`ofxProjectM` wraps `projectM 4` for openFrameworks and focuses on Milkdrop-style visual playback, texture output, playlist control, runtime parameter control, logging, touch input, and sprites.

The addon is especially useful as a companion addon for `ofxVlc4`.

There is no longer a maintained app example inside this repository. The recommended real integration example now lives in:

- [../ofxVlc4/ofxVlc4Example](../ofxVlc4/ofxVlc4Example)
  - full `ofxVlc4` + `ofxProjectM` GUI with playlist, video preview, `projectM` preview/display windows, and runtime diagnostics

## Note

Parts of this addon, its examples, and its documentation were developed with AI-assisted help during implementation and refinement.

## Release

- addon release version: `1.0.2`
- changelog: `CHANGELOG.md`

## Highlights

- `projectM 4` playback in openFrameworks
- internal FBO/texture output
- preset playlist and preset switching helpers
- runtime parameters:
  - FPS
  - mesh size
  - frame time
  - beat sensitivity
  - cut settings
  - texel offset
  - easter egg
  - preset start clean
- texture search path control
- runtime logging callback + log level
- touch API
- user sprites
- version info helpers

## Version helpers

There are now two different version concepts available:

- addon version
  - `ofxProjectM::getAddonVersionInfo()`
- wrapped runtime version
  - `ofxProjectM::getVersionInfo()`
  - reports the linked `projectM` runtime version and VCS string

## Source layout

The public facade stays in:

- `src/ofxProjectM.h`

Implementation is split into:

- `src/ofxProjectM.cpp`
  - core lifecycle, logging, shared callbacks, runtime parameters
- `src/ofxProjectMPlaylist.cpp`
  - playlist, preset loading, switching, filtering
- `src/ofxProjectMRender.cpp`
  - FBO/texture rendering, audio input, touch, sprites

Small internal helper headers:

- `src/ofxProjectMPlaylist.h`
- `src/ofxProjectMRender.h`

## Building projectM libraries

The unified shell script clones and builds `projectM` in a temporary directory outside the addon tree, then copies only the finished libraries and headers back into `libs/projectM`.

The repository keeps `libs/projectM` as placeholder directories only. Run the build script after cloning if you want the local static libraries and headers populated.

If you want one entry point across platforms, use:

```bash
bash scripts/build_projectm.sh
```

The wrapper dispatches to:

- macOS: native static build into `libs/projectM/lib/osx`
- Linux: native static build into `libs/projectM/lib/linux64`
- Git Bash / MSYS / Cygwin on Windows: embedded PowerShell build into `libs/projectM/lib/vs`
- WSL: auto-detected as Windows by default so a Windows checkout still fills `libs/projectM/lib/vs`

### Windows

Run:

```bash
bash scripts/build_projectm.sh
```

This builds both `Debug` and `Release` by default on Windows.
WSL now follows this Windows path automatically unless you override it.
If you only want one configuration, use for example:

```bash
bash scripts/build_projectm.sh --configuration Release
```

Outputs:

- `libs/projectM/lib/vs/Debug/libprojectM-4.lib`
- `libs/projectM/lib/vs/Debug/libprojectM-4-playlist.lib`
- `libs/projectM/lib/vs/Release/libprojectM-4.lib`
- `libs/projectM/lib/vs/Release/libprojectM-4-playlist.lib`
- `libs/projectM/include/projectM-4`

## VLC-backed integration

For the maintained `ofxVlc4` + `projectM` app example, use:

- [../ofxVlc4/ofxVlc4Example](../ofxVlc4/ofxVlc4Example)

That example owns the runnable `libVLC` + `projectM` integration story now.

### macOS

Run:

```bash
bash scripts/build_projectm.sh
```

Outputs:

- `libs/projectM/lib/osx/libprojectM-4.a`
- `libs/projectM/lib/osx/libprojectM-4-playlist.a`
- `libs/projectM/include/projectM-4`

By default the script asks CMake for a universal `arm64;x86_64` build. You can override that before the run, for example:

```bash
OSX_ARCHITECTURES=arm64 bash scripts/build_projectm.sh
```

### Linux / WSL

Run:

```bash
bash scripts/build_projectm.sh
```

Outputs:

- `libs/projectM/lib/linux64/libprojectM-4.a`
- `libs/projectM/lib/linux64/libprojectM-4-playlist.a`
- `libs/projectM/include/projectM-4`

If you are running inside WSL and want Linux artifacts instead of the default Windows/Visual Studio path, use:

```bash
bash scripts/build_projectm.sh --target linux
```

## Runtime assets

Preset and texture packs are now documented and downloaded from the maintained integration example:

- [../ofxVlc4/ofxVlc4Example/README.md](../ofxVlc4/ofxVlc4Example/README.md)

## Notes

- The addon uses one public `ofxProjectM` facade even though implementation is now split internally.
- The source split does not require `addon_config.mk` updates because openFrameworks auto-scans `src`.
- The full `ofxVlc4Example` exposes part of the `projectM` surface, but the addon API is broader than the current GUI.
- The maintained app-level example now lives in `ofxVlc4Example`, not in this repository.



