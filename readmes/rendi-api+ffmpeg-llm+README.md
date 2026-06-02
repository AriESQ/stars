# ffmpeg-llm

An FFmpeg plugin for Claude Code. Describe what you want, get the command.

A specialized ffmpeg plugin for when a general-purpose LLM isn't accurate enough. Use it to make Claude Code more reliable with ffmpeg. A few things it handles well:

- Files QuickTime can open
- Frame-accurate cuts at the timestamp you asked for
- HLS and DASH streams ready for the web


## Install

Inside Claude Code:

```
/plugin marketplace add rendi-api/ffmpeg-llm
/plugin install ffmpeg-llm@rendi-official
```

The first command registers this repo as a plugin marketplace; the second installs the plugin from it.

## Quick start

With the plugin loaded, describe what you want in plain English:

> *"burn the subtitles from sample.srt using Poppins 24pt"*

> *"high-quality GIF from clip.mp4, max 640px wide"*

> *"package input.mp4 as HLS VOD for a CDN"*

Or use the slash command:

```
/ffmpeg scale to 1080x1920 with black bars, web-optimized
```

For more complicated jobs (a filtergraph that won't compile, an encode that breaks on a real phone), Claude hands off to the `ffmpeg-expert` subagent.

## You describe the goal. Claude picks the flags.

No more researching **fast vs frame-accurate seek** or **quality-first vs size-first GIF**. Tell Claude what you actually care about ("smallest file", "plays on iPhone", "frame-accurate cut at 0:14") and the right approach falls out.

Covers transcoding, remuxing, trimming, filter graphs, audio, subtitles, GIFs, HLS/DASH, GPU encoding (NVENC/QSV/VAAPI).

## Handles the common gotchas

Two-dozen FFmpeg pitfalls are baked into the skills. A few:

- `setpts=PTS-STARTPTS` after `trim` for clean `concat` timing
- `FontName=` in subtitle filters uses the font's internal PostScript name
- `amix` uses both `duration=shortest` and the output flag `-shortest` for matched track lengths
- `fps`/`setsar=1`/`format=yuv420p` to normalize stream parameters before `concat`
- `-fps_mode passthrough` as the current frame-rate pass-through syntax
- `yadif` for clean deinterlacing of old AVI/WMV captures, including ones the metadata labels progressive

## License

MIT
