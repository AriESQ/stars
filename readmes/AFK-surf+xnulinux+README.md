# xnulinux

Run macOS userspace on Linux by loading the macOS kernel into it.

xnulinux builds XNU, the open-source kernel of macOS, from Apple's published sources and runs it as a loadable kernel
module (`xnu.ko`) inside an unmodified arm64 Linux kernel. The hosted XNU drives the CPU and MMU directly, so macOS
processes run natively next to Linux processes on the same CPUs, with no hypervisor between them. Linux lends XNU its
memory, timers, files, network and GPU through a small interface module (`fki.ko`).

With a stock Ubuntu kernel, `insmod xnu.ko` boots a macOS 27 system disk made by Apple's own installer to the
desktop: loginwindow, WindowServer, Dock, Finder, Safari and Chrome.

![macOS and Linux userspace side by side](docs/images/macos-and-linux.jpg)

*One system, two userspaces. Left: a Terminal in the hosted macOS 27.2.1 (`sw_vers`, the Darwin kernel, launchd,
WindowServer, Dock and Finder running). Right: from that macOS, an SSH session into the Linux it runs inside (Ubuntu,
Linux 7.0, the `xnu` and `fki` modules loaded, and the `insmod xnu.ko` process the macOS kernel runs in).
Straight from the hosted framebuffer, 1280×800.*

![The hosted macOS desktop](docs/images/desktop.jpg)

*The hosted desktop at the end of a 30-minute stress run, rendered on the CPU (no GPU bridge).*

| | |
|---|---|
| ![Safari on Wikipedia's XNU article](docs/images/safari-xnu.jpg) | ![Safari on kernel.org](docs/images/safari-kernel-org.jpg) |
| ![Safari on GitHub](docs/images/safari-github.jpg) | |

*Safari in the hosted macOS: Wikipedia's article on XNU, kernel.org and the Linux repository on GitHub, over the
hosted system's network link through Linux, with the GPU bridge on (`GPU=auto`).*

## How it works

```
 macOS processes (launchd, WindowServer, Safari...)    Linux processes (systemd, sshd, xnudrmd...)
 ──────────────────────────────────────────────────    ────────────────────────────────────────────
 XNU (source-built, LINUX64 machine layer, kexts)  │
   ↕ linux64 host calls (xnu-patches/include/linux64_abi.h)
 xnu.ko   (APSL side: loads and runs the kernel collection)
   ↕ FKI, the foreign kernel interface (fki_*)
 fki.ko   (GPL side: CPUs, memory, faults, IPIs, files, network, host calls)
 Linux kernel (stock distro kernel, 4K pages, PAC)
```

- **CPUs**: each hosted CPU is a Linux kernel thread pinned to a Linux CPU. XNU runs on it until it calls the host
  (idle, I/O, a timer); Linux keeps its own exception vectors, and `fki.ko` forwards the faults and user exceptions of
  XNU code to XNU's handlers.
- **Memory**: XNU gets one physically contiguous block from Linux (CMA) and manages it with its own pmap; XNU and Linux
  share the user half of the address space layout (4K pages).
- **Devices**: kexts in `kexts/` give macOS a disk (a file on the Linux side), a display (a framebuffer Linux reads), a
  keyboard and pointer, an Ethernet link (a Linux network interface), a keystore and a GPU bridge.
- **GPU**: Metal in the hosted macOS runs on `gpu/xnu-cpu-metal` (metal2vulkan over Vulkan). Vulkan reaches the Linux
  host's GPU through the DRM bridge (`kexts/XnuDrm` → host call → `gpu/xnu-drm/xnudrmd` → the Linux render node), using
  Mesa's Venus driver; without a GPU it falls back to Mesa lavapipe on the CPU.

## Status

Working, on an Apple Silicon Mac running an arm64 Linux VM (krunkit) with 1 to 6 hosted CPUs:

- macOS 27.2.1 boots to the desktop with auto-login in 31–48 s (an Apple Virtualization macOS VM on the same Mac: 49 s).
- Apps open and quit, Spotlight and the file system work; a 30-minute stress run (40 rounds of Safari, Notes,
  Calculator, TextEdit, System Settings, Spotlight and a disk walk) finishes with no panic and no crash report.
- Runs as a systemd service: started at boot, stopped cleanly with the VM, restarted after a hosted-kernel panic, each
  run's log kept in `/var/log/xnulinux/`.
- The GPU bridge gives hosted apps the host GPU (`Virtio-GPU Venus (Apple M5 Max)`) and is enabled by default
  (`GPU=auto`) when a Linux render node is present, falling back to CPU rendering (`GPU=off`) otherwise.

What is still a stopgap is listed in [`docs/production.md`](docs/production.md). Notably: the OS cryptex is merged into
the system volume, AMFI is patched and SIP relaxed, and memory access is slower than a native VM (4K pages vs 16K).

## Requirements

- An arm64 Linux host with PAC (Apple Silicon M1 or later in a VM: krunkit for GPU access, or tart), 4K pages, 16 GB of
  RAM (8 GB of it reserved for the hosted kernel).
- A Mac with Xcode to make the system disk and build the GPU parts.
- A macOS 27 installation (an Apple Virtualization VM disk) of your own. **No Apple binaries are in this repository or
  distributed by it**: the kexts Apple ships, the macOS system disk and its trust cache come from your own installation.

## Building and running

1. `scripts/vm-xnu-build.sh` (in the Linux VM, once): sets up the macOS-DroidVM Linux toolchain and builds XNU
   (`xnu-12377.121.6`) natively on arm64.
2. `scripts/vm-xnu-rebuild.sh`: applies `xnu-patches/`, builds the kernel and `kexts/`, and links the kernel collection
   with Apple's kexts from your macOS installation.
3. `scripts/mk-macvm-disk.sh` (on the Mac): turns a macOS VM disk made by Apple's installer into the hosted system's disk
   and copies it into the Linux VM.
4. `scripts/xnulinux-boot.sh` (in the Linux VM): builds `fki.ko` and `xnu.ko` against the running kernel, brings up the
   network (and the GPU bridge when there is a render node) and boots the hosted system. Its console is
   `scripts/xnu-console.sh`, its screen `tools/hosted/fb2png.py`, input `tools/hosted/xnu-input.py`.
5. `scripts/install-service.sh` (in the Linux VM): runs it as `xnulinux.service`, configured in `/etc/xnulinux.conf`
   (CPUs, memory, disk, GPU). On the Mac, `scripts/install-krun-agent.sh` keeps the VM itself running.
6. GPU (optional, on the Mac): `gpu/venus/build-darwin.sh` builds the hosted Vulkan driver, `gpu/xnu-cpu-metal/` the
   Metal plugin (see its README).

## Repository layout and licenses

The Linux side and the XNU side are kept apart by license and meet only at FKI. Every source file carries an
`SPDX-License-Identifier`; the license texts are in [`LICENSES/`](LICENSES).

| Path | License | What |
|---|---|---|
| `fki-ko/`, `linux/` | GPL-2.0-only | FKI: the out-of-tree module for stock kernels, and the same as an in-tree driver |
| `xnu-ko/` | APSL-2.0 | `xnu.ko`: loads XNU's kernel collection and runs it; calls Linux only through `fki_*` |
| `xnu-patches/` | APSL-2.0 | The LINUX64 machine layer and the other changes to XNU's sources, and their shared headers |
| `kexts/` | APSL-2.0 | The hosted system's kexts (CPU, disk, keystore, Metal accelerator, DRM bridge) |
| `kexts/XnuDisplay/`, `kexts/XnuEthernet/`, `kexts/XnuInput/` | BSD-2-Clause-Patent | Derived from [macOS-DroidVM](https://github.com/Droid-VM/macOS-DroidVM)'s kexts |
| `gpu/xnu-cpu-metal/` | GPL-2.0-or-later | The Metal plugin over metal2vulkan (GPL-2.0-or-later); `XnuCpuMetalShim.h` is BSD-2-Clause-Patent (from [AdrenoMetal](https://github.com/UniXNU/AdrenoMetal)) |
| `gpu/xnu-drm/` | GPL-2.0-only, MIT | `xnudrmd` (the Linux end of the DRM bridge) is GPL; the protocol header and `darwin/` (built into Mesa) are MIT |
| `gpu/venus/` | GPL-2.0-only; patches MIT | Build scripts and tests; the patches to Mesa and virglrenderer are under their upstream license (MIT) |
| `gpu/xnu-cpu-metal/patches/` | upstream's | Patches to Mesa (MIT) and metal2vulkan (GPL-2.0-or-later) |
| `scripts/`, `tools/`, `tests/`, `docs/` | GPL-2.0-only | Build, disk, boot, debugging and test tools; documentation |

`xnu.ko` is on the XNU side of the line: it runs XNU's code in its own address space, so it is APSL-2.0 like XNU, and
Linux reports it as a non-GPL module (`MODULE_LICENSE("Proprietary")`, which taints the kernel as ZFS does). It must not
include Linux headers beyond the module ABI, call Linux functions other than `fki_*`, or carry Linux code. Upstream code
(XNU, macOS-DroidVM's toolchain, Mesa, metal2vulkan, the Vulkan loader, LLVM) is fetched at pinned revisions and patched at
build time; it is never committed.

## Acknowledgements

- [macOS-DroidVM](https://github.com/Droid-VM/macOS-DroidVM) and [UniXNU](https://github.com/UniXNU): the 4K-page XNU
  base, the Linux-hosted XNU toolchain, and the display, Ethernet and input kexts these are derived from.
- [metal2vulkan](https://github.com/steelbrain/metal2vulkan), [Mesa](https://mesa3d.org) (Venus, lavapipe),
  [virglrenderer](https://gitlab.freedesktop.org/virgl/virglrenderer) and [krunkit](https://github.com/containers/krunkit).
- Apple's open-source XNU.

macOS, Metal and XNU are trademarks of Apple Inc. This project is not affiliated with or endorsed by Apple.

Copyright © 2026 Heyang Zhou and contributors.
