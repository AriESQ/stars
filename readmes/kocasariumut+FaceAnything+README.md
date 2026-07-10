<div align="center">

# Face Anything: 4D Face Reconstruction from Any Image Sequence

#### [Umut Kocasari](https://kocasariumut.github.io/) &nbsp;·&nbsp; [Simon Giebenhain](https://simongiebenhain.github.io/) &nbsp;·&nbsp; [Richard Shaw](https://scholar.google.com/citations?user=9qqtzK4AAAAJ&hl=en) &nbsp;·&nbsp; [Matthias Nießner](https://niessnerlab.org/members/matthias_niessner/profile.html)

### ECCV 2026

[![arXiv](https://img.shields.io/badge/arXiv-2604.19702-b31b1b)](https://arxiv.org/abs/2604.19702)
[![Project Page](https://img.shields.io/badge/Project_Page-green)](https://kocasariumut.github.io/FaceAnything/)
[![Video](https://img.shields.io/badge/▶_Video-red)](https://www.youtube.com/watch?v=wSGHpAscp0Y)
[![Code](https://img.shields.io/badge/GitHub-Code-black)](https://github.com/kocasariumut/FaceAnything)
[![Hugging Face Space](https://img.shields.io/badge/🤗_Hugging_Face-Space-blue)](https://huggingface.co/spaces/UmutKocasari/FaceAnything)

![teaser](assets/teaser.gif)

</div>

## Table of Contents

- [Overview](#overview)
- [What It Produces](#what-it-produces)
- [Installation](#installation)
- [Checkpoint](#checkpoint)
- [Usage](#usage)
- [Dataset](#dataset)
- [Acknowledgments](#acknowledgments)
- [Citation](#citation)
- [License](#license)

## Overview

Face Anything is a unified feed-forward model for high-fidelity 4D face
reconstruction and dense tracking from arbitrary image sequences. The key idea is
canonical facial point prediction, a representation that assigns each pixel a
normalized facial coordinate in a shared canonical space. This formulation
transforms dense tracking and dynamic reconstruction into a single canonical
reconstruction problem, producing temporally consistent geometry and reliable
correspondences.

## What It Produces

The teaser above is a single **grand tour** run: one orbit that morphs through
every modality. A full run writes:

| Output | Description |
|---|---|
| `videos/pointcloud.mp4` | Colored 3D point-cloud reconstruction (orbiting camera) |
| `videos/tracks.mp4` | 3D reconstruction with colorful, temporally-consistent point tracks |
| `videos/canonical.mp4` | 3D reconstruction colored by canonical facial coordinates |
| `videos/depth.mp4` | 3D reconstruction colored by depth |
| `videos/normals.mp4` | 3D reconstruction colored by surface normals (from depth) |
| `videos/grand_tour.mp4` | One orbit that morphs through all modalities (pointcloud → tracks → canonical → depth → normals) |
| `videos/grand_tour_2d.mp4` | The grand tour in image space (2D) |
| `videos/*_2d.mp4`, `maps/*` | Per-modality image-space (2D) videos and per-frame maps |
| `ply/{geometry,canonical,tracks}/frame_XXXX.ply` | Colored point clouds per timestamp (geometry, canonical, and tracks) |
| `cameras.npz`, `cameras.json` | Per-frame camera intrinsics and extrinsics |
| `raw_predictions.npz` | Raw `depth`, `intrinsics`, `extrinsics`, `canonical`, `conf`, `valid` |

## Installation

Face Anything needs a CUDA GPU. Tested with **Python 3.11 / PyTorch 2.9 (CUDA
12.8)**.

One-line setup (creates the conda env, installs everything, and downloads the
checkpoint):

```bash
git clone https://github.com/kocasariumut/FaceAnything.git
cd FaceAnything

bash install.sh
```

Or do it manually:

```bash
git clone https://github.com/kocasariumut/FaceAnything.git
cd FaceAnything

conda create -n faceanything python=3.11 -y
conda activate faceanything

# install PyTorch matching your CUDA, then the rest
pip install torch==2.9.0 torchvision==0.24.0 --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt

# install this package (exposes `faceanything` and `depth_anything_3`)
pip install -e .
```

`pip install -e .` is optional, since `run_inference.py` adds `src/` to the path
automatically, so once the dependencies are installed you can run it directly.

The architecture/config of the backbone is loaded from the public HuggingFace
model `depth-anything/DA3-GIANT-1.1` (downloaded automatically on first run; its
weights are then overwritten by our checkpoint). To use a local cache instead of
downloading, set `export HF_HOME=/path/to/hf_cache`.

## Checkpoint

Download the released `checkpoint.pt` (~15 GB) and place it at
`checkpoints/checkpoint.pt` (where it is loaded by default). `install.sh`
fetches it automatically; to do it manually, use either option below.

**Option 1: Google Drive**

```bash
pip install gdown
gdown --fuzzy "https://drive.google.com/file/d/1PdQQxzm-tU50RmJhgeoMCYVRlEiW3f8p/view?usp=sharing" \
    -O checkpoints/checkpoint.pt
```

**Option 2: Hugging Face** ([UmutKocasari/FaceAnything](https://huggingface.co/UmutKocasari/FaceAnything))

```bash
huggingface-cli download UmutKocasari/FaceAnything checkpoint.pt --local-dir checkpoints
```

(The Hugging Face model repository becomes public when the code is released.)

Use `--checkpoint /path/to/checkpoint.pt` to load it from elsewhere.

## Usage

```bash
python run_inference.py --input <INPUT> --output <OUT_DIR>
```

`<INPUT>` can be **a single image**, **a folder of images**, or **a video file**
(`.mp4/.mov/.avi/.mkv/...`). For a single image, the reconstruction is rendered
as a turntable orbit.

```bash
# image folder
python run_inference.py --input path/to/images --output output/demo
# video
python run_inference.py --input clip.mp4 --output output/clip
# single image
python run_inference.py --input face.jpg --output output/face
```

### Background removal

Backgrounds are removed automatically. If you don't provide masks, Face Anything
runs [Robust Video Matting](https://github.com/PeterL1n/RobustVideoMatting) to
segment the foreground and saves the generated masks to `<OUT_DIR>/masks`. You
can also supply your own masks with `--mask-dir /path/to/masks`, or disable
background removal entirely with `--no-background-removal` (use the full frame).

### Selecting outputs

Everything is produced by default. To produce a subset, pass a comma-separated
list to `--outputs` (choices: `pointcloud, depth, normals, canonical, tracks,
grandtour, ply, raw`):

```bash
python run_inference.py --input clip.mp4 --output output/clip \
    --outputs pointcloud,canonical,grandtour
```

### Processing modes & detail

`--process-mode` controls how frames are fed to the model, which trades off
surface detail against temporal/3D consistency:

* `all-at-once` (default): all frames are processed jointly, giving **more
  3D-consistent** results across the sequence but **less detailed** surfaces.
* `one-by-one`: each frame is processed independently, giving **more detailed
  surfaces** but **less 3D-consistent** results across frames. It also uses less
  memory, so it pairs well with a larger `--process-res` for higher-resolution,
  more detailed outputs.

### All options

<details>
<summary><b>Command-line options</b></summary>

| Flag | Default | Description |
|---|---|---|
| `--outputs` | `all` | subset of outputs to generate |
| `--max-frames` | all | cap the number of frames |
| `--process-res` | 504 | model resolution (increase for more detailed outputs) |
| `--process-mode` | all-at-once | `all-at-once` (joint: more 3D-consistent, less detail) or `one-by-one` (per-frame: more detailed surfaces, less 3D-consistent; lower memory) |
| `--stride` | 1 | use every N-th frame |
| `--render-size` | 1024 | output video resolution |
| `--point-size` | auto | point splat size (auto from resolution) |
| `--render-backend` | auto | `open3d` (smooth, default) or `torch` fallback |
| `--fps` | 10 | output frame rate |
| `--orbit` | `sway` | `sway` / `turntable` / `none` camera motion |
| `--orbit-amplitude` | 80 | sway amplitude in degrees (0 to -amp to 0 to +amp to 0) |
| `--orbit-frames` | 80 | number of orbit frames for a single-image input |
| `--n-tracks` | 100 | number of seeded point tracks |
| `--track-k` | 25 | canonical nearest-neighbours recolored per track |
| `--track-threshold` | 0.01 | max canonical distance for a correspondence |
| `--mask-dir` | (none) | use foreground masks from this directory |
| `--remove-background` | off | force RVM mask regeneration |
| `--no-background-removal` | off | reconstruct the full frame (no masks) |
| `--use-predicted-poses` | off | multi-view-consistent world frame instead of monocular |
| `--checkpoint` | `checkpoints/checkpoint.pt` | model checkpoint |
| `--save-frames` | off | also dump the individual rendered orbit frames |

Run `python run_inference.py --help` for the full list.

</details>

## Dataset

We release the **canonical maps** for the selected timestamps used in Face
Anything. To request access to the **FaceAnything NeRSemble** dataset, please
fill out [this form](https://forms.gle/AFFsq7T3dhqTzC7g9).

## Acknowledgments

Face Anything builds on [Depth-Anything-3](https://github.com/ByteDance-Seed/Depth-Anything-3).
We also thank the authors of [FLAME](https://flame.is.tue.mpg.de/),
[COLMAP](https://colmap.github.io/), and
[Robust Video Matting](https://github.com/PeterL1n/RobustVideoMatting) for their
open-source work, which we use in training data preparation and background
segmentation.

## Citation

```bibtex
@article{kocasari2026face,
  title={Face Anything: 4D Face Reconstruction from Any Image Sequence},
  author={Kocasari, Umut and Giebenhain, Simon and Shaw, Richard and Nie{\ss}ner, Matthias},
  journal={arXiv preprint arXiv:2604.19702},
  year={2026}
}
```

## License

[![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
