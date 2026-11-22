<h1 align="center">
  <br>
  <a>
  <img src="assets/logo.png" alt="Leonida" width="200">
</a>

  <br>
  <b>Leonida</b>
  <br>
</h1>

<h4 align="center">Grand Theft Auto VI (Xbox Series) running natively on Windows, built on your PC from your own copy.
</h4>

<p align="center">
  <a href="docs/i18n/README.md">Other languages</a> |
  <a href="#project-status">Status</a> |
  <a href="#how-to-build">How to build</a> |
  <a href="#how-it-works">How it works</a> |
  <a href="#want-to-help">Want to help?</a> |
  <a href="#credits">Credits</a> |
  <a href="#license">License</a> |
  <a href="https://discord.gg/rexed">Discord</a>
</p>

Leonida is a static recompilation project. The Xbox Series CPU is x86-64 like a PC, so the game's code is loaded
and run natively, and the console's system software is reimplemented. The console's precompiled RDNA2 GPU programs
are translated to SPIR-V for Vulkan. The game's models, textures and audio are read from your package. All of this
happens **on your PC, from your own copy of the game**.

> [!IMPORTANT]
> This repository **does not contain the game, keys or an executable**, and it does not explain how to get them. You
> need your own copy, with its files already readable on disk. Nothing here decrypts or works around any protection.
> Everything the build creates (the generated shaders, extracted assets, the runtime folder and your saves) comes
> from your game and stays on your PC. Never share those files.

Discord: https://discord.gg/rexed
<br>

## Project status

**Early. The game does not boot yet.** Everything that can be done without the game's executable is in place, so
work on booting can start as soon as one is available to a developer.

| What | Status |
|---|---|
| Finding and checking your copy (Xbox Series 1.0.2.1) | ✅ Works |
| Shaders: carve, unpack native RDNA2 code, disassemble | ✅ All 26,503 |
| Shaders: RDNA2 → SPIR-V translation | ✅ **All 26,503 translated**: 2,236 VS, 12,101 PS, 2,689 CS, 9,282 mesh, 195 geometry, with a per-shader metadata index for pipeline creation. All 26,503 passed `spirv-val` in the [LLVM 23.1.5 Linux run at `c432cdc`](https://github.com/ItsNotRexed/Leonida/issues/644#issuecomment-7072972586). A [full-corpus run at `43d4703`](https://github.com/ItsNotRexed/Leonida/issues/881#issuecomment-7075507328) also validated all 26,503 after the SPIR-V ID-bound fix. ⚠️ 21,545 are wave64: exact on 64-wide subgroups (AMD). On 32-wide subgroups (NVIDIA, Intel), compute and mesh shaders are exact with wave64 emulation (`--wave64-emulate`, on by default there); cross-half wave ops in vertex, pixel and geometry shaders are still approximate |
| Shader translator checked on a real GPU | ⚠️ The hand-written GPU tests (vertex fetch, texture sampling, exports, ALU ops, partial-register ops, barycentrics, wave-uniform branches, compute LDS/barriers/buffer stores, wave64 masks) have been run on more than 30 GPU and driver combinations, with results in [#166](https://github.com/ItsNotRexed/Leonida/issues/166): NVIDIA Turing, Ampere, Ada and Blackwell (Windows and Linux); AMD GCN3, RDNA1, RDNA2, RDNA3 and RDNA4 (Windows driver and RADV); Intel Gen9 (ANV); Apple M1 (MoltenVK, no geometry or mesh stages); and Mesa llvmpipe. Wave64 tests need 64-wide subgroups (AMD) or `LEONIDA_W64_EMULATE=1`. These are small test shaders: the game's own shaders are checked by `spirv-val` and by driver pipeline creation (`vk_pipeline_check`), not by their output |
| Models (OBJ with real names, UVs, material references) | ✅ Exported. Not all layouts are decoded yet |
| Texture dictionaries and world texture pools (DDS) | ✅ Exported. Pool entries stored as BCPack are still skipped by the export; a clean-room decoder (`tools/bcpack.py`) rebuilds BC1, BC3, BC4, BC5, BC6H and BC7 (most BC6H/BC7 chunks need a local history table, which the repo does not ship), and is not wired into `rpf9dump` yet ([notes](docs/textures.md)) |
| Audio banks (AWC: Opus, XMA2) | ✅ Exported whole. Opus repackaged **losslessly** as Ogg Opus; PCM (codec 0/2) as WAV; XMA2 decoded with ffmpeg. `--wav` adds 16-bit PCM WAV ([notes](docs/audio.md)) |
| Music/radio config | ? Measured. **1,589** audio-config records with exact durations and AWC stream ids; station grouping and content-id lists; no per-track start offsets ([notes](docs/audio_config.md)) |
| PE loader and import shims | ⚠️ Runs a stand-in executable end to end (`gta6rt --run`: CRT startup, statics, heap, files, threads, GDK imports through the shims, exit code back). Controllers through a GameInput shim on SDL3 (any controller SDL supports, rumble, DualSense trigger effects and lightbar; built when SDL3 is installed or with `-DLEONIDA_SDL3_FETCH=ON`, [notes](docs/gameinput.md)). `--trace-d3d12` logs every D3D12 call and its outcome for the first boot. Untested against the real executable |
| Xbox D3D12 → Vulkan | ⚠️ In progress. A Vulkan-backed device behind the Xbox-ABI proxy creates queues, command lists, fences, descriptor heaps, committed and reserved resources, render-target and depth views (3D targets included), texture views and samplers (2D, cube and 3D views, the depth and stencil planes of depth-stencil textures, packed formats such as B5G6R5, B4G4R4A4 and R9G9B9E5; they go into the bindless set), and query heaps. Barriers, clears, uploads, copies (BC included), colour resolves, predication, CPU-side texture reads and writes, and occlusion, timestamp and pipeline-statistics queries run on Vulkan, checked on one GPU. No buffer views, root signatures, pipelines, draws, placed resources, 1D textures or swapchain yet ([plan](docs/d3d12_vulkan.md)) |
| Booting, story mode, anything playable | ❌ No |

## How to build

The port isn't downloaded ready-made. It's built on your PC from your own copy.

**The easy way:**

1. Install the prerequisites below.
2. Download this project **with its submodule**: `git clone --recursive https://github.com/ItsNotRexed/Leonida`. A
   "Download ZIP" from GitHub leaves out `third_party/rpf9-explorer`. The build fetches it if `git` is installed,
   and otherwise tells you what to do.
3. Double-click **`Build.bat`**.

It finds your copy of the game by itself: it looks in Downloads, Desktop, Documents (also where Windows keeps them,
such as in OneDrive), Games, your home folder and the top of every drive, two folders deep. It recognises the
version from a few file sizes, without reading anything large. If you have more than one copy it asks which one, and if it finds none it asks you to paste the
folder. Before starting it checks that everything below is installed and that there is enough free space, and it
lists anything missing in one go. The result goes to `Documents\Leonida`. A stopped build continues where it left
off.

Your game folder is the one that holds `MicrosoftGame.Config` and the `.rpf` archives, as plain files.

**Prerequisites:**

- **Your own copy** of the Xbox Series package, version 1.0.2.1.
- **Windows 10/11 x64**, with about **350 GB** free for work files. They can go on another drive with `--work`.
- [Python 3.12+](https://www.python.org/downloads/) (tick "Add python.exe to PATH").
- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0).
- [Vulkan SDK](https://vulkan.lunarg.com/), for `spirv-as` / `spirv-val`.
- [LLVM 21+](https://github.com/llvm/llvm-project/releases) with the **AMDGPU target** for `llvm-mc`. The official
  Windows build has no AMDGPU target. On Windows, `scripts\build_llvm_mc.ps1` builds a native `llvm-mc.exe` with it
  (no WSL; needs git and the Visual Studio C++ tools below) and sets `LLVM_MC`. Or install `llvm-21` in WSL and set
  `LLVM_MC` to the whole command, `LLVM_MC="wsl -d Ubuntu -e /usr/lib/llvm-21/bin/llvm-mc"` (see
  [docs/design.md](docs/design.md#disassembling-shaders)). On Linux, `llvm-mc` on PATH is enough.
- Visual Studio 2022 with **Desktop development with C++** and the **Windows SDK 10.0.26100 or newer**, for the
  runtime stage (the runtime uses version 1.2 root signatures, which older SDKs don't declare).
- [ffmpeg](https://ffmpeg.org/download.html) on PATH (optional: decodes the XMA2 streams, and required for `--wav`).

**From a terminal**, with the same behaviour and more control:

```powershell
python -I make_game.py --find                          # list the copies found on this PC
python -I make_game.py --pick                          # choose the game folder in a folder dialog
python -I make_game.py --check                         # check your copy, build nothing
python -I make_game.py --check --full-check            # also compare SHA-256 of every file (slow)
python -I make_game.py --game "D:\path\to\your\package" --out "D:\Games\Leonida" --work "E:\leonida-work"
python -I make_game.py --stages shaders,assets         # only some stages
python -I make_game.py --game "D:\path\to\your\package" --wav   # also decode Opus to PCM WAV (large)
python -I make_game.py --wave64-emulate off            # auto (default), on or off; see below
```

`--wave64-emulate` decides whether wave64 compute and mesh shaders are translated to be exact on any subgroup size
(see "Wave64 emulation" in [docs/design.md](docs/design.md)). NVIDIA and Intel GPUs have 32-wide subgroups and need
it. The default, `auto`, asks `vulkaninfo` (part of the Vulkan SDK) and turns it on unless every GPU reports 64-wide
subgroups, or when it can't tell; it also turns it on when the GPU the runtime would use can't be made to run
compute and mesh shaders 64-wide. The mode is saved next to the translated shaders, and changing it translates them
again. With `auto`, a work folder that previously used emulation keeps it for later translations and retries, even if
the current GPU supports native wave64. Use `--wave64-emulate off` to translate it natively.

Four fallback flags are forwarded to the translator the same way, saved next to the translated shaders, and changing
them translates them again: `--no-float-controls` (drop `SignedZeroInfNanPreserve`, for devices whose pipeline check
skips a shader without `shaderSignedZeroInfNanPreserveFloat32`; needs PR #664's translator flag), `--bary-fallback`
(read raw barycentrics from an interpolated input, for devices without `VK_KHR_fragment_shader_barycentric`),
`--texel-offset-fallback` (fold `image_sample*_o` offsets into the coordinate, for devices without
`VK_KHR_maintenance8`) and `--mesh-compute` (mesh shaders as compute, for devices without `VK_EXT_mesh_shader`).
Each is documented in [docs/design.md](docs/design.md).

The build records which llvm-mc command and version produced the disassembly. Changing either, or reusing a work
folder that predates this record, reruns disassembly and translation while keeping the extracted shader inputs.

The build records which translator sources produced the shaders. A change to those files reruns translation using the
saved disassembly. Older work folders need one translation after upgrading to record this information.

Stages run in order: `check`, `shaders`, `assets`, `runtime`, `pipelines` (creates every translated shader on your
GPU driver and saves a pipeline cache, so the first boot doesn't compile them). The shader translation is the longest step: it runs
on `--jobs` processes (half the CPU threads by default).

`--wav` is off by default because 16-bit PCM WAV is several times larger than Ogg Opus. It decodes the repackaged Ogg
Opus streams to `work\assets\audio\wav` after the audio bank step; existing WAV files are skipped when a build resumes.

### Vulkan diagnostics on Linux

With CMake 3.24+, a C++20 compiler, and Vulkan development headers and loader installed:

```sh
cmake -S runtime -B runtime/build/linux
cmake --build runtime/build/linux --parallel
./runtime/build/linux/vk_pipeline_check /path/to/spirv
```

Pass the directory containing `index.json` and the translated SPIR-V files to `vk_pipeline_check`.

`make_game.py` runs on Linux too. The `pipelines` stage uses the `vk_pipeline_check` built above
(`runtime/build/linux`, or `runtime/build`), and builds it there itself before any other work if it is missing.

### Running the loader on Linux

The loader is a Windows program and runs under Wine or Proton; CI runs its tests under Wine on every change to
`runtime/` (the `wine` job of the Runtime workflow). On Linux the `runtime` stage cross-builds it into
`runtime/build/windows` with clang-cl and lld-link (LLVM 19+, but not 22.1.7 or 22.1.8, see [docs/testing.md](docs/testing.md#known-problems); plain names, or all five LLVM tools with one version
suffix such as `clang-cl-21`) against the MSVC CRT and Windows SDK that
[xwin](https://github.com/Jake-Shadle/xwin) lays out, in `XWIN_DIR` or `~/.local/share/xwin-sdk`
([docs/testing.md](docs/testing.md#the-windows-runtime-on-linux-under-wine-or-proton) has the one-time `xwin`
command). Without them the stage is left out of the default stages, and asking for it lists what is missing before
any work starts. A Windows build made elsewhere works too, such as the `runtime-windows` artifact of that workflow's
`windows` job, unzipped:

```sh
python3 -I make_game.py --runtime-build ~/Downloads/runtime-windows
```

Either way it copies `gta6rt.exe` and `gta6rt_tls_host.dll` into `--out` and writes `gta6rt.sh` next to them, which
starts `gta6rt.exe` with `wine`, or with the Wine named by `WINE` (for Proton, its `files/bin/wine`). The same option
skips the build on Windows.

## How it works

| Piece | What it does | Where |
|---|---|---|
| Version check | Every package file's name, size and SHA-256 for each supported version | `game/`, `make_game.py` |
| Shader pipeline | Carves DXBC containers from `shaders.rpf` without its encrypted table of contents. Unpacks the `XBCH` → `FSSM` native RDNA2 program, disassembles it with LLVM (`gfx1013`) and translates it to SPIR-V | `tools/shader_carve.py`, `fssm_unpack.py`, `shader_disasm.py`, `rdna2spirv.py` |
| Asset export | Finds validated resources inside RPF9 archives and the loose `.ttpf` texture pools | `tools/rpf9dump` (on rpf9-explorer's Core) |
| Runtime | Maps the PE image, resolves imports to shims (GDK, XMem, `d3d12_xs`) | `runtime/` |
| Research tools | PE/RTTI inspection, raw carving, texture tiling probes, GPU test harnesses | `tools/`, `runtime/test/` |

The translator's runtime contract (user SGPRs, push constants, memory model, bindless images, vertex fetch,
system values) and all the format notes are in [docs/design.md](docs/design.md); the format, asset, runtime
and validation notes are indexed in [docs/README.md](docs/README.md). The Xbox D3D12 plan is in
[docs/d3d12_vulkan.md](docs/d3d12_vulkan.md). Audio bank formats and the export tools are in
[docs/audio.md](docs/audio.md); [docs/related_projects.md](docs/related_projects.md) records the prior art we may
read and the licence limits on it.

## Want to help?

The biggest open pieces:

- **Shader translator on hardware**: compute, mesh and geometry now translate (see the translator contract in
  [docs/design.md](docs/design.md)); still open are the vertex-shader input layout (`v0` = `VertexIndex` is
  unverified if the console runs VS as NGG) and wave64 cross-half code in VS/PS/GS on 32-wide subgroups.
- **Xbox D3D12 → Vulkan**: the `d3d12_xs` command list and descriptor heap model.
- **Model layouts** the decoder rejects today.

See [CONTRIBUTING.md](CONTRIBUTING.md). Never attach game files, extracted assets or generated shaders to issues or
pull requests.

## Credits

- [rpf9-explorer](https://github.com/breadbbbb/rpf9-explorer) by breadbbbb: the RPF9 model, texture-pool and AWC
  decoders used by `tools/rpf9dump` (git submodule).
- [Mesa](https://gitlab.freedesktop.org/mesa/mesa) (MIT): GFX10 resource-descriptor layout (`tools/gfx10_formats.json`),
  and the ACO/RADV rules used as reference for 16-bit results and shader system registers.
- [libHttpClient](https://github.com/microsoft/libHttpClient) (MIT) by Microsoft: the XTaskQueue/XAsync implementation
  in `third_party/xtaskqueue`, used by the offline `xgameruntime` shim.
- [LLVM](https://llvm.org/): AMDGPU disassembler.
- Logo: ["Grand Theft Auto VI" icon by SlyDevil](https://www.steamgriddb.com/icon/122618) on SteamGridDB.
- [SPIRV-Tools](https://github.com/KhronosGroup/SPIRV-Tools): assembly and validation.

Grand Theft Auto and all related names are trademarks of their owners. This project is not affiliated with or
endorsed by them.

## License

GPLv3 (or any later version). See [LICENSE](LICENSE). Third-party code keeps its own license.
