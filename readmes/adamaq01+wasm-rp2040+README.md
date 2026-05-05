# WebAssembly on RP2040 with Rust

Simple example of running WebAssembly on the Raspberry Pi Pico (RP2040) using Rust and wasm-bindgen.

## Prerequisites

- [Rust](https://www.rust-lang.org/tools/install)
- [wasm-bindgen](https://github.com/rustwasm/wasm-bindgen)
- [binaryen](https://github.com/webassembly/binaryen)

## Build

```bash
./build_wasm.sh
cmake -B build
cmake --build build
```

This will generate a wasm-rp2040.uf2 file in the build directory that can be copied to the RP2040.