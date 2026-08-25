# Dropkick

A reproducible [projectM](https://github.com/projectM-visualizer/projectm) audio
visualizer for the **Raspberry Pi 5**, with GLES 3.1 support, organized preset
packs, and full phone/tablet remote control — including an in-browser preset
editor. Built to run on a TV over HDMI and be driven from the couch.


## Install

On a Raspberry Pi 5 (Raspberry Pi OS, aarch64):

```bash
git clone https://github.com/s66lem/dropkick.git
cd dropkick && ./scripts/bootstrap.sh
```

`bootstrap.sh` installs dependencies, builds the bundled libprojectM + frontend
with `-DENABLE_GLES=TRUE`, installs the `dropkick` launcher and a **Sound & Video**
menu entry, and creates the preset/texture/workshop directories.

To Launch:

```bash
dropkick
```

### Other platforms
Dropkick also builds on **Windows** (desktop OpenGL, from source) — see
[docs/setup-windows.md](docs/setup-windows.md). macOS and non-Debian Linux aren't
packaged yet but the code is portable (POSIX + `std::filesystem`); contributions
welcome.

## Features

- **Runs on the Pi 5's GPU.** Runtime GLES capability detection: the frontend
  requests the best OpenGL ES context that works (3.2 → 3.1 → 3.0) and libprojectM
  accepts a 3.1 / GLSL ES 3.10 floor — no hardcoded downgrades.
- **Phone / tablet remote** at `http://<pi>:8080` — a four-view web app:
  - **Now Playing** — transport, shuffle/lock/favorite, tap the name for its path.
  - **Browse** — search and jump across your whole preset library, grouped by category.
  - **Favorites** — star presets; "shuffle favorites" plays only your stars.
  - **Settings** — preset duration, transitions, beat sensitivity, hard cut, FPS,
    aspect correction, pack switching, audio input, and **Reduce flashing**.
  - Dark mode, and a responsive layout that scales up on tablets and desktops.
- **Make your own visualizations.** An in-browser editor (and a hot-reload
  `workshop/` folder) let you edit Milkdrop preset code and see it live on the TV.
  See [docs/authoring.md](docs/authoring.md).
- **Preset packs.** Organized under `~/.local/share/dropkick/presets/<pack>/`,
  switchable from the remote. See [docs/presets.md](docs/presets.md).
- **Reduce flashing.** An optional render filter that limits how fast the picture
  can brighten between frames, easing strobe-heavy presets.
- **Survives bad presets.** Some shader-heavy presets can hang the Pi's GPU;
  Dropkick auto-skips and quarantines them (plus an optional hardware watchdog for
  hard lockups). See "Robustness" in [docs/setup.md](docs/setup.md).

## Configuration

`~/.local/share/dropkick/dropkick.env` is the single source of truth (audio device,
preset pack, remote port/token, display). Edit it, run `./scripts/sync-config.sh`,
and restart. Full details in [docs/setup.md](docs/setup.md).

## Repository layout

- `external/` — vendored, patched libprojectM + projectMSDL frontend (no submodules)
- `remote/` — the mobile/desktop remote web app
- `scripts/` — `bootstrap.sh`, `build.sh`, `sync-config.sh`, `enable-watchdog.sh`, `seed-blocklist.sh`
- `config/` — `dropkick.env` and the `projectMSDL.properties` template
- `systemd/` — boot service unit
- `patches/` — exported documentation patches (the GLES changes)
- `docs/` — setup, presets, authoring, and patch notes

## Credits & license

Dropkick is built on **[projectM](https://github.com/projectM-visualizer/projectm)**
and the **[projectM SDL frontend](https://github.com/projectM-visualizer/frontend-sdl2)**
by the projectM Team and contributors. The frontend is GPLv3; libprojectM is LGPL
v2.1. Dropkick's own glue (scripts, remote web app, systemd, docs) follows suit —
see `external/*/LICENSE*` for the upstream terms.
