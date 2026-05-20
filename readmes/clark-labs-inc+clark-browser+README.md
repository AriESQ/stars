# clark-browser

![clark-browser bot detection check](./promo/clark-browser-bot-check.gif)

*by [Clark](https://clarkchat.com) — MIT licensed*

**Stealth Chromium for browser automation.** Anti-fingerprinting compiled into
the binary at the C++ source level — not a JavaScript injection, not a config
patch.

## What this is

A fork of [ungoogled-chromium](https://github.com/ungoogled-software/ungoogled-chromium)
148.0.7778.96 with a patch series that makes the binary indistinguishable
from a real Chrome install across the JS-visible fingerprint surface (navigator
properties, WebGL GPU strings, screen dimensions, plugins, timezones, etc.).

The patched binary is MIT-licensed — this is an open-source project, **not** a
commercial-licensed stealth browser like CloakBrowser or Multilogin. Build it
from source yourself, or use the prebuilt binaries from
[GitHub Releases](https://github.com/clark-labs-inc/clark-browser/releases).

## Why

Stock `chromium --headless` is trivially detectable: `navigator.webdriver
= true`, empty plugin list, `HeadlessChrome` in the User-Agent, software-renderer
WebGL strings, and a dozen other signals that detection sites grep for. JS-level
"stealth" shims (puppeteer-extra-plugin-stealth, playwright-stealth, undetected-
chromedriver) only paper over the surface — sites like FingerprintJS, BrowserScan,
and Cloudflare Turnstile catch them because the patches themselves are
detectable.

clark-browser patches Chromium where the values come from — at the C++ source
level, in blink/v8/net — so detection sites just see "a normal Chrome install."

## Supported platforms

| Platform | Status |
|---|---|
| Linux x86_64 | prebuilt binary in [releases](https://github.com/clark-labs-inc/clark-browser/releases) |
| macOS arm64 | prebuilt binary in [releases](https://github.com/clark-labs-inc/clark-browser/releases) |

Other targets (macOS x86_64, Windows) need a source build.

## Usage

Install the Python wrapper from PyPI:

```bash
pip install clark-browser
```

Use it as a Playwright launcher. The wrapper downloads the matching patched
Chromium build from GitHub Releases on first launch and caches it under
`~/.clarkbrowser/`.

```python
from clarkbrowser import launch

browser = launch()
page = browser.new_page()
page.goto("https://bot.sannysoft.com")
print(page.title())
browser.close()
```

You can also prefetch or inspect the browser binary with the CLI:

```bash
clark-browser info
clark-browser fetch
```

For Vercel `agent-browser` usage, see
[`examples/agent_browser.md`](./examples/agent_browser.md).

For direct CDP usage, download the tarball for your platform from the
[releases page](https://github.com/clark-labs-inc/clark-browser/releases),
extract it, and run the binary directly. Drive it via any Chrome DevTools
Protocol client (CDP over HTTP/WebSocket).

```bash
# Linux: extract and launch with CDP on port 9222
tar -xzf clark-browser-linux-x64.tar.gz
./headless_shell \
  --headless=new \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --fingerprint=12345 \
  --fingerprint-platform=windows \
  about:blank
```

The Linux tarball contains the `headless_shell` binary (~270 MB), a `chrome`
compatibility launcher, headless resource packs, and runtime helper libraries.
The macOS arm64 build produces a normal `Chromium.app` bundle.

## Stealth surface

`--fingerprint-*` switches drive the patches. All have seed-derived defaults
when omitted — pass `--fingerprint=<integer>` for a deterministic identity, or
let the binary pick a fresh seed at startup for per-launch variation.

```
--fingerprint=<int>              master RNG seed (10000..99999)
--fingerprint-platform=          windows | macos | linux
--fingerprint-platform-version=  client hints platform version
--fingerprint-brand=             Chrome | Edge | Opera | Vivaldi
--fingerprint-brand-version=
--fingerprint-gpu-vendor=        WebGL UNMASKED_VENDOR_WEBGL
--fingerprint-gpu-renderer=      WebGL UNMASKED_RENDERER_WEBGL
--fingerprint-hardware-concurrency=
--fingerprint-device-memory=     in GB
--fingerprint-screen-width=
--fingerprint-screen-height=
--fingerprint-taskbar-height=    Win=48, Mac=95, Linux=0
--fingerprint-storage-quota=     in MB
--fingerprint-timezone=          IANA tz, e.g. America/New_York
--fingerprint-locale=            BCP 47
--fingerprint-fonts-dir=         path to platform font directory
--fingerprint-location=          lat,lon for geolocation API
--fingerprint-webrtc-ip=         literal IPv4 to spoof in ICE candidates
--fingerprint-noise=             true | false  (canvas/audio noise on/off)
```

## Verified-working patches

Confirmed firing in CDP-driven smoke tests against the built binary
(`tests/linux_smoke.py`, `tests/integration_smoke.py`):

| Detection vector | Patched | Verification |
|---|---|---|
| `navigator.webdriver` | always `false` | `navigator.webdriver === false` |
| `navigator.plugins` | 5 PDF-viewer entries | `navigator.plugins.length === 5` |
| `window.chrome` | always an object | `typeof window.chrome === "object"` |
| `navigator.platform` | spoofed from `--fingerprint-platform` | returns `"Win32"` under `=windows` |
| `navigator.userAgentData` | brand/platform/version coherent with spoofed UA | returns Windows + Google Chrome under `=windows` |
| `navigator.hardwareConcurrency` | seed-derived from {4, 6, 8, 12, 16} | deterministic per seed |
| `navigator.maxTouchPoints` | matched to platform | `0` on `=windows` |
| timezone / locale | from `--fingerprint-timezone` / `--locale` | reaches Blink as set |
| User-Agent | no `HeadlessChrome` | full Chrome UA under `--user-agent=...` |
| Audio fingerprint | seed-derived deterministic noise | two distinct seeds yield distinct audio FP |

See [`PATCHES.md`](./PATCHES.md) for the full patch catalog and `specs/` for
per-category implementation notes.

## Methodology

We build on ungoogled-chromium (BSD-3) and inherit its existing Brave-derived
canvas/audio/clientRects noise infrastructure. Our patches are written from
public sources only — W3C specs, Chromium upstream code, MDN bot-detection
writeups, and curl-impersonate (MIT). We do not reverse-engineer or copy from
any proprietary stealth-browser binary. See [`METHODOLOGY.md`](./METHODOLOGY.md).

## Building from source

```bash
# 1. Fetch tooling
git clone https://github.com/clark-labs-inc/clark-browser
cd clark-browser

# 2. Fetch Chromium 148 source (~17 GB, ~30 min)
./build/fetch-source.sh

# 3. Apply patches (instant)
./build/apply-patches.sh

# 4. Build (4–12 hours, ~80 GB disk, 32+ GB RAM recommended)
./build/build.sh
```

For a clean Linux x86_64 build that mirrors what ships in our releases, use
`./build/build-linux.sh` instead (runs the full clone → patch → ninja pipeline
in a single script; designed for fresh Ubuntu hosts).

See [`build/README.md`](./build/README.md) for detailed prerequisites.

## License

MIT. ungoogled-chromium and Chromium upstream components retain their
respective BSD/MPL/other licenses; this project does not modify those.

## Status

**Alpha.** Linux x86_64 and macOS arm64 builds are reproducible end-to-end and
the patches above are runtime-confirmed against the built binary. The
remaining patches in the series compile in but need broader detection-site
benchmarking. Contributions welcome — see `specs/` for the patch backlog.
