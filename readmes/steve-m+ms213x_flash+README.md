# MS213x/MS213xS firmware flasher
## Cross-platform firmware backup and update of MS2130-series USB HDMI grabbers

This tool allows to backup, update and verify the firmware of HDMI capture sticks based on MacroSilicon/Ultrasemi MS2130, MS2130S, MS2131 and MS2131S on Linux, OS X and Windows.

Some use-cases include:
- install a newer firmware (e.g. [fixing Windows 11 compatibility](https://hanx.jp/4kbasic_fw_updater_202503/))
- install a patched firmware improving performance (e.g. by [disabling sharpening](https://github.com/steve-m/ms2130_patcher))
- firmware for special purposes like [HyperHDR](https://github.com/awawa-dev/HyperHDR/discussions/729#discussioncomment-8126044)


## Usage

When run without arguments, it will automatically backup the currently installed firmware to a file with auto-generated name, containing the checksums and firmware build date (if present).

```console
$ ./ms213x_flash  
MS213x flasher for MacroSilicon/Ultrasemi MS2130, MS2130S, MS2131 and MS2131S USB 3 HDMI capture sticks
https://github.com/steve-m/ms213x_flash - version 0.10
run with -h for help/usage

Found MS2130S via libusb

Reading flash (98356 bytes)
100% [############################################################]

Backup saved to MS2130S_2025-10-29_backup_24dc_8256.bin
Done.
```

When provided with a filename as the argument (or on Windows by drag-and-dropping a *.bin file to the application), a backup of the currently installed firmware is generated, the new firmware is flashed and then verified.

```console
$ ./ms213x_flash MS2130S_2025-10-29_backup_24dc_8256.bin
MS213x flasher for MacroSilicon/Ultrasemi MS2130, MS2130S, MS2131 and MS2131S USB 3 HDMI capture sticks
https://github.com/steve-m/ms213x_flash - version 0.10
run with -h for help/usage

Found MS2130S via libusb
FW date: 2025-10-29
Checksums of firmware file are correct, creating backup of current firmware

Reading flash (98356 bytes)
100% [############################################################]

Backup saved to MS2130S_2025-10-29_backup_24dc_8256.bin
Erasing flash...

Writing flash (98356 bytes)
100% [############################################################]

Verifying flash (98356 bytes)
100% [############################################################]

Successfully written and verified flash
Done.
```

-h as argument prints the other command line options, which allow e.g. flashing without verification or reading the firmware to a custom filename.
```console
$ ./ms213x_flash -h

Usage:
        [-r <read filename>] read flash to file
        [-w <write filename>] write file to flash
        [-n] no verify, skip verification after flashing
        [-h] display this help
```

## Installation

### Linux
To install the build dependencies and build the tool on a distribution based on Debian (e.g. Ubuntu), run the following commands:
```console
sudo apt-get install build-essential cmake pkgconf libusb-1.0-0-dev libhidapi-hidraw0 libhidapi-dev
git clone https://github.com/steve-m/ms213x_flash.git
mkdir ms213x_flash/build && cd ms213x_flash/build
cmake ..
cmake --build .
```

### OS X

Tested on OS X with homebrew, build instructions will follow.

### Windows

Can be built on Windows with the MSYS2 CLANG64 environment, build instructions will follow. See the releases section for a pre-compiled version.

