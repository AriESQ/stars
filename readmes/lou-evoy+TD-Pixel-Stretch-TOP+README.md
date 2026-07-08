# Pixel Stretch TOP — real-time GPU pixel stretch for TouchDesigner (CUDA)

A custom TOP that propagates the last surviving pixel's color across the parts of each
scanline removed by a threshold. The node allows for an optional fade-to-black and adjustable stretch length.

## Demo

https://github.com/user-attachments/assets/86fc6a35-1e2b-4fd0-95af-2d21d4f01ae9

## Why this one

- **No sort.** The effect is a single segmented inclusive scan over the frame — that's what
  keeps it cheap.
- **Allocate-once, zero-copy**, with built-in fade-to-black and stretch-length controls.

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

Copy the built `.dll` from `build\` to `%USERPROFILE%\Documents\Derivative\Plugins\` (or run `cmake --build build --target install_to_td`), restart TouchDesigner, and add the node via **OP Create → Custom → "Pixel Stretch"**.
