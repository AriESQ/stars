# Thauma Synth — Portable Alpha

Thauma Synth is a live visual synthesizer for Windows. It makes moving pictures from four shape
generators, mixes them, feeds the result back on itself to make trails and echoes, runs it
through an effects rack, and sends the picture to a screen, a projector or other programs. You
play it with the mouse, the keyboard and MIDI controllers.

This is an **alpha**: an early build shared with a few friends to try out. Expect rough edges,
and please tell Athron what you find (see [Reporting problems](#reporting-problems)).

> **Photosensitivity warning.** Thauma makes moving, colourful, sometimes fast-changing
> pictures. Thauma is built not to strobe (see [No strobing](#no-strobing)), but custom shaders
> from elsewhere and extreme settings can still flash. If you or anyone watching is sensitive to
> flashing light, take care.

---

## Download and run

1. Go to **Releases** on the right of this page and download
   `Thauma-Synth-Portable-Alpha-2026-10-17.zip`.
2. Unzip it anywhere you can write to: Desktop, Documents or a USB stick.
   **Not** `Program Files`: Thauma saves your looks and settings next to `Thauma.exe`.
3. Open the `Thauma Synth` folder and double-click **`Thauma.exe`**.

There is nothing to install and nothing is written outside that folder.

### "Windows protected your PC"

Thauma is not signed with a paid code-signing certificate, so Windows SmartScreen may warn you
the first time. Click **More info**, then **Run anyway**. That's normal for small apps shared
like this one. Only do it for a zip you got from this page.

### What you need

- Windows 10 or 11, 64-bit.
- A graphics card with OpenGL 3.3 or newer (any gaming card from the last ten years is fine).
- Two screens is ideal; one works too.

### Where things open

The picture and the control panel open on your **second screen**, so starting Thauma never
takes your main screen or keyboard away from other programs. With one screen, both open on it.
You can change this in the Setup window (F7): *monitor* for the picture, *panel_monitor* for
the panel.

---

## What it does

### Shapes

Four shape generators, A to D, each with its own colour, movement and mix level. There are
17 shape types: Bloom, Halo, Isobar, Lasso, Lava, Maze, Membrane, Murk, Nest, Palisade, Plume,
Pond, Reel, Starstream, Strata, Trace and Vault. Shapes can bend, colour or mask each other.

- **Reel** plays a video, a still picture or the webcam inside a shape. Any file FFmpeg reads
  plays: DXV, HAP, ProRes, H.264, H.265 and more, plus PNG, JPG, BMP, GIF, TIFF and WebP
  pictures. DXV, HAP and ProRes play backwards and bounce smoothly. H.264 and H.265 can stutter
  backwards.
- **Trace** draws the sound coming into your PC as a line.

### Trails and feedback loops

The mixed picture is fed back on itself to make trails. You set how long they last, how they zoom,
turn, drift and spin, and what comes back in from the edges (black, fold, tile or smear).

- **9 trail styles**: Wake, Iris, Glint, Shade, Inlay, Flipbook, Etch, Twin and Coil.
- **18 stages** that shape the feedback as it goes round: smoke, ink, tunnels, prisms, neon
  edges, kaleidoscope folds, melting, erosion, breathing and more.
- **Loops 2 to 4**: three more feedback loops, each with its own style, zoom, turn, drift, hue
  and edge. Each loop can sit on a single shape, after the trails, or after the effects.
- **Copy rate**: how many copies the feedback makes a second. It stays even whatever your
  frame rate does.
- **Paint**: draw into the trails with the mouse (P).

### Effects (FX page)

- **21 built-in effects**: Fold, Rosette, Tessera, Lenslings, Warble, Mosaic, Timeslice,
  Undertow, Splinter, Halation, Contour, Terrace, Dotscreen, Negative, Silver, Revenant, Corona,
  Rush, Whirl, Grade and Strata. Drag them into any order.
- **Only what you use is on screen.** Press **+ Add effect** to add a card for an effect. A
  card's **x** switches the effect off and hides it.
- **Focus knobs**: one set of knobs that moves whichever effect is in focus. Click a card or
  step with the arrows. Map them to a MIDI controller once and they reach every effect.
- **Chain strip**: the effects that are on, in the order they run.
- **8 custom shader slots** for ISF shaders (the `.fs` format VDMX and Resolume use). Every
  number, list and switch the shader has gets its own knob (up to 24 per slot). Colours and
  points get pickers, and events get buttons.
- **Shader browser** with categories, search and credits. About 50 shaders by other authors
  come with Thauma (credits in `custom-shaders\CREDITS.txt`).

### Movement (Motion page)

Four LFOs, a drunk walk, two 16-step sequencers, a random source and sound followers (level,
bass, mids, highs and kick) can move any control. **Eight macros** each move several controls
at once. Movement can follow tap tempo or a MIDI clock. Thauma limits how fast anything can
change, so movers never strobe.

### Looks

A **look** is a saved picture setup. Thauma comes with 17 starter looks.

- Save (Ctrl+S), save as new (Ctrl+Shift+S), and step through looks (Page Up / Page Down).
- Looks fade into each other. Right-click a look on the Looks page to give it a
  **Fade picture**, a transition drawn from the old look into the new one (13 come with Thauma).
- Snapshots A and B, morphing between them, **Mutate** (M) and **Evolve** (E) for happy
  accidents.
- Undo and redo for everything (Ctrl+Z / Ctrl+Y).

### Output

- **Spout**: other programs (OBS, Resolume, TouchDesigner, …) can take Thauma's picture.
  Pick the Spout source called **Thauma** (or **Thauma_1** if another program already uses
  the name). The picture stays on the graphics card, so this costs almost nothing.
- **Fullscreen** on whichever screen the picture is on: F11 or Alt+Enter.
- **Stage view** (F9): a simple gig screen with your Perform controls and looks.

### Panel and Setup

- Seven pages: Perform (F1), Shapes (F2), Trails (F3), FX (F4), Motion (F5), Looks (F6),
  Setup (F7).
- **Setup (F7)**: every setting with a plain name, grouped by topic. Each change works at once
  and is saved.
- The show bar along the top has tempo, sound meters, Undo/Redo, Clear trails, Freeze,
  Blackout and PANIC. The frames-a-second counter sits in the top-right corner. It turns red when
  Thauma runs slower than 90% of your frame cap.
- Ctrl+F finds any control by name.

---

## First steps

1. Start Thauma, press **F6** (Looks) and click a starter look.
2. Press **F2** (Shapes) and drag a few knobs. Drag **up and down** to turn a knob, and hold
   **Shift** for fine moves.
3. **Double-click** a knob to put it back. **Right-click** it for its menu: type a value, lock
   it, MIDI learn, see what moves it, or add it to the Perform page.
4. The **mouse wheel never changes a knob**. It only scrolls, so you can't bump a value by
   accident.
5. Press **F3** (Trails) and play with Amount, Zoom and Rotate. That's where most of the
   magic is.
6. Like what you see? **Ctrl+Shift+S** saves it as a new look.

### Handy keys

| Key | What it does |
|---|---|
| F1 – F7 | Panel pages |
| F8 / F9 | Presets drawer / Stage view |
| F11 or Alt+Enter | Fullscreen |
| B / F / C | Blackout / Freeze / Clear trails |
| Pause or Shift+Esc | Panic: calms everything down |
| T / Shift+T | Tap tempo / start a bar now |
| Ctrl+Z / Ctrl+Y | Undo / Redo |
| Ctrl+S / Ctrl+Shift+S | Save look / save as new look |
| Page Up / Page Down | Previous / next look |
| M / E | Mutate / Evolve on or off |
| Ctrl+F | Find a control |
| Ctrl + / Ctrl − / Ctrl+0 | Panel size |

---

## MIDI controllers

MIDI is **off** at first. Turn it on in Setup (F7), under MIDI.

- Thauma has ready-made maps for the **Novation Launch Control XL** and **Akai APC40** (mk1 and
  mk2). Any other controller gets a generic map. `CONTROLLERS.md` in the folder lists what every
  knob does.
- To put any control on any knob: right-click the control, choose **MIDI learn**, then move a
  knob.
- Tempo can follow a MIDI clock (Setup → MIDI).

The ready-made maps were checked with made-up MIDI messages. Real hardware may hold surprises.
Please report how yours behaves.

---

## Smooth motion: frame cap and Vsync

In Setup (F7):

- **Frame cap**: the most frames a second Thauma draws (60 at first). Set it to your screen's
  refresh rate, for example 120 on a 120 Hz screen.
- **Vsync**: turn it **on** for the smoothest motion. Without it, Thauma's frames and the
  screen's refreshes drift against each other, and every now and then a frame shows twice.
- If your graphics card can't keep up, the fps counter turns red. Lower the frame cap, or set
  *draw_scale* to 2, which draws at half size.

---

## No strobing

Thauma is built not to flash. A built-in check plays every shape type, trail style, stage,
effect, starter look and mover at its fastest. Anything that flashes more than three times a
second (the photosensitivity guideline) fails. The one style that flickers by nature,
**Flipbook**, has a **steady** switch that stops it.

Shaders from elsewhere were not made with that rule in mind. Try them at a few amounts before
showing them to anyone. Also, a shader that loops forever can stall your graphics card until
Windows resets it, so try new shaders before a show, not during one.

---

## Known limits of this alpha

- **Tested on one PC only.** Your graphics card, screens or Windows may behave differently.
- **Recording is switched off** in this build. Use OBS over Spout if you want to record.
- **Not tried with real files or hardware yet**: real HAP files and real DXV files exported from
  Resolume, a second webcam, and MIDI controllers plugged in for real.
- `README.txt` inside the zip is the long technical manual. A few parts of it are older than
  this build. Where it disagrees with this page (custom shader slots and knobs, recording),
  this page is right.

---

## Your files

Everything lives in the `Thauma Synth` folder:

| | |
|---|---|
| `Thauma.exe` | The program |
| `thauma-settings.txt` | Your settings (easiest to change in Setup, F7) |
| `presets\` | Your looks, the library and your controller setup |
| `custom-shaders\` | ISF shaders for the custom slots, with credits |
| `transitions\` | Fade pictures for look fades, with credits |
| `CONTROLLERS.md` | What every MIDI knob does |
| `README.txt` | The long technical manual |
| `THIRD-PARTY-LICENSES.txt` | Licences of every part Thauma uses |

Every save writes a new file and keeps the previous one as `.bak`. If Thauma ever crashes,
`crash.txt` next to `Thauma.exe` holds its last log lines. Problems at start are in
`startup-errors.txt`.

To move to a new version, copy your `presets` folder (and `thauma-settings.txt` if you like)
into the new folder.

---

## Reporting problems

Tell Athron directly. Useful things to send:

- what you did and what happened (a phone video helps a lot with visual glitches);
- your graphics card and Windows version;
- `crash.txt` or `startup-errors.txt` from the Thauma folder, if there is one.

---

## Licences

Thauma Synth is open source under the **MIT licence**, Copyright (c) 2026 Athron. See
[LICENSE](LICENSE).

Parts made by others are listed with their full licences in
[THIRD-PARTY-LICENSES.txt](THIRD-PARTY-LICENSES.txt): GLFW, GLEW, Spout2, nlohmann/json,
RtMidi, Dear ImGui, the MinGW-w64 and GCC runtime parts, the Quicksand font (SIL Open Font
Licence), and **FFmpeg** (LGPL 2.1 or later, built without any GPL parts). FFmpeg's complete
source code and the script that built it are in the zip under `FFmpeg\source`, and the FFmpeg
DLLs may be replaced with your own build of the same major version. The bundled custom shaders
and transitions belong to their authors. See the `CREDITS.txt` file in each folder.
