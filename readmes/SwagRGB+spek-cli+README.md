# spek-cli

`spek-cli` is a Rust command-line spectrogram viewer for quick audio inspection in the terminal.  
It is useful for checking frequency content, rolloff behavior, and noise floors across formats.

![Spectrogram Example - Showing frequency spectrum (0-22kHz) with color bar legend, axis labels, and spectral rolloff indicator](docs/spectrogram_example.png)

## Features

- High-resolution STFT spectrogram rendering (parallelized with `rayon`).
- Frequency/time axes and dB color legend on output image.
- Linear and logarithmic frequency scales.
- Optional spectral rolloff overlay (`--rolloff`, 85% cumulative energy threshold).
- Optional analysis overlays: spectral centroid, RMS/loudness trace, and peak frequency.
- Built-in palettes: `audacity`, `magma`, `viridis`, `inferno`, `grayscale`.
- Custom palette stops via `config.toml`.
- Broad decode support through `symphonia` (FLAC, MP3, WAV, ALAC, AAC, Vorbis, and more).
- Save as PNG (`--save`) or display in terminal via `viuer`.

## Color Palettes

Choose from 5 built-in color schemes:

<table>
  <tr>
    <td align="center">
      <b>Audacity</b> (Default)<br>
      <img src="docs/palette_audacity.png" width="400"/><br>
      <i>Classic blue-red-white gradient</i>
    </td>
    <td align="center">
      <b>Magma</b><br>
      <img src="docs/palette_magma.png" width="400"/><br>
      <i>Dark purple to bright yellow</i>
    </td>
  </tr>
  <tr>
    <td align="center">
      <b>Viridis</b><br>
      <img src="docs/palette_viridis.png" width="400"/><br>
      <i>Purple to green to yellow</i>
    </td>
    <td align="center">
      <b>Inferno</b><br>
      <img src="docs/palette_inferno.png" width="400"/><br>
      <i>Black to red to bright yellow</i>
    </td>
  </tr>
  <tr>
    <td align="center" colspan="2">
      <b>Grayscale</b><br>
      <img src="docs/palette_grayscale.png" width="400"/><br>
      <i>Simple black and white</i>
    </td>
  </tr>
</table>

Use `-p` or `--palette` flag to select: `spek-cli audio.flac -p magma`

## Installation

### Arch Linux

1. Install Rust:
```bash
sudo pacman -S rust
```
2. Clone and build:
```bash
git clone https://github.com/SwagRGB/spek-cli
cd spek-cli
cargo build --release
```
3. Install (optional):
```bash
sudo cp target/release/spek-cli /usr/local/bin/spek-cli
```

### Other Distributions

Install Rust via `rustup`, then build from source with the same commands.

## Usage

Basic usage:
```bash
spek-cli path/to/audio.flac
```

### Options

| Flag | Description |
|------|-------------|
| `-w, --width <PX>` | Output width in pixels |
| `-H, --height <PX>` | Output height in pixels |
| `--log` | Use logarithmic frequency scale |
| `--no-log` | Force **linear** frequency scale for this run (overrides config) |
| `-p, --palette <NAME>` | Built-in palette: `audacity`, `magma`, `viridis`, `inferno`, `grayscale` |
| `-q, --quiet` | Suppress progress and metadata output |
| `-s, --save <FILE>` | Save spectrogram to PNG file instead of displaying |
| `-v, --verbose` | Show timing statistics after processing |
| `--no-verbose` | Disable timing statistics for this run (overrides config) |
| `--rolloff` | Show **spectral rolloff** indicator line (85% energy threshold) |
| `--no-rolloff` | Disable spectral rolloff indicator for this run (overrides config) |
| `--overlay-centroid` | Draw spectral centroid overlay line |
| `--overlay-rms` | Draw RMS/loudness overlay line |
| `--overlay-peak` | Draw peak-frequency overlay line |

### Examples

Analyze with logarithmic scale and rolloff:
```bash
spek-cli music.flac --log --rolloff
```

Save a high-resolution PNG with Magma palette:
```bash
spek-cli music.flac -p magma -w 3000 -s output.png
```

Batch-style run (quiet mode):
```bash
spek-cli music.flac -q -s spectrogram.png
```

Temporarily override config defaults set to `true`:
```bash
spek-cli music.flac --no-log --no-rolloff --no-verbose
```

Enable all analysis overlays:
```bash
spek-cli music.flac --overlay-centroid --overlay-rms --overlay-peak --save overlays.png
```

## Understanding the Spectrogram

### Spectral Rolloff Indicator

`--rolloff` draws a line at the frequency below which 85% of frame energy is contained.

![Rolloff Indicator Example](docs/rolloff_example.png)

How to interpret it correctly:
- Lower rolloff often means less high-frequency energy.
- A sharp cutoff can indicate bandwidth-limited content (common in lossy sources).
- Rolloff alone is not proof of codec quality; use it with the full spectrogram pattern and source context.
- Absolute numbers depend on sample rate, mastering, and content type.

### Analysis Overlays

Overlays are meant to be read one-at-a-time first, then combined if needed.
The examples below use **grayscale palette + linear scale** (`-p grayscale --no-log`) for clarity.

**Baseline (no analysis overlays):**

![Baseline Spectrogram](docs/overlay_base.png)

**1) Spectral Centroid (`--overlay-centroid`)**

![Centroid Overlay](docs/overlay_centroid.png)

What it is:
- Frequency "center of mass" of each frame.

Why use it:
- Tracks overall brightness/dullness trend over time.
- Useful for spotting sections that become darker/brighter in tone.

**2) Peak Frequency (`--overlay-peak`)**

![Peak Overlay](docs/overlay_peak.png)

What it is:
- Frequency of the strongest spectral bin per frame.

Why use it:
- Tracks dominant tonal content or resonant peaks.
- Useful for seeing lead-note movement and strong narrow-band energy.

**3) RMS / Loudness Trend (`--overlay-rms`)**

![RMS Overlay](docs/overlay_rms.png)

What it is:
- Frame-level RMS energy trend, plotted as a relative line.

Why use it:
- Visualizes dynamics between quieter and louder sections.
- Useful for quick macro-level loudness contour checks.

Notes:
- RMS is normalized within the current file; do not compare its absolute y-position across files.
- Overlay lines are guides, not replacements for reading full spectrogram texture.

**All overlays together (with legend):**

![All Overlays](docs/overlay_all.png)

Combined mode is useful for deeper inspection, but can look busy. Start with one overlay, then add others as needed.

### Decibel (dB) Scale

The color bar represents relative spectral intensity in dB:
- Near `0 dB`: strongest components.
- Near `-100 dB`: very low-level content/noise floor.

## Configuration

On first run, `spek-cli` creates:

`~/.config/spek/config.toml`

CLI flags override config for that run, including explicit disable flags (`--no-log`, `--no-rolloff`, `--no-verbose`).

### Example Config
```toml
[defaults]
width = 2048
height = 1024 
log_scale = false      # true => log scale by default
palette = "audacity"   # built-in default palette name
rolloff = false        # true => show rolloff by default
verbose = false

[colors]
# Optional custom palette stops.
# If provided and non-empty, these are used unless CLI palette is explicitly set.
# stops = [
#     { position = 0.0, color = "#000000" },
#     { position = 1.0, color = "#FFFFFF" }
# ]
```

## Terminal Support

For best inline rendering, use a terminal with image protocol support (for example Kitty or WezTerm).  
You can always save output to PNG via `--save` if terminal image rendering is limited.
