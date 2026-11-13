# hwsvideo: one Linux driver for HWS PCIe capture cards (AVMatrix, ACASIS)

This driver, `hwsvideo`, runs the AVMatrix VC12-4K, VC41 and VC42, ACASIS's 4K, 1080p and AHD PCIe capture cards, and related cards. It replaces separate drivers built from the same code base: `HwsUHDX1Capture` ([AVMATRIX-VC12-4K-CAPTURE](https://github.com/GloriousEggroll/AVMATRIX-VC12-4K-CAPTURE)), `HwsCapture` ([AVMATRIX-VC41-VC42-CAPTURE](https://github.com/GloriousEggroll/AVMATRIX-VC41-VC42-CAPTURE)), and ACASIS's versions of those two plus `HwsAHDCapture`.

For each input, it gives you a V4L2 video device, which OBS and `v4l2-ctl` can open, and, except on the AHD cards, an ALSA sound card, which PipeWire and PulseAudio can record from. *n* counts the inputs from 1:

| Card | Inputs | Largest input | Video device | Sound card |
|---|---|---|---|---|
| VC12-4K, ACASIS 1-input 4K60 (VS2583) | 1 HDMI | 3840×2160 at 60 Hz, 1920×1080 at 240 Hz | **HUHDVideo *n*** | **HUHDAudio *n*** |
| VC41, VC42, ACASIS 1080p and relatives | 1, 2 or 4 | 1920×1080 at 60 Hz | **HVideo *n*** | **HAudio *n*** |
| ACASIS AHD | 2 or 4 analog cameras | 1920×1080 | **AVideo *n*** | None |

The names are the ones the separate drivers used.

The driver is not part of the Linux kernel. `install.sh` builds it with DKMS, which rebuilds it each time you install a new kernel.

## Supported hardware and systems

### Models

The driver recognises cards by PCI ID, and the vendors don't publish which ID is which model. These are the models the original drivers were released for:

| Vendor | Model | Inputs | Original driver |
|---|---|---|---|
| AVMatrix | VC12-4K | 1 HDMI | `HwsUHDX1Capture` |
| AVMatrix | VC41, VC42 | 1, 2 or 4 | `HwsCapture` |
| ACASIS | 1-channel 4K60 PCIe card | 1 | `HwsUHDX1Capture` |
| ACASIS | VS2583 4K60 PCIe card | 1 | `HwsUHDX1Capture` |
| ACASIS | 1080p PCIe cards, SDI and HDMI | 1, 2 or 4 | `HwsCapture` |
| ACASIS | 2- and 4-channel AHD cards | 2 or 4 analog cameras | `HwsAHDCapture` |

Other cards with these PCI IDs use the same code. Which code runs depends on the ID:

| Code path | PCI IDs (vendor:device) | Inputs |
|---|---|---|
| UHD | 8888:8581, 8888:85A1, 8888:8591, 1F33:8581 | 1 |
| HD | 8888:9534, 8888:8524, 1F33:8524, 1F33:6524, 1F33:8534, 1F33:8554, 1F33:8504, 8888:8504, 8888:6504 | 4 |
| HD | 8888:8532, 8888:8512, 1F33:6502 | 2 |
| HD | 8888:8501, 8888:8521 | 1 |
| HD, AHD cards | 8888:5504 | 4 |
| HD, AHD cards | 8888:5502 | 2 |

Most IDs need subsystem 8888:0007; the AHD IDs need 8888:0008. `lspci -nn -d 8888:` and `lspci -nn -d 1f33:` show yours. One PC can hold cards of different families.

- **Architecture:** x86-64 only.
- **Packages:** each [release](https://github.com/GloriousEggroll/HWS_VIDEO_CAPTURE_GENERIC/releases) has a package for Fedora 45 and 44, Debian 13 and 12, and Ubuntu 26.10 and 26.04.
- **Other builds:** `.github/workflows/build.yml` builds on every push against the newest Fedora, Arch, Ubuntu 24.04 (6.8) and 22.04 (5.15), Debian 12 (6.1), and CentOS Stream and AlmaLinux 9 (5.14) and 10 (6.12). The oldest kernel that builds is 5.14.

### Magewell cards

Magewell's Pro Capture cards aren't supported here. They are different from these cards to the driver; use Magewell's own `ProCapture` package. See [Magewell](docs/MERGE.md#magewell).

### The separate drivers

Once the new module has built, `install.sh` removes `HwsUHDX1Capture`, `HwsCapture` and `HwsAHDCapture`, whether from AVMatrix or ACASIS, because they claim the same cards. That includes the boot service and `/opt/HWS/ko` from ACASIS's Kylin installer. That includes kernels without headers, which have no capture driver until you install their headers and DKMS builds one. If one is still loaded, the installer tells you to reboot.

Options in `/etc/modprobe.d/hws.conf` use the module's name, so change an old `options HwsUHDX1Capture ...` or similar line to `options hwsvideo ...`. The installer warns you if it finds an old name.

### The kernel's own driver

Linux 7.2 and later include `hws`, a driver for the HD family's cards. Whichever of the two loads first gets the card. `install.sh` writes `/etc/modprobe.d/hwsvideo.conf`, which stops `hws` from loading, so this driver gets the card. To use the kernel's driver instead, run `./uninstall.sh` (or delete that file) and reboot.

## Install

### 1. Install the build tools and kernel headers

The headers must match the kernel you are running (`uname -r`).

| Distribution | Command |
|---|---|
| Fedora | `sudo dnf install dkms gcc make kernel-devel-$(uname -r)` |
| Ubuntu, Debian | `sudo apt update && sudo apt install dkms gcc make linux-headers-$(uname -r)` |
| Arch | `sudo pacman -Syu dkms gcc make linux-headers`, then reboot if the kernel was updated |

Desktop installs have the kernel's video and sound modules. Minimal kernels (cloud and some server installs) leave them out, and the driver then fails to load. The installer names the package to add.

### 2. Install the driver

**With a package, on Fedora, Debian or Ubuntu.** Download the file for your release from the [releases page](https://github.com/GloriousEggroll/HWS_VIDEO_CAPTURE_GENERIC/releases), then:

```sh
sudo dnf install ./hwsvideo-dkms-*.rpm    # Fedora
sudo apt install ./hwsvideo-dkms_*.deb    # Debian, Ubuntu
```

The package doesn't remove the old separate drivers. If it warns about one, remove it as it says.

**With the installer, on any distribution:**

```sh
git clone https://github.com/GloriousEggroll/HWS_VIDEO_CAPTURE_GENERIC.git
cd HWS_VIDEO_CAPTURE_GENERIC
./install.sh
```

`install.sh` asks for your password through `sudo`. It copies the sources to `/usr/src/hwsvideo-<version>`, builds the module for every installed kernel that has headers, removes the separate drivers, and loads the new one. If a build fails, it stops with the separate drivers still in place. It ends with one of these lines:

- `Loaded.` The driver is running.
- `The driver is already loaded. Reboot to use the version just installed (<version>).`
- `The old driver <name> is still loaded and has the card. Reboot to use hwsvideo.`
- `The in-kernel hws driver has the card. Reboot: ...` See [The kernel's own driver](#the-kernels-own-driver).
- `This kernel lacks modules the driver needs`, followed by the package to install.
- A Secure Boot message (see the next step).

**By hand:** see [Manual install](#manual-install).

### 3. Secure Boot: enrol the signing key once

With Secure Boot on, the kernel only loads modules signed by a key it trusts. DKMS signs this module with its own key, and `install.sh` prints the steps when that key isn't enrolled yet: run `sudo mokutil --import <key>`, choose a one-time password, reboot, then at the blue MOK manager screen choose "Enroll MOK", "Continue", "Yes", enter the password, and "Reboot".

### 4. Check it

```sh
v4l2-ctl --list-devices        # shows the video devices, one per input
arecord -l                     # shows the sound cards, one per input (none on AHD cards)
sudo dmesg | grep -i hws       # includes "UHD family, 1 input(s), FPGA version 122" or similar
modinfo -F version hwsvideo
```

## Manual install

Do these from the top of the source tree, after [step 1](#1-install-the-build-tools-and-kernel-headers). Remove any old separate driver first (`HwsUHDX1Capture`, `HwsCapture` or `HwsAHDCapture`), since they claim the same cards. On Linux 7.2 and later, also stop the kernel's own driver from taking the card:

```sh
echo "blacklist hws" | sudo tee /etc/modprobe.d/hwsvideo.conf
```

### With DKMS

DKMS rebuilds the module for each new kernel. It also signs the module for Secure Boot; see [step 3](#3-secure-boot-enrol-the-signing-key-once).

```sh
VER=$(sed -n 's/^PACKAGE_VERSION=//p' src/dkms.conf)
sudo mkdir -p /usr/src/hwsvideo-$VER
sudo cp src/*.c src/*.h src/Makefile src/dkms.conf /usr/src/hwsvideo-$VER/
sudo dkms add -m hwsvideo -v $VER
sudo dkms install -m hwsvideo -v $VER
sudo modprobe hwsvideo
```

To remove it: `sudo dkms remove -m hwsvideo -v $VER --all && sudo rm -rf /usr/src/hwsvideo-$VER`.

### Without DKMS

You have to repeat this after every kernel update. With Secure Boot on, you also have to sign the module yourself, or the kernel refuses it.

```sh
make -C src
sudo make -C src install
sudo depmod -a
sudo modprobe hwsvideo
make -C src clean
```

To remove it: `sudo modprobe -r hwsvideo`, delete `hwsvideo.ko*` from under `/lib/modules/$(uname -r)/`, and run `sudo depmod -a`. If `modprobe -r` hangs because PipeWire holds the sound device, reboot instead.

To try the module once without installing it, load what it depends on and then insert it:

```sh
make -C src
sudo modprobe -a videodev videobuf2-vmalloc videobuf2-dma-contig snd-pcm
sudo insmod src/hwsvideo.ko
```

## Use it in OBS

1. Add a **Video Capture Device (V4L2)** source and choose the input's video device.
2. Set **Resolution** to the input's size and **Video Format** to **YUYV 4:2:2**. Another size works too. The driver then scales on the CPU.
3. Set **Color Range** to **Full**. The cards deliver full-range video. With **Partial**, blacks look grey.
4. For sound, add an **Audio Input Capture** source and choose the input's sound card. To hear it, set the source's monitoring in **Advanced Audio Properties**.

If OBS lists the sound cards under unclear names, `tools/wireplumber-names.sh install` makes it show **HAudio *n*** and **HUHDAudio *n***. It needs WirePlumber 0.5 or later, and it restarts your audio services, which interrupts all audio for a moment. `tools/wireplumber-names.sh uninstall` undoes it, and so does `uninstall.sh`.

Several programs can capture from one input at the same time. They share one frame size: while one program is capturing, the others get its size. Each can choose its own frame rate.

## Upgrade

```sh
git pull
./uninstall.sh
./install.sh
```

With a package, install the new release's package instead. Then reboot, because `modprobe -r` can hang while PipeWire holds the card's sound device.

## Uninstall

```sh
./uninstall.sh
```

If you installed a package, remove that instead: `sudo dnf remove hwsvideo-dkms` or `sudo apt remove hwsvideo-dkms`.

`uninstall.sh` removes every version of this driver and of the separate drivers, including what their old installers left behind: the DKMS entries, the sources under `/usr/src`, `/usr/local/share/HWS`, the `/usr/bin/hws-*.sh` links, any of those modules under `/lib/modules`, ACASIS's Kylin service and `/opt/HWS/ko`, and the `hws` blacklist. It keeps `/etc/modprobe.d/hws.conf` if you made one. If the driver is loaded, it stays loaded until you reboot.

## Options

Set options in `/etc/modprobe.d/hws.conf`, for example:

```
options hwsvideo zero_copy=1
```

They take effect the next time the driver loads, so reboot after a change.

| Option | Default | What it does |
|---|---|---|
| `zero_copy` | off | VC12-4K only. The card writes each frame straight into the capturing program's buffers instead of the driver copying it there. At 3840×2160 this saves about 500 ms of CPU time per 600 frames. |
| `debug_dma` | off | Turns on DMA checks and debug files for driver development. Leave it off. |

`zero_copy` is used only when all of these hold. Otherwise the driver copies frames as usual and says why in the kernel log (`zero_copy is on but unavailable: ...`):

- the IOMMU translates addresses (the default on most systems; not with `iommu=pt` or with the IOMMU off);
- the card is a VC12-4K (`8888:8581`) with FPGA 122 or later;
- the kernel has `videobuf2-dma-contig` (RHEL 9 and its rebuilds don't);
- the program captures at the input's size with memory-mapped buffers, as OBS does.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| No video device | Run `lspci -nn -d 8888:` and `lspci -nn -d 1f33:`. If the card isn't listed, reseat it. If it is, run `sudo dmesg \| grep -i hws` and see the next rows. |
| The card is listed, but `/sys/bus/pci/drivers/hws/` has it | The kernel's own driver has it. Reboot after `install.sh`; see [The kernel's own driver](#the-kernels-own-driver). |
| `modprobe: ERROR: ... Key was rejected by service` | Secure Boot is on and the DKMS key isn't enrolled. Follow [step 3](#3-secure-boot-enrol-the-signing-key-once). |
| `Unknown symbol in module` | The kernel's video and sound modules are missing. See [step 1](#1-install-the-build-tools-and-kernel-headers). |
| `build failed` during install | The headers don't match the running kernel. Install the headers for `uname -r`, or reboot into the newest kernel. The full log is in `/var/lib/dkms/hwsvideo/<version>/build/make.log`. |
| A blue picture | The input sees no signal, or a mode the card doesn't take (the kernel log then says `unsupported input`). Check the cable and the source's output mode. |
| A black picture, and `HDCP active, delivering black frames` in the kernel log | The source protects its output with HDCP. The driver never passes protected video. Turn HDCP off on the source (for example a PS5's **HDCP** setting). |
| A short silence when the source changes resolution | Expected. The source stops sending audio while it changes mode, and the driver fills the gap with silence. |
| Colours look washed out in OBS | Set the source's **Color Range** to **Full**. |

## Limitations

| | VC12-4K, ACASIS 4K | VC41, VC42, ACASIS 1080p, AHD |
|---|---|---|
| Video format | YUYV 4:2:2 | YUYV 4:2:2; cards that capture YV12 or NV12 internally are converted on the CPU |
| Interlaced input | Line-doubled to progressive | Deinterlaced to progressive |
| Output sizes | The input's size, or one of 17 standard sizes from 720×480 to 4096×2160, scaled on the CPU | The input's size, or one of 13 standard sizes from 640×480 to 1920×1080 (AHD: 12, from 720×480), scaled on the CPU |
| Picture controls | Brightness, contrast, saturation | Brightness, contrast, saturation, hue |
| Colorimetry reported | Rec. 709, full range | BT.601, full range |

On every card with audio, it is 48 kHz, stereo, 16-bit per input. HDR and 10-bit video aren't supported, and HDCP-protected video is delivered as black frames. The line-in input some HD models have isn't supported.

## Known issues

- **VC12-4K capturing your own PC's GPU output.** When the card captures the same PC's graphics output, changing that output's resolution (or changing it shortly after the driver loads) has three times made an AMD Radeon RX 9070 drop off the PCIe bus and lock up the desktop. With the driver unloaded, or loaded but idle, 20 changes each ran cleanly; nothing found ties it to a driver defect. Consoles and other PCs as sources weren't affected. If you capture your own GPU, set its resolution before you start capturing and leave it.

## What's in this folder

- `install.sh`, `uninstall.sh`: install and remove the driver. `dkms-install.sh` runs `install.sh`.
- `CHANGELOG.md`: what changed. `SECURITY.md`: how to report a security problem.
- `src/`: the driver. `hws_video.c` holds nearly everything; `hws_scale.c` and `hws_convert.c` are the CPU scalers and pixel conversions; `hws_calc.h` holds pure calculations that the unit tests build in userspace.
- `packaging/`: the Fedora, Debian and Ubuntu packages. `.github/workflows/release.yml` builds them.
- `tests/`, `tools/`: test scripts and developer tools. `tests/zctest.sh`, `tests/modematrix.sh` and `tests/regprobe.py` are for the VC12-4K only. `make -C tests/unit check` needs no card.
- `docs/MERGE.md`: how the two drivers were combined and what to test. `docs/vc12-4k/` and `docs/vc41-vc42/` hold each driver's own development records, unchanged, so their module names and paths are the old ones.
- `doc/` and `play/` are AVMatrix's original material. Their install steps are out of date; follow this README instead.

## Where this driver comes from

`hwsvideo` is built from these drivers. All of them are published with `MODULE_LICENSE("GPL")`.

| Original driver | Source | Authors named in it |
|---|---|---|
| AVMatrix VC12-4K (`HwsUHDX1Capture`) | [AVMATRIX-VC12-4K-CAPTURE](https://github.com/GloriousEggroll/AVMATRIX-VC12-4K-CAPTURE), at `7a03be9`; originally from [avmatrix.com](https://avmatrix.com) | Alex Liu, Longtimetech |
| AVMatrix VC41/VC42 (`HwsCapture`) | [AVMATRIX-VC41-VC42-CAPTURE](https://github.com/GloriousEggroll/AVMATRIX-VC41-VC42-CAPTURE), at `95231a4`; originally from AVMatrix | AVMatrix (Sales) |
| ACASIS 1-channel 4K60 (`HwsUHDX1Capture`) | `PCIE_1CH_4K60_CAPTURE_CARD_DRIVER_FOR_LINUX.zip`, from [ACASIS](https://www.acasis.com) | Alex Liu, Longtimetech |
| ACASIS VS2583 4K60 (`HwsUHDX1Capture`) | `Linux_PCIE_VS2583_4K60Hz_20260324.zip`, from ACASIS | Alex Liu, Longtimetech |
| ACASIS 1080p (`HwsCapture`) | `1080P_PCIe_capture_card_drivers_for_Linux.zip`, from ACASIS | Alex Liu, Longtimetech |
| ACASIS AHD (`HwsAHDCapture`) | `2CH_4CH_AHD_capture_card_drivers_for_Linux.zip`, from ACASIS | Alex Liu, Longtimetech |

Work on the AVMatrix drivers after the vendor's release, from those repositories' histories:

- **GloriousEggroll (Thomas Crider):** ported the vendor drivers to newer kernels, added DKMS support, and published both repositories.
- **Blake Hoglo:** the 1.1.0 rework of both drivers: frame delivery, input information, the capture path, zero-copy, crash fixes, the installers, tests and most of the documents in `docs/`.
- **Matthew Hunter:** the kernel 7.0 fix for the video queue lock.
- **Grillo del Mal, Jacob Hall and PhoenixEmik:** other contributions to the VC12-4K driver.

[docs/MERGE.md](docs/MERGE.md) says what came from where. `docs/vc12-4k/` and `docs/vc41-vc42/` keep each AVMatrix driver's development records.

## Background and licence

The original README of the VC12-4K repository, by GloriousEggroll, who ported the vendor driver to newer kernels and added DKMS support:

> Preface:
>
> I am in no way affiliated with AVMATRIX.
>
> I bought this card on Amazon for around $250 because it has the same capabilities as the Magewell Pro Capture HDMI 4k LT, and I wanted to see if it held up in comparison. The Magewell card is a $900 card, as opposed to this one.
>
> Once I got the card, I found the standard ./install -did not work- on Fedora, and the code was slightly outdated for kernel 6.1. On top of that the drivers were being hosted on OneDrive.. which is sketchy.
>
> To add to that, since I also own the Magewell card already, I was able to do a driver comparison, and I found that this company had done a copy/paste of the Magewell driver install bash scripts and just modified them with their own driver sources.  This made porting over the DKMS functionality (and required kernel module signing) much easier!
>
> Therefore I updated their drivers for them, pointed out all the things wrong, and sent them an e-mail about it. In the meantime, here is the full driver source, which is has been updated and working on Fedora 37 as of Kernel 6.2.

The license for this project is GPL, as both the AVMATRIX driver -AND- the Magewell driver use GPL:

AVMATRIX:
```
$ grep -rni . -e license
./src/hws_video.c:5794:MODULE_LICENSE("GPL");
```

Magewell:
```
$ grep -rni . -e license
./src/sources/avstream/capture.c:611:MODULE_LICENSE("GPL");
```
