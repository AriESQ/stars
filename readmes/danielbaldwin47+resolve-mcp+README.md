# resolve-mcp

An MCP server that gives Claude Code hands inside **DaVinci Resolve Studio** — so the
musical and editorial reasoning happens in Claude and the mechanical work happens in Resolve.

Build contract: [issue #22](https://github.com/danielbaldwin47/resolve-mcp/issues/22)
(closed — the build is complete).

## Status

**v0.1.0** — the spec #22 build, complete: all four pillars (foundation, titling, the
style-driven concert cut, the transcript-driven rough cut), 40 tools. The fake tier,
mypy strict and ruff gate every PR; the live smoke tier last ran fully green against
Resolve Studio on the Windows 11 box (32 passed, 6 skipped, 2026-08-11).

The tools below are the mechanics. How an edit session actually runs — what the
director hands over, the analysis prep, the mandatory self-reviews, the review rounds —
is process, and lives in [`docs/agents/concert.md`](docs/agents/concert.md) (the concert
pillar) and [`docs/agents/rough-cut.md`](docs/agents/rough-cut.md) (the rough-cut
pillar); the taste the concert cut is measured against lives in `styles/`.

| Tool | What it does |
| --- | --- |
| `get_status` | Connection state, Resolve version, current project + timeline, fps |
| `list_projects` | Project names in the current database folder |
| `load_project` | Loads a project by name; the result echoes the new context |
| `snapshot_project` | Writes an opaque `.drp` backup before a big operation |
| `import_media` | Imports files and image sequences into a bin, still-duration workaround applied |
| `list_media` | Summarises media pool clips, with offline state; spills big listings to disk |
| `inspect_clip` | One clip in full: properties, metadata, audio mapping, markers, dual-time bounds |
| `set_clip_metadata` | Batch metadata writes, each field routed by what the clip reports |
| `organize_media` | Batch bin operations: create nested bins, move clips |
| `relink_media` | Points offline clips at media that moved (folder relink or file replace) |
| `list_timelines` | Timelines with version, duration, fps and track stack; names the newest cut |
| `inspect_timeline` | One timeline at a chosen detail and range, in dual time; `make_current` to read the flags Resolve only answers for the open timeline |
| `list_markers` | Markers in record time, narrowed by colour and range |
| `set_markers` | Batch marker writes; an existing marker is never overwritten unless asked |
| `export_timeline` | Writes a timeline out as OTIO, FCPXML or DRT |
| `import_timeline` | Materialises a **new** timeline from such a file — never overwrites one |
| `get_cut_schema` | The cut-file contract, its annotated example and the validation rules |
| `validate_cut` | Dry-runs a cut file: every error and warning at once, with fix hints |
| `build_timeline` | Builds a cut file into a fresh `<name> v<N>` timeline and verifies what landed |
| `swap_take` | Flips a built segment to one of its `alternates[]` in place — the one edit that skips the rebuild |
| `virtual_transcript` | Reads a cut file back as the words it will contain — the rough-cut self-review, run before every version ships |
| `get_titles_schema` | The titles-file contract, its annotated example and the validation rules |
| `validate_titles` | Dry-runs a titles file before the Titles track is touched |
| `apply_titles` | Places Text+ and PNG titles from `titles.json` onto an owned Titles track, fades and all |
| `list_titles` | Reads the Titles track back: what each placed title says and which inputs it exposes |
| `edit_title` | Fixes one placed title in place — its words or its exposed params, neighbours untouched |
| `grab_frames` | Grabs chosen moments on a clip as JPEGs (≤1568px) the agent reads off disk |
| `detect_scene_cuts` | Job: catalogs where a clip changes shot, gist inline and the full list on disk |
| `analyze_occlusion` | Job: scores how much of an angle a near-field body blocks, and returns the windows to keep a cut out of |
| `analyze_quality` | Job: scores an angle for sharpness, exposure, clipped highlights and stability, and returns the windows that miss the floors |
| `separate_stems` | GPU stem separation: mix → 4 stems, drums → kick/snare/toms/ride/crash, and on `split_wind` other → wind/comp |
| `transcribe_audio` | Job: word-level transcript of a source clip or the timeline mix, with confidence and measured silence spans |
| `analyze_music` | Job: beats, downbeats and energy of a mix WAV |
| `analyze_structure` | Job: tune boundaries from applause, gated by musical pulse; `solos=true` adds solo changes measured off the stems |
| `detect_drum_fills` | Job: drum fills from the separated drum stems, confidence-gated |
| `detect_phrases` | Job: phrase boundaries in the soloist's stem |
| `correlate_timeline` | Job: measures a cut against the music it was cut to — beat/transient offsets, bar position, tune, who's out front, per shot. Reports; never judges |
| `list_render_presets` | The project's render presets, spelled the way `render_timeline` needs |
| `render_timeline` | Renders a timeline or a range of one as a background job |
| `get_job` | Polls one background job: progress, result, or a structured failure |
| `list_jobs` | Lists jobs newest first — how a restarted session finds what it started |
| `run_python` | Escape hatch: runs scripting-API Python in the server process |

Bin paths are slash-separated from the media pool root (`Concert/Angles`) and
case-sensitive. A clip counts as **offline** when it has a file path that is not on
disk — Resolve's scripting API exposes no offline flag.

Interchange is the **structural escape hatch**. The scripting API cannot cut a transition,
so a dissolve is made by exporting the cut to OTIO, editing the transition into that
document, and importing it back. An `.otio` or `.fcpxml` import is given a name no timeline
in the project answers to — colliding names walk the `<base> v<N>` convention. A `.drt` is
Resolve's own document and accepts no import options at all, so it names its own timeline;
what holds there is the check on the way out. Either way the cut already in the project is
never the thing that gets written over.

Three fields read `null` on any timeline that is not the one open in Resolve: a track's
`enabled` and `locked`, and a shot's `takes`. Resolve answers those from editor state and
reports `False`/`0` for every other timeline — no error to catch, just a plausible wrong
number — so the server reports "unknown" rather than passing it on. The `currency` block in
the reply names them, and `make_current` switches to the timeline for the read and switches
back when you want the real values. It is opt-in because the switch is visible in the
Resolve window. [ADR 0004](docs/adr/0004-editor-state-getters-only-answer-for-the-current-timeline.md)
has the sweep that established which getters this covers, and which are proven safe.

Editing is declarative and split across two files that never mention each other. The
**cut file** owns the cut and materialises as a new `<name> v<N>` timeline every build.
**`titles.json`** owns the titles, and `apply_titles` owns the topmost video track named
`Titles` — every apply clears that track whole and re-places from the file, so the same
file always produces the same track. Title positions are offsets from the *blue marker*
naming their song rather than timeline frames, which is what lets one titles file be
re-applied unchanged to every rebuild.

Each event picks one of two routes, and both land in the same pass. **Text+** places an
instance of a GUI-authored template and writes its words and its fade into that instance's
Fusion comp — clip-level fades are not exposed to the scripting API at all, so the fade is
an opacity spline. **PNG** places a designed card exported to frames with alpha, its words
and its ramps already in the pixels; the server consumes cards, never generates them. A
card is imported once into `04_Assets/Text/<song>` and found rather than re-imported on
every later apply, and gets the one-time out-point write that makes Resolve honour the
requested length instead of dropping every image at the default still duration.

A typo is the exception to all of that. `edit_title` writes new words or new exposed
params straight into one already-placed Text+ instance — no clear, no append, no rebuild —
and proves it reached only that one by reading every other title on the track before and
after the write. `list_titles` is how you find the title and see which Fusion input ids it
exposes, since a media-pool template has no comp to ask. The edit changes the *timeline*
and not `titles.json`, so the next `apply_titles` puts the old wording back: fix the file
too whenever the change is one worth keeping.

Heavy work runs as a background job: every starter replies `{"job": record}` immediately —
one shape whichever starter it was — `get_job`
polls it, and results are cached under the cache root against the media and the parameters,
so an unchanged rerun is instant. Job records live on disk, which is what lets `list_jobs`
recover after a restart — a job that was still running when the server went down comes back
`failed` with code `job_interrupted`. Audio acquisition is internal to the starters: a
timeline is exported through Resolve's render queue (the only route that captures the
timeline *mix*, 48 kHz/24-bit WAV), a single source clip is extracted with ffmpeg unless its
audio mapping says the audio is linked or offset away from the file.

Seeing the picture takes two routes, both reading the file on disk rather than rendering
anything. `grab_frames` is not a job — a seek and one frame is faster than a poll would be,
so it runs inline and hands back JPEG paths at or under the client's 1568px image cap, cached
against the media all the same. `detect_scene_cuts` decodes the whole clip, so it is a job:
the catalog of every cut and shot goes to the cache in dual-time JSON and only a gist (how
many cuts, the shot lengths, the first few times, the path) comes back inline.
`analyze_occlusion` answers the question that comes before either: is anyone's head, hat or
back between this camera and the stage? It samples a range at about a frame a second, scores
each sample on near-field blocking, and returns the *windows* — the stretches to keep a cut
out of — with the whole per-sample curve on disk behind them. `analyze_quality` is its
sibling and answers the other half: not whether something is in the way, but whether the
picture the camera got is worth cutting to. Four readings a sample — sharpness, exposure,
clipped highlights and stability — three floors that decide what is unusable, and windows in
the same shape, each saying which floor it missed. A steady pan scores as stable and a cut is
unmeasurable rather than unstable; the floors are calibrated on real deliverables
(`docs/reference/image-quality-calibration.md`). `correlate_timeline` takes a scan of a
rendered cut and puts the four readings on that cut's own shots.

Deliverables come off one timeline the same way: `render_timeline` renders with a **preset**
— what a preset renders was decided in the Deliver page and saved there, so the server
overrides only where the file goes and which frames it covers. Name none and the configured
default is used (`H.265 Master`, a Resolve built-in; `RESOLVE_MCP_DEFAULT_RENDER_PRESET`
points it elsewhere), and the job says which preset ran and whether it was the default or
explicit. An unknown name is refused with the list of names that exist, never swapped for a
near-enough preset. On top of that goes an optional half-open
`[start, end)` range in the timeline's own frames, the numbers `inspect_timeline` and
`list_markers` report. That is a per-song file out of a concert set. Without a `target_dir`
the file lands in the cache's `renders` folder, which the server replaces freely on a
re-render; a directory you name is yours, and a file already sitting there is refused until
you pass `refresh`.

## Requirements

- Windows 11, DaVinci Resolve **Studio** 21.0.3 (external scripting must be enabled:
  _Preferences > System > General > External scripting using_ = **Local**)
- **CPython 3.12 x64 installed from python.org** — not a uv-managed interpreter. See
  [ADR 0001](docs/adr/0001-python-interpreter-must-be-a-registered-install.md): the
  Resolve scripting library crashes the process outright on a standalone build, so the
  server refuses to attach on one. [uv](https://docs.astral.sh/uv/) still manages the
  venv and the lockfile.
- Resolve running, with a project open, before the first Resolve-touching tool call
- **ffmpeg on PATH** for per-clip audio extraction, frame grabs and scene-cut detection
  (`RESOLVE_MCP_FFMPEG` points at it elsewhere). Timeline-scope audio goes through Resolve's
  own render queue and needs none. The analysis extra's torchcodec decodes through the
  FFmpeg **shared** DLLs (the `avcodec-*.dll` family), which the static executable does not
  carry — a separate install; `winget install Gyan.FFmpeg.Shared` puts them on PATH.
- **[python-audio-separator](https://github.com/nomadkaraoke/python-audio-separator) on
  PATH** for `separate_stems` (`pip install "audio-separator[gpu]"`, or
  `RESOLVE_MCP_AUDIO_SEPARATOR` points at the executable). It is run as a subprocess, not
  imported, so it can live in its own environment and its torch/CUDA stack never loads
  into the server. The two model files download on first use.
- **`uv sync --extra analysis`** for transcription and music analysis. The extra carries
  faster-whisper *and* the CUDA 12 runtime it needs (~1.3 GiB): the transcriber takes the
  GPU by default, and a runtime nobody installed is the one thing that breaks it. No
  hand-installed wheels, no `PATH` set before launch — the server puts the venv's own copy
  within reach. A box without an NVIDIA card still transcribes; set
  `RESOLVE_MCP_WHISPER_DEVICE=cpu` and expect it to be slow. The extra also carries the
  music stack (#37): `beat_this` (a git dependency — it has no PyPI release), torch,
  torchcodec, soundfile and `panns_inference`. On Windows torch, torchaudio and
  torchcodec come off the CUDA 13.0 wheel index rather than PyPI, which ships a CPU-only
  Windows wheel (#245); a box with no NVIDIA card still installs and imports them, and
  the beat and applause jobs warn that they are running on the CPU.
- **PANNs weights hand-placed in `~/panns_data/`** — `class_labels_indices.csv` and
  `Cnn14_DecisionLevelMax.pth` (327 MB), the two files `panns_inference` would fetch on
  first use via `os.system('wget …')`, which Windows does not have. The two fetches it
  would run: the weights from
  <https://zenodo.org/record/3987831/files/Cnn14_DecisionLevelMax_mAP%3D0.385.pth?download=1>
  (saved as `Cnn14_DecisionLevelMax.pth`) and the labels from
  <http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/class_labels_indices.csv>. No test tier can see this stack break —
  [ADR 0002](docs/adr/0002-analysis-models-are-injected-not-depended-on.md) injects the models,
  so the fakes stay green while real inference dies at import. The receipt that the
  installed stack works is `uv run pytest tests/test_live_analysis.py -m live`.

## Install

```sh
uv venv --python "C:/Users/<you>/AppData/Local/Programs/Python/Python312/python.exe"
uv sync
```

`uv sync` alone will pick a uv-managed interpreter, which runs the unit suite fine but
cannot attach to Resolve.

## Run

```sh
uv run resolve-mcp
```

The server speaks MCP over stdio and logs to stderr only. Register it with Claude Code:

```sh
claude mcp add resolve -- uv --directory C:/Users/Daniel/repos/resolve-mcp run resolve-mcp
```

## Configuration

Zero-config by default; every path has an environment override.

| Variable | Default | Purpose |
| --- | --- | --- |
| `RESOLVE_SCRIPT_API` | `%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting` | Scripting API root (holds `Modules/DaVinciResolveScript.py`) |
| `RESOLVE_SCRIPT_LIB` | `C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll` | Scripting library |
| `RESOLVE_MCP_CACHE` | `%LOCALAPPDATA%\resolve-mcp` | Cache root: snapshots, job records, cached results, acquired audio, grabbed frames, analysis catalogs, separated stems, model weights |
| `RESOLVE_MCP_FFMPEG` | `ffmpeg` (found on PATH) | ffmpeg executable used for per-clip audio extraction, frame grabs and scene-cut detection |
| `RESOLVE_MCP_AUDIO_SEPARATOR` | `audio-separator` (found on PATH) | python-audio-separator CLI used for stem separation |
| `RESOLVE_MCP_SEPARATOR_ALLOW_CPU` | `0` | A separator whose torch is the CPU build (`+cpu`) refuses to run — a GPU-capable box with that install is misconfigured, and the error names the fix. `1` accepts the CPU run on a box with no CUDA device; it is then a warning on the job record |
| `RESOLVE_MCP_STEM_MODEL` | `htdemucs_ft.yaml` | Pass one: the 4-stem model (vocals, drums, bass, other) |
| `RESOLVE_MCP_DRUM_MODEL` | `MDX23C-DrumSep-aufr33-jarredou.ckpt` | Pass two: the drum decomposition model (kick, snare, toms, ride, crash) |
| `RESOLVE_MCP_DEFAULT_RENDER_PRESET` | `H.265 Master` | Render preset `render_timeline` uses when the call names none. Must be a preset the project offers — an unknown name is refused, never swapped for another |
| `RESOLVE_MCP_WHISPER_DEVICE` | `auto` | Device faster-whisper transcribes on: `auto`, `cuda` or `cpu`. `auto` takes the GPU whenever there is one |
| `RESOLVE_MCP_WHISPER_COMPUTE_TYPE` | `default` | Precision: `default` is the model's stored precision (float16 for `large-v3`, widened to float32 on CPU). `float32` on `cuda` gives CPU-identical numbers at GPU speed |
| `RESOLVE_MCP_LOG_LEVEL` | `INFO` | Log level for the stderr logger |
| `RESOLVE_MCP_ALLOW_ANY_PYTHON` | unset | Bypass the interpreter check (see ADR 0001) |

## Development

```sh
uv run pytest                 # unit suite — runs with Resolve closed, against the fake seam
uv run pytest -m live         # live smoke tier — needs real Resolve running, on a python.org interpreter
uv run mypy                   # type check
uv run ruff check .           # lint
```

Tests exercise external behaviour only: they call the tool functions in-process (no stdio
transport) against a fake Resolve API object substituted at the connection singleton.
