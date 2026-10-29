# OpenShot-ComfyUI

OpenShot-ComfyUI is a focused set of ComfyUI nodes built for [OpenShot](https://www.openshot.org/). It exists to bring useful modern AI models into real editing workflows with simpler, more reliable, OpenShot-friendly integrations than most demo-oriented community graphs.

## Requirements

- ComfyUI
- PyTorch
- `ffmpeg` / `ffprobe`
- `git`
- Python `3.10` or `3.11` recommended

## Quick install

```bash
python -m pip install -r requirements.txt
python -m pip install --no-build-isolation git+https://github.com/facebookresearch/sam2.git

# Validate the install
python validate.py
```

Restart ComfyUI after install.

## How this works

- Wrap useful upstream models in simpler OpenShot-friendly nodes.
- Prefer practical, reliable workflows over demo-style graphs.
- Keep installs and first-use model downloads as simple as possible.

## What this includes

- `OpenShotDownloadAndLoadSAM2Model`
- `OpenShotSam2Segmentation` (single-image)
- `OpenShotSam2VideoSegmentationAddPoints`
- `OpenShotSam2VideoSegmentationChunked` (meta-batch/chunk friendly)
- `OpenShotGroundingDinoDetect` (text-prompted object detection -> mask + JSON)
- `OpenShotTransNetSceneDetect` (direct TransNetV2 inference -> IN/OUT JSON ranges)
- `OpenShotDeepFilterNetDenoiseAudio` (file-path based audio denoise -> FLAC path)
- `OpenShotLavaSRSpeechClarity` (LavaSR speech runner -> FLAC path)

## SAM2 nodes

These nodes are intended for practical OpenShot segmentation workflows, including image segmentation, promptable video segmentation, and chunk-friendly processing for longer clips.

- `OpenShotDownloadAndLoadSAM2Model` downloads and loads supported SAM2 checkpoints
- `OpenShotSam2Segmentation` handles single-image segmentation
- `OpenShotSam2VideoSegmentationAddPoints` adds prompt points for video workflows
- `OpenShotSam2VideoSegmentationChunked` is designed for chunked processing of longer videos

GroundingDINO and TransNetV2 are included alongside the SAM2 nodes to support object detection and scene boundary workflows that are useful in larger OpenShot pipelines.

## Audio denoise node

`OpenShotDeepFilterNetDenoiseAudio` is intentionally minimal:

- Input: `source_audio_path`, `noise_reduction`, `keep_model_loaded`
- Output: a new FLAC file path
- The node uses the upstream DeepFilterNet package and blends the enhanced result with the original signal using `noise_reduction` from `0.0` to `1.0`
- `0.0` means "keep the original audio" and still emits a FLAC copy
- `1.0` means "full denoise"

The node accepts typical audio formats that `ffmpeg` can decode and always writes a new `.flac` file into ComfyUI's output folder under `openshot_audio/`.

## Speech clarity node

`OpenShotLavaSRSpeechClarity` is intended for low-quality speech recordings:

- Input: `source_audio_path` or `audio`, `keep_model_loaded`
- Output: a new FLAC file path
- Uses LavaSR v2 speech enhancement
- Intended for speech/dialogue clarity, not general music restoration

LavaSR is installed through `requirements.txt` in the main Comfy environment.
The first `Clarity -> Speech` run will still take longer because LavaSR downloads its model snapshot from Hugging Face on demand.

## Troubleshooting

If `python -m pip install -r requirements.txt` fails on `deepfilterlib` with a Rust / Cargo error, you are most likely using Python `3.12+`.

Simplest fix:

- use a Python `3.10` or `3.11` Comfy environment

If you want to keep Python `3.12`, install Rust first and rerun the install:

```bash
curl https://sh.rustup.rs -sSf | sh
source "$HOME/.cargo/env"
python -m pip install -r requirements.txt
```

## Notes

- `OpenShotSam2VideoSegmentationChunked` returns only the requested chunk range (bounded memory) instead of collecting whole-video masks.
- For very long videos, pair chunked outputs with batch-safe downstream nodes (VHS meta-batch, staged processing, or on-disk intermediates).
- `torchaudio` is listed explicitly because DeepFilterNet imports it internally and some environments do not pull it in automatically.
- LavaSR preserves the original channel count by processing each channel independently before recombining the output.

## Acknowledgements

OpenShot-ComfyUI builds on several excellent open-source projects and model releases. A big thank you to the maintainers, contributors, and researchers behind these repos and models. This node pack would not exist without their work.

Core upstream repos used by these nodes:

- [`facebookresearch/sam2`](https://github.com/facebookresearch/sam2) for SAM 2 model code and checkpoints
- [`IDEA-Research/GroundingDINO`](https://github.com/IDEA-Research/GroundingDINO) for GroundingDINO open-set object detection
- [`soCzech/TransNetV2`](https://github.com/soCzech/TransNetV2) and [`transnetv2-pytorch`](https://github.com/soCzech/TransNetV2/tree/master/inference-pytorch) for scene / shot boundary detection
- [`Rikorose/deepfilternet`](https://github.com/Rikorose/DeepFilterNet) for DeepFilterNet audio denoising
- [`ysharma3501/LavaSR`](https://github.com/ysharma3501/LavaSR) for LavaSR speech enhancement
- [`langtech-bsc/vocos`](https://github.com/langtech-bsc/vocos) via LavaSR for the underlying Vocos-based enhancement stack
- [`kijai/ComfyUI-segment-anything-2`](https://github.com/kijai/ComfyUI-segment-anything-2) for integration ideas and surrounding ComfyUI ecosystem work

Please see the upstream repositories for full original licenses, credits, papers, and model details.

---

Copyright (C) 2026 OpenShot Studios, LLC

Licensed under the GNU General Public License v3.0 (GPLv3).
See [LICENSE.md](LICENSE.md) for the full license text.
