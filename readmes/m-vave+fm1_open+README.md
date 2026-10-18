# FM1 Open V13

English · [简体中文](README.zh-CN.md)

8 tracks, 8 sample slots, 16 FX demos; binary SDK included.

[Workbench and development kit](https://open.m-vave.com/fm1-workbench) · [Official forum](https://forum.m-vave.com)

Select "Source + SDK" in the workbench to download the development kit matching the online release.

## Build

Requires Windows x64, PowerShell, `curl.exe` and `tar.exe`. Firmware builds also require the [JieLi PI32v2 clang 4.0.1 r3 compiler](https://doc.zh-jieli.com/Tools/zh-cn/dev_tools/dev_env/jl_toolchain.html); its folder must contain `bin/clang.exe`.

Before running the commands below, set the `FM1_SOURCE_URL` environment variable to the HTTPS download URL of this build's source archive, including its changes, license notices and build/install scripts. Web and package builds stop if it is missing.

~~~powershell
.\build.bat --web
$env:FM1_PI32_TOOLCHAIN = 'C:\JL\pi32'
.\build.bat --package
~~~

The web version builds from the included C sources. The first build downloads WASI SDK 27; set `FM1_WASI_SDK` to reuse an existing installation.

Outputs: `build/preview/index.html` (preview), `build/dx7/generated/FM1_OFFICIAL_OPEN.fwsc` (firmware), `build/official-web/FM1-Official-Open-Source.html` (complete workbench).

Hardware drivers are in `app/board/`. The audio interrupt calls `fm1_engine_render()`; `app/audio_output.c` handles USB/Bluetooth mixing and USB recording.

The [per-track tuning API](app/instrument.h) supports custom tuning; a dedicated tuning editor is not included.

APP: [GPLv3 with an SDK linking exception](LICENSE.md); files with other license notices retain their terms. The native engine is supplied as a binary. See [SDK terms, third-party licenses and contributions](THIRD_PARTY.md).

Back up projects and samples, and keep the device powered during saves and firmware updates.
