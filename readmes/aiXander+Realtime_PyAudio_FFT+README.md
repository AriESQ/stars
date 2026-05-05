# Realtime Audio Feature Server

A localhost Python server that captures live audio (mic, line-in, soundcard, loopback device, ...), computes perceptually-tuned **low / mid / high** band energies and an optional **128-bin log-spaced FFT spectrum**, and publishes them to:

- **External apps over OSC/UDP** (TouchDesigner, Max/MSP, Unity, custom scripts) — every audio block (~187 Hz at 48 kHz / 256 samples).
- **A browser visualizer over WebSocket** — coalesced to ~60 Hz, plus a binary FFT frame.

The browser UI also sends control messages back (toggle FFT, change band crossovers, switch input device, change smoothing, save/load presets). All settings persist to `config.yaml`, so the server boots back into the last-used state.

End-to-end input-to-OSC latency target: **8–15 ms**. The audio callback is allocation-free and runs no DSP — all filtering and FFT runs in worker threads. See `realtime_audio_server_plan.md` for the full design.

## Setup

Requires Python 3.10+ and PortAudio.

```bash
# macOS
brew install portaudio

# Ubuntu/Debian
sudo apt install libportaudio2 portaudio19-dev
```

Then, from the repo root:

```bash
pip install -e ".[dev]"
```

## Run
python -m server.main --open

```bash
audio-server                  # reads ./config.yaml, opens WS on 8765, UI on 8766
audio-server --open           # also opens the UI in your default browser
audio-server --no-ws          # headless OSC-only mode
audio-server --device 2       # override input device by index
audio-server --config /path/to/cfg.yaml --log-level DEBUG
```

Equivalent to: `python -m server.main`.

The browser UI is at **http://127.0.0.1:8766** once the server is running. (Don't open `ui/index.html` directly with `file://` — ES modules won't load.)

---

## Integration guide (for external apps / coding agents)

This server is designed to be a feature provider for other projects. There are two ways to integrate, and they can be used together:

1. **OSC/UDP** — the "subscribe-only" path for realtime audio features (TouchDesigner, Max/MSP, Unity, p5.js, custom Python/JS apps). Lowest latency, every audio block.
2. **WebSocket** — full-duplex JSON + binary protocol used by the browser UI. Use this if you want to **change settings at runtime** (toggle FFT, switch input device, retune bands, save/load presets) or if you want **a richer feature payload** than OSC carries.

The server can run with both enabled (default), or in OSC-only headless mode (`--no-ws`).

### 1. Listening for audio features over OSC

OSC is sent to every destination listed under `osc.destinations` in `config.yaml`. Default is `127.0.0.1:9000`. Add more (or change the port) by editing the YAML and restarting:

```yaml
osc:
  destinations:
    - { host: 127.0.0.1, port: 9000 }
    - { host: 192.168.1.42, port: 7000 }
  send_fft: false              # set true to also stream /audio/fft
```

**Messages emitted:**

| Address      | Args                                                                                                       | Rate                                  | Notes                                                                                                       |
|--------------|------------------------------------------------------------------------------------------------------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `/audio/meta`| `sr:i  blocksize:i  n_fft_bins:i  low_lo:f low_hi:f  mid_lo:f mid_hi:f  high_lo:f high_hi:f`               | Once at startup, again on device/FFT/cutoff change | Three independent bandpass edges (Hz). Use this to size your spectrum buffer and learn the actual sample rate the device opened at. |
| `/audio/lmh` | `low:f  mid:f  high:f`                                                                                     | Every audio block (~187 Hz @ 48k/256) | **Auto-scaled to ~[0, 1]** (peak follower + soft noise gate + tanh). These are the values VJ tools want.    |
| `/audio/fft` | `bin_0:f  bin_1:f  …  bin_{N-1}:f`                                                                         | Every FFT hop (~94 Hz @ hop=512/48k)  | Only sent when **both** `fft.enabled: true` **and** `osc.send_fft: true`. Raw dB (typical range −80…0).      |

All floats are 32-bit. OSC addresses are flat (no nesting).

**Minimal Python receiver:**

```python
from pythonosc import dispatcher, osc_server

def lmh(_, low, mid, high):
    print(f"L={low:.2f} M={mid:.2f} H={high:.2f}")

def meta(_, sr, blocksize, n_fft_bins, low_lo, low_hi, mid_lo, mid_hi, high_lo, high_hi):
    print(f"sr={sr} bs={blocksize} fft_bins={n_fft_bins} "
          f"bands=[{low_lo}-{low_hi}] [{mid_lo}-{mid_hi}] [{high_lo}-{high_hi}]")

d = dispatcher.Dispatcher()
d.map("/audio/lmh", lmh)
d.map("/audio/meta", meta)
d.map("/audio/fft", lambda _addr, *bins: None)   # n_fft_bins floats

osc_server.BlockingOSCUDPServer(("127.0.0.1", 9000), d).serve_forever()
```

**TouchDesigner / Max:** point an OSC In CHOP / `udpreceive` at port 9000. Each `/audio/lmh` message arrives as three channels.

**Notes:**
- L/M/H over OSC is the **post-autoscale** value in `~[0, 1]`. Pre-autoscale (raw smoothed RMS) is only available over WebSocket (`low_raw/mid_raw/high_raw` in the snapshot message). A `/audio/lmh_raw` channel is on the v1.1 list.
- FFT bins over OSC are **raw dB**, not auto-scaled. Map them yourself (e.g. `clamp((db + 80) / 80, 0, 1)` matches what the bundled UI does).
- The FFT stream is gated by **two** flags: `fft.enabled` (turns the worker on) and `osc.send_fft` (decides whether to ship FFT bins to OSC consumers in addition to the WS client). You can have FFT enabled for the browser but skipped on OSC if you don't need it there.

### 2. Controlling the server over WebSocket

Connect to `ws://127.0.0.1:8765`. The server speaks JSON in both directions, plus binary frames for FFT data. **One** WebSocket carries control messages and data; multiple clients can connect simultaneously.

#### Outbound (server → client)

Text frames, JSON-encoded. `type` discriminates the message:

| `type`          | Payload (key fields)                                                                                                        | When                                          |
|-----------------|------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| `meta`          | `sr, blocksize, n_fft_bins, bands{low,mid,high → {lo_hz, hi_hz}}, fft_enabled, fft_db_floor, fft_db_ceiling, tau{low,mid,high}, autoscale{tau_release_s, noise_floor, strength}, ws_snapshot_hz, device{index, name}` | On connect; re-broadcast after any successful state mutation. Treat this as the source of truth for current settings. |
| `snapshot`      | `seq, low, mid, high, low_raw, mid_raw, high_raw, t`                                                                         | At `ws_snapshot_hz` (default 60 Hz). `low/mid/high` are auto-scaled `~[0, 1]`; `*_raw` are pre-autoscale smoothed RMS. |
| *(binary)*      | `[type=1:u8][reserved:u8][n_bins:u16 LE][float32 × n_bins LE]`                                                                | At FFT hop rate (~94 Hz) when FFT enabled. **Binary frame**, not JSON. Values are dB. |
| `devices`       | `items: [{index, name, hostapi, default_samplerate, max_input_channels, probed_signal?, probed_at?}]`                        | On connect, and in reply to `list_devices`.   |
| `presets`       | `items: [{name, saved_at}]`                                                                                                  | On connect, after `save_preset`, in reply to `list_presets`. |
| `server_status` | `cb_overruns, dsp_drops, fft_drops, perf{cb, dsp, fft, ws → {avg_ms, p95_ms, load_pct}, block_period_ms, hop_period_ms, ws_period_ms}` | At 2 Hz. Diagnostics — you usually don't need it. |
| `error`         | `reason: string`                                                                                                             | In reply to a malformed/invalid inbound message. The server state is unchanged. |

#### Inbound (client → server)

Text frames, JSON. Validation runs before any mutation; on failure you get an `error` reply and **state is unchanged**.

| `type`                | Required fields                                                                                  | Notes                                                                                                                            |
|-----------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `set_fft`             | `enabled: bool`                                                                                  | Turn the FFT worker on/off. Persisted immediately.                                                                               |
| `set_band`            | `band: "low" \| "mid" \| "high", lo_hz: number, hi_hz: number, commit?: bool`                    | Updates one of the three bandpasses. Range per band: `lo_hz ≥ 20`, `hi_hz > lo_hz + 50`, `hi_hz ≤ 0.45·sr`. Bands may overlap. Server-side debounce 50 ms. |
| `set_smoothing`       | `tau: {low?: number, mid?: number, high?: number}, commit?: bool`                                | Each τ in `[0.005, 2.0]` seconds. Only present bands are mutated.                                                                |
| `set_autoscale`       | `tau_release_s?: number, noise_floor?: number, strength?: number, commit?: bool`                 | `tau_release_s ∈ [5, 300]` s. `noise_floor ∈ [0, 0.1]` linear RMS. `strength ∈ [0, 1]` (1 = fully auto-scaled, 0 = raw). Either field optional. |
| `list_devices`        | `probe?: bool`                                                                                   | Returns a `devices` message. With `probe: true` the server briefly opens each device and reports which produced signal.          |
| `set_device`          | `index: int`                                                                                     | Hot-switches the input device. Stream is torn down + rebuilt; sample rate may change; filters/FFT/autoscaler re-init.            |
| `set_n_fft_bins`      | `n: int`                                                                                         | Range `[8, 1024]`. Rebuilds the log-bin map atomically.                                                                          |
| `set_ws_snapshot_hz`  | `hz: number, commit?: bool`                                                                      | Range `[15, 240]`. Affects WS L/M/H rate only — OSC stays at full block rate, FFT WS frames stay on the FFT worker's clock.       |
| `list_presets`        | —                                                                                                | Returns a `presets` message.                                                                                                     |
| `save_preset`         | `name: string`                                                                                   | Name `1–64` chars, `[A-Za-z0-9_\- ]` only. Snapshots DSP / autoscale / FFT view into `<config_dir>/preset-<name>.yaml`.           |
| `load_preset`         | `name: string`                                                                                   | Validates each field, applies via the same handlers a slider would, then persists the resulting state to `config.yaml`.          |

**Drag-aware persistence.** Sliders should send `commit: false` while dragging and `commit: true` on release. The audio mutation is applied immediately either way; only the YAML write is debounced (1 s during drag, 50 ms on commit, capped at 250 ms wall-clock from the first dirty change).

#### Minimal JS client

```js
const ws = new WebSocket("ws://127.0.0.1:8765");
ws.binaryType = "arraybuffer";

ws.addEventListener("message", (ev) => {
  if (typeof ev.data === "string") {
    const msg = JSON.parse(ev.data);
    if (msg.type === "snapshot") {
      // msg.low / msg.mid / msg.high in ~[0, 1]
    } else if (msg.type === "meta") {
      // current server settings
    }
  } else {
    // binary FFT frame
    const view = new DataView(ev.data);
    const nBins = view.getUint16(2, /*LE*/ true);
    const bins = new Float32Array(ev.data, 4, nBins);   // dB values
  }
});

ws.addEventListener("open", () => {
  ws.send(JSON.stringify({ type: "set_fft", enabled: true }));
  ws.send(JSON.stringify({ type: "set_band", band: "mid", lo_hz: 200, hi_hz: 4000, commit: true }));
});
```

#### Minimal Python client

```python
import asyncio, json, struct
import websockets

async def main():
    async with websockets.connect("ws://127.0.0.1:8765") as ws:
        await ws.send(json.dumps({"type": "set_fft", "enabled": True}))
        async for frame in ws:
            if isinstance(frame, str):
                msg = json.loads(frame)
                if msg["type"] == "snapshot":
                    print(msg["low"], msg["mid"], msg["high"])
            else:
                _t, _r, n = struct.unpack_from("<BBH", frame, 0)
                # bins = struct.unpack_from(f"<{n}f", frame, 4)

asyncio.run(main())
```

### 3. Toggling FFT from outside the UI

Three equivalent ways, depending on what you have:

- **WebSocket:** send `{"type": "set_fft", "enabled": true}`.
- **Edit `config.yaml`:** set `fft.enabled: true` and restart the server. (Live edits to `config.yaml` are not picked up — the server *writes* the file but does not watch it.)
- **For OSC consumers:** also set `osc.send_fft: true` in `config.yaml`, otherwise FFT bins won't be sent over OSC even when the worker is on.

### 4. Picking the input device

Either set it in `config.yaml`:

```yaml
audio:
  device: { name: "BlackHole 2ch", index: 3 }   # name preferred, index advisory
```

…or pass `--device <index>` on startup, or send `{"type": "set_device", "index": N}` over WS at runtime. To enumerate, send `{"type": "list_devices", "probe": true}` and read the `devices` reply.

For multichannel pro interfaces / aggregate devices where channel 0/1 isn't the stereo pair you want, use `sounddevice`'s device mapping rather than relying on the auto stereo mono-mix.

### 5. Headless / OSC-only deployments

If you don't need the browser UI or runtime control:

```bash
audio-server --no-ws
```

The WS server, broadcaster, and dispatcher are not started; only OSC + the audio pipeline + persistence run. Change settings by editing `config.yaml` and restarting (or temporarily run with WS enabled to tune via the UI, then drop back to `--no-ws`).

### 6. Defaults summary

| Knob                      | Default        | Where to change                                  |
|---------------------------|----------------|--------------------------------------------------|
| WS server port            | `8765`         | `config.yaml: ws.port`                           |
| UI HTTP port              | `8766`         | `config.yaml: ws.http_port`                      |
| OSC destination           | `127.0.0.1:9000` | `config.yaml: osc.destinations[]`              |
| OSC sends FFT             | `false`        | `config.yaml: osc.send_fft`                      |
| FFT enabled               | `false`        | WS `set_fft` or `config.yaml: fft.enabled`       |
| FFT bins                  | `128`          | WS `set_n_fft_bins` or `config.yaml: fft.n_bins` |
| Bandpass edges            | low `30–250`, mid `250–4000`, high `4000–16000` Hz | WS `set_band` or `config.yaml: dsp.{low,mid,high}` |
| Smoothing τ (low/mid/high)| `0.15 / 0.06 / 0.02` s | WS `set_smoothing` or `config.yaml: dsp.tau` |
| Autoscale window          | `60` s         | WS `set_autoscale` or `config.yaml: autoscale`   |
| Noise floor               | `0.001` linear RMS (~−60 dBFS) | same                            |
| Autoscale strength        | `1.0`          | same (0 = pass-through raw, 1 = fully scaled)    |
| WS snapshot rate          | `60` Hz        | WS `set_ws_snapshot_hz` or `config.yaml: ws.snapshot_hz` |

---

## Notes

- `config.yaml` is **rewritten automatically** every time the UI changes a setting (atomic, debounced). Make sure its parent directory is writable. Saved presets live alongside as `preset-<name>.yaml`.
- For non-default stereo channel pairs (aggregate devices, multichannel pro interfaces), pick the input channel via `sounddevice`'s device mapping rather than relying on the auto stereo mono-mix.
- Tests live under `tests/` but the suite is empty for now.
