# [Kimi Vendor Verifier](https://www.kimi.com/blog/kimi-vendor-verifier.html)

English | [中文](README_zh.md)

A model evaluation tool based on [inspect-ai](https://github.com/UKGovernmentBEIS/inspect_ai) framework for benchmarking Kimi models.

## Supported Benchmarks

| Benchmark | Description | Dataset |
|-----------|-------------|---------|
| **AIME 2025** | American Invitational Mathematics Examination | [math-ai/aime25](https://huggingface.co/datasets/math-ai/aime25) |
| **MMMU Pro Vision** | Multimodal understanding (vision, 10-way multiple choice) | [MMMU/MMMU_Pro](https://huggingface.co/datasets/MMMU/MMMU_Pro) |
| **OCRBench** | OCR text recognition | [echo840/OCRBench](https://huggingface.co/datasets/echo840/OCRBench) |

### Required Parameters

| Benchmark | Mode | Temperature | TopP | Max Tokens | Epochs |
|-----------|------|-------------|------|------------|--------|
| OCRBench | Non-Thinking | 0.6 | 0.95 | 8192 | 1 |
| OCRBench | Thinking | 1.0 | 0.95 | 16384 | 1 |
| MMMU | Non-Thinking | 0.6 | 0.95 | 16384 | 1 |
| MMMU | Thinking | 1.0 | 0.95 | 65536 | 1 |
| AIME 2025 | Non-Thinking | 0.6 | 0.95 | 16384 | 32 |
| AIME 2025 | Thinking | 1.0 | 0.95 | 98304 | 32 |

## Setup

### 1. Install Dependencies

```bash
uv sync && uv pip install -e .
```

### 2. Configure Environment

```bash
export KIMI_API_KEY="your-api-key"
export KIMI_BASE_URL="your-base-url"
```

Or copy `.env.example` to `.env` and fill in the values.

### 3. Pre-flight Check

Before running benchmarks, verify that the API correctly enforces parameter constraints:

```bash
# Kimi Official API
uv run python verify_params.py --model kimi/your-model-id --think-mode kimi --all

# Opensource deployments (vLLM/SGLang/KTransformers)
uv run python verify_params.py --model your-model-id --think-mode opensource --all
```

This checks that immutable parameters (temperature, top_p, etc.) are correctly enforced. **All tests must pass before proceeding with benchmark evaluations.**

## Running Evaluations

### OCRBench (Quick Validation)

#### Non-Thinking

```bash
uv run python eval.py ocrbench --model kimi/your-model-id \
    --think-mode kimi --max-tokens 8192 --stream
```

#### Thinking

```bash
uv run python eval.py ocrbench --model kimi/your-model-id \
    --thinking --think-mode kimi --max-tokens 16384 --stream
```

### MMMU Pro Vision

#### Non-Thinking

```bash
uv run python eval.py mmmu --model kimi/your-model-id \
    --think-mode kimi --max-tokens 16384 --stream
```

#### Thinking

```bash
uv run python eval.py mmmu --model kimi/your-model-id \
    --thinking --think-mode kimi --max-tokens 65536 --stream
```

### AIME 2025

#### Non-Thinking

```bash
uv run python eval.py aime2025 --model kimi/your-model-id \
    --think-mode kimi --max-tokens 16384 --stream
```

#### Thinking

```bash
uv run python eval.py aime2025 --model kimi/your-model-id \
    --thinking --think-mode kimi --max-tokens 98304 --stream
```

> **Tip**: Run OCRBench first for quick validation (~10 min). Once verified, proceed with MMMU and AIME full evaluations.

## Reference

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `benchmark` | Task: `ocrbench`, `mmmu`, `aime2025` | `ocrbench` |
| `--model` | Model identifier, e.g., `kimi/your-model-id` | **Required** |
| `--max-tokens` | Max output tokens (see Required Parameters) | **Required** |
| `--thinking` | Enable thinking mode (requires `--think-mode kimi/opensource`) | Off |
| `--think-mode` | Thinking param format: `kimi` or `opensource` (vLLM/SGLang/KTransformers) | `kimi` |
| `--temperature` | Sampling temperature | thinking: 1.0, non-thinking: 0.6 |
| `--top-p` | Top-p sampling | `0.95` |
| `--stream` | Enable streaming (recommended for long inference) | Off |
| `--max-connections` | Max concurrent connections | Per benchmark |
| `--epochs` | Number of sampling epochs | Per benchmark |
| `--client-timeout` | HTTP timeout in seconds | `86400` |

### Thinking Mode Parameters

| Model Type | Parameters | extra_body |
|------------|------------|------------|
| Kimi Official + thinking off | `--think-mode kimi` | `{"thinking": {"type": "disabled"}}` |
| Kimi Official + thinking on | `--thinking --think-mode kimi` | `{"thinking": {"type": "enabled"}}` |
| Opensource + thinking off | `--think-mode opensource` | `{"chat_template_kwargs": {"thinking": false}}` |
| Opensource + thinking on | `--thinking --think-mode opensource` | `{"chat_template_kwargs": {"thinking": true}}` |

### View Results

```bash
# Use inspect view to browse logs
uv run inspect view

# Logs are saved in logs/ directory
```

### Resume Interrupted Evaluations

```bash
uv run inspect eval-retry logs/<log-file>.eval
```

## Notes

### AIME 2025 Evaluation

AIME evaluation generates many output tokens. Keep in mind:

1. **Timeout Settings**
   - **Client**: Default `--client-timeout 86400` (24h), usually no change needed
   - **Server**: Ensure server timeout is also set long enough
   - **Gateway/Proxy**: If using nginx/ALB, adjust `proxy_read_timeout` etc.

2. **Streaming**
   - **Strongly recommended** to use `--stream`
   - Non-streaming requests may timeout in thinking mode
   - Streaming keeps connection alive, avoiding gateway timeouts

3. **Concurrency Control**
   - Default `max_connections=100`, adjust based on server capacity
   - If seeing many 429s or `RemoteProtocolError`, reduce concurrency

4. **Quick Validation**
   - First run with `--epochs 1` to verify configuration
   - Then run full `--epochs 32` evaluation

```bash
# Step 1: Quick validation (30 samples x 1 epoch)
uv run python eval.py aime2025 --model kimi/your-model-id \
    --thinking --think-mode kimi --max-tokens 98304 --stream --epochs 1

# Step 2: Full evaluation (30 samples x 32 epochs)
uv run python eval.py aime2025 --model kimi/your-model-id \
    --thinking --think-mode kimi --max-tokens 98304 --stream
```

### Automatic Retry

The following network errors are **automatically retried** (exponential backoff, 1-60s):

| Error Type | Description |
|------------|-------------|
| `RateLimitError` / `429` | Server rate limiting |
| `APIConnectionError` | Connection failure |
| `ReadError` / `RemoteProtocolError` | Network read error |

> Non-network errors (e.g., model output format issues) are not retried and logged for analysis.

## Project Structure

```
├── eval.py              # Main evaluation CLI
├── verify_params.py     # Pre-flight parameter validation
├── kimi_model.py        # Kimi Model API implementation
├── aime2025.py          # AIME 2025 benchmark
├── mmmu_pro_vision.py   # MMMU Pro Vision benchmark
├── ocr_bench.py         # OCRBench benchmark
├── logs/                # Evaluation logs
└── pyproject.toml       # Project configuration
```

## Contact Us

If you have any questions or suggestions, please contact contact-kvv@kimi.com.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
