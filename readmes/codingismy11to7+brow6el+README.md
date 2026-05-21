# Brow6el - Terminal Web Browser with Graphics Support

A full-featured web browser for the terminal using Chromium (CEF) with support for Sixel and Kitty graphics protocols.

> **WARNING**: Kitty image support (currently only in main branch builds) by its design nature is barelly usable in SSH when brow6el runs on remote host, this feature is usable when brow6el is executed on localhost. On ssh the responsivenes of browser is significantly affected, due to massive data transfers on each frame rendered

> **WARNING**: this is POC code quality. Build process tested in Ubuntu 25.10, Debian 13, Arch Linux. The browser itself was tested in foot terminal, wezterm, kitty, ghostty, yaft framebuffer terminal and Windows 11 Terminal with sixel support using WSL2.



## Screenshots
### Demo
[![brow6el web browser demo video](https://codeberg.org/janantos/brow6el/raw/branch/main/screenshots/brow6el.png)](https://codeberg.org/janantos/brow6el/raw/branch/main/screenshots/brow6el_demo.webm)

### Page view
![brow6el web browser running in linux virtual terminal window showing codeberg website](https://codeberg.org/janantos/brow6el/raw/branch/main/screenshots/brow6el.png "brow6el page view")


### JavaScript console
![brow6el web browser running in linux virtual terminal window showing codeberg website and opended javascript console](https://codeberg.org/janantos/brow6el/raw/branch/main/screenshots/brow6el_js_console.png "brow6el js console")

## Features

- **Graphics Protocols** - Supports both Sixel and Kitty graphics protocols with automatic detection
- **Tiled Rendering** - Optional tile-based Sixel rendering for improved responsiveness (Sixel only)
- **Mouse Support** - Click, scroll, and interact with web pages
- **Vim-Style Modal Control** - Efficient keyboard navigation with three modes (STANDARD, INSERT, MOUSE, VISUAL)
- **Grid Jump Mode** - Fast mouse positioning with recursive grid navigation (3-4 keystrokes to almost any element)
- **Element Inspector** - Browser DevTools-like element inspection in MOUSE mode
- **JavaScript Console** - Execute JS commands and view console logs
- **Bookmarks** - Save and organize your favorite pages
- **User Scripts** - Inject custom JavaScript into pages
- **Download Manager** - Save files with progress tracking
- **Popup Handling** - Terminal-friendly popup dialogs
- **Multi-Instance** - Run multiple browser windows simultaneously
- **Configurable Profiles** - Choose between temporary (private) or persistent (normal) browsing
- **DNS-over-HTTPS (DoH)** - Secure DNS with configurable providers and modes
- **Modern Web** - Full HTML5/CSS3/JavaScript support via Chromium

## Vim-Style Modal Control

Brow6el uses a vim-inspired modal keyboard interface with three modes. The current mode is always shown in the status bar (e.g., [S][T] for Standard mode with Tiled rendering).

### STANDARD Mode [S] - Default

Vim-like navigation with single-key commands (no Ctrl required):

**Navigation:**
- `h/j/k/l` or arrow keys - Navigate (left/down/up/right)
- `t/g` - Scroll up/down
- `p/n` - Back/forward in history

**Actions:**
- `r` - Reload page
- `u` - Navigate to URL
- `U` - Copy current URL to clipboard (Shift+U)
- `c` - Toggle JavaScript console
- `d` - Add bookmark
- `b` - Open bookmarks
- `f` - Hint mode (keyboard link navigation)
- `s` - User scripts menu
- `y` - Toggle auto-inject user scripts
- `z` - Toggle tiled rendering (Sixel only, reduces flicker)
- `Z` - Force full redraw (Sixel: monolithic render, Kitty: full refresh)
- `m` - Open downloads manager
- `x` - Exit browser

**Zoom Controls:**
- `+` or `=` - Zoom in
- `-` or `_` - Zoom out
- `0` - Reset zoom to 1.0x

**Mode Switch:**
- `i` - Enter INSERT mode
- `e` - Enter MOUSE mode
- `v` - Enter VISUAL mode (text selection)

### INSERT Mode [I]

All keypresses pass through to the webpage. Use for typing in forms, text areas, etc.

**Exit:** `ESC` - Return to STANDARD mode

### VISUAL Mode [V]

Text selection mode for copying page content. The caret starts at the first visible text, or if coming from MOUSE mode, at the mouse cursor position.

**Caret Positioning (initial):**
- `h` - Move cursor left by character
- `l` - Move cursor right by character
- `w` - Move cursor forward by word
- `b` - Move cursor backward by word
- `j` - Move cursor down by line
- `k` - Move cursor up by line
- `v` - Start selecting from current position

**Selection (after pressing v):**
- `h` - Extend selection left by character
- `l` - Extend selection right by character
- `w` - Extend selection forward by word
- `b` - Extend selection backward by word
- `j` - Extend selection down by line
- `k` - Extend selection up by line

**Actions:**
- `y` - Copy selection to clipboard, exit VISUAL mode
- `ESC` - Cancel selection, exit VISUAL mode

**Tip:** Use MOUSE mode (`e`) to position cursor, then press `ESC` and `v` to start text selection at that exact position!

### MOUSE Mode [M]

Keyboard-driven mouse emulation with visual cursor:

**Movement:**
- `h/j/k/l` or arrow keys - Move mouse (left/down/up/right)
- `q/f` - Toggle precision/fast speed
- `r` - Toggle drag-and-drop
- `g` - Toggle grid jump mode (fast navigation)

**Actions:**
- `SPACE` or `ENTER` - Click at cursor position or drop
- `i` - Toggle inspect mode (show element info on hover)
- `r` - Drop when drag-and-drop is active

**Exit:** `e` or `ESC` - Return to STANDARD mode

#### Grid Jump Mode

Fast mouse positioning using keyboard-driven grid navigation. Press `g` in MOUSE mode to activate:

- **Adaptive Grid Overlay** - A 3x3 grid with labeled cells appears (default keys: `qweasdzxc`)
- **Quick Jump** - Press a key (q/w/e/a/s/d/z/x/c) to jump to that grid cell
- **Recursive Zoom** - Automatically shows sub-grid in selected cell for precision
- **Visual Feedback** - Green grid indicates more zoom levels available, red indicates maximum zoom
- **Auto-Precision_movement** - At maximum zoom, grid switches to cursor movement mode with high precision
- **Navigation** - `Backspace` to zoom out, `ESC` to exit grid mode
- **Configurable Keys** - Customize grid keys in `~/.brow6el/browser.conf` (grid_keys setting)

Grid mode enables precise element selection with just 3-4 keystrokes, combining speed with accuracy.

#### Inspect Mode

While in MOUSE mode, press `i` to toggle inspect mode. This feature works similar to browser DevTools inspector:

- **Element Highlighting** - Cyan border around the element under cursor
- **Info Panel** - Shows element details including:
  - Tag name, ID, and classes
  - Key attributes (href, src, type, name, etc.)
  - Dimensions and position
  - Text content preview
- **Real-time Updates** - Info updates as you move the cursor
- **Toggle Off** - Press `i` again to exit inspect mode

This is useful for debugging web pages, understanding page structure, or finding specific elements.

### Smart Mode Switching

The browser automatically switches modes based on context:
- Clicking an input field in MOUSE mode → Auto-switch to INSERT mode
- Clicking a select box in MOUSE mode → Auto-switch to STANDARD mode
- Page navigation → Auto-reset to STANDARD mode

## Advanced Navigation Modes

### Hint Mode (f key)
Press `f` to show yellow hint labels on all links. Type the hint label (e.g., "a", "ab") and press Enter to navigate. This provides keyboard-only navigation without needing a mouse. Press `ESC` or `f` again to exit.

### Mouse Emulation Mode (e key)
Press `e` to activate a yellow mouse cursor overlay. Use hjkl or arrow keys to move it around the page and press SPACE/Enter to click at that position. `q` toggles precision mode, `f` toggles fast mode. Press `i` to toggle inspect mode which shows detailed element information as you hover. This works on all elements including iframes and consent dialogs. Press `ESC` or `e` again to exit.

## Quick Start

```bash
# 1. Download CEF binary (~670MB, one-time)
./download_cef.sh 

# 2. Build
./build.sh

# 3. Run
./build/run_brow6el.sh https://example.com

# Multiple instances supported!
# Open additional terminals and run more instances
```

## Examples

The `examples/` directory contains:
- **userscripts/** - Example user scripts (dark mode, Google customization, etc.)

See [examples/README.md](examples/README.md) for details.

## Advanced Features

### Bookmarks
- Press `d` (in STANDARD mode) to bookmark the current page
- Press `b` (in STANDARD mode) to view and manage bookmarks
- Navigate with ↑/↓ or j/k, press Enter to open, 'd' to delete
- Bookmarks stored in `~/.brow6el/bookmarks`

### User Scripts
Custom JavaScript injection system similar to Greasemonkey/Tampermonkey.

**Quick Start:**
1. Create script directory: `mkdir -p ~/.brow6el/userscripts`
2. Add `.js` files to the directory
3. Configure URL patterns in `~/.brow6el/userscripts.conf`
4. Press `s` to manually inject or `y` to toggle auto-inject

**Example config** (`~/.brow6el/userscripts.conf`):
```
auto_inject=true

dark-mode.js|Dark Mode|true|*
google-custom.js|Google Custom|true|*google.com*,*google.co.*
```

See [USERSCRIPTS.md](USERSCRIPTS.md) for detailed documentation.

**Bundled Scripts:**
The browser comes with several pre-installed scripts in the `scripts/` directory:
- **view-source.js** - View HTML source code with syntax highlighting, formatting, and line numbers (keyboard navigable)
- **reader-mode.js** - Simplifies pages to just article content (like Firefox Reader View)
- **adblock.js** - Basic ad blocking functionality
- **force-light-mode.js** - Forces light color scheme on all pages
- **frameset-redirect.js** - Redirects from frameset pages to actual content

To use bundled scripts, add them to your `~/.brow6el/userscripts.conf`:
```
view-source.js|View Page Source|true|*
```
Then press `s` to open the user scripts menu and select "View Page Source", or enable auto-inject and press the script's trigger key.

### Profile Modes
Brow6el supports different profile modes for different use cases:

**Temporary Mode (Default):**
- Each session uses a new profile
- All data (cookies, cache, history) deleted on exit
- Perfect for private browsing
- No data persists between sessions

**Persistent Mode:**
- Profile saved in `~/.brow6el/profile`
- Cookies and login sessions maintained
- Cache speeds up repeated visits
- Works like a normal browser

**Configuration** (`~/.brow6el/browser.conf`):
```ini
# Choose profile mode: temporary, persistent, or custom
profile_mode=temporary

# Custom profile location (when mode=custom)
profile_path=~/.brow6el/profile

# Cache settings
cache_size_mb=500
clear_cache_on_exit=false

# Privacy options (for persistent/custom)
clear_cookies_on_exit=false

# Default homepage URL
default_url=https://example.com

# Grid keys for mouse emulation grid jump (must be exactly 9 characters)
# Default: qweasdzxc (3x3 grid matching keyboard layout)
# Alternative: abcdefghi (alphabetical)
grid_keys=qweasdzxc

# Graphics Protocol Selection
# Choose graphics protocol: auto, sixel, or kitty
# auto: Detect terminal capabilities (default)
# sixel: Force Sixel protocol (recommended, faster)
# kitty: Force Kitty graphics protocol
graphics_protocol=auto

# DNS-over-HTTPS (DoH) Configuration
# Enable secure DNS to encrypt DNS queries
doh_enabled=false
doh_server=https://cloudflare-dns.com/dns-query
doh_mode=secure
# DoH mode options:
#   secure: Mandatory DoH, no fallback (recommended for blocking)
#   automatic: Use DoH when available, fallback to system DNS
#   off: Disable DoH
# Popular DoH servers:
#   Cloudflare: https://cloudflare-dns.com/dns-query
#   Google: https://dns.google/dns-query
#   Quad9: https://dns.quad9.net/dns-query

# Tiled Rendering (Sixel only)
# Enable tile-based sixel rendering (reduces flicker on updates)
# When enabled, only changed screen regions are redrawn
# When disabled, the entire screen is redrawn on every update
# Note: Kitty protocol always uses monolithic rendering
tiled_rendering=true

# Terminal Cell Dimensions (optional override)
# Leave at 0 for auto-detection (recommended)
# Only override if auto-detection produces incorrect results
#cell_width=0
#cell_height=0

# Zoom settings
# Default zoom level (1.0 = no zoom, 2.0 = 2x zoom)
zoom_level=2.5
# Zoom step size for +/- keyboard shortcuts
zoom_step=0.25
# Default zoom behavior: auto, fixed, or none
# auto: Automatically adjust zoom based on terminal DPI and window size
# fixed: Use fixed zoom level from zoom_level setting
# none: No automatic zoom (start at 1.0x, manual control only)
default_zoom_behavior=fixed

# Proxy Configuration
# Route browser traffic through HTTP/HTTPS/SOCKS proxy
proxy_enabled=false
proxy_server=
proxy_username=
proxy_password=
proxy_bypass_list=localhost,127.0.0.1
```

**Examples:**
- Private browsing: `profile_mode=temporary` (default)
- Normal browsing: `profile_mode=persistent`
- Multiple profiles: `profile_mode=custom` with different paths
- Semi-private: `persistent` with `clear_cookies_on_exit=true`
- Secure DNS with blocking: `doh_enabled=true` with `doh_mode=secure`
- HTTP proxy with auth: `proxy_enabled=true`, `proxy_server=http://proxy.local:8080`, `proxy_username=user`

### DNS-over-HTTPS (DoH)

Brow6el supports DNS-over-HTTPS to encrypt DNS queries and prevent DNS-based tracking or blocking.

**Configuration** (`~/.brow6el/browser.conf`):
```ini
doh_enabled=true
doh_server=https://cloudflare-dns.com/dns-query
doh_mode=secure
```

**DoH Modes:**
- `secure` - Mandatory DoH with no fallback to system DNS (recommended for ad-blocking/privacy)
- `automatic` - Attempts DoH first, falls back to system DNS on failure
- `off` - Disables DoH

**Popular DoH Providers:**
- **Cloudflare:** `https://cloudflare-dns.com/dns-query` (fast, privacy-focused)
- **Google:** `https://dns.google/dns-query` (reliable, global)
- **Quad9:** `https://dns.quad9.net/dns-query` (security-focused, blocks malicious domains)

**Note:** When using `secure` mode, ensure your DoH server resolves `google.com` (used by CEF for connectivity checks) or allows all domains, otherwise DoH may fail to initialize.

### Proxy Configuration

Brow6el supports routing browser traffic through HTTP, HTTPS, and SOCKS proxies with optional authentication.

**Configuration** (`~/.brow6el/browser.conf`):
```ini
# Enable proxy
proxy_enabled=true

# Proxy server (format: scheme://host:port - NO credentials in URL)
# Supported: http://, https://, socks4://, socks5://
proxy_server=http://127.0.0.1:8080

# Proxy authentication (optional)
# Leave empty if proxy doesn't require authentication
proxy_username=myuser
proxy_password=mypass

# Bypass proxy for these hosts (comma-separated)
proxy_bypass_list=localhost,127.0.0.1,*.local
```

**Proxy Schemes:**
- `http://` - HTTP proxy
- `https://` - HTTPS proxy (connects to proxy via HTTPS)
- `socks4://` - SOCKS v4 proxy
- `socks5://` - SOCKS v5 proxy

**Authentication:**
- **HTTP/HTTPS proxies**: Full authentication support via `proxy_username` and `proxy_password`
- **SOCKS proxies**: Authentication not supported by Chromium's proxy implementation
- If credentials are configured, authentication happens automatically (no dialog)
- If credentials are empty and proxy requires auth, interactive dialog will appear

**Examples:**
- SOCKS5 proxy (no auth): `proxy_server=socks5://127.0.0.1:1080`
- HTTP proxy: `proxy_server=http://proxy.example.com:8080`
- HTTPS proxy: `proxy_server=https://secure-proxy.example.com:443`
- Corporate proxy: `proxy_server=http://proxy.corp.local:3128`

**Note:** Set `proxy_enabled=false` or leave `proxy_server` empty to disable proxy.

### Graphics Protocols

Brow6el supports both Sixel and Kitty graphics protocols with automatic terminal detection.

**Sixel Protocol (recommended):**
- Default and most widely supported
- Supports both tiled and monolithic rendering
- Tiled rendering reduces flicker significantly
- Generally faster for typing-heavy workflows
- Supported terminals: mlterm, xterm, wezterm, foot, etc.

**Kitty Protocol:**
- Alternative graphics protocol for Kitty-compatible terminals
- Always uses monolithic rendering (entire screen redrawn)
- Double buffering prevents flicker
- 30 FPS frame rate for smooth animations
- Supported terminals: kitty, ghostty, wezterm, etc.

**Configuration** (`~/.brow6el/browser.conf`):
```ini
# Graphics protocol selection
graphics_protocol=auto  # auto, sixel, or kitty

# Tiled rendering (Sixel only)
tiled_rendering=true

# Optional: Override auto-detected terminal cell dimensions
#cell_width=11
#cell_height=25
```

**Runtime Controls:**
- Press `z` (in STANDARD mode) to toggle tiled/monolithic rendering (Sixel only)
- Press `Z` (in STANDARD mode) to force full redraw
- Current mode shown in status bar: `[S][T]` (Sixel tiled), `[S][M]` (Sixel monolithic), `[S]` (Kitty)

**How It Works:**

*Sixel Tiled Rendering:*
- Tiles dynamically sized based on terminal resolution (~30-40 tiles per screen)
- CEF dirty rectangles indicate changed regions
- Only tiles intersecting dirty regions are redrawn
- Tiles aligned to terminal cell boundaries for artifact-free rendering

*Kitty Monolithic Rendering:*
- Entire screen encoded as RGBA and transmitted via base64
- Double buffering (alternating image IDs) prevents flicker
- Uncompressed for optimal typing performance
- Images placed below text layer (z=-1) so dialogs appear on top

### Zoom Control

Brow6el provides intelligent zoom control with three modes and per-site customization.

**Keyboard Controls (STANDARD mode):**
- `+` or `=` - Zoom in
- `-` or `_` - Zoom out  
- `0` - Reset zoom to 1.0x

**Zoom Modes:**

*Auto Mode (default_zoom_behavior=auto):*
- Automatically calculates optimal zoom based on:
  - Terminal cell size (DPI adaptation) - 60% weight
  - Window resolution - 40% weight
- Larger windows get bigger text, smaller windows get compact text
- Adapts to high-DPI displays and large fonts
- Recalculates on window resize
- Range: 0.5x to 3.0x

*Fixed Mode (default_zoom_behavior=fixed):*
- Uses zoom level from `zoom_level` setting
- Consistent zoom across all pages
- Ideal for high-DPI displays that need constant scaling

*None Mode (default_zoom_behavior=none):*
- Starts at 1.0x zoom
- Manual control only via keyboard shortcuts
- No automatic adjustments

**Per-Site Zoom:**

Create `~/.brow6el/zoom.conf` for site-specific zoom levels that override auto/fixed modes:
```
# Format: domain=zoom_multiplier
github.com=2.5
wikipedia.org=2.75
google.com=2.0
```

Site-specific zoom works with subdomains (e.g., `github.com` matches `www.github.com`).

**Configuration** (`~/.brow6el/browser.conf`):
```ini
# Default zoom level for fixed mode
zoom_level=2.5

# Zoom step for +/- keyboard shortcuts
zoom_step=0.25

# Zoom behavior: auto, fixed, or none
default_zoom_behavior=auto
```

**Auto Zoom Formula:**
- Reference: 1600x900 resolution, 10x20 pixel cells
- Cell zoom = (cell_height/20 × 0.7) + (cell_width/10 × 0.3)
- Resolution zoom = (window_height/900 × 0.5) + (window_width/1600 × 0.5)
- Final zoom = (cell_zoom × 0.6) + (resolution_zoom × 0.4)

This ensures text is readable on both high-DPI laptops and large desktop monitors.

### JavaScript Console
- Press `c` (in STANDARD mode) to open/close the console
- Type JavaScript and press Enter to execute
- Scroll through output with ↑/↓
- All console.log/warn/error messages are captured

### CEF Configuration

Brow6el uses a configuration file for Chromium command-line flags. On first run, a default configuration is created at `~/.brow6el/cef_flags.conf`.

**Features:**
- Enable/disable WebGL support
- Configure rendering options
- Adjust logging verbosity
- Set custom user agent
- And more!

**Edit the config:**
```bash
nano ~/.brow6el/cef_flags.conf
```

Changes take effect on next browser start. See the config file for available options and documentation links.

### Privacy & Data

**What persists:**
- Bookmarks (`~/.brow6el/bookmarks`)
- User scripts (`~/.brow6el/userscripts/`)
- User script config (`~/.brow6el/userscripts.conf`)
- CEF flags config (`~/.brow6el/cef_flags.conf`)

**What doesn't persist (default temporary mode, persists in persistent mode):**
- Cookies (cleared on exit)
- localStorage (cleared on exit)
- Cache (cleared on exit)
- History (not stored)

Each browser instance uses an isolated cache directory `/tmp/brow6el_<PID>` that is automatically deleted when you close the browser.

### Multiple Instances
You can run multiple browser instances simultaneously:
```bash
# Terminal 1
./build/run_brow6el.sh https://github.com

# Terminal 2
./build/run_brow6el.sh https://google.com

# Terminal 3
./build/run_brow6el.sh https://example.com
```

## Requirements

**Graphics-capable terminal**: Terminal emulator supporting Sixel or Kitty graphics protocols:
- **Sixel** (recommended): mlterm, xterm, foot, wezterm, yaft, etc.
- **Kitty**: kitty, ghostty, wezterm, etc.

The browser automatically detects graphics support - no manual configuration needed. If both protocols are supported, Sixel is preferred by default.

**Build Dependencies**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    build-essential cmake git pkg-config curl \
    libsixel-dev \
    libx11-dev libxcomposite-dev libxdamage-dev libxext-dev libxfixes-dev \
    libxrandr-dev libgbm-dev libxcb1-dev \
    libpango1.0-dev libatk1.0-dev libcups2-dev libasound2-dev \
    libnss3-dev libnspr4-dev libglib2.0-dev

# Arch Linux
sudo pacman -S base-devel cmake git pkg-config curl \
    libsixel \
    libx11 libxcomposite libxdamage libxfixes libxrandr \
    mesa pango atk cups alsa-lib nss nspr glib2
```

**Runtime Dependencies** (automatically satisfied on most systems):
- libsixel, X11 libraries, NSS/NSPR (SSL), GLib, D-Bus, ALSA, Pango, Cairo

## How It Works

CEF renders web pages offscreen → Graphics conversion (Sixel or Kitty protocol) → Output to terminal

**Sixel pipeline:** CEF BGRA buffer → libsixel conversion → Sixel escape sequences  
**Kitty pipeline:** CEF BGRA buffer → RGBA conversion → base64 encoding → Kitty escape sequences

The browser continuously renders at 30 FPS, with synchronized input handling for mouse and keyboard events.

## Distributions packages (community)

* Artix Linux, in the Omniverse repository : https://wiki.artixlinux.org/Main/Repositories#Omniverse
* Arch Linux, in the Arch User Repository (AUR) : https://aur.archlinux.org/packages/brow6el-git


## License
MIT

Uses CEF (BSD clause 3 exception) and libsixel (MIT). See respective licenses for details.
