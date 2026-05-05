## Description

pico2-debug runs on the (typically dormant) second core of a RP2350 MCU and provides a USB CMSIS-DAP interface to debug the primary core.  No hardware is added; it is as if there were a virtual debug pod built-in.

Boot the RP2350 with the BOOTSEL button pressed, copy over pico2-debug.uf2, and it immediately reboots as a CMSIS-DAP adapter.  pico2-debug loads as a RAM only .uf2 image, meaning that it is never written to flash and doesn't replace existing user code.

If this sounds familiar, [pico-debug](https://github.com/majbthrd/pico-debug) does the same thing, but for the RP2040.

With **pico2-debug-gimmecache**, 504kBytes (~97% of total) of SRAM is available for running user code; pico2-debug gives plenty of elbow room by occupying only ~3% at the very top of SRAM and leaving the flash cache operational.

If viewing this on github, pre-built binaries are available for [download](https://github.com/majbthrd/pico2-debug/releases) on the right under "Releases".

## License

TinyUSB and code specific to pico2-debug is licensed under the [MIT license](https://opensource.org/licenses/MIT).

ARM's CMSIS_5 code is licensed under the [Apache 2.0 license](https://opensource.org/licenses/Apache-2.0).

