<h1 align="center">sidemdm</h1>

<p align="center">
  Enroll an Android phone from your own computer, then hand it back <b>unmanaged</b>.<br>
  No cloud. No account. No company. Just your LAN.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platforms">
  <img src="https://img.shields.io/badge/python-3.10%2B-green.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/github/v/release/lukeponio/sidemdm?color=orange" alt="Latest release">
</p>

<p align="center">
  <a href="#key-features">Key Features</a> &nbsp;•&nbsp;
  <a href="#tested-devices">Tested Devices</a> &nbsp;•&nbsp;
  <a href="#how-to-use">How To Use</a> &nbsp;•&nbsp;
  <a href="#download">Download</a> &nbsp;•&nbsp;
  <a href="#how-it-works">How It Works</a> &nbsp;•&nbsp;
  <a href="#build-it-yourself">Build</a> &nbsp;•&nbsp;
  <a href="#credits">Credits</a> &nbsp;•&nbsp;
  <a href="#license">License</a>
</p>

sidemdm turns the phone's built-in **six-tap QR** enterprise setup into something you run entirely on your own network. Your computer shows a QR, the phone creates a work profile owned by a tiny app, and then you tap **Remove Work Profile**. You end up with an ordinary, unmanaged phone whose personal side was never touched.

A personal-use tool for phones **you own**. It has been verified on the devices below; other models may behave differently.

## Key Features

- 🔌 **Fully local** — the APK is served from your computer over your LAN. No management server, no telemetry, and the app has no internet permission.
- 🤖 **Agent-ready** — paste one prompt into Claude Code, Codex or Grok and it does every computer-side step for you.
- 🧹 **Clean teardown** — one tap removes only the work profile; your personal apps, files and accounts stay. No factory reset to undo it.
- 🔒 **Tamper-proof delivery** — the QR pins the APK by SHA-256, so a swapped file is rejected even over plain HTTP.
- 🛡️ **Can't go rogue** — the app will only ever create a *work profile*; it refuses to become a full-device owner.
- 💻 **No install dance** — Windows, macOS and Linux with just **Python 3.10+**. QR generation is bundled, so there's nothing to `pip install`, and no Android SDK, domain or certificate.

## Tested devices

| Device | Android / API | Build / firmware | Enroll | Remove | Notes |
|---|---|---|---|---|---|
| Motorola moto g power (2026) | Android 16 · API 36 | `W1WEOS36.48-22-3-3-4-2` (patch 2026-04-01) | ✅ | ✅ | Served over plain HTTP on the LAN, computer online. |
| Motorola moto g power (2026) | Android 16 · API 36 | `W1WEOS36.48-22-3-3-4-9` (patch 2026-10-01) | ✅ | ✅ | Locked bootloader; verified boot green. Teardown recorded above. |

Verified a device yourself? Open a PR adding a row with the model, Android/API level, and `adb shell getprop ro.build.fingerprint`.

## How To Use

You need a computer with **Python 3.10+** on the same Wi-Fi as an Android phone you're willing to **factory reset**.

### The easy way — let your AI agent do it

**1.** Start your agent in an empty folder: run `claude` (Claude Code), `codex` (Codex) or `grok` (Grok CLI).

**2.** Paste this prompt:

```
Set up and run sidemdm for me so I can enroll an Android phone and then remove the work profile, ending with a clean unmanaged phone. Clone https://github.com/lukeponio/sidemdm, read its AGENTS.md, and do all the computer-side steps (needs only Python 3.10+, nothing to pip install): put the latest sidemdm APK from the repo's GitHub Releases into dist/, detect my LAN IP, then run `python sidemdm.py --ip <that IP>` as a running process and show me the QR. Keep it running, then give me the exact phone steps I must do myself and wait.
```

The agent handles the computer; it will then walk you through the phone steps (which only you can do).

### The manual way

```bash
gh release download --repo lukeponio/sidemdm --pattern '*.apk' --dir dist   # or download the APK by hand
python sidemdm.py
```

`sidemdm.py` finds your LAN IP, serves the APK, and prints a QR in the terminal. Pass `--ip 192.168.0.22 --port 8080` if it picks the wrong address or the port is busy.

### Then, on the phone

1. **Factory reset** the phone — back it up first if it holds anything you want to keep (enrollment only starts from first-run setup).
2. On the welcome screen, **tap six times** to open the QR scanner.
3. **Scan the QR**, then join the **same Wi-Fi** as your computer when it asks.
4. Accept the work-profile setup. A **Work** tab appears in your app drawer.
5. In your app drawer, open the **Work** tab, launch the **Work Profile** app there, and tap **Remove Work Profile** (two confirmations).

Done: a clean, unmanaged phone. Press **Ctrl+C** to stop the server — it isn't needed after the download, and removal works with no network at all.

## Download

Grab the signed APK from the [**Releases**](https://github.com/lukeponio/sidemdm/releases/latest) page and drop it in `dist/`. The QR verifies the exact file by SHA-256, so you always know you're serving the right build.

## How It Works

Three small pieces, no backend:

- **The app** (`app/`) — a Kotlin Device Policy Controller. It only ever selects `PROVISIONING_MODE_MANAGED_PROFILE` and cancels if the phone offers just full-device mode, so it can never become a device owner. The one destructive action, **Remove Work Profile**, calls `wipeData` on the work profile alone — after re-checking it truly owns a managed profile, behind two confirmations — and never a device-wide wipe. No internet permission.
- **The launcher** (`sidemdm.py`) — detects your LAN IP, builds the provisioning QR, and serves the APK over HTTP on your network.
- **The QR tool** (`tools/generate_qr.py`) — computes the checksum, builds an immutable release, and refuses non-LAN or unsafe URLs.

## Build It Yourself

Prefer not to trust a prebuilt binary? Build and sign your own, then drop it in `dist/`:

```bash
cd android
./gradlew :app:testDebugUnitTest :app:assembleRelease   # Windows: gradlew.bat ...
cp app/build/outputs/apk/release/app-release.apk ../dist/sidemdm-1.0.1.apk
```

The Android project lives in [`android/`](android/). Signing is read from `android/keystore.properties` or environment variables — see [docs/release.md](docs/release.md). Needs JDK 17 and Android SDK Platform 36.

## Known limits

- **Short tested list.** See [Tested devices](#tested-devices). Other OEMs and the no-internet case are untested.
- **Plain HTTP by default.** The SHA-256 pin guarantees integrity, but some firmware may refuse an HTTP provisioning download. An HTTPS mode exists ([docs/offline-lan-setup.md](docs/offline-lan-setup.md)) but needs a hostname and certificate.
- **Approved-DPC allowlist.** Some devices only allow Google-approved enterprise DPCs. If you see "App blocked to protect your device," this method won't work there, and there's no bypass.
- **Factory reset required** to start the six-tap flow. Back up first.
- **No warranty** — see [LICENSE](LICENSE). Use on phones you own and data you've backed up.

## Repository layout

| Path | What it is |
|---|---|
| `sidemdm.py`, `run.sh`, `run.bat` | The launcher: detect IP, build QR, serve the APK. |
| `android/` | The Android Device Policy Controller (Kotlin) and its Gradle build. |
| `tools/generate_qr.py` | QR + immutable release builder, with a LAN-safety check. |
| `server/` | Optional Docker/nginx server (plain-HTTP and HTTPS configs). |
| `docs/` | [Offline LAN setup](docs/offline-lan-setup.md) · [release](docs/release.md) · [testing](docs/testing.md). |
| [`AGENTS.md`](AGENTS.md) | Checklist for AI coding agents driving this. |
| `dist/` | Where the prebuilt APK goes. |

## Credits

Built with [Kotlin](https://kotlinlang.org/) and the Android `DevicePolicyManager` API, [segno](https://github.com/heuer/segno) for QR generation, and [nginx](https://nginx.org/) for the optional server. README format inspired by [Markdownify](https://github.com/amitmerchant1990/electron-markdownify).

## License

[MIT](LICENSE)

---

> Made for people who want to understand — and undo — what "enrollment" does to their own phone.
