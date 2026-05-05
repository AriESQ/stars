# rp2350-minimal-riscv

As in my rp2350-minimal repository, we refer to RP2350's datasheet as [rp2350]. It can be found at <https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf>.

The present repository is a twin to the [rp2350-minimal](https://github.com/mtkos/rp2350-minimal) repository. It contains the same programs, but adapted to run on the RISC-V cores. The only exception is the `systick` program. SysTick is an ARM
peripheral, not present on RP2350's RISC-V cores. Instead, there is the RISC-V platform timer, see [rp2350], section 3.1.8, which can be used for similar purposes. The program is still called
`systick`, although it is very different from the ARM version.

## Prerequisites

Compiler `riscv64-unknown-elf-gcc` is needed.

* Debian/Ubuntu: install package `gcc-riscv64-unknown-elf`.

### Minimum GCC version

Probably the minimum GCC version to build a code for RP2350 is 12.2, see [raspberrypi/pico-bootrom-rp2350#Getting a RISC-V compiler](https://github.com/raspberrypi/pico-bootrom-rp2350/blob/master/README.md#getting-a-risc-v-compiler):
> Not all the fancy instructions supported by Hazard3 will be in the compilers in people's package managers right now (and we do want to use them here since the bitmanip instructions improve code density). At time of writing the master branch of `riscv-gnu-toolchain` is GCC 12, which does support the bit manipulation instructions.
>
> The following compiler is known to be correct: `corev-openhw-gcc-ubuntu2204-20240114`. Others may or may not; because space is very tight, slight compiler variations can cause code not to fit.

## How to use

Navigate into a needed folder (for example, with `cd …` command), then run `make all` to build binaries.

Flashing: copy `*.uf2` file into the Raspberry PI pico2 volume.

[rp2350]: https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf
