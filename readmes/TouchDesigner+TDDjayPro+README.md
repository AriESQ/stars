# djay Pro ⇄ TouchDesigner

A TouchDesigner receiver for djay Pro's OSC stream. Listens on a single UDP port, splits incoming traffic by purpose (streams, parameters, state, metadata, unknown), and routes every value to one or more of:

- **CHOPs** for animation-driving numeric channels
- **Tables** for inspectable per-turntable snapshots
- **Callbacks** for reacting to discrete state transitions

Pick whichever fits how you want to consume the value — a continuous knob is most useful as a CHOP channel, a "what's loaded right now" lookup wants the table, and a state edge wants the callback.

## Installation

Using DJjay Pro main menu access, the Settings dialog. In the advanced section ensure the Target Port is set to 10000 and the Listen Port is set to 10001. Click the Start button.

<img width="642" height="97" alt="Screenshot 2026-05-05 at 12 52 51 PM" src="https://github.com/user-attachments/assets/13b24153-9eb4-479e-b9cd-2afb63c46d27" />


## OSC namespace

djay Pro v3 publishes under two top-level scopes (note: prefix is `/djay`, not `/djayPro`):

```
/djay/turntable<N>/<category>/<...>     N ∈ {1, 2, 3, 4}
/djay/mixer/<...>
```

All values are floats on the wire; strings carry song metadata and FX names.

## Data taxonomy

Channels are classified by how they behave, independent of namespace. This drives where they go in the receiver.

| Kind | Cadence | Examples | Surface |
|---|---|---|---|
| **stream** | per-frame (60 Hz) | `playback/time`, `song/bpm`, `neuralmix/*/audibleVolume`, `mixer/turntable<N>/meter` | CHOP only |
| **parameter** | on user input | `neuralmix/*/level`, `fx/*/dryWet`, `loop/inTime`, `mixer/crossfader` | CHOP + table |
| **state** | on transition | `playback/playing`, `song/loaded`, `loop/active`, `fx/*/active`, `neuralmix/*/mute\|solo` | CHOP + table + callback |
| **metadata** | on song load | `song/title\|artist\|album\|genre\|key\|duration`, `fx/*/type` | Table + callback |

## Per-turntable channels

For each turntable `<N>` ∈ {1,2,3,4}:

### playback

| Address | Kind | Type | Notes |
|---|---|---|---|
| `playback/time` | stream | float | Track position, seconds |
| `playback/bar` | stream | int-valued float | Current bar (1-based) |
| `playback/beat` | stream | int-valued float | Current beat in bar |
| `playback/phase` | stream | float | Phase within beat, 0–1 |
| `playback/barPhase` | stream | float | Phase within bar |
| `playback/playing` | state | 0/1 | Transport state |

### song

| Address | Kind | Type | Notes |
|---|---|---|---|
| `song/bpm` | stream | float | Current playback BPM (varies with pitch fader) |
| `song/loaded` | state | 0/1 | Track present on deck |
| `song/duration` | metadata | float | Track length, seconds |
| `song/key` | metadata | float | Numeric key code; `-1` = unknown |
| `song/title` | metadata | string | |
| `song/artist` | metadata | string | |
| `song/album` | metadata | string | |
| `song/genre` | metadata | string | |

### neuralmix

djay Pro v3 calls per-turntable stems "NeuralMix" on the wire. For each stem ∈ {`vocals`, `harmonic`, `drums`, `bass`}:

| Address | Kind | Type | Notes |
|---|---|---|---|
| `neuralmix/<stem>/audibleVolume` | stream | float | Stem level gated by mute, 0–2. Effectively `level × (1 − mute)` — drops to 0 when the stem is muted, otherwise tracks the knob. Does **not** include line fader, neuralmix EQ, or crossfader, despite what the v3 spec implies — see [QUIRKS.md](QUIRKS.md). |
| `neuralmix/<stem>/level` | parameter | float | Slider value, 0–1 |
| `neuralmix/<stem>/mute` | state | 0/1 | |
| `neuralmix/<stem>/solo` | state | 0/1 | |

Per-turntable NeuralMix EQ (separate from the channel-strip mixer EQ below):

| Address | Kind | Type | Notes |
|---|---|---|---|
| `neuralmix/eq/low` | parameter | float | 0–2 (1.0 = unity) |
| `neuralmix/eq/mid` | parameter | float | 0–2 |
| `neuralmix/eq/high` | parameter | float | 0–2 |

### loop

| Address | Kind | Type | Notes |
|---|---|---|---|
| `loop/inTime` | parameter | float | Loop start, seconds |
| `loop/outTime` | parameter | float | Loop end, seconds |
| `loop/beats` | parameter | float | Loop length in beats (e.g. 4.0) |
| `loop/active` | state | 0/1 | |

### fx

For each slot ∈ {`1`, `2`, `3`}:

| Address | Kind | Type | Notes |
|---|---|---|---|
| `fx/<slot>/active` | state | 0/1 | |
| `fx/<slot>/type` | metadata | string | e.g. `"Echo"`, `"Space Hop"` |
| `fx/<slot>/dryWet` | parameter | float | |
| `fx/<slot>/parameterContinuous` | parameter | float | Knob in continuous mode |
| `fx/<slot>/parameterIsBeats` | state | 0/1 | Knob mode toggle |
| `fx/<slot>/parameterBeats` | parameter | float | Knob in beats-quantized mode |

## Mixer channels (global)

| Address | Kind | Type | Notes |
|---|---|---|---|
| `mixer/crossfader` | parameter | float | 0–1, center = 0.5 |
| `mixer/turntable<N>/lineFader` | parameter | float | Per-turntable channel fader |
| `mixer/turntable<N>/eq/low` | parameter | float | 0–2 (1.0 = unity), channel-strip low band |
| `mixer/turntable<N>/eq/mid` | parameter | float | 0–2 |
| `mixer/turntable<N>/eq/high` | parameter | float | 0–2 |
| `mixer/turntable<N>/meter` | stream | float | Per-turntable VU, **dB scale** (pre-fader, post-processing). `-300` = silence floor, `0` = start of "red" / clip warning (not the ceiling), up to `+24` and beyond in headroom. |

## Album art

JPEG bytes are too large for OSC, so djay Pro hands them over via an HTTP request/response handshake:

1. djay broadcasts `/djay/turntable<N>/song/artworkAvailable 1` when art is present on a deck.
2. `oscin_events_callbacks` replies with `/djay/request/turntable<N>/artwork http://127.0.0.1:9988/artwork/<N>` via `oscout1`.
3. djay HTTP-POSTs the JPEG body to that URL.
4. `webserver1` (port 9988) writes the bytes to `cache/artwork_<N>.jpg`, pulses `artwork_<N>` (a moviefileinTOP) to reload, and fires `onArtworkReady`.

When the art goes away — `artworkAvailable` flips to `0`, or djay POSTs a 0-byte body — the cache file is stamped with `assets/black.jpg` (a 1×1 black seed) and `onArtworkCleared` fires, so the moviefileinTOP never shows a stale or invalid image.

The four `cache/artwork_<N>.jpg` files are committed as black seeds (`git update-index --skip-worktree` is set so runtime overwrites stay out of `git status`). On a fresh clone the moviefileinTOPs come up black; once djay broadcasts state, the real art lands within a frame or two.

We re-request on every `artworkAvailable=1` (not just rising edges) so a TD restart mid-session still pulls the current art without needing djay to bounce the flag.

## Sync — use Ableton Link, not OSC

For tight beat / bar / phase sync, **Ableton Link is the recommended path**, not the OSC playback channels. The receiver includes an Ableton Link CHOP at `/djayPro/ableton2` that joins the local Link session — when djay Pro has Link enabled (Global Volume Settings → Ablelton Link toggle), it participates in the same session and the timing is sample-accurate and continuous.

OSC's `playback/time`, `playback/phase`, and `playback/barPhase` are useful for *where in the track we are*, but they tick at packet rate (~60 Hz over UDP) and can stutter or drop under load. Use them for HUDs and read-state needs; use Link CHOP channels (`beat`, `phase`, `tempo`) when you're driving anything beat-synced visually.

Rule of thumb: **OSC for *what* is loaded / playing, Link for *when* the next beat lands.**

## Reading current values

Three places to look depending on what you're doing:

| Need | Use |
|---|---|
| Animate a viz from a continuous value | CHOP: `oscin_chan_stream`, `oscin_chan_parameter` |
| Inspect "what's loaded on deck 2 right now" | Table: `metadata_table[<field>, '2']` |
| Read a state boolean | Table: `state_table['playing', '<N>']` |
| Read a parameter value | Table: `parameter_table['<param>', '<N>']` or `mixer_table[<param>, 'value']` |
| React to a transition | Callback: see below |

All tables are transposed for readability — parameter names are rows, turntables are columns (`1`/`2`/`3`/`4`).

## Callbacks

Implement these in your callbacks DAT. Every callback takes a single `info: dict`.
Common keys: `info['ownerComp']`, `info['callbackName']`, `info['turntable']`.

### Playback / transport

| Callback | Trigger | Extra info |
|---|---|---|
| `onPlay(info)` | `playback/playing` 0 → 1 | — |
| `onPause(info)` | `playback/playing` 1 → 0 | — |

### Song lifecycle

| Callback | Trigger | Extra info |
|---|---|---|
| `onSongLoaded(info)` | `song/loaded` 0 → 1 (deferred by `Messagedeferwindow` s) | `title`, `artist`, `album`, `genre`, `key`, `duration` snapshotted in `info` |
| `onSongCleared(info)` | `song/loaded` 1 → 0 | — |

### Loop

| Callback | Trigger | Extra info |
|---|---|---|
| `onLoopSet(info)` | `loop/active` 0 → 1 | — |
| `onLoopClear(info)` | `loop/active` 1 → 0 | — |

### FX

| Callback | Trigger | Extra info |
|---|---|---|
| `onFxActive(info)` | `fx/<slot>/active` 0 → 1 | `slot`, `type` (str \| None — last-known FX name) |
| `onFxInactive(info)` | `fx/<slot>/active` 1 → 0 | `slot` |
| `onFxTypeChanged(info)` | `fx/<slot>/type` changes | `slot`, `type` |

### Stems (NeuralMix)

| Callback | Trigger | Extra info |
|---|---|---|
| `onStemMute(info)` | `neuralmix/<stem>/mute` 0 → 1 | `stem` |
| `onStemUnmute(info)` | `neuralmix/<stem>/mute` 1 → 0 | `stem` |
| `onStemSolo(info)` | `neuralmix/<stem>/solo` 0 → 1 | `stem` |
| `onStemUnsolo(info)` | `neuralmix/<stem>/solo` 1 → 0 | `stem` |

### Album art

| Callback | Trigger | Extra info |
|---|---|---|
| `onArtworkReady(info)` | djay POSTed JPEG bytes for a deck | `path` (cache file), `bytes` (length) |
| `onArtworkCleared(info)` | `artworkAvailable` 1 → 0, or empty-body POST | `path` (cache file, now a copy of `assets/black.jpg`) |

## Discovery

`oscin_unknown` listens for any address not in the known scope and logs it to `unknown_addresses` with a count and last-seen args. New addresses surface here automatically — useful when djay Pro adds something we haven't catalogued.

## Limitations

A few things djay Pro doesn't expose over OSC today (verified empirically — see [QUIRKS.md](QUIRKS.md)):

- **Cues / hotcues** — interacting with cue points produces no OSC traffic. There's no way to read cue positions, react to a cue jump, or know which hot-cues are set on a deck. Plan around it (e.g. drive cue-aware visuals from playback time, not cue events).
- **User-defined labels** — anything typed inside djay Pro (custom cue labels, named loops, tags) doesn't cross the OSC boundary. Only file-derived metadata (title/artist/album/genre) and built-in FX type names come through as strings.

## Roadmap (incoming from Algoriddim)

| Feature | Address | Notes |
|---|---|---|
| Dump request | `/djay/request/dumpAll` | Inbound OSC trigger that asks djay to re-broadcast its full current state. Coming in a future build. |

For a running list of djay Pro emission quirks discovered through testing, see [QUIRKS.md](QUIRKS.md).

## License

Shared Use License — see [LICENSE](LICENSE).
