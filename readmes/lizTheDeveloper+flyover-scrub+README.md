# flyover-scrub

Remove aircraft Doppler signatures from audio and video, so a recording can't be
geolocated from the planes flying over it.

The attack was shown by **colsto** in
[*I discovered a sound that leaks your exact location (and it's everywhere)*](https://www.youtube.com/watch?v=UytYrhYLOKI)
([@colsto](https://www.youtube.com/@colsto)). This repo is a defence against it, plus an independent replication.

> **It works on real phone videos.** On my own iPhone videos and public ADS-B data, a Cessna nobody could hear
> located an indoor selfie to 61–134 m, and a helicopter heard from a parked car picked the right aircraft out of 18.
> It survived 32 of 34 codec and filter chains, and TikTok passes faint tones through untouched.
> Full write-up, data and a reproducible proof of concept: [`research/`](research/README.md).

![One sound. 787 m from the true spot.](research/figures/video/03_where_it_was_recorded.png)

<details><summary>All figures</summary>

| | |
|---|---|
| ![The sound you can't hear](research/figures/video/01_the_sound_you_cant_hear.png) | ![18 aircraft nearby. One fits.](research/figures/video/02_eighteen_aircraft_one_fits.png) |
| ![Re-encoding doesn't hide it](research/figures/video/04_reencoding_doesnt_hide_it.png) | ![Posting it doesn't wash it out](research/figures/video/05_platforms_keep_it.png) |
| ![flyover-scrub: the line is gone](research/figures/video/06_before_after_scrub.png) | ![Ordinary processing barely dents it](research/figures/video/07_what_removes_it.png) |

</details>

```sh
uv tool install .                         # or: uv run flyover-scrub ...
flyover-scrub input.mov -o output.mov     # audio scrubbed, video copied, metadata stripped
flyover-scrub --check input.mp4           # report long tonal ridges, write nothing
```

Both modes also report **grid hum (ENF)**: mains hum whose frequency wanders with the power grid, which can date
a recording and tell which grid it was made on. Scrubbing removes it by default (`--keep-hum` keeps it). See
[`research/`](research/README.md#4-the-other-leak-grid-hum-enf).

## Audit your own recordings against real flights

```sh
# 1. While you record, log aircraft around where you are (gently: one small
#    request every 5 s to the free adsb.lol community API, with backoff).
flyover-capture --at 42.36,-83.13 --minutes 15 -o flights.jsonl

# 2. Ask: would the attack have found me? And after scrubbing?
flyover-audit recording.mov --flights flights.jsonl --scrub

# 3. If you can see a line in the spectrogram, fit it directly (stronger on real recordings):
flyover-audit recording.mov --flights flights.jsonl --scrub --trace 10,75,65,95   # t_lo,t_hi,f_lo,f_hi
```

```
  N123AB (C172, cat A1) closest 1.1 km
    original  top guess    158 m from you, your spot ranked 3/1357, signal 34.4x chance  -> EXPOSED
    scrubbed  top guess   1553 m from you, your spot ranked 506/1352, signal  1.1x chance  -> not located
```

The audit reads the start time and position from the file's own tags (iPhone
`.MOV` has both), or takes `--start` and `--at`. It **requires your true
location**. It answers "am I exposed?" and isn't meant for locating recordings you
didn't make. For the same reason, the package has no bulk or historical flight download. (The research
scripts include one that reads adsb.lol's public daily archive with ranged requests, used to find aircraft passes
in my own clips.)

"Signal × chance" compares the best match against the same search run on the
time-reversed spectrogram, where aircraft lines rise instead of falling and can
only match by chance. It reads ~0.5 with no aircraft, ~1–2 after scrubbing and
20–35 for an inaudible *synthetic* light-aircraft flyover. The verdict threshold is 4. A real Cessna flyover
scored only 2–3× while ranking the true spot first, so 2–4× with the true spot in the top 10 reads "possibly exposed". These
calibration numbers come from a handful of synthetic cases; treat borderline
results with care.

Notes: the live API only records the present, so start `flyover-capture` before
you record. Exports, edits and messaging apps often rewrite a file's creation
date, so pass `--start` if the file has been through anything. Each aircraft is
audited separately; jets and helicopters are tested too, though the scorer was
tuned on propeller tones.

## The attack

[colsto showed](https://www.youtube.com/watch?v=UytYrhYLOKI) that one minute of
audio with an *inaudible* propeller flyover is enough to locate a recording to
within a couple of hundred feet. The method:

1. A long-window, whitened spectrogram shows the aircraft's Doppler curve, even
   when you can't hear it.
2. Public ADS-B data gives every aircraft's track.
3. For each candidate location, model the exact curve that track would produce
   there. The pitch heard at time *t* depends on the plane's motion when it
   **emitted** the sound, not where it is at *t*.
4. Sum the spectrogram energy under each modelled curve. The best match is the
   location.

He showed that a high-pass filter doesn't stop this (boosting brings the line
back), that talking over it doesn't either, and that it survives phone-call
compression.

`flyover_scrub.attack` is a working reference implementation of the scorer.
It's here so the defence can be **measured** rather than assumed.

`flyover_scrub.trace` is the trace-and-fit variant colsto uses for faint curves: follow the visible line, solve
the source pitch in closed form for each candidate spot, and score the RMS residual in cents. On real recordings
it is the stronger of the two (see [`research/`](research/README.md)).

## Why "just denoise it" isn't enough

The attack is a **matched filter**. It adds up evidence along a long,
precisely predicted curve, so it can recover lines far below the noise floor and
lines that were only *attenuated*. A defence must leave the affected bins with
**no information about the curve**, not just make them quieter. A per-frame
detector can't do this alone: we measured that a −28 dB line and chance noise
chains look the same frame by frame.

## The defence

For every STFT bin in the protected band (default 20–2000 Hz):

| Bin type | Treatment |
|---|---|
| Background (< 12 dB above the local floor) | **Re-synthesised** with fresh random-phase noise at the same local power. The room tone sounds the same, and sub-floor lines are gone. |
| Long, slowly gliding narrowband ridges (aircraft, drones, traffic, HVAC, hum) | Replaced with floor-level noise (removed) |
| Other foreground (speech, music, transients) | Passed through untouched |

Level corrections use only one whole-file number per frequency, so they can't
reintroduce time-varying structure.

## Results

A physically modelled propeller flyover (700 m AGL, gentle turn) was mixed into
two real iPhone recordings. The recording's GPS fix is the ground truth. The
attacker gets an ADS-B-like copy of the track (1 Hz, metre-level noise, smoothed),
a clock that is off by 2.5 s, and a 10 × 10 km search box with ~2,400–3,000
candidates refined to 50 m. Run with `eval/run_eval.py`.

| Condition | Location error | Rank of true location |
|---|---|---|
| No aircraft (control) | 1.5–5.3 km | random |
| Raw, flyover −30 dB (inaudible) | 0–461 m | #1 in 4/6, #3 and #15 otherwise |
| Raw, flyover −10 dB | 0–461 m | #1 in 4/6, #2 and #10 otherwise |
| High-pass 300 Hz then boost | 0–112 m | #1 (no defence, matching the video) |
| **flyover-scrub** (12 runs: 2 recordings × 3 seeds × 2 levels) | **1.1–5.1 km** | **351–2087**, no better than chance |

Quality (vs the aircraft-free original, phase-insensitive):

* Above 2 kHz: untouched (0.01 dB).
* 120 Hz–2 kHz: long-term tonal balance within ~1 dB.
* Below 100 Hz: −4 to −9 dB, because steady hum and machine tones are removed. Mains
  hum is a separate forensic leak (ENF timestamping), so this is the default;
  `--keep-hum` keeps perfectly steady tones.
* Foreground content between 8 and 12 dB above the floor is re-synthesised. Quiet
  details close to the noise floor get softer.

## Limits (read these)

* **Tested against both scorers**: on simulated flyovers in real recordings, and on two real
  ADS-B-matched flyovers (a Cessna and an R44 helicopter; after scrubbing, neither leaves a traceable line). Not yet
  tested against learned detectors or multiple flights with a locked offset. Treat the results as evidence, not a guarantee.
* Aircraft energy that **overlaps loud foreground** (speech harmonics crossing the
  line) is kept along with the foreground. In our tests the residual was too small
  to score, but louder flyovers under continuous speech are the most likely leak.
* It only protects the copy you publish. The original file, live streams, calls and
  CCTV are out of scope.
* Stereo channels are scrubbed independently, so the background noise becomes
  decorrelated (slightly wider room tone).
* **Cutting** the audio (no long continuous stretches) remains a cheap, complementary
  defence. **Metadata** is a far easier leak than any of this, so the CLI strips it by
  default.

## Development

```sh
uv run pytest -q
uv run python eval/run_eval.py path/to/recording.wav --level-db -30 --seed 1
uv run python eval/quality.py path/to/recording.wav out_dir raw scrub
```

## Credits

* **colsto**, [*I discovered a sound that leaks your exact location (and it's everywhere)*](https://www.youtube.com/watch?v=UytYrhYLOKI):
  the attack, the emission-time Doppler model and the trace-and-fit method.
* [adsb.lol](https://adsb.lol): open ADS-B data.

MIT licensed.
