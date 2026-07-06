# corridorkey-mlx

MLX inference port of [CorridorKey](https://github.com/nikopueringer/CorridorKey) for Apple Silicon.

## Architecture

```
RGB image + coarse alpha hint (4ch)
        │
        ▼
┌──────────────────┐
│  Hiera backbone   │  (timm, features_only)
│  → 4 multiscale   │
│    feature maps    │
└──────────────────┘
        │
   ┌────┴────┐
   ▼         ▼
┌───────┐ ┌───────┐
│ Alpha │ │  FG   │
│ head  │ │ head  │
│ (1ch) │ │ (3ch) │
└───────┘ └───────┘
   │         │
   └────┬────┘
        ▼
┌──────────────────┐
│   CNN Refiner     │  RGB + coarse preds (7ch)
│   → delta logits  │  → sigmoid
└──────────────────┘
        │
        ▼
  final alpha + fg
```

## Phased Roadmap

| Phase | Scope | Status |
|-------|-------|--------|
| 1 | PyTorch reference harness + fixture dump | Done |
| 2 | MLX decoder/refiner blocks + parity tests | Done |
| 3 | Checkpoint conversion (PyTorch → MLX) | Done |
| 4 | Hiera backbone port | Done |
| 5 | Full model assembly + e2e parity | Done |
| 6 | Optimization + benchmarking | Done |

See `prompts/` for detailed phase instructions.

## Usage

### Setup

```bash
uv sync --group dev
```

### Download weights

Model weights (~400 MB) are distributed via GitHub Releases — not committed to git
(binary blobs bloat history and exceed Git LFS free tiers).

**CLI (quickest):**

```bash
# download latest release to platform cache dir
uv run python -m corridorkey_mlx weights download

# specific tag
uv run python -m corridorkey_mlx weights download --tag v1.0.0

# override asset name
uv run python -m corridorkey_mlx weights download --asset corridorkey_mlx.safetensors

# force re-download
uv run python -m corridorkey_mlx weights download --force

# print local path (for scripting)
WEIGHTS=$(uv run python -m corridorkey_mlx weights download --print-path)
```

If installed as a package, a `corridorkey-weights` console script is also available:

```bash
corridorkey-weights download --tag v1.0.0 --print-path
```

**Where weights are cached:**

| Platform | Path |
|----------|------|
| macOS | `~/Library/Caches/corridorkey_mlx/weights/<tag>/` |
| Linux | `~/.cache/corridorkey_mlx/weights/<tag>/` |
| Windows | `%LOCALAPPDATA%\corridorkey_mlx\Cache\weights\<tag>\` |

**Environment variable overrides:**

| Variable | Purpose |
|----------|---------|
| `CORRIDORKEY_MLX_WEIGHTS_REPO` | `owner/repo` for a different GitHub repo |
| `CORRIDORKEY_MLX_WEIGHTS_TAG` | Default tag (instead of `latest`) |
| `CORRIDORKEY_MLX_WEIGHTS_ASSET` | Default asset filename |
| `GITHUB_TOKEN` | Auth token for higher API rate limits |

**Python API:**

```python
from corridorkey_mlx.weights import download_weights

path = download_weights(tag="v1.0.0")
```

### Publishing weights to a GitHub Release

Generate the checksum, then upload both files:

```bash
# generate sha256 sidecar
shasum -a 256 corridorkey_mlx.safetensors > corridorkey_mlx.safetensors.sha256

# create release and upload assets
gh release create v1.0.0 \
    corridorkey_mlx.safetensors \
    corridorkey_mlx.safetensors.sha256 \
    --title "v1.0.0" --notes "Initial weights release"
```

The downloader verifies the SHA256 automatically. If no `.sha256` sidecar or
`SHA256SUMS` file is found, verification is skipped with a warning.

### Convert weights

Convert the PyTorch checkpoint to MLX safetensors (one-time):

```bash
uv run python scripts/convert_weights.py \
    --checkpoint checkpoints/CorridorKey_v1.0.pth \
    --output checkpoints/corridorkey_mlx.safetensors
```

### Single-image inference

```bash
uv run python scripts/infer.py \
    --image input.png \
    --hint alpha_hint.png \
    --output-dir output/
```

Outputs `output/alpha.png` (alpha matte) and `output/foreground.png` (foreground).

Options:
- `--checkpoint PATH` — MLX safetensors file (default: `checkpoints/corridorkey_mlx.safetensors`)
- `--img-size N` — model input resolution (default: 512)
- `--output-dir DIR` — output directory (default: `output/`)

### Python API

```python
from corridorkey_mlx.inference.pipeline import load_model, infer_and_save

model = load_model("checkpoints/corridorkey_mlx.safetensors", img_size=512)
results = infer_and_save(model, "input.png", "alpha_hint.png", "output/")
```

## Development

```bash
uv run pytest              # tests
uv run ruff check .        # lint
uv run ruff format .       # format
uv run ty check            # type check
```

For PyTorch reference work:
```bash
uv sync --group reference
```

## Reference Fixtures

Phase 1 generates golden reference tensors from PyTorch for MLX parity testing.

**Format:** single `reference/fixtures/golden.npz` (numpy compressed archive)

**Generate:**
```bash
uv run --group reference python scripts/dump_pytorch_reference.py \
    --checkpoint checkpoints/CorridorKey_v1.0.pth
```

**Contents (all float32, NCHW, batch=1, img_size=512):**

| Key | Shape | Description |
|-----|-------|-------------|
| `input` | (1, 4, 512, 512) | Random input (seed=42) |
| `encoder_feature_0` | (1, 112, 128, 128) | Backbone stride-4 |
| `encoder_feature_1` | (1, 224, 64, 64) | Backbone stride-8 |
| `encoder_feature_2` | (1, 448, 32, 32) | Backbone stride-16 |
| `encoder_feature_3` | (1, 896, 16, 16) | Backbone stride-32 |
| `alpha_logits` | (1, 1, 128, 128) | Alpha decoder output (H/4) |
| `fg_logits` | (1, 3, 128, 128) | FG decoder output (H/4) |
| `alpha_logits_up` | (1, 1, 512, 512) | Alpha logits upsampled |
| `fg_logits_up` | (1, 3, 512, 512) | FG logits upsampled |
| `alpha_coarse` | (1, 1, 512, 512) | sigmoid(alpha_logits_up) |
| `fg_coarse` | (1, 3, 512, 512) | sigmoid(fg_logits_up) |
| `delta_logits` | (1, 4, 512, 512) | Refiner output (10x scaled) |
| `alpha_final` | (1, 1, 512, 512) | Final alpha prediction |
| `fg_final` | (1, 3, 512, 512) | Final FG prediction |

## Parity Results

End-to-end parity vs PyTorch reference (512×512, float32):

| Tensor | Max Abs Error | Mean Abs Error |
|--------|--------------|----------------|
| alpha_logits | 8.8e-05 | 1.6e-05 |
| fg_logits | 1.5e-04 | 7.2e-06 |
| alpha_coarse | 9.7e-06 | 1.1e-06 |
| fg_coarse | 6.7e-06 | 1.1e-06 |
| delta_logits | 1.1e-04 | 4.3e-06 |
| alpha_final | 2.6e-05 | 8.7e-08 |
| fg_final | 9.5e-06 | 1.1e-06 |

## Performance

### Compiled inference

Use `compile=True` for fused execution on fixed-resolution inputs:

```python
model = load_model("checkpoints/corridorkey_mlx.safetensors", img_size=512, compile=True)
```

The first call incurs a one-time compilation cost. Subsequent calls at the same
resolution run faster. Shapeless compilation (`shapeless=True`) is **not recommended**
due to shape-dependent reshapes in the Hiera backbone.

### Benchmarking

```bash
uv run python scripts/bench_mlx.py
uv run python scripts/bench_mlx.py --resolutions 256 512 1024 --bench-runs 20
```

Reports eager vs compiled latency, warmup cost, and parity check per resolution.

### Large images (tiled inference)

For images larger than the model's input resolution, use tiled inference with
overlap blending:

```python
from corridorkey_mlx.inference.tiling import tiled_inference

model = load_model("checkpoints/corridorkey_mlx.safetensors", img_size=512)
x = preprocess(rgb, alpha_hint)  # full-resolution (1, H, W, 4)
result = tiled_inference(model, x, tile_size=512, overlap=64)
```

### Recommended settings for Apple Silicon

| Setting | Value | Notes |
|---------|-------|-------|
| `img_size` | 512 | Good speed/quality balance |
| `compile` | True | ~1.5–2x faster after warmup |
| `tile_size` | 512 | Match `img_size` for tiling |
| `overlap` | 64 | Smooth blending at tile boundaries |

### Comparing against PyTorch reference

```bash
uv run python scripts/compare_reference.py
```

## Using as a CorridorKey backend

This repo can be consumed as a drop-in MLX backend by the main CorridorKey app.

### Install (editable, from sibling checkout)

```bash
# from the main CorridorKey repo directory
uv pip install -e ../corridorkey-mlx
```

### Engine API

```python
from corridorkey_mlx import CorridorKeyMLXEngine

engine = CorridorKeyMLXEngine(
    checkpoint_path="/abs/path/to/corridorkey_mlx.safetensors",
    img_size=2048,       # production (512 for dev)
    use_refiner=True,
    compile=True,        # faster after first call
)

result = engine.process_frame(rgb_uint8, mask_uint8)
# result["alpha"]     — (H, W) uint8 alpha matte
# result["fg"]        — (H, W, 3) uint8 foreground
# result["comp"]      — (H, W, 3) uint8 fg composited over black
# result["processed"] — (H, W, 3) uint8 (placeholder, same as fg)
```

### Expected inputs

- **image**: numpy uint8 `(H, W, 3)` RGB. sRGB color space (standard).
- **mask**: numpy uint8 `(H, W)` or `(H, W, 1)` grayscale alpha hint.
- **checkpoint**: `.safetensors` format, converted from PyTorch via `scripts/convert_weights.py`.

Inputs are resized internally to `img_size` for inference, then outputs are
resized back to the original input resolution.

### Smoke test

```bash
uv run python scripts/smoke_engine.py \
    --image input.png --hint hint.png \
    --checkpoint checkpoints/corridorkey_mlx.safetensors \
    --img-size 512
```

### 2048 smoke test

Validates full end-to-end inference at CorridorKey's native 2048 resolution.
Uses `samples/sample.png` + `samples/hint.png` by default; falls back to
synthetic inputs if samples are unavailable.

```bash
uv run python scripts/smoke_2048.py
```

With real images:
```bash
uv run python scripts/smoke_2048.py --image shot.png --hint hint.png
```

Reports timing, peak memory, output shapes, and value-range diagnostics.
This is an execution check, not a 2048 parity validation.

To run the slow pytest version:
```bash
uv run pytest -m slow
```

### Standalone scripts vs engine usage

| | Standalone (`scripts/infer.py`) | Engine (`CorridorKeyMLXEngine`) |
|---|---|---|
| Input | file paths | numpy arrays |
| Output | saved PNGs | in-memory dict |
| Returns | `alpha`, `foreground` | `alpha`, `fg`, `comp`, `processed` |
| Default img_size | 512 | 2048 |
| Use case | one-off CLI inference | app backend integration |

### Stubs (not yet implemented)

- `despill_strength` — accepted but ignored (warns once)
- `auto_despeckle` / `despeckle_size` — accepted but ignored (warns once)
- `input_is_linear` — accepted but no-op (model expects sRGB)

### Python version

Requires Python >=3.11. Compatible with the main CorridorKey repo's 3.11 target.

## Current Status

Phases 1–6 complete. Full model assembly with end-to-end parity verified.
Optimization, benchmarking, and tiled inference available.
Engine integration surface available for backend consumption.
