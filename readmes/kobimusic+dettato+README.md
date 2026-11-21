# dettato

<p>
  <a href="https://huggingface.co/collections/kobimusic/dettato"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-md-dark.svg">
    <img alt="Model on Hugging Face" src="https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-md.svg">
  </picture></a>
  <a href="https://huggingface.co/kobimusic"><img alt="Hugging Face: kobimusic" src="https://img.shields.io/badge/Hugging%20Face-kobimusic-FFD21E?logo=huggingface&logoColor=000"></a>
  <a href="https://kobi.music"><img alt="kobi.music" src="https://img.shields.io/badge/web-kobi.music-B73E6A"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=fff">
</p>

KobiMusic's **dettato** is an audio to MIDI transcriber. You give it a recording and it writes a MIDI file, with one track for
each instrument and a drum track. On nine public benchmark sets it beats MuScriptor 1.3B, which is the next best open model. It
scores 59.2 composite F1 and MuScriptor scores 45.1. On the three sets that Mirelo publishes, it also scores a bit higher than
Mirelo A2M v1.1 Pro, which is a closed model (60.8 to 56.1). The part I benchmarked is 20M parameters, and MuScriptor is about 65
times bigger.

dettato is four models in a chain. The transcriber (15.3M parameters) finds the notes. The evidence repairer (4.9M) fixes
them using the transcriber's evidence. The grouper (2.9M) puts the notes into instrument tracks, and the drum model (5.0M) writes
the drums. The code and the weights are under Apache-2.0, so commercial use is fine.

**No copyrighted recordings.** dettato was trained on a mix of synthetic instrument recordings and CC solo instruments from the
URMP dataset. The rest of the instruments morph together around 20 soundfonts, using the
[soundfont babies](https://kobi.music/research/making-soundfont-babies) technique I published. The vocals and the other
augmentation are CC data too, and the grouper and drum model cards list the CC research datasets they use. No benchmark recording
was used for training.

**What to expect.** It is hard to know how well it will work for your music from benchmarks alone, so I would try it first. The
weakest step is putting the notes into the instrument tracks they belong in. For instance, on jazz recordings a quarter of the saxophone
notes can land in the piano track. It also writes performance MIDI. This means the notes keep the timing of the recording, and
they are not quantized to a beat. If you want something you can play from, like sheet music, I would recommend
[Songscription](https://www.songscription.ai) or [Klangio](https://klang.io). They are both great tools.

![Composite F1 on all nine benchmark sets, and each system on each set it reports](https://raw.githubusercontent.com/kobimusic/dettato/main/docs/figures/bench_all_sets.png)

The benchmark is the eight sets from Table 2 of the MuScriptor paper, plus the Slakh2100 test set. The eight sets are Bach10,
Dagstuhl ChoirSet, PHENICX-Anechoic, RWC Popular, RWC Classical, RWC Genre, RWC Jazz and RWC Royalty-Free. I scored them with the
rules from that paper. The composite is the mean of the note onset, note frame, note offset and drum F1.

| system | parameters | composite | onset | frame | offset | drums |
|---|---|---|---|---|---|---|
| **dettato transcriber + drums** | 20.3M | **59.2** (95% 57.9-60.6) | **67.2** | **77.9** | **44.8** | **47.1** |
| MuScriptor | 1.3B | 45.1 | 48.6 | 70.2 | 27.8 | 34.0 |

Mirelo A2M v1.1 Pro reports three of the sets: PHENICX-Anechoic, RWC Classical and RWC Royalty-Free. On those three, dettato
scores 60.8. Mirelo A2M scores 56.1 (Mirelo published that number), MuScriptor scores 47.4 and YourMT3+ scores 45.7.

![The three sets Mirelo A2M reports: composite and each measure for dettato, Mirelo A2M, MuScriptor and YourMT3+](https://raw.githubusercontent.com/kobimusic/dettato/main/docs/figures/bench_mirelo_sets.png)

On the eight MuScriptor sets alone, dettato scores 58.4. MuScriptor scores 44.6 and YourMT3+ scores 41.1, which are the numbers
from the paper. The tables for each set are on the [dettato](https://huggingface.co/kobimusic/dettato) and
[dettato-drums](https://huggingface.co/kobimusic/dettato-drums) cards.

The table scores the notes from the transcriber and the hits from the drum model. I measured the evidence repairer alone
(+0.30 composite with the base network of the transcriber in front). The grouper was measured on my own track benchmark, and their
cards have the details. I have not scored the four models as one chain yet, the way this package runs them.

## Install

```bash
pip install git+https://github.com/kobimusic/dettato
dettato song.mp3 -o out/        # -> out/song.mid + out/song.json
```

The weights download from the Hugging Face Hub on first use ([the dettato collection](https://huggingface.co/collections/kobimusic/dettato)).

![Beethoven, Symphony No. 5, i.: dettato's MIDI, one lane per instrument track plus timpani](https://raw.githubusercontent.com/kobimusic/dettato/main/docs/figures/example_tracks.png)

## Models

Four models, 28.1M parameters in all, collected in the [dettato collection](https://huggingface.co/collections/kobimusic/dettato). Each has its own model card:

| stage | model | parameters | what it does |
|---|---|---|---|
| 1 | [kobimusic/dettato](https://huggingface.co/kobimusic/dettato) | 15.3M | notes from audio: onset, end and pitch on 88 keys, two voices per key |
| 2 | [kobimusic/dettato-evidence](https://huggingface.co/kobimusic/dettato-evidence) | 4.9M | repairs the notes using the transcriber's own evidence: drops wrong notes, fixes onsets and ends, adds missed notes |
| 3 | [kobimusic/dettato-grouper](https://huggingface.co/kobimusic/dettato-grouper) | 2.9M | puts every note in an instrument track and names the instrument |
| 4 | [kobimusic/dettato-drums](https://huggingface.co/kobimusic/dettato-drums) | 5.0M | drum hits on General MIDI drum keys, drum kits and orchestral percussion |

## Use

### Command line

```bash
dettato song.mp3 other.wav folder/ -o out/
```

- Takes any number of files and folders. Folders are searched recursively, and the folder structure is kept under `out/`.
- Writes `out/<name>.mid` and `out/<name>.json` (the tracks, note counts, the tuning estimate, which drum model ran).
- Uses the GPU when there is one (`--device cpu` to force the CPU).

### Python

```python
import dettato

result = dettato.transcribe("song.mp3")       # loads the models once, then reuses them
result.save_midi("song.mid")
for track in result.tracks:
    print(track.name, track.program, track.is_drum, len(track.notes))   # notes: (N, 4) onset s, end s, pitch, velocity
```

For many files, load once and keep the object:

```python
from dettato import Dettato

model = Dettato.from_pretrained("cuda")
for path in paths:
    model.transcribe(path).save_midi(path + ".mid")
```

Each stage can also be used on its own (`dettato.transcriber`, `dettato.evidence`, `dettato.grouper`, `dettato.drums`). The model
cards show how.

### Weights offline

Set `DETTATO_WEIGHTS` to a folder holding the four model repos (`dettato/`, `dettato-evidence/`, `dettato-grouper/`,
`dettato-drums/`, each with its `config.json` and `model.safetensors`) to load them from disk instead of the Hub.

## How it works

![The pipeline: transcriber, evidence repairer, grouper and drum model](https://raw.githubusercontent.com/kobimusic/dettato/main/docs/figures/pipeline.png)

1. **Transcriber.** A pitch-equivariant lane network reads a harmonic log-frequency spectrogram and gives onset, frame and offset
   probabilities for every key, for two voices per key, at 20 ms. The song is processed in overlapping 8 s windows (one every
   2 s, averaged with a Hann taper), and notes come from peak picking. The network runs once per recording: that one pass feeds
   the repairer and the grouper (below). The recording's tuning is estimated first, and the pass runs on the retuned audio when
   it sits clearly off A440.
2. **Evidence repairer.** A note-level transformer reads each note together with the transcriber's evidence for it (its probability
   maps around the note and its last hidden state) and decides which notes to keep, where they start and end, and which notes are
   missing.
3. **Grouper.** The transcriber's internal features (the same pass, averaged over every other window) are gathered at every
   repaired note, and a note-level transformer gives each note an instrument and a track embedding. Notes are clustered into
   tracks. A track is kept only when it is clearly its own instrument, and tracks with the same instrument are merged.
4. **Drums.** A small drum-kit model and an orchestral-percussion model. A router listens to the whole recording and picks one.
   The drum model needs audio recorded at 40 kHz or more and is skipped for lower-rate sources.

## Requirements

- Python 3.10+, PyTorch 2.2+. A CUDA GPU is recommended: on an RTX 5060 (8 GB) a 4-minute song takes about 15 s and a 6-minute song
  about 25 s, and both peak under 4 GB of GPU memory (above 250 s the transcriber's feature buffers are kept in host memory,
  about 10 MB per second of audio, so GPU memory stops growing with the song's length). The CPU works but is slow (a 15 s clip took 87 s on a laptop CPU,
  model loading included).
- Audio is read with `soundfile`. Formats it cannot read (m4a / aac, some mp3s) go through `ffmpeg`, which must then be on the PATH.

## Limits

- Pitched notes cover the 88 piano keys, with at most two notes on the same key at once.
- Instrument names are only roughly right: on real jazz about a quarter of a saxophone's or lead guitar's
  notes can land in the piano's track, synth-heavy music is named less reliably, and a concert band gets rough names.
- No drums for sources recorded below 40 kHz.

The example recordings in the figures are in the public domain: Beethoven's Symphony No. 5 and Grieg's Piano Concerto by Musopen
(via Wikimedia Commons) and *The Stars and Stripes Forever* by the United States Marine Band.

## Licence

Code and model weights: Apache-2.0 (see [LICENSE](https://github.com/kobimusic/dettato/blob/main/LICENSE) and [NOTICE](https://github.com/kobimusic/dettato/blob/main/NOTICE)). The model cards list the datasets each model was
trained with and their licences. Some of the grouper's and the drum model's training datasets carry non-commercial terms.

## Citation

```bibtex
@software{dettato2026,
  title  = {Dettato: multi-instrument audio-to-MIDI transcription},
  author = {Mills, Nathan},
  year   = {2026},
  url    = {https://github.com/kobimusic/dettato}
}
```
