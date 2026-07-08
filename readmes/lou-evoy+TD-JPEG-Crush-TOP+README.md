# JPEG Crush TOP — real-time JPEG artifact engine for TouchDesigner (CUDA)

A custom TOP that runs an actual JPEG/DCT codec on the input each frame — RGB→YCbCr,
forward DCT, quantization, inverse DCT — so the result is genuine compression artifacts
(8×8 block quantization, ringing, chroma bleed) rather than an imitation, with controls to
drive them well past a normal encoder.

## Demo

https://github.com/user-attachments/assets/018f9594-9398-4617-addc-0854d2b7a64a

## Why this one

- **A real codec, not a filter.** The artifacts come from actual coefficient-domain
  quantization, not a "JPEG-look" approximation.
- **Generation loss.** Recompresses the image repeatedly on a shifted block grid,
  accumulating the deep-fried / re-saved-to-death look.
- **Codec controls.** Variable transform block size (8/16/32), independent luma/chroma
  quantization, and chroma subsampling.

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

Copy the built `.dll` from `build\` to `%USERPROFILE%\Documents\Derivative\Plugins\` (or run `cmake --build build --target install_to_td`), restart TouchDesigner, and add the node via **OP Create → Custom → "JPEG Crush"**.
