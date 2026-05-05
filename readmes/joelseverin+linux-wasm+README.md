# Scripts for Building a Linux/Wasm Operating System
This project contains scripts to download, build and run a Linux system that can be executed on the web, using native WebAssembly (Wasm).

These scripts can be run in the following way:
* Directly on a host machine.
* In a generic docker container.
* In a specific docker container (see Dockerfile).

## Parts
The project is built and assembled from following pieces of software:
* LLVM Project:
    * Base version: 18.1.2
    * Patches:
        * A hack patch that enables GNU ld-style linker scripts in wasm-ld.
    * Artifacts: clang, wasm-ld (from lld), compiler-rt
* Linux kernel:
    * Base version: 6.4.16
    * Patches:
        * A patch for adding Wasm architecture support to the kernel.
        * A wasm binfmt feature patch, enabling .wasm files to run as executables.
        * A console driver for a Wasm "web console".
    * Artifacts: vmlinux, exported (unmodified) kernel headers
    * Dependencies: clang, wasm-ld with linker script support, (compiler-rt is *not* needed)
* musl:
    * Base version: 1.2.5
    * Patches:
        * A hack patch (minimal and incorrect) that:
            * Adds Wasm as a target to musl (I guessed and cheated a lot on this one).
            * Allows musl to be built using clang and wasm-ld (linker script support may be needed).
    * Artifacts: musl libc
    * Dependencies: clang, wasm-ld, compiler-rt
* Linux kernel headers for BusyBox
    * Base version: from the kernel
    * Patches:
        * A series of patches, originally hosted by Sabotage Linux, but modified to suit a newer kernel. These patches allow BusyBox to include kernel headers (which is not really supported by Linux). This magically just "works" with glibc but needs modding for musl.
    * Artifacts: modified kernel headers
    * Dependencies: exported Linux kernel headers
* BusyBox:
    * Base version: 1.36.1
    * Patches:
        * A hack patch (minimal and incomplete) that:
            * Allows BusyBox to be built using clang and wasm-ld (linker script support might be unnecessary).
            * Adds a Wasm defconfig.
    * Artifacts: BusyBox installation (base binary and symlinks for ls, cat, mv etc.)
    * Dependencies: musl libc, modified headers for BusyBox
* A minimal initramfs:
    * Notes:
        * Packages up the busybox installation into a compressed cpio archive.
        * It sets up a pty for you (for proper signal/session/job management) and drops you into a shell.
    * Artifacts: initramfs.cpio.gz
    * Dependencies: BusyBox installation
* A runtime:
    * Notes:
        * Some example code of how a minimal JavaScript Wasm host could look like.
        * Error handling is not very graceful, more geared towards debugging than user experience.
        * This is the glue code that kicks everything off, spawns web workers, creates Wasm instances etc.

Hint: Wasm lacks an MMU, meaning that Linux needs to be built in a NOMMU configuration. Wasm programs thus need to be built using -fPIC/-shared. Alternatively, existing Wasm programs can run together with a proxy that does syscalls towards the kernel. In such a case, each thread that wishes to independently execute syscalls should map to a thread in the proxy. The drawback of such an approach is that memory cannot be mapped and shared between processes. However, from a memory protection standpoint, this property could also be beneficial.

## Running
Run ./linux-wasm.sh to see usage. Downloads happen first, building afterwards. You may partially select what to download or (re)-build.

Due to a bug in LLVM's build system, building LLVM a second time fails when building runtimes (complaining that clang fails to build a simple test program). A workaround is to build it yet again (it works each other time, i.e. the 1st, 3rd, 5th etc. time).

Due to limitations in the Linux kernel's build system, the absolute path of the cross compiler (install path of LLVM) cannot contain spaces. Since LLVM is built by linux-wasm.sh, it more or less means its workspace directory (or at least install directory) has to be in a space free path.

### Docker
The following commands should be executed in this repo root.

There are two containers:
* **linux-wasm-base**: Contains an Ubuntu 20.04 environment with all tools installed for building (e.g. cmake, gcc etc.).
* **linux-wasm-contained**: Actually builds everything into the container. Meant as a disposable way to build everything isolated.

Create the containers:
```bash
docker build -t linux-wasm-base:dev ./docker/linux-wasm-base
docker build -t linux-wasm-contained:dev -f ./docker/linux-wasm-contained/Dockerfile .
```
Note that the latter command will copy linux-wasm.sh, in its current state, into the container.

To launch a simple docker container with a mapping to host (recommended for development):
```bash
docker run -it --name my-linux-wasm --mount type=bind,src="$(pwd)",target=/linux-wasm linux-wasm-base:dev bash
(Inside the bash prompt, run for example:) /linux-wasm/linux-wasm.sh all
```

To actually build everything inside the container (mostly useful for build servers):
```bash
docker run -it --name full-linux-wasm linux-wasm-contained:dev /linux-wasm/linux-wasm.sh all
```

To change workspace folder, docker run -e LW_WORKSPACE=/path/to/workspace ...blah... can be used. This may be useful together with docker volumes.

