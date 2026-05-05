# PyTV – A Time-Synchronized TV Emulator

PyTV is a multi-channel TV emulator that synchronizes playback using a shared, internal time source.  
It is conceived as a *self-portrait*: every frame is calculated from one fixed “birth” timestamp (`REFERENCE_START_TIME`) in **config.py**.

---

## Architecture – A Deterministic Time-Based Scheduler

* **Universal timeline** — anchored to `REFERENCE_START_TIME`, the “birth” of the system.  
* **Scheduler (`channel_manager.py`)** — pure function  
  `f(current_wall_time, REFERENCE_START_TIME, user_time_offset) → (file_path, file_offset)`
* **Enforcer (`app.py`)** — main loop that compares the *correct* state to the current player state each frame.  
* **“Dumb” player (`video_player.py`)** — obeys whatever the Enforcer tells it; its PTS clock is irrelevant.  
* **Synchronized UI (`overlays.py`)** — queries the Scheduler so overlays always show the mathematically correct time.

---

## Features

* **Deterministic sync** – playback is fully derived from the wall clock.  
* **Multi-channel playlists** – auto-loads `movies/chan_NN` directories.  
* **Pause-aware playlists** – `playlist_builder.py` inserts `__PAUSE__` sentinels.  
* **Web-based remote control** – `main.py` runs a `web_remote` server.  
* **Dynamic time-shifting** – `adjust_offset` skews the whole timeline (not just a seek).  
* **Extensible events** – central `EventManager.post()` API for new inputs.

---

## Getting Started

### 1. Dependencies

#### Python packages (see `requirements.txt`)

```
pygame
numpy
av
```

#### System libraries

**macOS (Homebrew)**

```bash
brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad pygobject3
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

**Linux (Debian/Ubuntu)**

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gst-plugins-base-1.0 \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad
sudo apt install libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0
```

### 2. Bootstrap

```bash
bash bootstrap.sh
```

Creates `movies/` with example channel folders; add your video files to `movies/chan_*`.

### 3. Configure

Edit `config.py` to set your birth time:

```python
import time
REFERENCE_START_TIME = time.time()
```

### 4. Run

```bash
bash run.sh
```

The script sets up a virtual environment, installs dependencies, runs `playlist_builder.py`, and starts the application.

---

## Controls

`← / → / Space` — change channel  
`i` — toggle info overlay  
`f` — toggle fullscreen  
`q / Esc` — quit

### Advanced sync controls

`1 / 2` — adjust time offset ±1 ms  
`3 / 4` — adjust time offset ±100 ms  

(These modify `self.time_offset` in **app.py**, skewing this instance relative to `REFERENCE_START_TIME`.)

---

## Extending PyTV

Add new inputs (e.g. IR remote, GPIO) by posting actions to the central EventManager:

```python
from events import EventManager

def on_ir_code_received(code):
    if code == "KEY_CHANNELUP":
        action = {"type": "switch_channel", "to": "next"}
        EventManager.post(action)
```

---

## License

TBD
