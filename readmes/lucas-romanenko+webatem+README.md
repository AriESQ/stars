<p align="center"><img src="docs/brand/banner.png" alt="webATEM. Browser control for ATEM switchers. Run the server, open a tab, cut the show." width="100%"></p>

**Browser control for ATEM switchers.** Run the server on a Mac, a Windows
PC or a Linux box, and control your ATEMs in a browser from any device on
the network: desktop, laptop, tablet or phone. WebATEM finds the switchers
for you and gives you the whole control surface: switching, keyers, audio,
media pool, macros. Run the server, open a tab, cut the show.

<p align="center">
  <a href="https://github.com/lucas-romanenko/webatem/releases/latest"><img src="https://img.shields.io/github/v/release/lucas-romanenko/webatem?style=flat-square&color=2FD07A&label=release" alt="Latest release"></a>
  <a href="https://pypi.org/project/webatem/"><img src="https://img.shields.io/pypi/v/webatem?style=flat-square&color=9A9E9F&label=pypi" alt="On PyPI"></a>
  <a href="https://github.com/lucas-romanenko/webatem/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/lucas-romanenko/webatem/ci.yml?branch=main&style=flat-square&label=tests" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-9A9E9F?style=flat-square" alt="MIT licensed"></a>
</p>

<p align="center">
  <a href="https://github.com/lucas-romanenko/webatem/releases/latest/download/webatem-windows-x64-setup.exe"><img src="https://img.shields.io/badge/Download-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Download for Windows"></a>
  &nbsp;
  <a href="https://github.com/lucas-romanenko/webatem/releases/latest/download/webatem-macos-arm64.dmg"><img src="https://img.shields.io/badge/Download-macOS%20(Apple%20silicon)-000000?style=for-the-badge&logo=apple&logoColor=white" alt="Download for macOS, Apple silicon"></a>
  &nbsp;
  <a href="https://github.com/lucas-romanenko/webatem/releases/latest/download/webatem-macos-intel.dmg"><img src="https://img.shields.io/badge/Download-macOS%20(Intel)-333333?style=for-the-badge&logo=apple&logoColor=white" alt="Download for macOS, Intel"></a>
  &nbsp;
  <a href="https://github.com/lucas-romanenko/webatem/releases/latest/download/webatem-linux-x64"><img src="https://img.shields.io/badge/Download-Linux-E95420?style=for-the-badge&logo=linux&logoColor=white" alt="Download for Linux"></a>
</p>
<p align="center"><sub>Download it, open it, and your switchers appear. &nbsp;·&nbsp; Windows installs per-user, no admin needed. &nbsp;·&nbsp; The Linux build runs on desktop <b>and</b> headless servers.</sub></p>

Three ways to run it, all simple:

- **Just you, right now** → **download it** for your Mac or Windows machine
  and open it. It lives in your menu bar / system tray (with a *Start at
  login* switch), opens your browser, and your switchers appear. Like ATEM
  Software Control, but in your browser, and on every device on the network.
- **Your whole team, always on** → **host it** on a Linux box, VM or Raspberry
  Pi with one Docker command; everyone on the network opens one address, from
  any device. No accounts.
- **Already have Python?** → `pipx install "webatem[desktop]"`, then `webatem`.

Every way of running it **auto-discovers the ATEMs on your network**
(Bonjour/mDNS) and lists them by name, exactly like ATEM Software Control.
Open the page and they are already there:

<p align="center">
  <img src="docs/screenshot-connect.png" alt="WebATEM connect page: recent connections and the switchers found on the network, each listed by name and address" width="900">
</p>

<p align="center">
  <img src="docs/screenshot-control.png" alt="WebATEM control surface: program/preview buses, T-bar, keyers, transitions and macros" width="900">
</p>

## What you get

- **Full switcher control.** Program/preview buses per M/E, cut/auto,
  transition styles (mix, dip, wipe, DVE, stinger) with per-style settings,
  fade to black, color generators, aux routing, source renaming that follows
  live switcher labels.
- **Upstream and downstream keyers.** USK 1 to 4 (luma, chroma, pattern, DVE with
  fly keyframes, masks), DSKs with tie/rate/clip/gain, on-air countdowns.
- **Fairlight audio.** Per-strip faders, EQ, dynamics, master bus, and live
  audio meters streamed over WebSocket (tab-gated so idle pages cost nothing).
- **Media pool.** Live thumbnails of every still slot, and drag-and-drop
  image upload straight onto a slot: any image, fitted to the switcher's own
  video mode server-side.
- **Macros.** Browse and run switcher macros.
- **Save and restore switcher state.** Full switcher profile export/import as
  XML, compatible with ATEM Software Control’s “Save Switcher State”,
  including media pool images and macro bytecode.
- **HyperDeck transport.** Clip browser and play/pause/stop/loop for decks
  bound to the ATEM (TCP/9993), from the same page.
- **Multi-operator by design.** One pooled connection per switcher shared by
  all operators; state fan-out over WebSockets with adaptive polling
  (30 ms during transitions, relaxed when idle).

Deep per-switcher settings live in the Settings panel: color generators,
each upstream keyer (luma / chroma / pattern / DVE), downstream keyers,
transitions, video mode, input labels, outputs and HyperDecks:

<p align="center">
  <img src="docs/screenshot-settings.png" alt="WebATEM settings panel: color generators and an upstream keyer expanded, showing HSL controls, fill-source dropdown and wipe patterns" width="900">
</p>

Full **Fairlight audio**, a per-strip mixer with input gain, EQ and dynamics
curves, faders, pan and live meters, and a writable 6-band parametric EQ
behind each strip:

<p align="center">
  <img src="docs/screenshot-audio.png" alt="WebATEM Fairlight audio mixer: 14 strips with input, EQ, dynamics, faders, pan and meters" width="900">
</p>

The **media pool**: live thumbnails of every still slot and what each media
player is holding, with drag-and-drop upload straight onto a slot:

<p align="center">
  <img src="docs/screenshot-media-pool.png" alt="WebATEM media pool: two media players, MP1 on air with colour bars, and twenty still slots, five holding stills (bars, a lower third, a Starting soon card, a logo bug, a Back in five card)" width="900">
</p>
---

## Which switchers has it run on?

**Every hour it has ever run has been against ATEM 1 M/E Constellation HD
switchers**, where it drives a working broadcast operation daily. That is one
model out of a large family, and it is the honest answer to "will it work
with mine".

It should work more widely than that. The protocol is the same across the
range, the control surface is built from what each switcher reports about
itself rather than from a hardcoded model list, and features a switcher does
not have simply do not appear. But should is not the same as does, and
nobody has checked.

So if you have a Mini, a Mini Pro, a Television Studio, a 2 M/E or 4 M/E, or
anything else with an ATEM badge on it, **trying this and telling me what
happened is the single most useful thing you can do for the project**. It
does not matter whether it works. An issue saying which model you have and
what went wrong is worth more than one that says it went fine.

A [switcher report](../../issues/new?template=switcher-report.yml) takes a
minute and needs no code. If you go further and fix what you found, a patch
for a switcher I do not own is welcome on your word plus a green test suite:
see [CONTRIBUTING.md](CONTRIBUTING.md).

One known limit while you are here: still upload and capture follow the
switcher's own video mode, but only 1080p switchers have been tested. If yours
runs another mode, that report is especially welcome.

---

## Get started

### Option A. Download it  *(Mac, Windows)*

1. Click your platform's **Download** button at the top (or the
   [Releases](https://github.com/lucas-romanenko/webatem/releases) page).
2. Open it. The icon appears in the menu bar / tray and the launcher window
   comes up: pick the interface and port if the defaults are not right, then
   **Launch GUI** opens the control page in your browser with the ATEMs on
   your network listed. Pick one and you're controlling it.

That's the whole setup. Nothing to install alongside it, no Python, no Docker.

**On a Mac, one line in Terminal does both steps** and skips the first-launch
security prompt described below (it downloads the right build for your chip,
puts WebATEM in Applications and opens it):

```sh
curl -fsSL https://github.com/lucas-romanenko/webatem/releases/latest/download/install-mac.sh | sh
```

While it runs it is a small window plus an icon in the **menu bar (Mac) /
system tray (Windows)**, the way Bitfocus Companion works, with nothing in the
Dock or on the taskbar, only the icon. The window shows
**Running** and the address other devices use, and holds the settings:
**Interface** (all of them, one adapter, or this computer only), **Port**,
**Start minimized**, **Run at login**, with **Launch GUI** (opens the control
page in your browser), **Hide** and **Quit**. Closing the window just hides
it; the tray menu is three items: **Show/Hide window**, **Launch GUI**,
**Quit**. Changing the interface or port restarts the server on the new
address right there; handy on a laptop with Wi-Fi, Ethernet and a VPN at
once. **Launch GUI** opens the address shown, the real interface and port,
the same one other devices use (this computer also answers at `127.0.0.1`
whichever interface is chosen). Nothing listens until you have picked an
interface in the window: it opens on **Not running** and waits for your
choice. Tick **Run at login** (or **Start minimized**) and it comes back up
on that interface by itself from then on, including when the machine boots
with no window and no second choice. The default port is **8880** (Bitfocus Companion has 8000); if
the port is taken anyway, the next free one is used and the window says so.

<details>
<summary><b>First-launch security prompt</b> (the app isn't code-signed yet)</summary>

Because the downloads aren't signed with a paid developer certificate, the OS
warns you the first time. One-time, then it opens normally:

- **macOS:** double-click, let it get blocked, then **System Settings →
  Privacy & Security → “Open Anyway”**. (On older macOS: right-click → Open.)
  Or skip it entirely with the Terminal line above: a browser marks what it
  downloads for that check, and curl does not.
- **Windows:** **More info → Run anyway** on the SmartScreen prompt for the
  installer, once. (Windows warns about any unsigned program the first time.)

The macOS build signs and notarizes itself as soon as the repository holds
an Apple Developer ID (the build workflow says which secrets); from that
release on the download opens with no warning. Windows signing is a
separate paid certificate, not done.
</details>

### Option B. Host it  *(a whole team; always on)*

Run it on a **Linux box, VM or Raspberry Pi on the same network as your
ATEMs** (the ATEM-Software-Control-on-a-server model). The published image
is built for amd64 and arm64:

```bash
docker run -d --name webatem --network host --restart unless-stopped \
  -v webatem-data:/app/data ghcr.io/lucas-romanenko/webatem:latest
```

Open `http://<that-box>:8880` from any device on the network. It comes back
automatically on reboot. No `.env` file needed: every setting has a working
default (SQLite DB + a generated secret key live in the `webatem-data`
volume); see [.env.example](.env.example) for knobs like `PORT`, `TIME_ZONE`,
`ALLOWED_HOSTS`. (In Docker the address and port come from that environment.) Prefer Compose? The repository's
[compose.yml](compose.yml) runs the same image: `docker compose up -d`.

Without Docker: the `webatem-linux-x64` binary from the Releases page runs
headless too: on a machine with no display it skips the browser and tray and
prints the address to open from another device:

```
WebATEM is running.
  On this machine:      http://127.0.0.1:8880/atem/
  From another device:  http://192.168.1.50:8880/atem/
```

Keep it up with a systemd unit, `tmux` or `nohup`.

> **Why Linux for hosting?** Discovery needs the app to see your LAN directly.
> That works natively on Linux (the container uses host networking). Docker
> Desktop on **Mac/Windows** runs containers in a VM that can’t see LAN
> discovery traffic, so on a Mac or PC use the download (Option A) or pipx
> (Option C), not Docker.

### Option C. pipx  *(you already have Python 3.10+)*

```bash
pipx install "webatem[desktop]"      # or, with uv: uvx --from "webatem[desktop]" webatem
webatem
```

Same behaviour as the download: a native process on your real network, the
tray icon and the launcher window appear where there is a desktop. Prebuilt wheels
for every platform mean no compiler is needed. Upgrade with
`pipx upgrade webatem`.

---

## Finding your switchers

Three ways, in order of magic:

1. **Automatic (Bonjour/mDNS).** On the same network as your ATEMs, they show
   up under **“On Your Network”** with their names, no typing. This is what
   ATEM Software Control does.
2. **Scan subnet.** For ATEMs that don’t advertise over Bonjour, type your
   subnet (e.g. `192.168.1`) and hit **Scan**, which finds them by IP.
3. **Manual IP.** Type an address and connect. Recent connections are
   remembered for one-click reconnect.

> Automatic discovery is **same-network only**: Bonjour/mDNS is link-local
> and doesn’t cross a router or VPN (this is true of ASC too). Reaching your
> ATEMs over a **VPN**? Auto-discovery won’t see them, but **Scan** and
> **manual IP** work fine over the tunnel.

---

## WebATEM vs. ATEM Software Control

ATEM Software Control (ASC) is Blackmagic’s own free control app, and it’s
excellent, and WebATEM isn’t trying to replace all of it. The difference is
*access*: ASC is a desktop app tied to one machine; WebATEM is a control
surface any device on your network can open (and you can still run it locally
like ASC if you want).

|  | **WebATEM** | **ATEM Software Control** |
|---|---|---|
| **Runs on** | Any browser: Windows, macOS, **Linux**, ChromeOS, iPad, phone | Windows & macOS desktop only |
| **Client install** | None, just open a URL | Installed per machine |
| **Access from** | Any device on the network | The machine it’s installed on |
| **Multiple operators** | One shared switcher session, many operators | Each machine opens its own session |
| **Phones / tablets** | ✓ Responsive | ✗ |
| **How to run** | Download it, host one instance for everyone (Docker), or `pipx install "webatem[desktop]"` | Install on each machine |
| **Price** | Free, open source | Free (proprietary) |
| **Feature breadth** | Core: switching, keyers, Fairlight audio, media pool, macros, profiles, HyperDeck | Everything, incl. camera control (CCU), streaming & recording, SuperSource |
| **Support** | Community / self-hosted | Official Blackmagic |

**Reach for ASC** when you need the full feature set on one operator’s machine
camera control, streaming/recording, SuperSource, recording macros.

**Reach for WebATEM** when you want the core control surface available to
anyone on the network, on any device or OS: a second operator on an iPad, a
Linux box in the rack room, a phone at the camera position.

## Running it for real

- **There is no login, by design.** Like the hardware panel, anyone who can
  reach the page can control your switchers. Keep it on the studio network. If
  you must expose it further, put your reverse proxy’s auth (basic auth, SSO)
  and TLS in front, and set `CSRF_TRUSTED_ORIGINS=https://your.host`.
- **Web pages can’t drive it cross-origin.** The control WebSocket only
  accepts browser connections from the app’s own pages (same-origin), so a
  malicious website open in an operator’s browser can’t reach the switchers.
  If your reverse proxy rewrites `Host`, list the browser-facing host in
  `WEBSOCKET_ALLOWED_ORIGINS`.
- It talks raw UDP to switchers on port 9910 (the ATEM protocol has no
  authentication, which is the hardware and not this app), so it needs to be on a
  network that can reach them.
- **Logs.** The desktop app and pipx write `webatem.log` in their data folder
  (macOS `~/Library/Application Support/WebATEM`, Windows
  `%LOCALAPPDATA%\WebATEM`, Linux `~/.local/share/WebATEM`). The launcher
  window's **Show log** button opens it. It rotates at 2 MB and keeps three
  old copies. With Docker: `docker compose logs webatem`.
- **Single instance, by design.** The switcher connection pool, media-pool
  watcher, and channel layer are process-local; one instance handles many
  switchers and operators. Don’t run several against the same switchers.
- Still upload and capture follow the switcher's own video mode; only **1080p**
  has been tested (all production use so far).

## Architecture

```
Browser (Alpine.js + WebSockets)
   │  ws/atem/ · HTTP
   ▼
Django + Channels (single ASGI worker, uvicorn)
   │  pooled UDP session per switcher (atemwire)
   ▼
ATEM switchers (UDP 9910) · HyperDecks (TCP 9993 / FTP)
```

- **[atemwire](https://github.com/lucas-romanenko/bmdwire/tree/main/atemwire)** is the
  ATEM protocol library, a substantially modified fork of Martijn Braam's
  pyatem: declarative wire-format DSL, hardened UDP transport (in-order
  delivery, retransmit serving, clean session close), ref-counted connection
  pooling, native interleaved bulk transfers, macro bytecode transfer, and
  ASC-compatible profile save/restore. A small C extension does YCbCr↔RGB
  conversion. **[hyperdeckwire](https://github.com/lucas-romanenko/bmdwire/tree/main/hyperdeckwire)**
  drives the HyperDecks. Both ship in the one
  [bmdwire](https://pypi.org/project/bmdwire/) distribution, which
  `pyproject.toml` asks for as a range and `requirements.txt` pins; a
  library change is a release there and a pin bump here.
- **`atem_control/`** is the Django app: the WebSocket consumer, a declarative
  command dispatch table, the media-pool watcher, LAN discovery, and the UI.
- **`webatem/`** is the project package: settings, the ASGI entry, the
  WebSocket origin guard, and `launcher.py`, the `webatem` command that runs
  the same web app locally and lives in the tray with its launcher window. The
  downloads are that launcher frozen per OS by PyInstaller
  (`build/desktop/`); the PyPI package is the same code installed by pip.
- **One tag, three deliverables.** A `v*` tag publishes the Mac / Windows /
  Linux downloads to the GitHub release, the Docker image to GHCR (amd64 +
  arm64) and the `webatem` package to PyPI.
- **SQLite** for persistence (connection history). No external database.

## Development

```bash
git clone https://github.com/lucas-romanenko/webatem.git
cd webatem
npm install && npm run build:css      # the stylesheet; without it the app renders unstyled
pip install -e ".[test]"              # Python 3.10+; the device libraries install as wheels
python -m webatem                     # the launcher: server + tray + window
python -m pytest tests/ -q            # the suite (no hardware needed)
```

Or entirely in Docker: `docker compose up -d --build` runs the app and
`docker compose exec webatem pytest tests/ -q` runs the suite in it. The suite
(the command dispatch table, the T-bar, the consumer's state-change and
session-cleanup rules, upload policy, tally safety, profile dialogs, the
media-pool thumbnail cache, LAN discovery identity, WebSocket origin checks)
runs against fake protocol layers. CI runs it on every push. The protocol
libraries carry their own suites in [bmdwire](https://github.com/lucas-romanenko/bmdwire).

`python manage.py runserver` works too for plain Django development. The
per-OS downloads are built by the **Desktop builds** workflow
(`pyinstaller build/desktop/webatem.spec`).

## Updating and removing it

**Updates are one click.** The launcher looks for a new version when it starts
and twice a day, and the launcher window and the tray menu then offer
**Update to x.y.z**. That downloads it, checks it against the checksum GitHub
publishes, installs it over the old one and starts it again on the same
interface. Untick **Check for updates automatically** to stop the checks
(**Check now** still works). Offline, it finds nothing and says so quietly.
From a terminal: `webatem --update`. With pipx it's `pipx upgrade webatem`;
with Docker, `docker compose pull && docker compose up -d`.

**Updating keeps everything**: your interface and port, the connection
history, start at login. Installing a new download over the old one does the
same; don't uninstall first.

**Uninstalling removes everything** WebATEM put on the machine: the program,
your settings and connection history, start at login, and on a Mac the
launcher window's own data.

- **Any desktop install:** the launcher window's **Uninstall…** button, bottom
  right. It lists exactly what will go before anything does, then WebATEM
  closes and removes itself. On Windows it hands over to Windows' own
  uninstaller.
- **Windows:** or Settings → Installed apps → WebATEM → Uninstall, even while
  WebATEM is running in the notification area.
- **macOS, app already in the Trash:** the Terminal installer cleans up what
  the Trash left behind:
  ```sh
  curl -fsSL https://github.com/lucas-romanenko/webatem/releases/latest/download/install-mac.sh | sh -s -- --uninstall
  ```
- **From a terminal:** `webatem --uninstall` (it asks first; `--yes` skips
  the question). That's the Linux binary itself, or on a Mac
  `/Applications/WebATEM.app/Contents/MacOS/webatem --uninstall`.
- **pipx:** `webatem --uninstall` removes your data and start at login, then
  `pipx uninstall webatem` removes the program.
- **Docker:** `docker compose down -v`. The `-v` removes the `webatem-data`
  volume, which holds the settings, history and key.

If you point `DATA_DIR` somewhere of your own, uninstalling removes only the
files WebATEM writes there, never the rest of that folder.


## License

- Application code: [MIT](LICENSE).
- The ATEM protocol library, [atemwire](https://github.com/lucas-romanenko/bmdwire/tree/main/atemwire),
  is a separate package (a fork of the [OpenAtem pyatem
  library](https://git.sr.ht/~martijnbraam/pyatem)) and is **LGPL-3.0-only**;
  WebATEM uses it as an installed dependency, unmodified.
  [hyperdeckwire](https://github.com/lucas-romanenko/bmdwire/tree/main/hyperdeckwire) is MIT.
- Bundled frontend assets (Alpine.js and its collapse plugin, Bootstrap Icons,
  Tailwind/daisyUI) are MIT and the Archivo and IBM Plex Mono fonts are OFL,
  with notices in
  [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

**The downloads are a Combined Work under the LGPL.** The Windows, macOS and
Linux builds bundle atemwire and pystray, both LGPL-3.0, rather than
installing them alongside. Their full licence texts travel inside the bundle,
and because every line of WebATEM is public and MIT, you can install a
modified atemwire and rebuild: `pip install -e ".[desktop]"` then
`pyinstaller build/desktop/webatem.spec`. The macOS and Windows builds are
one-directory, so the library also sits replaceable in `_internal/`; the Linux
download is a single file, so rebuilding is the route there.

Security posture and how to report vulnerabilities: [SECURITY.md](SECURITY.md).

Not affiliated with or endorsed by Blackmagic Design. ATEM and HyperDeck are
trademarks of Blackmagic Design Pty Ltd. Use against production hardware at
your own risk.

---

Independent project. Not affiliated with or endorsed by the switcher
manufacturer. The red and green are broadcast convention, sampled to their
own values; the brand lives in [docs/brand/](docs/brand/).

## Hosting the control app inside another Django project

`atem_control` is a normal Django app (label `webatem_atem`), and everything
it needs from its surroundings goes through one class,
`atem_control.hooks.Hooks`: who may open the page and drive the socket, where
operator actions and connect/disconnect events are recorded, what a switcher
is called, the switcher list for the suggestions, HyperDeck names, sightings
(video mode, deck model, binding differences), where a dropped still goes,
and extra template context. Every method has a working default, because the
standalone app *is* the defaults, so a host subclasses it and overrides what
it has:

```python
# settings.py
INSTALLED_APPS += ['atem_control']
WEBATEM_HOOKS = 'myplatform.webatem_hooks.PlatformHooks'
```

```python
# myplatform/webatem_hooks.py
from atem_control.hooks import Hooks

class PlatformHooks(Hooks):
    def check_access(self, request):        # None = allowed, else the response
        ...
    def can_use(self, user):                # the WebSocket gate
        ...
    def record_activity(self, **event):     # the audit log
        ...
    def name_for_ip(self, ip):              # the inventory's name
        ...
```

Templates are overridden the Django way (a `base.html`, a
`control/_header.html` in the host's own template directory), and
`control.html` carries a `control_extra` block for the host's panels and
scripts. Discovery is off with `discovery_enabled` returning False.

