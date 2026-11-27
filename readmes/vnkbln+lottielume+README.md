# Lottie for Resolume

GPU Lottie sources for Resolume: **Lottie Player** and **Lottie Emitter**.

![Lottie Player running in Resolume Arena](assets/preview.png)

**1.0.0-beta.1** — first public Windows beta.

## Features

- Transparent vector animations rendered at output resolution.
- Native Position Timeline/BPM Sync for Player: slow playback, loops and scrubbing.
- Overlapping Emitter instances with source, speed, opacity, transforms and palette captured at spawn.
- Audio/MIDI mapping through Resolume.
- Integrated folder playlists with Random, Previous/Next and Next on Start.
- Four native color controls for prepared shapes, gradients and supported AE Fill effects.
- Vector transforms before rasterization; Fit, Fill, Stretch and Original modes.
- Embedded square LottieLogo demo: works without selecting a file.

Vector geometry stays sharp when enlarged; raster images retain their pixel resolution. Performance depends on content, effects, output size and overlapping instances.

## Install

Download the Windows plugin ZIP from [Releases](https://github.com/vnkbln/lottielume/releases).

1. Close Resolume. Extract LottiePlayer.dll and LottieEmitter.dll to a dedicated folder.
2. Add it in Preferences → Video → FFGL Plugin Directories and restart Resolume.
3. Find Lottie Player and Lottie Emitter in Sources.

Requires Windows x64 and OpenGL 4.1. Native-host testing used **Arena 7.29**; other versions are not comprehensively tested. For missing runtime components, install Microsoft's [Visual C++ v14 x64 runtime](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist).

ThorVG, codecs and expressions are linked into the two DLLs. Do not install the development CPU fallback alongside GPU Player: both use LT01. Remove the retired standalone Playlist prototype if installed.

## Usage

**Player:** select JSON in File or use the demo. Change Position from Basic to Timeline or BPM Sync in Resolume; save a preset. The plugin cannot select this mode automatically. Timeline duration is configured in Resolume, not matched automatically to each JSON.

**Playlist:** uses the selected file's folder. Random changes order; Next on Start advances on activation. Previous/Next navigate and request Player Position reset. One-file/demo navigation restarts it. File shows the current selection.

**Emitter:** Spawn starts an independent instance. Spawn Options contains Speed, Opacity, Max Instances, Spawn on Start and Clear. Each spawn captures its source and settings; later changes affect new instances. Opacity multiplies authored transparency. Spawn on Change optionally spawns on navigation. Disconnect clears instances; Connect optionally spawns.

**Lottie Transform:** transforms vector content before rasterization. Crop to Canvas defaults off. When enabled it constrains content to the fitted canvas; Emitter moves content inside that fixed boundary. Original centers the authored canvas at its pixel size.

**Lottie Colors:** replaces authored RGB colors #f318e8, #9c32fe, #277ff4 and #00f3e9. Black, white and other colors remain unchanged. Raster pixels are not recolored. See [palette preparation](docs/COLORS.md).

## Centerline

[130 animations](assets/packs/Centerline_v01/README.md), 13 thematic folders with 10 files each: 40 Shapes (4s), 60 One_Shot (2s), 30 BG (8s). Transparent 1000×1000 canvas, 60fps. Adjust fit/crop for your output aspect; vectors render at target resolution.

## Beta limitations

- Windows x64 and JSON only. No .lottie, themes, state machines, macOS.
- ThorVG implements a subset of AE/Bodymovin. Test complex masks, effects, expressions and fonts. AE Stroke effect recoloring is not implemented.
- External resources must remain accessible relative to JSON. Selecting the same JSON again reloads it and resources; Reload is hidden.
- Extreme slow motion can reveal spatial Bezier interpolation limits. Arbitrary exports are not guaranteed smooth at every speed.
- No universal FPS guarantee. Back up compositions/presets from private builds: schemas changed during development.

## Development and licenses

[Build](BUILD.md) · [Tests](TESTING.md) · [Architecture](ARCHITECTURE.md) · [Roadmap](ROADMAP.md) · [Release](RELEASE.md).

Code/scripts/docs: **MIT**. Centerline: **CC BY 4.0**, credit **vnkbln**. Commercial use is permitted. See [ATTRIBUTION](ATTRIBUTION.md), [LICENSE](LICENSE), [LICENSE-ASSETS](LICENSE-ASSETS), [third-party notices](third_party/README.md).

Guides: [Player timing](docs/TIMELINE.md) · [Emitter](docs/EMITTER.md) · [Playlists](docs/PLAYLIST.md) · [Transforms](docs/TRANSFORMS.md) · [Resources](docs/RESOURCES.md) · [GPU rendering](docs/GPU.md).
