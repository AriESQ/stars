# HyperFlow H3 Flash

[![Hacker News](assets/hacker-news-badge.svg)](https://news.ycombinator.com/item?id=50405263)

HyperFlow H3 Flash is [Video Rebirth](https://www.videorebirth.com/)'s compressed, few-step version of [MiniMax-H3](https://huggingface.co/MiniMaxAI/MiniMax-H3). It generates video and synchronized stereo audio together.

**[Showcase](https://www.videorebirth.com/lp/hyperflow-flash)** · **[Weights (Hugging Face)](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash)** · **[ComfyUI nodes](https://github.com/Video-Rebirth/ComfyUI-HyperFlow-Flash)** · **[GGUF setup guide](integrations/README.md)** · **[8-step LoRA for full-size MiniMax-H3](https://github.com/Video-Rebirth/hyperflow)**

- **Output:** 5.2–15 s of video at 24 fps (1344×768 by default) with a 32 kHz stereo soundtrack.
- **Sampling:** 4, 6 (default), or 8 steps, without classifier-free guidance (CFG).
- **Speed (5.2 s clip, 6 steps):** 8.7 s on 4× B200, 36 s on 1× H200, 92 s on 1× RTX 5090.
- **Real time on 4× Blackwell GPUs:** [NVIDIA SOL-H3](https://github.com/NVlabs/Sana/tree/sol-engine/models/minimax_h3/HyperFlow-Flash) runs HyperFlow H3 Flash in real time on 4× B-series GPUs. SOL-H3 is our inference-acceleration partner and supports this model from day 0.
- **Model size:** 13.7B (`fl2va`) or 13.9B (`ref2va`) parameters, less than half of the ~31B MiniMax-H3 transformer.
- **Minimum footprint:** `Q4_K_M` is **9.1 GB** (`Q8_0` is 14.9 GB). It runs on 24 GB and 32 GB GPUs in PCs with **16 GB of system RAM**. 16 GB GPUs are not measured yet.

## Supported Tasks

| Task | Input | ComfyUI template | GGUF | Python INT8 |
|---|---|---|---|---|
| `t2va` | Text prompt | `hyperflow_t2v` | Yes | Yes |
| `fl2va` | Prompt + first keyframe, or first and last keyframes | `hyperflow_i2v`, `hyperflow_flf2v` | Yes | Yes |
| `ref2va` | Prompt + up to 12 references | `hyperflow_ref2v` | Images only | Images, videos, and audio |

---

## Choose a Runtime

**Decision rule:** In ComfyUI on 24 GB+ RTX GPUs, use the **INT8 safetensors** (16 GB+ of system RAM; a PyTorch built for CUDA 13.0 or newer, or `--enable-triton-backend`). Use **GGUF** on smaller GPUs and in stable-diffusion.cpp or Unsloth Studio. Use the **INT8 convrot** Python package on data-center GPUs, or on 24 GB+ RTX GPUs with at least 69 GiB of system RAM.

All weights are in [`VideoRebirthAI/hyperflow-h3-flash`](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash).

| | GGUF | INT8 convrot |
|---|---|---|
| **Runtime** | [ComfyUI, Unsloth Studio, stable-diffusion.cpp](#comfyui-unsloth-studio--stable-diffusioncpp-gguf) ([setup guide](integrations/README.md)) | [This Python package](#python-package-int8-convrot) (`hyperflow-h3-flash` CLI and `diffusers`); [ComfyUI](integrations/README.md#comfyui-int8) (`*_int8` templates) |
| **Precision & size** | `Q3_K_M` to `Q8_0` (7.2–15.2 GB) | W8A8 INT8 + low-rank (~16 GB) |
| **Hub folders** | `fl2va_gguf/`, `ref2va_gguf/` | `fl2va_int8_convrot/`, `ref2va_int8_convrot/`; single-file ComfyUI copies in `fl2va_int8_convrot_comfyui/`, `ref2va_int8_convrot_comfyui/` |
| **`ref2va` inputs** | Images | Images, videos, and audio |
| **Target GPU** | Consumer RTX GPUs (measured on 24 GB and 32 GB) | H100 / H200 / B200 / B300 (1–8 GPUs), or 24 GB+ RTX GPUs |
| **System RAM** | 16 GB+ | 16 GB+ in ComfyUI. Python package: ~16 GiB without offload; ≥ 69 GiB (`fp8` text encoder) or ≥ 91 GiB (`bf16`) with offload |

---

<a id="comfyui-unsloth-studio--stable-diffusioncpp-gguf"></a>
## GGUF Runtimes (ComfyUI, Unsloth Studio, stable-diffusion.cpp)

| Quant | `fl2va_gguf/` | `ref2va_gguf/` | When to use |
|---|---:|---:|---|
| **`Q4_K_M`** | **9.1 GB** | **9.2 GB** | **Recommended GGUF quant** |
| `Q8_0` | 14.9 GB | 15.2 GB | Closest to full precision when VRAM and system RAM fit |
| `Q3_K_M` | 7.2 GB | 7.4 GB | Smallest footprint (`Q4_K_S`, `Q5_K_M`, and `Q6_K` are also available) |

**Full setup guide: [`integrations/README.md`](integrations/README.md).** Quick start:

- **ComfyUI ([`Video-Rebirth/ComfyUI-HyperFlow-Flash`](https://github.com/Video-Rebirth/ComfyUI-HyperFlow-Flash)):**
  1. Clone [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) and [ComfyUI-HyperFlow-Flash](https://github.com/Video-Rebirth/ComfyUI-HyperFlow-Flash) into `ComfyUI/custom_nodes/`.
  2. Download the 15.7 GB `qwen3vl_32b_minimax_h3_nvfp4_awq` text encoder.
  3. On 16 GB or 32 GB PCs, start ComfyUI with `python main.py --fast-disk`.
  4. Open **Workflow > Browse Templates > ComfyUI-HyperFlow-Flash** and select `hyperflow_t2v`, `hyperflow_i2v`, `hyperflow_flf2v`, or `hyperflow_ref2v`.
  5. On 24 GB+ GPUs, use the INT8 safetensors from `fl2va_int8_convrot_comfyui/` or `ref2va_int8_convrot_comfyui/` with the `*_int8` templates instead (ComfyUI-GGUF is not needed). Start ComfyUI with `--enable-triton-backend`, or use a PyTorch built for CUDA 13.0 or newer ([INT8 safetensors](integrations/README.md#comfyui-int8)).
- **Unsloth Studio ([setup guide](integrations/README.md#unsloth-studio)):**
  1. Point `SD_CLI_PATH` at the patched `sd-cli` binary and run `unsloth studio`.
  2. Load `VideoRebirthAI/hyperflow-h3-flash` (`fl2va_gguf/` or `ref2va_gguf/`).
  3. Studio downloads the companion text encoder and VAEs automatically. It runs the built-in 6-step schedule at `CFG = 1`.
- **stable-diffusion.cpp ([`integrations/stable-diffusion.cpp/`](integrations/stable-diffusion.cpp)):**
  Apply `hyperflow-two-time.patch` to upstream commit `3be2378`. The patch adds the two-time `(t, r)` embedder, low-rank linear layers, the default 6-step schedule from GGUF metadata, and 32-bit matmul token splitting for long clips.

---

<a id="python-package-int8-convrot"></a>
## Python Package (INT8 convrot)

### Install

```bash
pip install git+https://github.com/Video-Rebirth/hyperflow-h3-flash
pip install "hyperflow-h3-flash[hopper] @ git+https://github.com/Video-Rebirth/hyperflow-h3-flash"  # H100 / H200: FlashAttention-3
pip install "hyperflow-h3-flash[fp8] @ git+https://github.com/Video-Rebirth/hyperflow-h3-flash"     # --text-encoder-precision fp8
```

- **Requirements:** Python 3.10+, PyTorch 2.6+ with CUDA and Triton (`pip install triton-windows` on native Windows), an Ampere or newer NVIDIA GPU, and `diffusers >= 0.40`. Multi-GPU (`--gpus` > 1) requires Linux or WSL2 (raise `memory=` in `%UserProfile%\.wslconfig` on WSL2).
- **First-run download:** ~90 GB, or ~68 GB with `--text-encoder-precision fp8`. This includes the MiniMax-H3 text encoder, VAEs, and the 16 GB HyperFlow INT8 transformer for the selected task. The 62 GB base transformer is never downloaded.
- **First-run compilation:** Triton INT8 kernels compile on first use (~1 min).

### Command Line

Run `hyperflow-h3-flash` or `python -m hyperflow_h3_flash`:

```bash
# Text to video + audio (t2va)
hyperflow-h3-flash --prompt "A chef slides a steaming bowl of ramen across a wooden counter; rain taps on the window." \
    --output ramen.mp4

# First keyframe, or first + last keyframe (fl2va)
hyperflow-h3-flash --prompt "..." --image first.png --output clip.mp4
hyperflow-h3-flash --prompt "..." --image first.png --last-image last.png --output clip.mp4

# Reference images, videos (with soundtrack), and audio clips in prompt order (ref2va)
hyperflow-h3-flash --prompt "<Picture 1> walks through the scene of <Picture 2> ..." \
    --reference person.png --reference scene.png --output clip.mp4

# 15 s clip, context-parallel across 4 GPUs (or --gpus auto for up to 4 visible GPUs)
hyperflow-h3-flash --prompt "..." --num-frames 360 --gpus 4

# 4 steps (speed), 6 steps (default), or 8 steps (quality)
hyperflow-h3-flash --prompt "..." --steps 4
```

| Option | Values / Default | Description |
|---|---|---|
| `--steps` | `4`, `6` (default), `8` | Sampling steps: `4` for speed, `6` balanced, `8` for quality. Sigma grids are in [`schedule.py`](src/hyperflow_h3_flash/schedule.py). |
| `--num-frames` | `124`–`362` (default `124`) | Frame count at 24 fps (`5.2` to `15 s`). Rounds up to `17n + 5` (`360` becomes `362`). |
| `--height`, `--width` | Multiples of 32 | Default: 768 on the short edge. Follows the `--image` aspect ratio, or 16:9 for `t2va`. |
| `--reference` | Repeatable path | `ref2va` inputs matching `<Picture i>`, `<Video i>`, and `<Audio i>` in prompt order. Limits: 9 images, 3 videos, 3 audio clips, 12 total. |
| `--gpus` (`--num-gpus`) | `1`, `2`, `4`, `7`, `8`, `auto` | Multi-GPU context and VAE tile parallelism. Re-launches automatically under `torchrun`. |
| `--offload` | `auto` (default), `none`, `model`, `stream` | GPU memory placement. See [Offload Modes](#offload-modes-hyperflow-h3-flash). |
| `--text-encoder-precision` | `bf16` (default), `fp8` | `fp8` loads [`Qwen/Qwen3-VL-32B-Instruct-FP8`](https://huggingface.co/Qwen/Qwen3-VL-32B-Instruct-FP8). Saves ~22 GiB system RAM when offloading. Requires the `[fp8]` extra. |
| `--fp8-gemm` | `triton` (default), `deepgemm` | GEMM backend of the `fp8` text encoder. `deepgemm` needs Hopper or newer. |
| `--attention` | `auto` (default), `sdpa`, `fa3` | Uses FlashAttention-3 (`fa3`) on Hopper when `kernels` is installed. Uses PyTorch `sdpa` otherwise. |
| `--block-chunk` | `0` (default), `16384`, ... | Slices every token-wise op of a transformer block to bound VRAM activations. `16384` fits 15 s mixed `ref2va` in 24 GB VRAM. |
| `--weights`, `--subfolder`, `--base-model` | Hub ID or local path | Override the transformer repo, task subfolder, or base `MiniMaxAI/MiniMax-H3` snapshot. |

[`examples/benchmark.py`](examples/benchmark.py) times every pipeline stage and per-GPU peak memory under `torchrun`.

### Python API

```python
import torch
from diffusers.utils.export_utils import encode_video
from hyperflow_h3_flash import load_pipeline

pipe = load_pipeline("t2va")  # "fl2va": pass image=... (and last_image=...); "ref2va": pass references=[...]
out = pipe(
    prompt="A chef slides a steaming bowl of ramen across a wooden counter.",
    num_frames=124,
    num_inference_steps=6,  # 4, 6, or 8
    generator=torch.Generator().manual_seed(0),
    output=["videos", "audio", "sampling_rate"],
)
encode_video(
    out["videos"][0],
    fps=24,
    output_path="ramen.mp4",
    audio=out["audio"][0],
    audio_sample_rate=out["sampling_rate"],
)
```

- **Multi-GPU under `torchrun`:** Call `torch.distributed.init_process_group("nccl")` and pass `device=f"cuda:{local_rank}"` to `load_pipeline`. The pipeline shards execution across ranks and returns the full output on every rank.
- **Standalone transformer (`AutoModel`):** Each INT8 Hub folder ships self-contained model code. Load it without installing this package:
  `from diffusers import AutoModel`, then `AutoModel.from_pretrained("VideoRebirthAI/hyperflow-h3-flash", subfolder="fl2va_int8_convrot", trust_remote_code=True, torch_dtype=torch.bfloat16)`.

<a id="offload-modes-hyperflow-h3-flash"></a>
### Offload Modes

`--offload` sets GPU memory placement. `auto` (default) selects a mode from per-GPU VRAM:

| `--offload` | Kept in GPU VRAM | `auto` threshold (1 GPU / multi-GPU) | System RAM (`bf16` / `fp8` text encoder) |
|---|---|---|---|
| `none` | All components | ≥ 90 GiB / ≥ 65 GiB | ~16 GiB |
| `model` | One active component at a time | ≥ 60 GiB / ≥ 45 GiB | ~91 GiB / ~69 GiB |
| `stream` | Active VAE + one transformer block or text-encoder layer at a time | < 60 GiB / < 45 GiB | ~91 GiB / ~69 GiB |

- `stream` is only ~2% slower than `none` on the same GPU.
- `model` and `stream` keep offloaded weights in one pinned host-memory allocation.
- The loader drops unused Qwen3-VL layers above the conditioning tap. This saves ~14 GB. `--text-encoder-precision fp8` saves another ~22 GiB.
- In containers, read the memory limit from `/sys/fs/cgroup/memory.max`, not from `free`.

---

## Benchmarks

All runs are end-to-end at **1344×768 and 6 steps**: text encoding, transformer, and video and audio VAE decode. Each `a / b` cell is total time for a **5.2 s / 15 s** clip (124 / 362 frames).

<a id="rtx-gpus-in-a-home-pc-32-gb-or-16-gb-of-host-ram-q4_k_m-comfyui"></a>
### Consumer RTX GPUs: `t2va`

| GPU | ComfyUI INT8 | GGUF, ≥ 64 GB RAM | GGUF, 32 GB RAM | GGUF, 16 GB RAM | Python INT8, ≥ 69 GiB RAM |
|---|---|---|---|---|---|
| **RTX 5090 (32 GB)** | 83 s / 518 s | 99 s / 575 s | 118 s / 618 s | 130 s / 615 s | 92 s / 551 s |
| **RTX 4090 (24 GB)** | 152 s / 747 s | 157 s / 830 s | 151 s / 815 s | 153 s / 812 s | 130 s / 750 s |
| **RTX 3090 (24 GB)** | — | 315 s / 1835 s | 318 s / 1869 s | 325 s / 1866 s | 266 s / 1684 s |
| *Peak VRAM* | *5090: 31 GiB; 24 GB: 21 GiB (5.2 s)* | *5090: 28 / 27 GiB; 24 GB: 23 / 22 GiB* | *same* | *same* | *12.0–12.5 / 21.8–22.4 GiB* |

- **ComfyUI INT8 setup:** The `*_int8_convrot_comfyui/` file on ComfyUI 0.44.0 with PyTorch 2.13 + CUDA 13.0 and the `nvfp4` text encoder. These runs used separate RunPod pods (60 GB / 31 GB of system RAM) and did not save the MP4. On the same pods, `Q4_K_M` took 96 s / 562 s (5090) and 160 s / 834 s (4090), so INT8 is 5–15% faster. With 12 GiB of system RAM left to ComfyUI (a 16 GB PC) and no `--fast-disk`, INT8 took 88 s (5090) and 153 s / 821 s (4090) ([details](integrations/README.md#int8-performance)).
- **GGUF setup:** ComfyUI, `Q4_K_M`, and the 15.7 GB `nvfp4` text encoder. 32 GB and 16 GB PCs use `--fast-disk` with models on NVMe ([Host RAM](integrations/README.md#host-ram)). Peak RSS is 34–37 GiB on ≥ 64 GB PCs. Anonymous RSS is ~8–16 GiB on 32 GB PCs and ~8 GiB on 16 GB PCs.
- **Python INT8 setup:** `hyperflow-h3-flash --offload stream`. It needs ≥ 91 GiB of system RAM with the `bf16` text encoder, or ~69 GiB with `fp8`, because it keeps all offloaded weights in pinned RAM. The 15 s RTX 5090 run used `fp8`.
- **INT8 is faster in both runtimes.** The transformer takes over 80% of the time and is compute bound, and ComfyUI dequantizes `Q4_K_M` weights at run time. The Python package's INT8 transformer is 10–20% faster than GGUF.
- **Use `--fast-disk` on 16 GB and 32 GB PCs.** It streams unresident weights from the OS file page cache. Without it, ComfyUI-GGUF copies the 9 GB transformer into pinned RAM when VRAM overflows. 16 GB PCs then run out of RAM on 15 s clips. On 32 GB PCs, the RTX 3090 and 5090 become 13% and 21% slower (text encoding takes 27–31 s instead of 7–9 s).
- **32 GB of VRAM holds both models.** On the RTX 5090, the text encoder and transformer stay in VRAM together (0.8 s text encoding). On 24 GB GPUs, ComfyUI swaps them between stages (10–16 s text encoding).
- **Keyframe tasks (`i2v`, `flf2v`):** See [GGUF guide: Performance](integrations/README.md#what-to-expect).

<a id="ref2va-on-consumer-rtx-gpus"></a>
### Consumer RTX GPUs: `ref2va`

| GPU | Python INT8, 2 images | Python INT8, mixed | GGUF `match`, 2 images | GGUF `max`, 2 images |
|---|---|---|---|---|
| **RTX 5090 (32 GB)** | 266 s / 914 s | 503 s / 1318 s | 135 s / 660 s | 295 s / 995 s² |
| **RTX 4090 (24 GB)** | 319 s / 1167 s | 630 s / 1702 s¹ | 194 s / 885 s | 398 s / 1275 s² |
| **RTX 3090 (24 GB)** | 726 s / 2763 s | 1441 s / 4033 s¹ | 401 s / 2059 s | 885 s / 2995 s² |
| *Peak VRAM* | *19.5–19.8 / 23.3–25.6 GiB* | *19.6–20.2 / 22.8–28.5 GiB* | *5090: 31 GiB; 24 GB: 22 GiB (5.2 s)* | *5090: 30 GiB; 24 GB: 21 GiB (5.2 s)* |

- **References:** Two 768p stills generated with `t2va` (a person and a street market). **Mixed** is one still, one 5.2 s reference video with its soundtrack, and one audio clip.
- **Python INT8 setup:** 100–125 GB of system RAM (80–88 GiB process RSS). ¹ On 24 GB GPUs, 15 s mixed runs need `--block-chunk 16384`. Without it, they run out of VRAM.
- **GGUF setup:** ComfyUI on ≥ 64 GB RAM, with `hyperflow_ref2v_api.json` and the `nvfp4` text encoder. `ref_image_size` `match` (default) downscales each reference to the output's pixel area and keeps its aspect ratio. `max` downscales only above a 2048 short edge. The `max` runs used the stills upscaled to 3584×2048, the size the INT8 pipeline uses. ² `max` at 15 s needs `python main.py --disable-cuda-malloc`. The default `cudaMallocAsync` allocator fails with `CUDA error: invalid argument`.
- **Each reference adds tokens to every step.** At a 2048 short edge, one image adds ~14,300 tokens (about seven 768p latent frames). The clip itself is 37,710 tokens at 5.2 s and 109,062 at 15 s. Attention cost grows with the square of the token count. So at 5.2 s, the INT8 transformer takes 2.6–2.9× its `t2va` time with two images and 5.2–5.8× with the mixed set.
- **GGUF `match` is the fastest image-reference path.** It adds 24–36% to `t2v` at 5.2 s and 7–15% at 15 s. At the same reference size (`max`), GGUF is 11–25% slower than INT8 at 5.2 s and 8–9% slower at 15 s.
- **`--fast-disk` also works for `ref2v`.** 32 GB and 16 GB PCs ran 5.2 s and 15 s clips on all three GPUs, within 4% of ≥ 64 GB RAM at 15 s. See [GGUF guide: Host RAM](integrations/README.md#host-ram).

### Data-Center GPUs (INT8)

| GPUs | `--offload` | 5.2 s | 15 s | Peak VRAM / GPU (5.2 s / 15 s) | System RAM / GPU |
|---|---|---|---|---|---|
| 1× H200 (141 GB) | `none` | 36 s | 229 s | 80 / 91 GiB | 16 GiB |
| 2× H200 (141 GB) | `none` | 24 s | 119 s | — / 71 GiB | 16 GiB |
| 4× H200 (141 GB) | `none` | 12.6 s (16 s SDPA) | 66 s | 47 / 59 GiB | 16 GiB |
| 4× B200 | `none` | 8.7 s | — | 46 GiB | 16 GiB |

- **Real-time inference:** The table measures this package. For real time on 4× B-series GPUs, use [NVIDIA SOL-H3](https://github.com/NVlabs/Sana/tree/sol-engine/models/minimax_h3/HyperFlow-Flash).
- **INT8 GEMM backend:** The 4× H200 row uses the default Triton kernel (12.6 s). `int8_gemm="sgl"` (CUTLASS INT8 via `sgl-kernel`) measured 12.3 s.
- **4-GPU stage times (5.2 s):** Text encoder 0.11–0.16 s. 6-step transformer 7.8–7.9 s on 4× H200 and 5.0 s on 4× B200. Video VAE decode 3.3–4.0 s.
- **1088p (1920×1088, 362 frames):** 743 s on 1× H200 (106 GiB VRAM). 220 s on 4× H200 (68 GiB VRAM/GPU).

---

## Architecture and Hardware Notes

### How It Works

HyperFlow H3 Flash changes the MiniMax-H3 transformer in three ways:

1. **Structural pruning and low-rank factorization:**

| Partition | Hub folders | Replaces | Dropped blocks | Factored linears | Parameters |
|---|---|---|---|---|---|
| `fl2va` (serves `t2va` and `fl2va`) | `fl2va_int8_convrot/`, `fl2va_gguf/` | `transformer` | 3 of 50 (blocks 6, 21, 22) | 102 | 13.7B |
| `ref2va` | `ref2va_int8_convrot/`, `ref2va_gguf/` | `transformer_ref` | 1 of 50 (block 9) | 114 | 13.9B |

2. **Rotated W8A8 INT8 quantization (`convrot`):** 180 linear layers are quantized to W8A8 INT8 behind a block-diagonal Hadamard rotation.
3. **Two-time `(t, r)` conditioning:** Every token receives the current noise level `t` and the step endpoint `r`. This enables 4-to-8-step sampling without CFG. Conditioning tokens stay at their anchor noise level (`r = t`).

### Multi-GPU and Kernel Dispatch (`hyperflow-h3-flash`)

- **Sequence and VAE parallelism (`--gpus N`):** Ulysses context parallelism splits the packed transformer sequence across $N$ GPUs. Ranks encode keyframes and references and decode spatial video VAE tiles in parallel. Then they all-gather and blend the tiles to match single-GPU output bitwise.
- **Text encoder placement:** With `--offload none` and the `bf16` text encoder, FSDP2 shards the 50 GiB text encoder across GPUs. This cuts 4-GPU peak VRAM from 91 GiB to 59 GiB/GPU. When offloading or using `fp8`, rank 0 runs the text encoder and broadcasts the embeddings (~2 MB).
- **INT8 GEMM dispatch:**

| GPU architecture | Kernel backend |
|---|---|
| Ampere, Ada, Hopper, consumer Blackwell (`sm_80`–`sm_90`, `sm_120`) | Fused Triton kernels within the 99 KiB shared-memory limit (or CUTLASS INT8 via `sgl-kernel` on Hopper) |
| Data-center Blackwell (`sm_100`) | `cuBLASLt` INT8 |
| B300 (`sm_103`) | BF16 tensor cores with `fp32` accumulation (INT8 tensor throughput is throttled on `sm_103`; requires PyTorch 2.8+ with `sm_103` Triton support) |

- **Reproducibility:** The same seed, GPU architecture, GPU count, and attention backend produce bitwise-identical clips. `text_encoder_fsdp` and `vae_parallel` preserve bitwise output.

---

## Development

```bash
make install   # create .venv and install editable package with dev tools
make test      # run unit tests on tiny models (CUDA tests skip without a GPU)
make lint      # ruff check + format check
```

### Repository Layout

```text
.
├── src/hyperflow_h3_flash/        # Python package (INT8 runtime)
│   ├── cli.py                     # `hyperflow-h3-flash` CLI entry point
│   ├── __main__.py                # `python -m hyperflow_h3_flash` entry point
│   ├── hostmem.py                 # Host RAM estimate before loading
│   ├── pipeline.py                # `load_pipeline`: loads models, trims unused text-encoder layers, configures offload/multi-GPU
│   ├── blocks.py                  # Modular Pipeline blocks swapped into the official MiniMax-H3 workflows
│   ├── transformer.py             # `HyperFlowH3FlashTransformer3DModel`: dropped blocks, low-rank linears, two-time (t, r) conditioning
│   ├── int8.py                    # Hadamard-rotated W8A8 linear layers (Triton, cuBLASLt, CUTLASS, and B300 BF16 kernels)
│   ├── schedule.py                # 4-, 6-, and 8-step sigma grids and per-token (t, r) pairs
│   ├── offload.py                 # Single-GPU memory placement (`none`, `model`, `stream`)
│   └── distributed.py             # Multi-GPU execution (torchrun launch, Ulysses attention, FSDP2 / rank-0 text encoder, parallel VAE)
├── integrations/                  # GGUF runtimes for consumer GPUs
│   ├── README.md                  # Step-by-step setup guide for ComfyUI, Unsloth Studio, and stable-diffusion.cpp
│   ├── ComfyUI-HyperFlow-Flash/   # Custom nodes (`loader_nodes.py`, `model_patch.py`, `gguf_io.py`, `safetensors_io.py`; GPL-3.0)
│   │   └── example_workflows/     # Four UI workflows (`hyperflow_t2v`, `hyperflow_i2v`, `hyperflow_flf2v`, `hyperflow_ref2v`), their `*_int8` copies, and API versions in `api/`
│   └── stable-diffusion.cpp/      # `hyperflow-two-time.patch` for upstream commit `3be2378` (MIT)
├── examples/                      # `benchmark.py` (per-stage timings and peak memory)
├── tests/                         # Unit tests on tiny models (CUDA tests skip without a GPU)
├── Makefile                       # `make install`, `make test`, and `make lint`
├── pyproject.toml                 # Package metadata and optional extras (`hopper`, `sgl`, `fp8`, `dev`)
├── LICENSE                        # Apache License 2.0
└── THIRD_PARTY_NOTICES.md         # Notices for components adapted from `diffusers`
```

## License

- **Repository code:** [Apache License 2.0](LICENSE), except `integrations/ComfyUI-HyperFlow-Flash` (GPL-3.0) and `integrations/stable-diffusion.cpp` (MIT).
- **Third-party notices:** Components adapted from `diffusers` retain their notices in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- **Model weights:** A Model Derivative of MiniMax-H3 distributed under the MiniMax H3 Community License Agreement. The CLI and `load_pipeline` download them on first run, and using them means accepting that Agreement. The Agreement does not cover use in the European Union, the United Kingdom, the Republic of Korea, or the United States without MiniMax's authorization, and it includes an Acceptable Use Policy. See the [model card](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash) for license terms and notices.
