<div align="center">

# wdm

**The native macOS CLI for people who actually use multiple displays.**

`list · arrange · switch · cycle · mirror · save · restore · brightness · rotate · flip · pip · virtual · scene · doctor · sleep · edid · hotkeys · ddc · rename · scale · hdr · panorama` — atomically, with auto-revert if the projector goes black.

The CLI is the source of truth. Every verb is a typed `WDMKit` op underneath, so a Mac GUI or a local web server (`wdm-web`, included as a proof of concept) can drive the exact same surface without touching `WDMSystem`.

[![Tests](https://img.shields.io/badge/tests-446%2F103%20green-brightgreen)](#tests)
[![Build](https://img.shields.io/badge/build-warnings--as--errors%20clean-brightgreen)](#building)
[![macOS](https://img.shields.io/badge/macOS-13%2B-blue)](#install)
[![Swift](https://img.shields.io/badge/Swift-6-orange)](https://swift.org)

</div>

---

## Why wdm

You're a workshop teacher, conference speaker, hot-desking remote, or just someone with two monitors. You hit a deadline. The projector picks the wrong resolution. The mirror flips the wrong way. Your terminal lands on the screen the audience can't see. You give up and reach for the trackpad.

`wdm` exists because that whole sequence should be one keystroke. It is the **smallest possible** correct way to drive every aspect of every attached display from a UNIX shell, with safety nets that make destructive changes painless to try.

|                                              | wdm | displayplacer | BetterDisplay | System Settings |
|----------------------------------------------|:---:|:-------------:|:-------------:|:---------------:|
| Pure CLI, scriptable, JSON output            | ✅  | ✅            | partial       | ❌              |
| Atomic safe-transaction with auto-revert     | ✅  | ❌            | ❌            | partial         |
| Save / restore named profiles                | ✅  | ❌            | ✅            | ❌              |
| Native HUD confirm overlay (Tahoe)           | ✅  | ❌            | ❌            | ❌              |
| Brightness control (built-in)                | ✅  | ❌            | ✅            | ✅              |
| Software overlay flip (any Mac, incl. AirPlay) | ✅ | ❌           | partial       | ❌              |
| Picture-in-picture display mirror            | ✅  | ❌            | partial       | ❌              |
| Virtual display (no hardware, real `CGDirectDisplayID`) | ✅ | ❌    | ✅ (closed)   | ❌              |
| `wdm doctor` per-display diagnostics         | ✅  | ❌            | ❌            | ❌              |
| Issue-#1 (`AppleHPM` panic) `wdm sleep` workaround | ✅ | ❌       | ❌            | ❌              |
| Crash-recovery `wdm restore last`            | ✅  | ❌            | ❌            | ❌              |
| Parsed EDID + stable per-display ID          | ✅  | ❌            | partial       | ❌              |
| Global hotkeys for any wdm verb              | ✅  | ❌            | partial       | ❌              |
| External-monitor brightness/contrast/input via DDC/CI | ✅ | ❌    | ✅           | ❌              |
| Display rename (alias + system override)     | ✅  | ❌            | ✅            | ❌              |
| Per-display HDR toggle                       | ✅  | ❌            | ✅            | partial         |
| 100% e2e tested, hermetic suite              | ✅  | ❌            | ❌            | n/a             |

---

## Install

### Homebrew (recommended)

```sh
brew tap Arthur-Ficial/wdm
brew install wdm
```

### One-liner installer

```sh
curl -fsSL https://raw.githubusercontent.com/Arthur-Ficial/workshop-display-manager/main/install.sh | bash
```

The installer verifies the SHA-256, the Developer-ID code signature, and the notarization ticket before placing the binary at `/usr/local/bin/wdm`. Pass `--user` to install under `~/.local/bin` instead.

### From source

```sh
git clone git@github.com:Arthur-Ficial/workshop-display-manager.git
cd workshop-display-manager
make release && make install
```

Requires Swift 6, macOS 13+. See [`docs/contributing.md`](docs/contributing.md).

---

## Quickstart

```sh
wdm list                                     # see every display
wdm doctor probe                             # full diagnostic per display (mode, origin, rotation, mirror)
wdm arrange list --json                      # real-time read of every display's origin + rotation (drag-GUI hook)
wdm arrange move 1 -1920 0 2 0 0             # bulk rearrange in one safe transaction
wdm switch                                   # swap main between two displays
wdm cycle                                    # rotate main forward through all displays
wdm mode 2 1920x1080@60                      # set resolution+refresh, with safe revert
wdm mirror 1 2                               # mirror display 1 onto display 2
wdm flip-overlay 2 vertical                  # software flip (any Mac, incl. AirPlay) — Ctrl+C to stop
wdm pip 2 --on 1 --size 800x450              # picture-in-picture: BenQ in a window on built-in
wdm brightness main 0.5                      # 50% brightness on the built-in
wdm save desk-A                              # snapshot current arrangement
wdm save --auto                              # snapshot keyed by EDID set (auto-recognised by daemon)
wdm restore desk-A                           # apply it back later
wdm profiles remove desk-A                   # delete a saved profile
wdm watch --json                             # stream display reconfig events
wdm workshop start --audience 2              # one-step "main → projector, save the rest"
wdm workshop stop                            # restore the pre-workshop arrangement
wdm sleep                                    # drain AppleHPM before unplug (issue #1 workaround)
wdm daemon install                           # auto-restore arrangements at login
```

| Command | What it does |
|---|---|
| `wdm list [--json]` | Enumerate every connected display: ID, name, current mode, origin, rotation, main flag, mirror source. |
| `wdm get <id\|main> [field]` | Read one field of one display. Pipe-friendly. |
| `wdm arrange list [--json]` | Real-time read of every display's origin + rotation. Pipe-friendly snapshot for drag-to-rearrange GUIs. |
| `wdm arrange move <id> <x> <y> [<id> <x> <y> ...]` | Bulk move multiple displays in one safe transaction. Triples are positional. |
| `wdm arrange set @-\|@<path>` | Apply a JSON arrangement plan from stdin / file. Round-trips with `arrange list --json`: `wdm arrange list --json \| jq … \| wdm arrange set @-`. |
| `wdm doctor probe [<id>] [--json]` | Full diagnostic per display — what wdm sees, side-by-side with what you expected. |
| `wdm doctor disconnect <id> [--duration-ms N]` | Soft-disconnect via `CGDisplayCapture` (public API). Display blanks, other apps stop drawing to it. Release: SIGTERM, or `--duration-ms` elapses. |
| `wdm virtual create --name <s> [--mode WxH@Hz] [--hidpi]` | **Software-backed virtual display via Apple's `CGVirtualDisplay` SPI.** Gets a `CGDirectDisplayID`, appears in System Settings → Displays, and starts a cursor edge portal so physical mouse movement can cross onto adjacent virtual bounds. If macOS refuses the event tap, `wdm` exits with an error instead of pretending the cursor path works. Lifetime is process-bound (kill to remove). |
| `wdm switch` | Swap which of two displays is main. <1 second. |
| `wdm cycle` | Rotate "main" forward across N displays. |
| `wdm mode <id> <WxH@Hz>` | Set resolution + refresh. Safe-tx wrapped. |
| `wdm rotate <id> <0\|90\|180\|270>` | Physical framebuffer rotation (IOKit). |
| `wdm flip <id> <none\|h\|v\|hv\|off>` | Framebuffer flip (IOKit) — same Apple-Silicon caveat as rotate. |
| `wdm flip-overlay <id> <axis>` | Software overlay flip via ScreenCaptureKit + CALayer. Works on every Mac including AirPlay & Sidecar. |
| `wdm pip <src> [--on <dst>] [--size WxH] [--flip <axis>]` | Movable / resizable picture-in-picture mirror window. |
| `wdm save <name>` / `wdm restore <name>` | Named profiles in `~/.config/wdm/profiles/`. |
| `wdm profiles remove <name>` | Delete a saved profile. Exits 6 if it doesn't exist (never silent). |
| `wdm restore last` | Recover the last pre-mutation snapshot, even after a crash. |
| `wdm brightness <id> [0..1]` | Read or set brightness on the built-in display. |
| `wdm watch [--json]` | Stream display reconfiguration events (added/removed/mode/move/mirror/main). |
| `wdm workshop start --audience <id>` / `wdm workshop stop` | One-step presentation toggle with auto-revert. |
| `wdm sleep` | Sleep the Mac via IOPMSleepSystem. Drains the AppleHPM PD/DP-AltMode queue before you unplug a projector — workaround for the macOS kernel-panic bug filed in [issue #1](docs/known-issue-applehpm-panic.md). |
| `wdm daemon install` | Install a LaunchAgent so the daemon auto-restores per-EDID profiles at login. |

---

## Workshop scenarios

### One-projector talk

You walk into the room, plug into HDMI, plug your dock back in, get to work:

```sh
wdm save desk                # save your dock setup once
# … later, in the workshop room …
wdm switch --confirm         # main → projector, native HUD asks for confirmation
wdm save room-A              # workshop config saved
wdm mode 2 1920x1080@60      # if the projector defaults to a weird mode
# done — give the talk
wdm restore desk             # back at your desk
```

### Hot-desk dock setup

```sh
wdm save desk                # one time
# next time you plug in the dock:
wdm watch --json | jq -r 'select(.kind=="added")' | xargs -n1 wdm restore desk --no-confirm
```

### Dual-projector + iPad mirror (advanced)

```sh
wdm mirror 1 3               # iPad sidecar mirrors built-in
wdm main 2 --confirm         # projector becomes main, with auto-revert if mistaken
wdm save talk-twin
```

### Rear-projection / mirrored stage (flip the projector)

```sh
# IOKit framebuffer flip — Intel Macs and Apple-Silicon externals
# that expose IODisplayConnect:
wdm flip 2 horizontal --no-confirm

# Software overlay flip — every Mac, including AirPlay / Sidecar.
# Press Ctrl+C (or `pkill -f 'wdm flip-overlay'`) to stop.
wdm flip-overlay 2 horizontal
```

### Picture-in-picture preview (presenter sees the audience view)

```sh
# Live mirror of the projector in a draggable window on your built-in:
wdm pip 2 --on 1 --size 1280x720
# Same idea but flipped, e.g. for a teleprompter:
wdm pip 2 --on 1 --flip horizontal
```

### Demo on a "second screen" without one being plugged in

```sh
# Create a virtual 1920x1080 display, then PIP it onto the built-in so you
# can see it. Drag windows into the new display; everything works as if
# you'd plugged in a real monitor.
nohup wdm virtual create --name "Demo Screen" --mode 1920x1080@60 --hidpi >/tmp/v.log 2>&1 &
sleep 2
wdm list                              # third row appears
wdm pip "Demo Screen" --on 1 --size 1280x720 &
# … demo time …
pkill -TERM -f 'wdm virtual create'   # virtual display vanishes
pkill -TERM -f 'wdm pip'              # pip window closes
```

### Safe unplug (avoid the AppleHPM kernel panic — issue #1)

```sh
wdm save desk-A                  # snapshot first
wdm sleep                        # drains AppleHPM, then macOS sleeps
# … unplug the projector cable while the lid / display is asleep …
# wake the Mac → `wdm restore desk-A` if needed
```

---

## The safety model

Every mutating command goes through three layers of revert. **You cannot break out of this** by accident:

```
┌────────────────────────────────────────────────────────────┐
│ 1. SafeTransaction                                         │
│    ─ pre-snapshot                                          │
│    ─ apply                                                 │
│    ─ confirm (terminal prompt | native HUD | scripted)    │
│    ─ on no/timeout: re-apply pre-snapshot via ProfileApplier│
└────────────────────────────────────────────────────────────┘
                       ↓ on crash mid-mutation
┌────────────────────────────────────────────────────────────┐
│ 2. `last` profile                                          │
│    ─ MutationDispatch writes pre-state to                  │
│      `~/.config/wdm/profiles/last.json` BEFORE apply       │
│    ─ recover with `wdm restore last`                       │
└────────────────────────────────────────────────────────────┘
                       ↓ on CG-side commit failure
┌────────────────────────────────────────────────────────────┐
│ 3. CGRestorePermanentDisplayConfiguration                  │
│    ─ fired automatically if CGCompleteDisplayConfiguration │
│      itself returns an error                               │
└────────────────────────────────────────────────────────────┘
```

Full sequence diagram in [`docs/safety.md`](docs/safety.md).

### Confirmation flags

```
(default)        terminal prompt on stderr (`y` within 15s to keep)
--confirm        native macOS HUD overlay with countdown (SPACE keep, any other key cancel)
--no-confirm     skip the prompt (use this in scripts and CI)
```

---

## Architecture

```
WDMCore     pure value types        Mode · DisplayInfo · Snapshot · Point · ArrangementEntry
   │
WDMSystem   effects                  DisplayProvider · CGDisplayProvider · FixtureDisplayProvider
   │                                 CursorIO · ProcessLister · ProcessSignaler · Screenshotter
   │                                 Recorder · PipFlipper · OverlayFlipper · DisplayCapturer …
   │
WDMKit      typed façade (SSOT)     WDMController · safety primitives · profile/scene stores
   │                                 typed errors (WDMError) · provider factories · alias overlay
   │                ┌────────────────┴────────────────┐
WDMCLI       thin   │                                  │   thin   WDMWeb (proof of concept)
   │                                                                JSON HTTP via Network.framework
wdm  executable                                              wdm-web executable
```

**Layering rule.** Dependencies only point downward. Frontends are siblings;
they never depend on each other. Every command goes through the `DisplayProvider`
protocol — the same code path is exercised in tests against a JSON-fixture provider
as on real hardware.

**Single source of truth.** Every user-visible verb has exactly one
`WDMController` op. Adding a verb = (1) add the Kit method (test-first),
(2) wrap it in each frontend that exposes it. Two frontends never duplicate
business logic. The CLI is the primary frontend; `wdm-web` ships as a proof
that the lib is interface-agnostic — same fixture, same output, no `WDMSystem`
imports.

Full breakdown in [`docs/architecture.md`](docs/architecture.md).

### Drive every verb from a non-CLI frontend

```sh
# Start the local web bridge (proof of concept; same lib, same fixture).
wdm-web --port 8080 &
curl -s http://127.0.0.1:8080/displays | jq                     # === wdm list --json
curl -s http://127.0.0.1:8080/arrangement | jq                  # === wdm arrange list --json
curl -s -X POST http://127.0.0.1:8080/arrangement \
  -d '[{"id":1,"origin":{"x":-1920,"y":0}},{"id":2,"origin":{"x":0,"y":0}}]'
                                                                 # === wdm arrange set @-
```

### AI-controllable GUI (planned: `wdm-mac --remote`)

The forthcoming Mac GUI (`wdm-mac`, see [meta #8](https://github.com/Arthur-Ficial/workshop-display-manager/issues/8) and [meta #99](https://github.com/Arthur-Ficial/workshop-display-manager/issues/99)) ships every interaction over a localhost API modelled on Vercel's `agent-browser` — `GET /ui/snapshot` is the primary machine-readable state surface, `GET /ui/events` is a live SSE stream, `POST /ui/click|scroll|drag|fill|…` covers every action a human can perform, and a halo overlay shows the local user what the AI just did. Off by default; `wdm-mac --remote` opens `127.0.0.1` with a per-launch token. Full contract in [`CLAUDE.md` § AI-controllable frontends](CLAUDE.md) and [`docs/superpowers/specs/2026-05-04-ai-controllable-gui-design.md`](docs/superpowers/specs/2026-05-04-ai-controllable-gui-design.md).

---

## Tests

```sh
make test                    # 190+ tests in 45 suites, hermetic, ~0.2s
make smoke                   # opt-in: runs read-only ops against your real displays
WDM_REAL_HARDWARE=1 swift test            # hardware-gated read smoke
WDM_REAL_HARDWARE_FLIP=1 swift test       # actually flips your external display, then restores
WDM_REAL_HARDWARE_ROTATE=1 swift test     # actually rotates, then restores
```

Every user-facing command has an end-to-end test that spawns through the actual `CLIRunner` against a JSON-fixture display provider. Hermetic, fast, no real hardware needed in CI.

The full **50-scenario workshop checklist** lives in `Tests/WDMCLITests/WorkshopScenariosE2ETests.swift` — each scenario is either covered by an existing test (referenced inline) or a `RED` `.disabled` stub that's the prioritized backlog.

---

## Building

```sh
make build                   # debug
make release                 # release with -warnings-as-errors
make test                    # full hermetic suite
make install                 # copies to /usr/local/bin/wdm
make clean
```

Zero third-party runtime dependencies. Swift 6, macOS 13+ deployment target.

---

## Documentation

- [`CLAUDE.md`](CLAUDE.md) — contributor contract: TDD iron law, modular rules, exit codes
- [`docs/architecture.md`](docs/architecture.md) — module boundaries, layering, why
- [`docs/safety.md`](docs/safety.md) — three-layer revert, sequence diagrams
- [`docs/workflows.md`](docs/workflows.md) — workshop / hot-desk / dual-projector walkthroughs
- [`docs/troubleshooting.md`](docs/troubleshooting.md) — known limitations + workarounds
- [`docs/contributing.md`](docs/contributing.md) — how to add a feature, the iron law
- [`docs/release.md`](docs/release.md) — maintainer release process

API reference (DocC) is published at https://Arthur-Ficial.github.io/workshop-display-manager/ on every push to `main`.

---

## License

Proprietary, all rights reserved. © 2026 Franz Enzenhofer / fullstackoptimization.com.

This is a private project, not licensed for use outside the copyright holder's workshops, projects, and infrastructure. See [`LICENSE`](LICENSE).
