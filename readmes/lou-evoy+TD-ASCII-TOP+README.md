# ASCII TOP — edge-preserving real-time ASCII for TouchDesigner (CUDA)

A custom TOP that converts an image to ASCII glyphs each frame while **preserving edges**:
flat regions map to a luminance-ramped glyph set, while contours found by a
Difference-of-Gaussians pass are drawn with direction-matched line glyphs (`|` `-` `/` `\`),
so the picture keeps its structure instead of dissolving into a flat character grid. This is a port of [Acerola's ASCII shader](https://github.com/GarrettGunnell/AcerolaFX).

## Demo

https://github.com/user-attachments/assets/b5c1d711-c63d-4984-8341-c80409f5f8f5

## Why this one

- **Edge preservation.** A Difference-of-Gaussians + Sobel-direction pass lays line glyphs
  *along* the contours, so structure (faces, silhouettes, hard edges) survives instead of
  washing out the way brightness-only ASCII does.
- **Fused kernel.** The full pipeline runs in a single CUDA kernel — roughly one read and one
  write per pixel.
- **Adjustable** glyph set, cell density, and source-color tinting.

## Getting the node

The compiled plugin isn't distributed here — precompiled builds are available on **[Gumroad](https://louevoy.gumroad.com)**. To build it yourself, read on.

## Build it yourself

**Requirements:** TouchDesigner 2025.32050+, CUDA Toolkit 12.8+, Visual Studio 2022/2026 (Desktop development with C++), CMake 3.24+, and an NVIDIA GPU (Turing / RTX 20 or newer).

The TD C++ SDK headers (`TOP_CPlusPlusBase.h`, `CPlusPlus_Common.h`) aren't in this repo — they ship with TouchDesigner at `<TD install>/Samples/CPlusPlus/CudaTOP`. Point `-DTD_SDK_DIR` there if your install isn't the default below.

Run from the **x64 Native Tools Command Prompt for VS** (a normal shell won't have `cl`/`nvcc` on `PATH`):

```bat
cmake -S . -B build -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release ^
      -DTD_SDK_DIR="C:/Program Files/Derivative/TouchDesigner/Samples/CPlusPlus/CudaTOP"
cmake --build build
```

Copy the built `.dll` from `build\` to `%USERPROFILE%\Documents\Derivative\Plugins\` (or run `cmake --build build --target install_to_td`), restart TouchDesigner, and add the node via **OP Create → Custom → "ASCII"**.
