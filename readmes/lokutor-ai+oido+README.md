# Oído: speech recognition that fits in a $5 chip

*¡Oído!* is what cooks call out in a Spanish kitchen to confirm an order: *heard, got it*.

[![Oído demo: speech recognition on a $5 chip](docs/demo.gif)](https://huggingface.co/lokutor-ai/oido-ctc-small-int8/blob/main/demo.mp4)

*Animated demo; [full video with sound](https://huggingface.co/lokutor-ai/oido-ctc-small-int8/blob/main/demo.mp4).
The transcripts are Oído's chip-exact output, sped up. Footage from a physical board is coming.*

Speech-to-text for any English sentence, running entirely on an **ESP32-S3** (240 MHz dual-core Xtensa LX7, 8 MB PSRAM,
16 MB flash). No cloud, no command list, no neural accelerator. Built by [Lokutor](https://lokutor.com).
Models on Hugging Face: [int8](https://huggingface.co/lokutor-ai/oido-ctc-small-int8) ·
[int4](https://huggingface.co/lokutor-ai/oido-ctc-small-int4).

> **Status (30 September 2026).** Every transcript below comes from the exact arithmetic of the on-chip engine: the host
> build is bit-identical to the firmware, and firmware transcripts under Espressif's QEMU emulator match it word for word.
> Real-time speed is **estimated** from exact emulator instruction counts. Measurements on physical boards follow in the
> next days and will be added here.

## Accuracy

Word error rate (%) on LibriSpeech, same text normalization for every system.

| System | Runs on | test-clean | test-other | Size |
|---|---|---|---|---|
| **Oído**: NVIDIA Conformer-CTC Small, int8, greedy (this repo) | ESP32-S3 | **3.7** | **8.2** | 14.0 MB |
| **Oído int4** (`models/nemo4.tnm`, 4-bit quantization-aware fine-tune), greedy | ESP32-S3 | 4.6 | 10.0 | **8.3 MB** |
| **Oído int8 + language model** (`models/nemo_lm.tlm`, beam search on chip) | ESP32-S3 | 3.3 | 7.2 | 15.3 MB |
| **Oído int4 + language model** | ESP32-S3 | 3.8 | 8.4 | 9.6 MB |
| Oído with NVIDIA Conformer-Transducer Small, int8 (weights not included, see below) | ESP32-S3 | 3.0 | 6.7 | 15.5 MB |
| Espressif MultiNet7 (ESP-SR benchmark; its API takes fixed command lists) | ESP32-S3 | 8.5 | 21.3 | 2.7 MB |
| Moonshine tiny, fp32 | laptop | 5.0 | 12.1 | 27 M params |
| Whisper tiny.en, fp32 | laptop | 6.3 | 15.9 | 39 M params |
| Vosk small (Kaldi) | laptop | 9.9 | 21.6 | 40 MB |

- On-chip rows use the full test sets. Laptop baselines use 500 evenly spaced utterances per set. MultiNet7 figures are from
  Espressif's ESP-SR benchmark page.
- The int8 engine is within 0.1 points of full precision: 3.70 / 8.23 on chip vs 3.68 / 8.11 for the original fp32 model.
- The language model is a 1.3 M-parameter GRU trained only on public-domain books (the LibriSpeech LM corpus). The
  device runs CTC prefix beam search with it (beam 4). It is optional: without it the engine decodes greedily.
- To our knowledge this is the most accurate LibriSpeech result published for any microcontroller. It is not the first
  open-vocabulary recognizer on one (Arm has shown Conformer models on Cortex-M55 + Ethos-U NPUs).

**Robustness** (300 LibriSpeech utterances under real DEMAND noise, babble and room reverb; `eval/make_robust.py`,
full numbers in [`results/robustness.json`](results/robustness.json)):

| Mean WER over 14 conditions | CTC int8 (chip) | CTC int8 + LM (chip) | Transducer int8 (chip) | Whisper tiny.en | Moonshine tiny | Vosk small |
|---|---|---|---|---|---|---|
| | **8.4** | 7.5 | 6.7 | 12.1 | 12.2 | 21.7 |

For the transducer, car and kitchen noise at 5 dB SNR cost under 1 point, and living-room noise about 1.7. Four-talker babble at 5 dB and very
reverberant rooms are the hard cases.

## Speed and memory

| | |
|---|---|
| Flash | 14.0 MB (int8), or **8.3 MB (int4), which leaves a 6 MB app partition for your own code** (`partitions_nemo4.csv`) |
| PSRAM | 2.4 MB working memory peak for a 20 s utterance (measured in QEMU); the rest caches the most-reused weights |
| Compute | ~225 M instructions per second of audio across both cores, ~121 M on the dual-core critical path (exact, QEMU `-icount`) |
| Real-time factor | **estimated 0.7–0.95**: 1.3–1.6 cycles per instruction at 240 MHz, plus flash/PSRAM stalls. Not yet measured on silicon |
| Latency | Utterance mode. Text appears after a 0.8 s pause plus compute: about 3 s for a 2–4 s command |

## How it works

- **Front end:** log-mel features, then 2× (3×3, stride 2) convolution subsampling to 25 Hz.
- **Encoder:** 16 Conformer layers (d = 176, 4 heads, relative-position attention, conv kernel 31).
- **Decoding:** CTC over 1024 BPE tokens. The engine also supports an RNN-T head (LSTM 320 + joint network) and a GRU
  language model with CTC prefix beam search.

The engine (`esp32/components/tinyasr`) is new C written for the ESP32-S3's PIE vector unit:
- int8 matrix kernels on `EE.VMULAS.S8.ACCX` (16 MACs per instruction), plus int4 outer-product kernels;
- int8 relative-position attention with a lookup-table softmax;
- dual-core scheduling;
- tiling so that each weight is streamed from flash once per 64 frames (weight traffic cut from 18 to 7.5 MB/s);
- a VAD/AGC utterance segmenter;
- an optional SSD1306 OLED that shows the live transcript.

## Try it

**On a laptop, with the chip's exact arithmetic.** Needs Python with numpy, soundfile, sentencepiece and sounddevice.

```bash
cd esp32/host && make
./tasr_cli ../../models/nemo8.tnm recording.wav      # 16 kHz mono PCM16 wav
python live_demo.py                                   # microphone -> the firmware's VAD + engine, with ESP32 time estimates
python live_demo.py --model fast --no_lm              # int4, greedy decoding
```

**On a board.** ESP32-S3-DevKitC-1 **N16R8**, an INMP441 I2S microphone (SCK→GPIO4, WS→GPIO5, SD→GPIO6, L/R→GND),
and optionally a 0.96" SSD1306 OLED (SDA→GPIO8, SCL→GPIO9). Needs ESP-IDF v5.5.

```bash
esp32/tools/flash.sh /dev/ttyUSB0 models/nemo8.tnm              # live microphone, most accurate (+ models/nemo_lm.tlm)
esp32/tools/flash.sh /dev/ttyUSB0 models/nemo4.tnm              # int4: 8.3 MB, leaves 6 MB of flash for your app
TASR_OLED=1 esp32/tools/flash.sh /dev/ttyUSB0 models/nemo8.tnm  # + transcript on the OLED
TASR_MODE=file esp32/tools/flash.sh /dev/ttyUSB0 models/nemo8.tnm clip.wav "reference"   # prints measured RTF
NO_LM=1 esp32/tools/flash.sh /dev/ttyUSB0 models/nemo8.tnm      # greedy decoding, no language model
```

**In the emulator** (Espressif QEMU 9.x): runs the real firmware, then reports the transcript and instruction counts.

```bash
esp32/tools/emulate.sh clip.wav
```

**The transducer model.** Its weights are NVIDIA's, distributed on NGC under NVIDIA's terms, so they are not included
here. You can fetch and convert them yourself:

```bash
cd train && python fetch_nemo_small.py ../models/nemo_rnnt --transducer
python export_nemo.py ../models/nemo_rnnt ../models/rnnt8.tnm 8
```

## Repository

```
esp32/components/tinyasr/  on-chip engine: tasr_nemo.c (Conformer CTC/RNN-T), kernels.c (PIE SIMD), tinyasr_lm.c
                           (GRU LM + beam search), tasr_seg.c (VAD), tinyasr.c (streaming engine)
esp32/firmware/            ESP-IDF app: live I2S microphone or benchmark mode, OLED, partition layouts
esp32/host/                host build of the engine: tasr_cli, live_demo.py, seg_test, eval_engine.py, benchmark.py
esp32/tools/               flash.sh, emulate.sh, run_qemu.sh, bench_latency.py, mkimages.py
train/                     PyTorch port of NVIDIA's model (nemo_small.py, rnnt_small.py), exporters, GRU LM training
eval/                      WER normalization, robustness benchmark builder, laptop baselines
results/                   benchmark outputs behind the numbers above
models/                    nemo8.tnm (int8, 14.0 MB), nemo4.tnm (int4, 8.3 MB), nemo_lm.tlm (language model, 1.3 MB),
                           and the tokenizer
```

## Limitations

- English only.
- Text appears after each utterance, not word by word.
- Very noisy crowds and reverberant rooms remain hard.
- Speed is estimated until board measurements are published.
- Requires an ESP32-S3 with 16 MB flash and 8 MB octal PSRAM (N16R8).

## License

- **Code** is licensed under the **GNU GPL v3** ([`LICENSE`](LICENSE)).
- For products that cannot meet GPLv3 terms (for example, consumer devices that do not allow users to install modified
  firmware), Lokutor offers commercial licenses and support. See [`COMMERCIAL.md`](COMMERCIAL.md).
- **Model weights** are derived from NVIDIA's `stt_en_conformer_ctc_small`: `nemo8.tnm` is under **CC-BY-4.0**,
  and `nemo4.tnm` (fine-tuned on public corpora that include share-alike data) is under **CC-BY-SA-4.0**. The language
  model `nemo_lm.tlm` is under **CC-BY-4.0**. See [`NOTICE`](NOTICE).

Lokutor also has Spanish and other-language models and an on-device TTS for the same chip. Contact us for these.
