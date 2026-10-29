# openshot-mcp

An MCP server that lets an AI agent (Claude Code, Codex, or any other MCP client) build a video
edit inside an [OpenShot](https://www.openshot.org/) 4.0 project file.

You give it a music track and a folder of clips. The agent finds the tempo, lays the clips out on
the beat grid, drops a marker at every section change, and saves the project. You then open the
project in OpenShot and finish the edit by hand, with everything already lined up to the music.

It was built for game trailers, where the raw material is a pile of short screen captures and a
score with a clear beat, but nothing in it is game specific.

## What it does

- **Imports media.** Any file ffprobe can read becomes an OpenShot file entry with the right
  frame rate, duration, and stream metadata.
- **Turns a music file into a beat grid.** Tempo and beat phase are detected with librosa and
  refined by searching for the grid that lines up best with the audio's onsets. Section changes
  are estimated from energy and onset density. If you already know the BPM and sections from your
  DAW, pass them in and skip detection.
- **Places clips on the grid.** Every cut lands on a beat, quantized to the project's frame rate
  with exact fractions so adjacent clips never drift apart.
- **Adds section markers** so you can see the musical structure on the OpenShot timeline.
- **Saves safely.** It backs up the project first, writes atomically, refuses to write while
  OpenShot has the project open, and refuses if the file changed on disk since it was loaded.

## What it does not do

- Drive the running OpenShot application. OpenShot has no API for that, so this server edits the
  project file. Close the project in OpenShot before saving, then reopen it.
- Render or export video. Use OpenShot for that.
- Make editorial decisions. The server exposes primitives; which clip goes where is up to the
  agent or the person driving it.
- Effects, transitions, titles, or keyframe animation (planned for a later version).

## Requirements

- Python 3.12 or newer
- ffmpeg (for the `ffprobe` command) on your PATH
- OpenShot 4.0.x to open the results. The project file format is checked on load and other
  versions are refused.

Developed and tested on Windows. The code has no Windows-only dependencies except the check that
detects an open OpenShot window, which is skipped on other platforms.

## Install

```sh
git clone https://github.com/alecray/openshot-mcp.git
cd openshot-mcp
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"     # on macOS/Linux: .venv/bin/pip
.venv/Scripts/python -m pytest -q         # should report all tests passing
```

Register the server with your MCP client. For Claude Code, add this to the project's `.mcp.json`
(adjust the path to wherever you cloned the repo):

```json
{
  "mcpServers": {
    "openshot": {
      "command": "/path/to/openshot-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "openshot_mcp"]
    }
  }
}
```

## Typical session

An agent working through the tools looks like this:

1. `open_project` on an existing `.osp`, or `new_project` to start a 720p 30 fps one.
2. `import_media` with the music file and every clip.
3. `analyze_music` on the music file. It returns the BPM, the offset of the first beat, and a list
   of section start times, and sets that grid as active. Or call `set_grid` with values you know.
4. `place_sequence` with a list of clips and how many beats each should last. Clips are laid back
   to back starting at beat zero. Use `add_clip` for anything that needs a specific spot.
5. `get_timeline` to review the result, then `save_project`.
6. Open the project in OpenShot.

## Tools

| Tool | Purpose |
|---|---|
| `open_project(path)` | Load an existing OpenShot 4.0 project |
| `new_project(path)` | Start a new HD 720p 30 fps project (written on save) |
| `import_media(paths)` | Probe files and add them to the project. Importing the same path twice returns the same id |
| `list_media()` | List imported files and their ids |
| `analyze_music(file_id, bpm?, offset_s?, sections?, apply?)` | Detect the beat grid from an audio file. Explicit values override detection |
| `set_grid(bpm, offset_s?, sections?, beats_per_bar?)` | Set the beat grid from known values |
| `get_grid(total_s?)` | Return the active grid, including beat times |
| `add_clip(file_id, layer, position_s, start_s?, end_s?, snap?)` | Place one clip. `snap` is `beat`, `bar`, or `none` |
| `place_sequence(layer, items, from_s?)` | Place several clips back to back on the grid |
| `update_clip(clip_id, ...)` | Move, trim, or retitle a clip |
| `remove_clip(clip_id)` | Delete a clip |
| `add_marker(position_s, title?)` / `clear_markers()` | Manage timeline markers |
| `get_timeline(layer?)` | List clips in order, with any gaps or overlaps |
| `validate_project()` | Check ids, references, bounds, and overlaps |
| `save_project(path?, backup?, force?)` | Write the project file |

Layers use OpenShot's numeric ids: `1000000` for L1 through `5000000` for L5.

## How the project file is written

- Existing content is left untouched. New files, clips, and markers are appended.
- New clips carry the full set of default properties captured from a real OpenShot 4.0 project
  (`templates/clip_defaults.json`), so OpenShot treats them exactly like clips it created itself.
- Media paths follow OpenShot's own rules: relative to the project folder when on the same drive,
  `@assets/...` for files in the project's assets folder, absolute otherwise.
- Thumbnails and waveform caches are not written. OpenShot regenerates them when it opens the
  project.
- Marker titles are stored but OpenShot does not display them; markers appear as icons.

## Accuracy notes

Tempo and beat phase detection is reliable on anything with a steady pulse. On the first real
trailer score it recovered 88.0 BPM exactly with an 18 ms offset. Section detection is a rough
guess and works best as a starting point; pass `sections` from your DAW when you know them.

## Repository layout

```
src/openshot_mcp/   server.py (MCP tools), project.py (project model and save logic),
                    media.py (ffprobe), grid.py (beat grid and audio analysis), lock.py
templates/          empty project and default clip properties captured from OpenShot 4.0
tests/              pytest suite with generated fixtures
docs/               design notes, decision records, specs, and reviews
```

## Contributing

Issues and pull requests are welcome. Run the tests before opening a PR. Commit messages follow
the Conventional Commits format (`feat:`, `fix:`, `docs:`, and so on), enforced by the hook in
`.githooks` once you run `git config core.hooksPath .githooks`.

## License

MIT. See [LICENSE](LICENSE).
