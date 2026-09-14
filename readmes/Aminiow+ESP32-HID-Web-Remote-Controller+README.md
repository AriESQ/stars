# ESP32-HID-Web-Remote-Controller — V9.0.0

**ESP32‑S3 Wi‑Fi → USB HID bridge with web‑based mouse/keyboard control, captive portal, STA/AP mode, auto‑channel selection, hidden SSID, secure over‑the‑air (OTA) firmware updates with three‑tier TLS verification, consumer controls (media keys), gyro mouse support, mDNS, Wi‑Fi power management, idle sleep, and SHA‑256 verified firmware uploads.**

Control your computer or TV wirelessly from your phone or tablet — settings survive power cycles.

[![GitHub release](https://img.shields.io/github/v/release/Aminiow/ESP32-HID-Web-Remote-Controller)](https://github.com/Aminiow/ESP32-HID-Web-Remote-Controller/releases)
[![PlatformIO](https://img.shields.io/badge/PlatformIO-ESP32S3-orange)](https://platformio.org/)
[![Arduino Core](https://img.shields.io/badge/Arduino%20Core-2.x%20%7C%203.x-blue)](https://github.com/espressif/arduino-esp32)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Flash: 4MB+](https://img.shields.io/badge/Flash-4MB%20min%20%7C%208MB%20recommended-informational)]()

---

## 🌟 Features

- 🖱 **Mouse** – move, click (left/right/middle), double‑click, press/release, scroll wheel.
- ⌨ **Keyboard** – type text, send key taps (including special keys), press & hold modifiers (Ctrl, Alt, Shift, Win).
- 🔧 **Sticky modifiers** – tap to toggle Ctrl, Alt, Shift, Win (visual feedback on web UI).
- 💾 **Persistent settings** – sensitivity, repeat interval, legacy mode, boot protocol, gyro enable, TX power, and power save are stored in NVS and restored after power‑cycle.
- 📶 **Wi‑Fi Access Point** – creates its own network with **auto‑channel selection** (scans for the least crowded channel).
- 🔒 **Hidden SSID** – the AP name (`ESP32-Mouse`) is hidden by default for privacy.
- 🔗 **STA (Client) Mode** – can simultaneously connect to an existing Wi‑Fi network. Credentials are saved and auto‑reconnect with retries.
- 📡 **Wi‑Fi scanning** – scan for networks and connect via the web interface (supports WPA3 and hidden networks).
- 🔁 **Automatic retry** – if STA connection fails, it retries up to 3 times with a configurable delay.
- 🔗 **Captive Portal** – any DNS request resolves to the ESP32; any HTTP request redirects to the web UI (HTTP 302).
- 📱 **Responsive Web Interface** – works on phones, tablets, and desktops; touch‑friendly with a mouse pad.
- 📊 **On‑board logging** – view logs in the web UI to help debug; raw logs available at `/logs` (JSON).
- 🎛 **Adjustable Settings** – sensitivity, repeat interval, legacy mode, boot protocol, TX power, and power save.
- ⚡ **USB HID** – uses TinyUSB to emulate a standard USB mouse and keyboard.
- 🔄 **Robust USB enumeration** – `USB.begin()` is called first for reliable detection.
- 🛡 **JSON escaping** – all API responses are properly JSON‑escaped to prevent injection.
- 🚀 **Over‑the‑Air (OTA) Firmware Updates** – three‑tier security: **Root CA** → **certificate fingerprint** → **insecure** (user‑confirmed).
- 🔐 **SHA‑256 Verified Uploads** – manual uploads verified against hash in version file.
- 📡 **Live progress via SSE** – Server‑Sent Events stream OTA logs and a real‑time progress bar to the browser.
- 🎛️ **Consumer Controls (Media Keys)** – volume, mute, channel, power, input menu/select.
- 📱 **Gyro Mouse Support** – use phone orientation sensors to move the cursor.
- 🌐 **mDNS** – access the web interface at `esp32-mouse.local`.
- 🔋 **Wi‑Fi Power Management** – adjustable TX power (0–20 dBm) and modem sleep.
- 😴 **Idle Sleep** – reduces CPU to 80 MHz and enables max modem sleep when idle.
- 📋 **Dynamic Version Display** – web UI shows current firmware version.

---

## 🆕 What's New in v9

- **Three‑tier Secure OTA** – Root CA chain validation → SHA‑256 certificate fingerprint → insecure fallback (with user confirmation). Each tier is tried in order; failures are logged and the next tier runs automatically.
- **Server‑Sent Events (SSE) for OTA** – live log stream (`/events`) plus a real‑time progress bar with byte‑count and percentage.
- **Core 3.x Compatibility** – uses `getFingerprintSHA256(uint8_t[32])` post‑handshake on core 3.x, and `setFingerprint()` on core 2.x (with a shim).
- **Non‑blocking update checks** – `handleCheckUpdate` spawns a FreeRTOS task; the daily auto‑check does the same.
- **`checkRunning` guard** – prevents concurrent update checks.
- **Idle‑sleep OTA guard** – CPU is kept at 240 MHz during any OTA.
- **`clientFingerprintHex()` helper** – clean fingerprint extraction.
- **Version bump** – firmware version is now `9.0.0`.
- **Fixed fingerprint** – `GITHUB_LEAF_FP` updated to match the current `raw.githubusercontent.com` leaf.
- **Dedicated `/update` page** – its own HTML page with its own CSS, styled to match the main UI.
- **Bug fixes** – dangling `else` in WebSocket handler, `handleUpload` double‑`send()`, `fetchVersionInfo` duplicate variable, `configTime()` signature for core 3.x.

---

## 🧰 Hardware Requirements

### ✅ Boards that work well

| Board | Flash | PSRAM | Notes |
|---|---|---|---|
| **ESP32‑S3‑DevKitC‑1 (N8R2)** | 8 MB | 2 MB | **Recommended** – used for development |
| **ESP32‑S3‑DevKitC‑1 (N8R8)** | 8 MB | 8 MB | Same as above with more PSRAM |
| **ESP32‑S3‑DevKitC‑1 (N16R8)** | 16 MB | 8 MB | Best headroom for OTA + filesystem |
| **ESP32‑S3‑Mini‑1** | Varies | Varies | Compact, same USB‑OTG support |
| **ESP32‑S3‑Zero** | 4 MB | – | Works but tight on flash |
| **ESP32‑S2 boards** | Varies | – | Works; S2 has native USB‑OTG |
| **ESP32‑P4** | Varies | – | Works; new chip with USB 2.0 OTG |

### ❌ Boards that will NOT work

| Board | Why |
|---|---|
| **ESP32 (original)** | No native USB‑OTG peripheral |
| **ESP32‑C3** | USB Serial/JTAG only; no USB device‑mode OTG |
| **ESP32‑C6** | USB Serial/JTAG only; no USB device‑mode OTG |
| **ESP32‑H2** | No USB peripheral at all |

> The firmware requires the **USB‑OTG (TinyUSB)** peripheral, which only exists on ESP32‑S2 / S3 / P4.

### Minimum setup
- **ESP32‑S3** (or S2/P4) dev board
- **USB‑C cable** – data‑capable, not charge‑only
- **4 MB flash minimum**, **8 MB recommended**

---

## 📦 Software & Libraries

Written for the **Arduino framework** (compatible with Arduino IDE and PlatformIO).

### Required libraries

| Library | Source | Purpose |
|---|---|---|
| `WiFi` | built‑in | Wi‑Fi stack |
| `WebServer` | built‑in | HTTP server on port 80 |
| `DNSServer` | built‑in | Captive portal DNS |
| `WebSocketsServer` | [arduinoWebSockets](https://github.com/Links2004/arduinoWebSockets) | Real‑time mouse movement |
| `USB`, `USBHIDMouse`, `USBHIDKeyboard`, `USBHIDConsumerControl` | built‑in | TinyUSB HID |
| `Preferences` | built‑in | NVS settings storage |
| `HTTPClient` | built‑in | OTA downloads |
| `Update` | built‑in | Flash writing |
| `WiFiClientSecure` | built‑in | TLS |
| `mbedtls/sha256` | built‑in | Hashing |
| `ESPmDNS` | built‑in | `esp32-mouse.local` |
| `esp_wifi`, `esp_sleep` | built‑in | Power management |
| `esp_partition`, `esp_ota_ops` | built‑in | Partition queries |

### Supported Arduino ESP32 Core versions

| Core | Status | Notes |
|---|---|---|
| **2.x** | ✅ Supported | Uses `setFingerprint()` during handshake |
| **3.x** | ✅ Supported | Uses `getFingerprintSHA256()` after handshake |
| **< 2.x** | ❌ Not supported | Missing USB HID APIs |

A compile‑time shim (`#if ESP_ARDUINO_VERSION_MAJOR >= 3`) picks the right API automatically.

---

## 🚀 Installation & Flashing

### 1. Clone the repository

```bash
git clone https://github.com/Aminiow/ESP32-HID-Web-Remote-Controller.git
cd ESP32-HID-Web-Remote-Controller
```

### 2. Open in Arduino IDE (or PlatformIO)

- **Arduino IDE**: open `ESP32-HID-Web-Remote-Controller.ino`
- **PlatformIO**: open the project folder

### 3. Board settings (Arduino IDE)

| Setting | Value |
|---|---|
| Board | **ESP32S3 Dev Module** |
| **USB Mode** | **USB‑OTG (TinyUSB)** |
| Upload Mode | UART0 / Hardware CDC |
| **USB CDC On Boot** | **Disabled** ← critical for HID |
| USB Firmware MSC On Boot | Enabled (S2/S3 only) |
| **Flash Size** | **8 MB / 64 Mb** *(or 16 MB for N16 boards)* |
| **Partition Scheme** | **8M with spiffs (3MB APP/1.5MB SPIFFS)** ← see next section |
| PSRAM | OPI PSRAM (if your board has it) |
| Upload Speed | 921600 |
| Erase All Before Sketch Upload | Enabled (optional, recommended on first flash) |

### 4. Upload

- Connect the ESP32‑S3 via the **USB‑C port that supports OTG** (usually labelled `USB` or `USB‑OTG`, not `UART`).
- Press **Upload**.
- If needed, hold **BOOT** while plugging in to enter download mode.

After flashing, the ESP32 creates Wi‑Fi network **`ESP32-Mouse`** (password `12345678`). The SSID is **hidden** — add it manually.

---

## 🧩 Partition Schemes Explained

The code uses **two app partitions** (for OTA) plus NVS. The **filesystem partition is unused** — the firmware never mounts SPIFFS/LittleFS/FATFS — but any scheme you pick will still reserve one.

### What the firmware actually needs

| Requirement | Size | Why |
|---|---|---|
| `nvs` | ≥ 20 KB | `Preferences` storage |
| `otadata` | 8 KB | OTA boot state |
| `app0` (`ota_0`) | ≥ 1.5 MB *(1.4 MB absolute floor)* | Active firmware |
| `app1` (`ota_1`) | **same size as app0** | OTA target |
| Filesystem | optional | Not used by the code |

Current firmware binary size: **~1.29 MB**. Add ~20–30% headroom for growth → **1.5 MB is the safe target per app partition**.

### Recommended schemes by flash size

| Flash | Recommended scheme | App per slot | Filesystem | Notes |
|---|---|---|---|---|
| **4 MB** | `Minimal SPIFFS (1.9MB APP with OTA/128KB SPIFFS)` | 1.875 MB ×2 | 128 KB | Small but works |
| **4 MB** | `No FS 4MB (2MB APP x2)` | 2.0 MB ×2 | – | Best 4MB option |
| **8 MB** | **`8M with spiffs (3MB APP/1.5MB SPIFFS)`** | 3.0 MB ×2 | 1.5 MB | **Firmware default** |
| **16 MB** | `16M Flash (3MB APP/9.9MB FATFS)` | 3.0 MB ×2 | 9.9 MB | Comfortable |
| **32 MB** | `32M Flash (4.8MB APP/22MB FATFS)` | 4.8 MB ×2 | 22 MB | Overkill but fine |

### Full compatibility matrix

| Scheme | Works? | App per slot | Notes |
|---|---|---|---|
| Default 4MB with spiffs | ⚠️ Very tight | 1.25 MB ×2 | ~20 KB headroom at 98% |
| Default 4MB with ffat | ⚠️ Very tight | 1.25 MB ×2 | Same |
| **8M with spiffs (3MB APP/1.5MB SPIFFS)** | ✅ **Recommended** | 3.0 MB ×2 | 41% usage |
| Minimal (1.3MB APP/700KB SPIFFS) | ❌ | single app | No `ota_1` |
| No FS 4MB (2MB APP x2) | ✅ | 2.0 MB ×2 | No FS — fine |
| No OTA (2MB APP/2MB SPIFFS) | ❌ | single app | No OTA |
| No OTA (1MB APP/3MB SPIFFS) | ❌ | single app | No OTA |
| No OTA (2MB APP/2MB FATFS) | ❌ | single app | No OTA |
| No OTA (1MB APP/3MB FATFS) | ❌ | single app | No OTA |
| Huge APP (3MB No OTA/1MB SPIFFS) | ❌ | single app | No OTA |
| Minimal SPIFFS (1.9MB APP with OTA/128KB SPIFFS) | ✅ | 1.875 MB ×2 | Good for 4 MB |
| 16M Flash (2MB APP/12.5MB FATFS) | ✅ | 2.0 MB ×2 | |
| 16M Flash (3MB APP/9.9MB FATFS) | ✅ | 3.0 MB ×2 | |
| RainMaker 4MB | ⚠️ Very tight | 1.25 MB ×2 | Same as Default 4MB |
| RainMaker 4MB No OTA | ❌ | single app | No OTA |
| RainMaker 8MB | ✅ | ~2.5–3 MB ×2 | |
| 32M Flash (4.8MB APP/22MB FATFS) | ✅ | 4.8 MB ×2 | |
| 32M Flash (4.8MB APP/22MB LittleFS) | ✅ | 4.8 MB ×2 | |
| 32M Flash (13MB APP/6.75MB SPIFFS) | ✅ | 13 MB ×2 | |
| ESP SR 16M (3MB APP/7MB SPIFFS/2.9MB MODEL) | ✅ | 3.0 MB ×2 | |
| Zigbee ZCZR 4MB with spiffs | ❌ | reduced by Zigbee | No room |
| Zigbee ZCZR 8MB with spiffs | ⚠️ Verify | reduced by Zigbee | Test it |
| Custom | depends | must have `ota_0` + `ota_1` ≥ 1.5 MB each | |

> **Rule of thumb:** if the scheme name contains **"No OTA"**, the firmware boots, but any `/trigger_update`, `/start_ota_*`, or auto‑update call will fail with `No OTA partition found`.

---

## 💾 Flash Size Requirements

| Flash | Verdict |
|---|---|
| **2 MB** | ❌ Cannot fit two 1.5 MB app partitions |
| **4 MB** | ⚠️ **Absolute minimum** — works today at ~98% usage |
| **8 MB** | ✅ **Recommended floor** — ~41% usage, real OTA headroom |
| **16 MB** | ✅ Comfortable |
| **32 MB** | ✅ Overkill but fully supported |

### Space used by the current firmware

Measured on a real **ESP32‑S3 DevKit N8R2** build:

| Metric | Value | Notes |
|---|---|---|
| Program (flash) | **1,291,473 bytes ≈ 1.23 MB** | Compiled `.bin` |
| Global variables (RAM) | **126,988 bytes ≈ 124 KB** | ~38% of 320 KB DRAM |
| Sketch + data | ~1.30 MB | Fits in 1.5 MB partition with ~200 KB headroom |

### OTA headroom needed

Each OTA update writes the incoming `.bin` to the **other** app partition:

```
app0 (active firmware)   ← currently running
app1 (OTA target)        ← new firmware written here, then reboot
```

So you need:

```
flash  ≥  2 × max(firmware size)  +  NVS  +  otadata  +  filesystem
```

With a 1.29 MB firmware, that means **≥ 2.6 MB for the two apps alone**. On 4 MB flash this leaves barely any room for filesystem or growth; on 8 MB there's plenty.

---

## 📱 Usage

### Quick Start

1. **Add the Wi‑Fi network** `ESP32-Mouse` (password `12345678`) manually — it won't appear in scans because it's hidden.
2. **Open any browser** — the captive portal redirects to `http://192.168.4.1/`, or use `esp32-mouse.local`.
3. **Plug the ESP32** into your computer/TV via USB‑C.
4. **Use the web UI** to control the cursor, type, send media commands.

### Web Interface

- **Mouse Pad** – drag to move cursor; tap for left‑click
- **Arrow keys** – hold for repeated movement (interval adjustable)
- **Mouse buttons** – left/right/middle, double‑click, press/release
- **Keyboard grid** – full QWERTY layout with sticky modifiers
- **Text input** – type arbitrary ASCII text
- **Real‑time input** – live typing with backspace support
- **Settings** – sensitivity, repeat, legacy, boot protocol, TX power, power save (debounced autosave)
- **Gyro Mouse** – phone orientation → cursor movement
- **Media / TV** – consumer control buttons
- **Logs** – client‑side log panel + `/logs` JSON endpoint
- **Firmware Update** – dedicated `/update` page (see below)

### Wi‑Fi STA (Client) Mode

1. Click the **📶** icon (or go to `/sta`)
2. The page auto‑scans for Wi‑Fi networks
3. Click a network to autofill SSID and BSSID
4. Enter password (tick **Hidden network** if applicable)
5. Click **Connect** — status updates live

The ESP32 remembers credentials and retries up to 3 times per boot.

---

## 🔄 Firmware Update Methods

The firmware supports **four** update paths:

### 1. Manual upload (web UI)

`/update` → file picker → **Upload & Update**

- Multipart POST to `/upload`
- Streams firmware chunks directly into `Update.write()`
- SHA‑256 computed incrementally
- If STA is connected, expected hash is fetched from version URL and compared
- On success: reboot

**Best for:** offline recovery, testing builds, bypassing network issues.

### 2. Secure OTA (three‑tier)

`/update` → **Start Secure OTA** (`/start_ota_secure`)

The flow tries three tiers in order:

| Tier | Method | What it verifies |
|---|---|---|
| **1** | `WiFiClientSecure::setCACert(rootCACertificate)` | Full X.509 chain to **Secigo Root E46** |
| **2** | `setFingerprintSHA256()` *(core 3.x)* / `setFingerprint()` *(core 2.x)* | Leaf cert SHA‑256 of `raw.githubusercontent.com` |
| **3** | `setInsecure()` — **only after user confirmation** | Nothing — user explicitly trusts the network |

If tier 1 or 2 succeeds, the download proceeds automatically. If both fail, the SSE stream emits `ota_state: insecure_offer`, which reveals the **"Retry Insecurely"** button on the page. Clicking it starts a new task in `OTA_INSECURE` mode.

**Best for:** normal use — the CA tier usually succeeds, and the fingerprint tier catches the rare CA rotation.

### 3. URL / auto update

`/update` → **Check for Update** → **Trigger URL Update**

- `checkAndUpdate()` fetches `version.txt` from the configured URL and compares against `FW_VERSION_STR`
- If a newer version is available, the **Trigger URL Update** button calls `startSecureOta(false)` — same three‑tier flow as above

**Best for:** keeping devices up to date without manual uploads.

### 4. Automatic check

On boot (if STA connected) and once per 24 h in `loop()`, `checkAndUpdate()` runs in a FreeRTOS task. It only fetches metadata — it does **not** flash automatically.

**Best for:** notifying users that a new firmware is available via the web UI.

### Live progress (SSE)

During any secure OTA, the browser receives:

- `log` events — one per OTA log line
- `progress` events — `{written, total, pct}` every 500 ms
- `ota_state` events — `idle`, `running`, `insecure_offer`, `rebooting`, `failed`
- `time` events — uptime + UTC time every 1 s

The progress bar on the `/update` page updates live from the `progress` events.

### Update URL configuration

Two URLs, both editable via the web UI:

- **Version URL** — plain text: `version\nsha256_hash` (two lines)
- **Binary URL** — points to the firmware `.bin`

Defaults:
```
version.txt: https://github.com/Aminiow/ESP32-HID-Web-Remote-Controller/raw/refs/heads/main/version.txt
firmware.bin: https://github.com/Aminiow/ESP32-HID-Web-Remote-Controller/raw/refs/heads/main/firmware.bin
```

> **Note:** GitHub redirects `github.com/.../raw/...` → `raw.githubusercontent.com`. The fingerprint tier uses the **final** peer cert, so `GITHUB_LEAF_FP` must match `raw.githubusercontent.com`'s leaf, not `github.com`'s. The default fingerprint is updated for the current leaf.

---

## 🔐 Security Model

| Layer | Mechanism | Strength |
|---|---|---|
| Transport | TLS 1.2+ via mbedTLS | Standard |
| **Tier 1** | Root CA chain validation (Secigo E46) | Highest — full chain |
| **Tier 2** | Leaf cert SHA‑256 fingerprint | Strong — pins exact cert |
| **Tier 3** | Insecure (user‑confirmed) | Trust‑based |
| Firmware integrity | SHA‑256 of `.bin` body | Prevents corruption |
| Manual upload | SHA‑256 vs version file | Optional |

### Fingerprint lifecycle

`raw.githubusercontent.com` is fronted by **Fastly**. The leaf cert rotates roughly every **90 days**.

When it rotates:
- Tier 1 (Root CA) still works — CA certs last years.
- Tier 2 (fingerprint) fails — the pinned hash no longer matches.
- Flow falls through to **tier 3 offer** — user clicks "Retry Insecurely".

To refresh the pin, run:

**PowerShell:**
```powershell
$c = New-Object System.Net.Sockets.TcpClient("raw.githubusercontent.com",443)
$s = New-Object System.Net.Security.SslStream($c.GetStream(),$false,{$true})
$s.AuthenticateAsClient("raw.githubusercontent.com")
$cert = $s.RemoteCertificate
$sha = [System.Security.Cryptography.SHA256]::Create().ComputeHash($cert.GetRawCertData())
($sha | ForEach-Object { $_.ToString("x2") }) -join ""
```

**Linux/macOS:**
```bash
openssl s_client -connect raw.githubusercontent.com:443 -servername raw.githubusercontent.com </dev/null 2>/dev/null \
  | openssl x509 -noout -fingerprint -sha256
```

Paste the result into `#define GITHUB_LEAF_FP "..."`.

---

## ⚙️ Default Configuration

### Firmware defaults

| Setting | Default | Storage |
|---|---|---|
| Firmware version | `9.0.0` | `#define FW_VERSION_STR` |
| AP SSID | `ESP32-Mouse` | `ap_ssid` |
| AP password | `12345678` | `ap_password` |
| AP hidden | `true` | `WiFi.softAP(..., true)` |
| Sensitivity | `2.0` | NVS `settings/sens` |
| Repeat interval | `100 ms` | NVS `settings/repeat` |
| Legacy mode | `false` | NVS `settings/legacy` |
| Boot protocol | `false` | NVS `settings/bootproto` |
| Gyro enabled | `false` | NVS `settings/gyro` |
| TX power | `20 dBm` | NVS `settings/txpwr` |
| Power save | `true` | NVS `settings/psave` |
| Update version URL | GitHub `main/version.txt` | NVS `updates/verUrl` |
| Update binary URL | GitHub `main/firmware.bin` | NVS `updates/binUrl` |
| NTP servers | `pool.ntp.org`, `ir.pool.ntp.org`, `ntp.time.ir` | hardcoded |
| mDNS name | `esp32-mouse.local` | hardcoded |
| Consumer volume step | HID usage `0xE9`/`0xEA` | `#define` |
| Max log entries | `200` | `#define` |
| Idle sleep threshold | `60 s` | hardcoded |
| OTA CA cert | Secigo Public Server Auth Root E46 | hardcoded PEM |
| GitHub leaf fingerprint | `71f1077d...cf84` | `#define` |

### NVS namespaces

| Namespace | Keys |
|---|---|
| `settings` | `sens`, `repeat`, `legacy`, `bootproto`, `gyro`, `txpwr`, `psave` |
| `wifi` | `ssid`, `pass`, `hidden`, `bssid` |
| `updates` | `verUrl`, `binUrl` |

> **Warning:** Switching partition scheme erases NVS. Re‑configure Wi‑Fi and update URLs after the first boot on a new layout.

---

## 📊 Language Composition

This is a **single‑file Arduino sketch** (`.ino`) that embeds HTML, CSS, and JavaScript as `PROGMEM` string literals. Estimated composition by source bytes:

| Language | % | What it's used for |
|---|---|---|
| **C++** | **~52 %** | Core firmware logic, HID control, Wi‑Fi, OTA, TLS, NVS |
| **JavaScript** | **~18 %** | Web UI logic — mouse/keyboard events, SSE client, OTA progress |
| **HTML** | **~15 %** | Page structure — index, STA config, update page |
| **CSS** | **~13 %** | Dark theme, responsive layout, progress bar |
| **JSON / other** | **~2 %** | API responses, comments, markdown |

![C++](https://img.shields.io/badge/C%2B%2B-52%25-blue?style=flat-square&logo=cplusplus)
![JavaScript](https://img.shields.io/badge/JavaScript-18%25-yellow?style=flat-square&logo=javascript)
![HTML](https://img.shields.io/badge/HTML-15%25-orange?style=flat-square&logo=html5)
![CSS](https://img.shields.io/badge/CSS-13%25-blueviolet?style=flat-square&logo=css3)
![Other](https://img.shields.io/badge/Other-2%25-lightgrey?style=flat-square)

> Percentages are byte‑count estimates of the `.ino` source file, not counting comments or blank lines separately.

---

## 📸 Screenshots

> **Note:** Placeholder images — replace URLs with your own uploads.

### 📱 Phone view (touch layout)

<details>
<summary><b>Tap to expand — 6 phone screenshots</b></summary>

#### 1. Home / mouse pad

![Phone - Home](https://placehold.co/400x800/1e1e1e/5b9aff?text=Phone%3A+Home+%2F+Mouse+Pad)

*Top card with Wi‑Fi status, sensitivity slider, and the large touch pad. Drag to move, tap to left‑click.*

#### 2. Keyboard grid

![Phone - Keyboard](https://placehold.co/400x800/1e1e1e/5b9aff?text=Phone%3A+Keyboard)

*Full QWERTY with sticky modifiers and text input field.*

#### 3. Media controls

![Phone - Media](https://placehold.co/400x800/1e1e1e/5b9aff?text=Phone%3A+Media+Controls)

*Volume, mute, channel, power, and input selection buttons.*

#### 4. Wi‑Fi settings (`/sta`)

![Phone - WiFi](https://placehold.co/400x800/1e1e1e/5b9aff?text=Phone%3A+WiFi+Settings)

*Network scan, SSID/password fields, hidden network toggle, connect/disconnect/forget buttons.*

#### 5. Update page (`/update`)

![Phone - Update](https://placehold.co/400x800/1e1e1e/5b9aff?text=Phone%3A+Update)

*Secure OTA, auto‑update URLs, manual upload, live progress bar, log panel.*

#### 6. OTA in progress

![Phone - OTA Progress](https://placehold.co/400x800/1e1e1e/5b9aff?text=Phone%3A+OTA+Running)

*Progress bar + SSE log stream during a live secure OTA.*

</details>

### 🖥️ PC view (desktop layout)

<details>
<summary><b>Tap to expand — 4 PC screenshots</b></summary>

#### 1. Home — full two‑column layout

![PC - Home](https://placehold.co/1200x800/1e1e1e/5b9aff?text=PC%3A+Home+Full)

*Mouse pad on the left, keyboard on the right, media controls below.*

#### 2. Update page — full view

![PC - Update](https://placehold.co/1200x800/1e1e1e/5b9aff?text=PC%3A+Update+Page)

*Secure OTA, URL config, manual upload, live progress, log panel.*

#### 3. OTA progress with SSE log

![PC - OTA Progress](https://placehold.co/1200x800/1e1e1e/5b9aff?text=PC%3A+OTA+Live)

*Progress bar at 47%, log lines streaming in.*

#### 4. Raw logs (`/logs`)

![PC - Logs](https://placehold.co/1200x800/1e1e1e/5b9aff?text=PC%3A+Raw+Logs+JSON)

*JSON output of the in‑RAM ring buffer.*

</details>

---

## 🛠 Troubleshooting

| Symptom | Possible cause / solution |
|---|---|
| **TV/computer does not recognise USB HID** | 1. Ensure **USB CDC On Boot** is **Disabled**.<br>2. Use a data‑capable USB cable.<br>3. Power externally if USB can't supply enough current.<br>4. Verify the USB port supports OTG. |
| **Can't find Wi‑Fi AP** | SSID is **hidden**. Manually add `ESP32-Mouse` / `12345678`. |
| **Captive portal not redirecting** | Manually go to `http://192.168.4.1` or `esp32-mouse.local`. |
| **Keyboard keys not sending** | Verify USB connection and that the host has focus on a text field. |
| **STA connection fails / retries** | Check SSID/password. Retries up to 3× with 5 s interval. See `/logs`. |
| **Settings not saved** | Ensure NVS has enough space. Settings persist across power‑cycles. |
| **Wi‑Fi scan doesn't show networks** | Confirm range and antenna. |
| **Firmware update fails** | Check URLs; ensure hash matches (if provided); ensure STA connected. |
| **"No OTA partition found"** | You're on a **"No OTA"** partition scheme. Switch to `8M with spiffs`. |
| **Sketch too big / 100% flash** | You're on 4 MB with `Default 4MB with spiffs`. Switch to `8M with spiffs` (you have 8 MB). |
| **Manual upload rejected with "Hash mismatch"** | The uploaded file doesn't match the version file's hash. Download a fresh copy. |
| **OTA fails with "Fingerprint mismatch"** | GitHub rotated its leaf cert. Re‑capture `GITHUB_LEAF_FP` or use **Retry Insecurely**. |
| **OTA fails with "Root CA failed"** | NTP not synced, or CA rotation. Try later or use **Retry Insecurely**. |
| **Consumer controls not working** | Some hosts don't support USB HID consumer control. Try another device. |
| **Gyro mouse not working** | On iOS, grant motion permission. Check browser `deviceorientation` support. |
| **Web interface slow** | Disable power save; increase TX power; ensure not in idle sleep. |
| **Version not updating in UI** | Check `/update_status` returns valid JSON; UI polls every 30 s. |
| **`configTime` compile error on core 3.x** | Reduced to 3 NTP servers max: `configTime(0, 0, "pool.ntp.org", "ir.pool.ntp.org", "ntp.time.ir");` |
| **`setFingerprint` compile error on core 3.x** | Use `getFingerprintSHA256()` post‑handshake. See `clientFingerprintHex()` helper. |

---

## 📜 License

MIT — see [LICENSE](LICENSE).

---

## 🤝 Contributing

Contributions welcome! Open an issue or PR on [GitHub](https://github.com/Aminiow/ESP32-HID-Web-Remote-Controller).

---

## 🙏 Acknowledgements

- [Espressif Systems](https://www.espressif.com/) — ESP32‑S3 and Arduino core
- [TinyUSB](https://github.com/hathach/tinyusb) — USB stack
- [arduinoWebSockets](https://github.com/Links2004/arduinoWebSockets) — WebSocket support
- [Secigo](https://www.secigo.com/) — TLS Root CA
- [Fastly](https://www.fastly.com/) — GitHub raw CDN

---

**Happy controlling!** 🎮
