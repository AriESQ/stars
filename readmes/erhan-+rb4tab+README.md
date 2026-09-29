# rb4tab — the CDJ-3000X rekordbox player (`EP145`) on a postmarketOS tablet

> **Author:** Erhan — [Instagram @i.erhan.es](https://www.instagram.com/i.erhan.es/)
>
> **Disclaimer:** this is an unofficial, independent project — **not affiliated
> with, authorised by, endorsed by or sponsored by AlphaTheta Corporation or
> Pioneer DJ.** `CDJ`, `rekordbox` and `PRO DJ LINK` are trademarks of AlphaTheta
> Corporation; `Pioneer DJ` is a trademark of Pioneer Corporation, used under
> licence. No firmware, decryption keys or other AlphaTheta material are included —
> you must supply your own legally obtained firmware. See [`NOTICE.md`](NOTICE.md).

**Goal:** run the **CDJ-3000X player application** (`EP145`, the aarch64 rekordbox
engine that drives the CDJ-3000X 9" screen) natively on a **postmarketOS tablet**,
with the tablet's own touchscreen, display and audio — and, where the tablet has
no physical DJ controls, an external controller (e.g. Denon DJ LC6000 PRIME over
USB) standing in for the CDJ's sub-CPU panel.

## Features

**Player & display**
- Runs the **CDJ-3000X v1.40 `EP145`** application natively (aarch64 + glibc)
  inside an unprivileged `bwrap` chroot — no root, no CPU emulation.
- Full-panel output: the tablet's **1920x1200 panel is exactly 1.5x** EP145's
  native 1280x800, so it fills the screen with no rotation or letterboxing
  (rootful Xwayland, with gamescope also supported).
- **On-screen CDJ-3000X controller** drawn around the real player window: top nav
  row (SOURCE…MENU), hot-cue pads, transport (CUE / PLAY / SEARCH / TRACK / BEAT
  JUMP), loops, sync/master, tempo fader, direction rocker, jog wheel and mode
  buttons — see [`docs/12`](docs/12-controller-ui.md).
- **Jog wheel** with the hardware's physics (linear brake, free-running
  3240-tick/rev position, inverse-velocity encoding) and the app's own jog-LCD
  shown inside the wheel.
- **Live LED feedback** (the app's MOSI frame) so lit buttons, pads, jog ring and
  the ON AIR bar match the player.
- **Two display modes**: the full deck, and “EP145's screen fullscreen” with a
  small control strip.

**Input**
- **Touch** on the real MT-B panel is forwarded to the `/dev/input/by-id/gt928`
  panel EP145 expects; touches on the controller are hit-tested into sub-CPU
  input.
- **Denon DJ LC6000 PRIME** over USB-MIDI drives controls, LEDs and the
  jog / Select / pitch; the loop encoder acts as 8 BEAT LOOP.
- **Any keyboard** can press every CDJ button and turn the Select knob, with a
  customizable keymap ([`docs/10`](docs/10-keyboard.md)).

**Audio**
- Output through `plug -> dmix -> hw:<card>,<dev>` with 96k -> 48k speexrate
  conversion, absorbing EP145's sub-millisecond periods.
- **Automatic card selection**: internal speaker, or a USB audio device when one
  is plugged in.

**Media & connectivity**
- **Removable media**: a USB stick auto-mounts and is presented to EP145 as a CDJ
  source (`/media/usb/<dev>`, `/proc/udev_usb1`, real volume label); plug-in
  hotplug works, and USB STOP ejects it ([`docs/04`](docs/04-media.md)).
- **Pro DJ Link** membership: DJPL discovery/status and the NFS + dbserver media
  paths are implemented and verified ([`docs/11`](docs/11-prolink-link-media.md)).

**System integration**
- GNOME app-grid entries, desktop icons and **Start / Stop / Eject**; plus a
  one-shot `rb4tab-restart.sh` that prints a status table.
- Panel **orientation + rotation lock** (and a 180° flip when the detachable
  keybase is attached), and **keep-awake / no-suspend** while playing.
- Debug helpers: headless render check, tap injection, four-corner touch
  calibration.

**Known gaps** (full detail in [`docs/08`](docs/08-limits.md))
- The **system volume does not control the player** on the shipping dmix route
  (a PulseAudio route works but is parked on latency).
- **Media removal** needs a player restart (EP145 reads the media event channel
  once per launch).
- **Pro DJ Link peer-library browsing** is blocked by the app's internal
  Nexus/TLS (TCP 50006) path — open item.
- **LC6000 wheel display**, **USB-C host mode** and **Bluetooth audio** are not
  wired / verified.

> **STATUS — RUNNING ON THE TABLET, ONE OPEN ITEM (2026-09-18).** EP145 boots
> natively from the glibc chroot; USB media mounts and is browsable; the LC6000
> drives the CDJ controls; and audio plays through `plug -> dmix -> hw:<card>,<dev>`
> — the internal speaker, or a **USB audio device when one is plugged in**
> (detected at launch by `device/launcher/rb4tab-audio.sh`, see
> [`docs/03`](docs/03-launcher.md)).
>
> **The tablet now shows the full CDJ-3000X controller** (a faithful port of the
> [`cdj3k-emu`](https://github.com/nsaintot/cdj3k-emu) chassis):
> `rb4tab-deck.py` draws the top button row, hot cues,
> transport, jog wheel, tempo fader and mode buttons around EP145's real screen
> in the LCD, and `rb4tab-xtouch.py` turns touches on that chassis into sub-CPU
> input — see [`docs/12-controller-ui.md`](docs/12-controller-ui.md). The old
> on-screen top-button bar ([`docs/09`](docs/09-top-buttons.md)) is superseded.
> **Open: the system volume does not control the player.** The design is in the
> tree (a `softvol` gain stage plus `rb4tab-volume.service`, which mirrors the
> default sink's volume onto its mixer control) but EP145 will not open that
> chain, so the shipping config is still plain dmix - see
> [`docs/08-limits.md`](docs/08-limits.md). **Any keyboard** can still press the
> CDJ's buttons and turn the Select knob
> ([`docs/10-keyboard.md`](docs/10-keyboard.md)).
> The tablet also hard-powers-off on a low battery, so **keep it on a charger**.
>
> **Pro DJ Link (2026-09-18):** the firewall was silently dropping all DJPL, so
> the CDJ was never discovered; that is fixed (`docs/11-prolink-link-media.md`).
> The CDJ is now a link member, its NFS export mounts, and its media query and
> dbserver both answer when driven manually. EP145 still does not list the
> CDJ-2000nexus's stick: its per-member path tries a Pioneer-internal **Nexus
> TLS channel on TCP 50006** (which the 2000nexus does not run) and never falls
> back to the media query / dbserver / NFS. Open item, full work log in
> `docs/11-prolink-link-media.md`.

## Reusable pieces

| Layer | Reusable? | Notes |
|---|---|---|
| `EP145` glibc chroot (Buildroot 2018.02 rootfs) | **yes, as-is** | aarch64 + glibc 2.29; hardware-independent |
| `device/ep145_shim.c` — X11 window, `/dev/subucom_spi1.0`, touch, media paths, cabinet stub | **mostly** | touch device node, jog-LCD DRM and ALSA device names are host-specific |
| LC6000 MIDI map + LED/wheel-display SysEx | **yes** | plain USB-MIDI, host-agnostic |
| gamescope/`bwrap` launch recipe | **likely** | depends on the tablet's compositor (Wayland vs Xorg) |
| ALSA → PulseAudio audio bridge | **no** | the app's audio path is host-specific; the tablet codec differs |
| virtual `goodix-ts` touch panel | **no** | tablet has a real touchscreen |
| sub-CPU SPI frame | **yes** | protocol knowledge, not hardware |

## The tablet

| fact | value |
|---|---|
| device | **Lenovo IdeaPad Duet Chromebook** — `google,krane-sku176`, MediaTek **MT8183**, 4 GB RAM, 116 GB eMMC |
| OS | **postmarketOS edge** (musl, systemd, GNOME Shell on Wayland) |
| kernel | `7.2.2-mt81` |
| panel | DSI-1 native `1200x1920` → **1920x1200 landscape = exactly 1.5 × EP145's 1280×800** |
| audio | MT6358 + MAX98357 internal speaker, **plus USB audio** (auto-detected, e.g. a USB-C dongle) |
| touch | real MT-B touchscreen `hid-over-i2c 27C6:0E30` = `/dev/input/event4` |
| access | `user@google-kukui.local` (`192.0.2.136`), pass `CHANGEME` |

Full inventory: [`docs/01-tablet-survey.md`](docs/01-tablet-survey.md).

## Quick start

Full instructions: [`docs/06-reproduce.md`](docs/06-reproduce.md).

```sh
export TABLET=user@<tablet> PASS=<password>

# host: rootfs -> chroot -> shim + tools -> ship
./scripts/extract-rootfs.sh /path/to/CDJ3000Xv140
./scripts/build-chroot.sh          # or reuse an existing build: CHROOT_DIR=/path/to/chroot
./scripts/build-shim.sh
./scripts/deploy-tools.sh
./scripts/ship.sh

# tablet: system bits (root), then the user session
sudo sh ~/cdj3k/device/udev/install.sh   # udev rules, tmpfiles, polkit, touch bridge
sh ~/cdj3k/device/launcher/install.sh    # units + icons (incl. the on-screen top
                                         #   buttons and the keyboard bridge)

# run and verify
systemctl --user start rb4tab.service            # or tap the Start icon
SUDO_PASS=$PASS sh ~/cdj3k/device/launcher/rb4tab-restart.sh   # clean start + status table
```

## Docs

```
docs/00-overview.md        goal, reusable pieces, the answered questions
docs/01-tablet-survey.md   device/OS/display/input/audio/net inventory (read off the device)
docs/02-bringup-log.md     round-by-round history of the bring-up
docs/03-launcher.md        the launcher: units, icons, orientation, keep-awake, audio path
docs/04-media.md           USB/SD media: bind, udev events, hotplug and its limit
docs/05-touch.md           touch: Xwayland bridge, the proven translation, calibration
docs/06-reproduce.md       *** step-by-step from a bare tablet ***
docs/07-knobs.md           every environment knob, with defaults
docs/08-limits.md          what does not work yet, with evidence and the route
docs/09-top-buttons.md     the on-screen CDJ top buttons (SOURCE..MENU + EXIT)
docs/10-keyboard.md        any keyboard -> the CDJ's buttons and Select knob
docs/11-prolink-link-media.md  Pro DJ Link: browsing a CDJ-2000nexus's media
                              (DJPL works, NFS/dbserver verified, media query
                              never sent — the 50006 Nexus gate; open item)
docs/12-controller-ui.md   *** the on-screen CDJ-3000X deck (the GUI) ***
```

## Credits

The on-screen CDJ-3000X chassis look, the jog-wheel display and physics, and
some guest-shim protocol facts are based on the
[`nsaintot/cdj3k-emu`](https://github.com/nsaintot/cdj3k-emu) project
(MIT OR Apache-2.0). See [`NOTICE.md`](NOTICE.md).

## License

Our own code and documentation are **MIT** (see [`LICENSE`](LICENSE)). Everything
else — firmware, trademarks and third-party components — belongs to its
respective owners; see [`NOTICE.md`](NOTICE.md) for the full affiliation,
trademark, firmware and attribution notice.
