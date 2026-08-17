# Mosh TOP

Real-time datamoshing and motion-vector glitch as a custom TOP for TouchDesigner.

Mosh TOP ingests any TOP, re-encodes it on the fly to a P-frame-bearing codec, and
lets you corrupt, drop, duplicate, and smooth the compressed bitstream in real
time - then decodes the result back to RGBA. The glitches are authentic codec
artifacts, not pixel-domain imitations.

By **Philosophical Tools** (Eric Souther).

## Features

- **Mosh modes** - I-Frame Drop, P-Frame Duplicate, Bit-Flip Corruption, and a
  Motion-Vector warp driven by the decoder's exported motion vectors.
- **Bloom** - cache-and-replay bloom that sustains one motion direction across a
  streak, with burst and refresh controls.
- **Live Bloom Scrub** - a rolling compressed P-frame timeline for streaming
  sources. Scrub from the oldest stored packet to live, then press Bloom Pulse
  to reinject that exact packet into the current decoder reference. Repeated
  pulses at the same position reapply the same real motion/residual data. With
  Bloom Active off it is a bounded one-shot; with Bloom Active on it reseeds
  the continuous bloom.
- **Fluid Motion** - authentic encoder source-prep across all eight
  inter-frame codecs.
  MPEG-4 and Snow gain 4MV + quarter-pel, FLV1 gains 4MV, and the MPEGVideo
  family gains `forcemv`, `nopimb`, and strict-GOP motion so bloom moves across
  the full frame instead of jumping in 16x16 blocks.
- **Bitstream Motion Lab** (MPEG-1/2/4) - edits vectors *inside* the compressed
  bitstream via ffglitch transplication, so the decoder itself produces the
  melt. Motion can come from the packet's own source, input 1, input 2, the
  opposite input, or **Motion Paint**: a third TOP input sampled at macroblock
  centers whose red/green channels are written directly into the real vector
  syntax. The field can then be smoothed, uniformly zoomed, rotated, drifted,
  quantized, or frozen as absolute vectors or predictor deltas. Two parse-only
  source taps keep the input-1/2 motion carriers paired to the correct video
  frame. Only macroblocks whose syntax already codes writable vectors are ever
  painted; nothing synthetic is invented.
- **Edit Mask** (input 3) - one spatial gate over **both** bitstream labs.
  Only the macroblocks and blocks whose control-input luma passes the
  threshold receive syntax edits; everywhere else the encoder's original coded
  values survive byte-for-byte. Density stays meaningful because it is
  measured against the masked-in syntax rather than the whole frame. Paint
  where the melt, the texture corruption, or the macroblock shuffle happens
  with a Ramp, a Circle, optical flow, or a tracker. (Quantizer tables are
  global syntax and ignore the mask.)
- **Bitstream Texture Lab** (MPEG-1/2 + MJPEG, plus Macroblock Shuffle on
  MPEG-4) - rewrites real quantized DCT coefficients, DC values, quantizers,
  or coefficient blocks. MPEG-1/2 expose the complete lab. MJPEG exposes
  coefficients, coefficient deltas, embedded quantization tables, and DCT
  Block Repeat. Adaptive safety backs off aggressive rewrites or passes the
  original compressed packet when a damaged packet cannot be decoded; it never
  substitutes a synthetic pixel effect.
- **Macroblock Shuffle** (MPEG-1/2/4) - reorders whole coded macroblocks
  inside the compressed packet using FFglitch's per-macroblock bytestream
  syntax. Blocks are swapped rather than duplicated, and each one carries its
  coded bit size with it so the rewritten packet stays aligned; skipped
  macroblocks stay put, so nothing is invented. Density sets how much of the
  frame participates and Block Shift sets the distance in macroblocks.
- **Sub-pixel MV warp** - bilinear, spatially/temporally smoothed motion-vector
  warp for Motion Vector mode, regression-tested across all eight inter-frame
  codecs.
- **Pixel Sort** - luma-run databending pass (rows / columns / both), inspired
  by ASDFPixelSort.
- **Chroma boost**, and a **dual-input splice** with Source Mix (true A/B
  endpoints), Chimera Mix (both encoded streams persist in the same frame),
  Hard Cut (instant packet-source toggle while the incoming motion field moves
  the outgoing source's carried pixels), clocked Round-Robin, and protected
  GOP-Aligned recovery. A slow Pixel Source Refresh periodically admits the
  selected encoder's next real keyframe so carried pixels can reveal the live
  source without rebuilding the operator or crossfading decoded images.
- **Snow Codec Lab** - real native Snow reference-memory, wavelet, motion-search,
  and inter-persistence controls. Both platform encoders use a pinned
  entropy-context reset patch so packet replay, source splicing, and bit
  corruption can recover on later frames instead of blacking out the stream.
- **Nine intermediate codecs** - MPEG-2, MPEG-4, WMV1, WMV2, MPEG-1, FLV1,
  MS-MPEG-4 v3, experimental Snow, and intra-only MJPEG - each with its own
  glitch personality.
- **Real-time worker path** - GPU downloads, codec work, and optional image
  passes stay off TouchDesigner's cook thread; latest-frame mailboxes, recycled
  RGBA storage, shared bitstream edit passes, and a persistent task pool keep
  latency and allocation bounded.

## Codec capability map

| Codec | Fluid / decoded MV | Bitstream Motion | Bitstream Texture |
|---|---:|---:|---:|
| MPEG-1, MPEG-2 | Yes | Full | Full + Macroblock Shuffle |
| MPEG-4 | Yes | Full | Macroblock Shuffle |
| WMV1, WMV2, FLV1, MS MPEG-4 v3 | Yes | - | - |
| Snow | Yes + native Snow controls | - | - |
| MJPEG | Intra-only | - | Coefficients, coefficient deltas, quantizer tables, DCT Block Repeat |

Unavailable cells are passed through with a visible warning. The pinned
FFglitch build does not expose safe editable motion syntax for those codecs.
MJPEG has no predictive frames, so Bloom and motion-carry modes cannot exist in
their normal form; Bloom and Live Bloom Scrub are disabled instead of being
visually simulated. In Motion Vector mode, MJPEG therefore continues to show
its live decoded frames (and any real Texture-Lab edits) instead of holding the
first frame.

WMV2 keeps its full-strength historical smear at Intensity 1. Below that,
Motion Vector magnitude ramps with Intensity, low Bit-Flip settings leave a
fraction of the real packets clean, and Bloom progressively admits authentic
WMV2 recovery frames. This exposes more of the inputs at the gentle end without
crossfading or substituting a simulated glitch.

## Requirements

- TouchDesigner 2025 or newer
- macOS 11+ on Apple Silicon (arm64), **or** Windows 10/11 (x64)

## Install

**macOS** - download the `.pkg` from [Releases](https://github.com/ericsouther-source/mosh-top/releases) and open it. It
installs `MoshTOP.plugin` into your user TouchDesigner Plugins folder - no admin
password. It is unsigned, so the first open may need a right-click -> **Open**.

**Windows** - download the `.exe` installer from
[Releases](https://github.com/ericsouther-source/mosh-top/releases) and run it.
The wizard shows the license, then installs the plugin and an uninstaller. It is
unsigned, so SmartScreen may warn once: choose **More info** -> **Run anyway**.

Restart TouchDesigner, then press **Tab** -> **Custom** category -> drop a **Mosh**.
Wire any TOP into the input.

## Build from source

Prebuilt ffglitch/FFmpeg static libraries are included under `third_party/`, so a
normal checkout builds without compiling FFmpeg.

The pinned upstream source identity, archive checksums, and reproducible library
build scripts live in `third_party/ffglitch.lock`, `third_party/SHA256SUMS`, and
`build/build_ffglitch_{mac,}.sh`.

The CTest suite exercises decoder priming/reset, authentic Bloom and Bit-Flip
corruption across all eight inter-frame codecs (including dual-source Snow),
dual-input routing, MPEG-1/2/4 motion carriers in absolute and predictor-delta
syntax, MPEG-1/2 texture edits, MJPEG coefficient/quantizer-table edits,
historical Bloom packet reinjection across every inter-frame codec,
motion-vector export, dependency hash/license consistency, release inputs, and
the final three-symbol macOS plugin ABI:

```bash
ctest --test-dir build-mac --output-on-failure
```

**macOS (arm64):**

```bash
cmake -S . -B build-mac -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build build-mac --config Release
```

This produces `build-mac/MoshTOP.plugin`. Copy it to a TouchDesigner Plugins
folder, or opt into the post-build copy with `-DPT_AUTO_INSTALL=ON`. Build a
distributable installer with `./installer/build_installer.sh`.

**Windows:** open `vs2022/MoshTOP.sln` in Visual Studio 2022 and build
Release / x64.

## License

- The plugin wrapper (`src/`, build files, installer, packaging) - **MIT**
  (see [`LICENSE`](LICENSE)).
- The macOS libraries are **LGPL 2.1+**. The checked-in Windows archives were
  configured with GPL/version-3 features, so the combined Windows binary is
  **GPL v3 or later**. See [`SOURCES.md`](SOURCES.md) for the verified flags,
  hashes, and corresponding-source details.

## Credits

Built on [**ffglitch-core**](https://github.com/ramiropolla/ffglitch-core) by
Ramiro Polla - the motion-vector editing and bitstream transplication that make
the authentic glitches possible. FFmpeg © the FFmpeg developers.

This software uses libraries from the [FFmpeg](https://ffmpeg.org) project
(via the ffglitch-core fork) under the LGPLv2.1 on macOS and the GPLv3 on
Windows. FFmpeg is a trademark of Fabrice Bellard, originator of the FFmpeg
project. This project is not endorsed by or affiliated with the FFmpeg or
FFglitch projects.

Pixel sorting is an independent implementation inspired by
[ASDFPixelSort](https://github.com/kimasendorf/ASDFPixelSort) by Kim Asendorf.
The bloom mechanism was re-implemented in real-time C++ from techniques
documented in [Datamosher Pro](https://github.com/Akascape/Datamosher-Pro) by
Akash Bora and `tomato.py` by Kaspar Ravel. No code from those projects is
included or distributed here.
