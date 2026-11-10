<h1 align="center"><img src="docs/images/logo.svg" width="360" alt="zebkit"></h1>

<p align="center"><b>Chrome as a library — light, fast, everywhere, and easy.</b><br>One API on Linux, macOS and Windows. Add it in a few lines.</p>

<p align="center">
<a href="https://crates.io/crates/zebkit"><img src="https://img.shields.io/crates/v/zebkit.svg?label=crates.io" alt="crates.io"></a>
<a href="https://pypi.org/project/zebkit/"><img src="https://img.shields.io/pypi/v/zebkit.svg?label=PyPI" alt="PyPI"></a>
<a href="https://github.com/ikey4u/zebkit/releases/latest"><img src="https://img.shields.io/github/v/release/ikey4u/zebkit?label=engine" alt="Engine release"></a>
</p>

## Introduction

zebkit is Chromium's engine as one library you link into your own
application: Blink, V8 with every JIT tier, PDFium, FFmpeg and the rest of
what Chrome is made of, with nothing of Chrome's browser and nothing of
Electron's runtime. Your application stays yours, in C, C++, Rust, Python,
Go or JavaScript, with its own windows and toolkit. Where it needs the web,
it adds a zebkit view; where it needs a PDF, media, compression or crypto,
it calls zebkit's API: in C, or through the bindings for Rust, Python, Go
and JavaScript (`zebkit-js`, and `zebkit.*` in the application's own pages).

<p align="center"><img src="docs/images/architecture.svg" width="900" alt="The application links one library, zebkit, which runs Chromium's content layer, Blink and V8 inside the application's process; pages run in sandboxed helper processes; on Linux, macOS and Windows"></p>

- **Integrate it, don't build on it.** Electron is a base: an application
  is built inside it, on its runtime, its windows and its packaging.
  zebkit is a part: an application adds it, as it adds SQLite, and keeps
  its process, its toolkit and its way of shipping. It runs inside the
  application's own event loop (`zebkit_init()`, `zebkit_pump()`), and draws
  in the application's windows, as frames you draw or in a child of a window
  you give it, an X11 window, an `NSView` or an `HWND` (`examples/native-host`),
  and gives back the window a page is in for the system's dialogs.
- **Take what you need.** Web views, in a window or off-screen with their
  frames handed to you; a full PDF API; saving what a page plays; your own
  URL schemes; native UI from JavaScript; Playwright's API and CDP for
  agents. Use one, or all.
- **The real Chrome engine.** Pages see Chromium 157: its user agent and
  client hints, `window.chrome`, popups blocked without a click, and
  nothing of a debugger attached (`docs/API.md` has what still differs,
  Google's sign-in among it).
- **Lighter than Electron.** Against the latest Electron, 45.2.1: 34% smaller,
  a cold start in 2.3 s against 6.6, a page in 29% less memory, and the DOM, text
  layout and JavaScript level ([Benchmark](#benchmark)).
- **No Node.** No second JavaScript runtime and no IPC through one. The
  application is native code, or JavaScript run by `zebkit-js` on the
  engine's V8.
- **Chromium's libraries are yours.** 17 C libraries inside the engine, about
  7,490 functions on each of Linux, macOS and Windows (7,487 on all three, the
  rest each system's own), exported under `zebkit_vendor_*`: SQLite, LevelDB, BoringSSL,
  zlib, Zstandard, Brotli, ICU, HarfBuzz, libxml2, libwebp, libjpeg-turbo,
  FFmpeg, dav1d, Opus, libvpx, FreeType and PDFium. You do not ship them twice.
- **PDF built in.** A full API on Chromium's PDFium: rendering and tiles,
  text with layout, search, outline, links, annotations as an editor has them
  (line endings, cloudy borders, free text with callouts and rich text, stamps,
  replies and states, measurement, XFDF and FDF), forms, redaction, page editing,
  merging, attachments, metadata, and signatures checked for integrity; hooks for
  an application's own annotation kinds, appearances, events with undo, render
  layers, OCR, fonts, trust and actions. In C, Rust, Python and JavaScript.
- **2D drawing and shaping.** `<zebkit/canvas.h>` on the engine's Skia and
  `<zebkit/text.h>` on its HarfBuzz, without shipping either again.
- **Media, saved as it plays.** Whatever a page plays, a file, MSE/DASH or
  HLS, written to MP4 or WebM as it was sent, without re-encoding and
  without a second download (`<zebkit/media.h>`).
- **Bytes as they are.** A page's calls to the application go over its
  frame's own Mojo channel, large ones through shared memory: no base64, the
  page's JSON handed on as it was written, as fast as Electron's IPC for small
  calls and faster for large ones.
- **The window around a page, from JavaScript.** `zebkit.ui` draws
  windows, prompts and dialogs with Chromium's views toolkit: signals,
  JSX, Tailwind classes, and automation for tests and agents. Rich UI is
  a page; `zebkit.ui` is the chrome around it (`docs/UI.md`).
- **Playwright's API, natively.** The whole of Playwright (locators,
  actions that wait until they can be done, keyboard, mouse and touch,
  routes, dialogs, downloads, contexts, workers, traces, HAR, video) runs
  inside the engine, without CDP or a Node.js driver: 3 to 10 times faster
  than Playwright over CDP, and a click in 3 to 5 ms instead of 33
  (`<zebkit/automation.h>`, `docs/AUTOMATION.md`). Playwright's own
  clients, in any of its languages, connect to it unchanged with
  `chromium.connect()`.
- **Made for agents.** `tools/zebkit-mcp` gives them pages, PDFs, files, media
  and native windows as MCP tools, over standard input and HTTP, within bounds
  its operator sets (`docs/MCP.md`). They can also drive zebkit through
  Playwright's API or over CDP, Chromium's own DevTools server, headless or
  windowed.
- **Customise it from your code, down to the desktop.** Native hooks decide
  what the engine does, in C, Rust, Python and JavaScript: permissions,
  navigation, popups, dialogs, downloads, certificates and client
  certificates, sign-in, network requests and responses at every stage,
  settings at run time, your own URL schemes, what a page may call, scripts
  before the page's own (`docs/ROADMAP_HOOKS.md`). And everything a page or
  the engine would show the person or ask of the system goes through the
  application: the window's frame (system, overlay or none, with the page as
  the title bar), menus and the context menu, JavaScript dialogs and sign-in,
  file and device choosers, screen capture, notifications, the tray, the
  Dock and taskbar, sharing, the system's theme, power and displays
  ([Fit it into the desktop](#fit-it-into-the-desktop),
  `docs/SYSTEM_INTEGRATION.md`).
- **Safe by default.** A page has no `zebkit` object unless the
  application grants it, per view, per origin and per capability; the
  origin is the browser's, never the page's word; the renderer stays
  sandboxed; permissions a browser would ask about are not granted.

| | |
|---|---|
| Engine | Chromium 157.0.8103.38 (`upstream.lock`): content layer, Blink, V8 with every JIT tier |
| Linux | x86-64, glibc 2.17 or newer (CentOS 7 and later), X11 and (`--ozone-platform=wayland`) Wayland: `libzebkit.so.1` and `zebkit-helper` |
| macOS | Apple silicon: `Zebkit.framework`, built natively or cross-built on Linux (`docs/MACOS.md`) |
| Windows | x64, Windows 10 or newer: `zebkit.dll` and `zebkit-helper.exe`, cross-built on Linux (`docs/WINDOWS.md`) |
| Version | `VERSION`: 0.4.0 |

## Quick start

### Get the engine

A package is a directory with the library, the helper, the engine's data
and `include/`. Either unpack a release's archive
(`zebkit-<version>-<target>.tar.xz` from GitHub's releases), or build one:

```sh
mise run r      # dist/release (Linux), dist/release-macos (macOS), dist/release-windows; hours the first time
```

Each archive also holds the tools, built for its system beside the library
and ready to run from where it is unpacked: `zebkit-run`, `zebkit-js` and
`zebkit-mcp` (`.exe` on Windows, sandboxed there too).

On an Apple silicon Mac with full Xcode installed, `scripts/dist.sh release`
builds the engine locally into `dist/release`. Then run
`scripts/example.sh macos-basic` to build and launch the C embedding demo
in `dist/example/Zebkit Embedded Browser.app`.

Building needs about 30 GB for Chromium's tree (`docs/BUILD.md`). Below,
`$PKG` is the package directory.

### Add it to a program you already have

zebkit is a library: your program keeps its `main()` and calls it. This
one renders a PDF's first page to a PNG and reads its text, with PDFium
and the image encoders inside zebkit, and nothing else to install:

```c
#include <stdio.h>
#include <zebkit/pdf.h>
#include <zebkit/services.h>

/* Your program, your main(): zebkit is just a library it calls. */
int main(int argc, char **argv) {
    char *error = NULL;
    zebkit_pdf *pdf = zebkit_pdf_open_file(argv[1], NULL, &error);
    if (!pdf) {
        fprintf(stderr, "%s\n", error);
        return 1;
    }

    /* The first page as a PNG, at twice its size. */
    zebkit_pdf_render_options options = {.scale = 2, .background = 0xffffffff};
    int width, height;
    uint8_t *rgba = zebkit_pdf_render(pdf, 0, &options, &width, &height, &error);
    size_t size;
    uint8_t *png = zebkit_image_encode(ZEBKIT_IMAGE_PNG, rgba, width, height, 0, &size, &error);
    fwrite(png, 1, size, fopen("page1.png", "wb"));

    /* And its text. */
    char *text = zebkit_pdf_text(pdf, 0, &error);
    printf("%d pages; page 1 says: %.80s\n", zebkit_pdf_page_count(pdf), text);

    zebkit_free(text), zebkit_free(png), zebkit_free(rgba);
    zebkit_pdf_close(pdf);
    return 0;
}
```

```sh
cc thumb.c -I$PKG/include -L$PKG -l:libzebkit.so.1 -Wl,-rpath,$PKG -o thumb   # Linux
cc thumb.c -I$PKG/include -F$PKG -framework Zebkit -Wl,-rpath,$PKG -o thumb   # macOS
./thumb report.pdf     # 2 pages; page 1 says: Quarterly report ...
```

The PDF API, compression, crypto, URLs, image codecs, ICU and the
libraries inside the engine (`zebkit_vendor_*`, FFmpeg's among them) need
no engine loop (`docs/API.md`); only HTTP through the engine's network
stack and web pages do.

### Add a web view

Web pages need the engine running. Here the engine runs the loop: the
program starts it with `zebkit_main()` and works in its callbacks. A program
with its own loop (GTK, Qt, AppKit, winit) starts it with `zebkit_init()` and
calls `zebkit_pump()` (`examples/native-host`).

```c
#include <stdio.h>
#include <zebkit/zebkit.h>

static void printed(zebkit_view *view, const char *json, const char *error, void *data) {
    printf("%s\n", json ? json : error);
    zebkit_quit();
}

static void loaded(zebkit_view *view, zebkit_load_event event, const char *url, void *data) {
    if (event == ZEBKIT_LOAD_FINISHED)
        zebkit_view_evaluate(view, "document.title", printed, NULL);
}

static void ready(void *data) {
    zebkit_view *view = zebkit_view_new("https://example.com/", 1024, 768);
    zebkit_view_on_load(view, loaded, NULL);
}

int main(int argc, char **argv) {
    return zebkit_main(argc, argv, ready, NULL);
}
```

```sh
cc app.c -I$PKG/include -L$PKG -l:libzebkit.so.1 -Wl,-rpath,$PKG -o app   # Linux
cc app.c -I$PKG/include -F$PKG -framework Zebkit -Wl,-rpath,$PKG -o app   # macOS
clang-cl /MT app.c /I%PKG%\include %PKG%\zebkit.dll.lib %PKG%\zebkit_sandbox.lib   # Windows
./app --remote-debugging-port=9222     # with CDP for Puppeteer and Playwright
```

On Windows the executable takes part in Chromium's sandbox: it links
`zebkit_sandbox.lib` and calls `zebkit_win_startup()` first in `main()`
(`docs/WINDOWS.md`).

Without unprivileged user namespaces the engine refuses to start and says why: install its
helper, or in a container of its own add `--no-sandbox` (`docs/SANDBOX.md`).

### The page and the application

The application serves its own pages from a scheme and gives them
functions to call; a page has nothing of `zebkit` unless it is granted.

```c
/* The page calls zebkit.app.greet("Ada"). */
static void greet(zebkit_view *view, const char *origin, const char *args_json,
                  zebkit_call *call, void *data) {
    char answer[256];
    snprintf(answer, sizeof answer, "{\"hello\": %s}", args_json);
    zebkit_call_resolve(call, answer);
}

/* app://main/... from ./ui, in ranges for media. A real handler refuses "..". */
static void serve(zebkit_request *request, void *data) {
    char path[1024];
    snprintf(path, sizeof path, "ui%s", zebkit_request_url(request) + sizeof "app://main" - 1);
    zebkit_request_respond_file(request, path, NULL);
}

static void closed(zebkit_view *view, void *data) { zebkit_quit(); }

static void ready(void *data) {
    zebkit_view *view = zebkit_view_new("app://main/index.html", 1024, 768);
    zebkit_view_grant(view, "app://main", ZEBKIT_ALLOW_APP | ZEBKIT_ALLOW_PDF, NULL);
    zebkit_view_bind(view, "greet", greet, NULL);
    zebkit_view_on_close(view, closed, NULL);
}

int main(int argc, char **argv) {
    zebkit_scheme_register("app", ZEBKIT_SCHEME_STANDARD | ZEBKIT_SCHEME_SECURE | ZEBKIT_SCHEME_FETCH);
    zebkit_scheme_handle("app", serve, NULL);
    return zebkit_main(argc, argv, ready, NULL);
}
```

In the page, every call is a promise and bytes are `Uint8Array`s:

```js
const reply = await zebkit.app.greet('Ada');            // the application's function
const pdf = await zebkit.pdf.open(await (await fetch('report.pdf')).bytes());
const rgba = await pdf.render(0, {scale: 2});           // a page as pixels
const hits = await pdf.search('revenue');
const packed = await zebkit.compress('zstd', bytes, 19);
const hash = await zebkit.crypto.digest('SHA-256', 'abc');
```

### Fit it into the desktop

Each thing the engine would show the person, or ask of the system, has a
default that works and a function of the application's that replaces it.
Nothing reaches the system without a decision the application can take;
without a function, a page gets what a careful browser gives it, and
nothing at all where a browser would ask.

```python
import zebkit

zebkit.scheme_register("app")   # served by a scheme_handle(), as in the C example above
zebkit.init(["app"])
# The page is the title bar: the window's buttons over it, dragged by its CSS.
view = zebkit.View("app://main/index.html", 1000, 700, options={
    "frame": "overlay", "controls": {"height": 40, "color": "#1b1d2a", "symbolColor": "#ffffff"},
    "dragRegions": {"source": "css", "origins": ["app://main"]}})

# The application's menu bar (macOS) and keys, with state that changes in place.
zebkit.app_set_menu([{"title": "File", "items": [{"title": "Autosave", "id": "autosave", "checked": True}]}],
                    lambda item: zebkit.app_update_menu_item(item, checked=False))

# A tray icon, the Dock's or the taskbar's badge, and the page's notifications as the application's.
tray = zebkit.Tray(open("icon.png", "rb").read(), "My application")
zebkit.app_set_badge("3")
zebkit.on_notification(lambda event: print("show in my own UI:", event))

# What a page asks for: a USB device, a screen to capture, a colour, a share.
view.on_device_chooser(lambda request: request.respond(request.metadata["devices"][0]["id"]))
view.on_media_access(lambda request: request.respond(True, None, "view"))
view.on_share(lambda request: request.respond(True))

# The system: its theme and its changes, the session's lock, the screens.
zebkit.on_environment_changed(lambda env: print("dark" if env["colorScheme"] == "dark" else "light"))
zebkit.on_power_event(lambda event: print(event["event"]))   # suspend, resume, lock, unlock
print(zebkit.displays())
```

| | The default | The application's |
|---|---|---|
| Window frame | the system's | `overlay` (Window Controls Overlay) or `none`, title, colours, drag regions, state, actions |
| Menus | the menu bar on macOS; the default context menu | items with state by id; the context menu replaced, extended or run |
| Dialogs | the system's alerts; the engine's prompt and sign-in where there is a window | `zebkit_view_on_dialog`, `on_http_auth`, `on_client_certificate`, the eye dropper |
| Files and devices | the system's file dialog; no device | the file chooser and File System Access; WebUSB, WebHID and Web Serial choosers |
| Capture and media | camera and microphone by permission; no screen | `getDisplayMedia()`'s source: the view itself or the screen |
| Notifications | undecided; then the system's own service | shown in the application's UI, with clicks and closes back to the page |
| Desktop | none | the tray, the Dock's and the taskbar's badge, progress and attention, the Dock menu, Web Share, opening URLs and folders |
| The system | a light page | the system's dark mode and contrast followed live; power, lock and display events; keeping awake |

`docs/SYSTEM_INTEGRATION.md` has each surface, its default, its status on
each system and why; `docs/API.md` has the calls in the four languages;
`examples/custom-titlebar` is a window whose title bar is the page.

### Rust

[`zebkit`](https://crates.io/crates/zebkit) on crates.io, with
[`zebkit-build`](https://crates.io/crates/zebkit-build) to put the engine
beside your program; the build downloads the engine for your system once and
checks its SHA-256.

```toml
[dependencies]
zebkit = "0.4.0"

[build-dependencies]
zebkit-build = "0.4.0"
```

```rust
// build.rs: puts the engine beside the executable
fn main() { zebkit_build::bundle(); }

// main.rs
fn main() {
    std::process::exit(zebkit::run(|| {
        let view = zebkit::View::new(Some("https://example.com/"), 1024, 768);
        view.grant("https://example.com", zebkit::Allow::APP, None);
        view.bind("greet", |call| {
            let answer = format!("\"hello, {}\"", call.args_json());
            call.resolve(&answer)
        });
        view.on_close(zebkit::quit);
    }));
}
```

`ZEBKIT_DIR` points the build at a package (`bindings/rust/README.md`).

### Python

[`zebkit`](https://pypi.org/project/zebkit/) on PyPI is the binding; the
engine is the archive for your system from the
[releases](https://github.com/ikey4u/zebkit/releases) of the same version,
with `ZEBKIT_DIR` pointing at it:

```sh
pip install zebkit
export ZEBKIT_DIR=/path/to/zebkit-0.4.0-x86_64-unknown-linux-gnu
```

```python
import zebkit                      # pure Python on ctypes: nothing to compile

def ready():
    view = zebkit.View("https://example.com/")
    view.grant("https://example.com", zebkit.ALLOW_APP)
    view.bind("greet", lambda name, origin: f"hello, {name}")

zebkit.main(ready)                 # the engine is found in $ZEBKIT_DIR
```

### Go

[`bindings/golang`](bindings/golang), on cgo: views, pages calling Go
functions, the application's schemes, the page hooks and the system's
services, on Linux and macOS. Build with the engine's headers and library:

```sh
go get github.com/ikey4u/zebkit/bindings/golang@main
export CGO_CFLAGS="-I$ZEBKIT_DIR/include" CGO_LDFLAGS="-L$ZEBKIT_DIR -Wl,-rpath,$ZEBKIT_DIR"
```

```go
os.Exit(zebkit.Main(func() {
    view := zebkit.NewView("", 1024, 768)
    view.Grant("https://example.com", zebkit.AllowApp, "")
    view.Bind("greet", func(call *zebkit.Call) {
        call.Resolve(fmt.Sprintf("\"hello, %s\"", call.Args))
    })
    view.OnClose(zebkit.Quit)
    view.Load("https://example.com/")
}))
```

### JavaScript, without Node

`zebkit-js` runs an ES module on the engine's V8, for applications
written in JavaScript, with views, the same APIs, and native windows:

```js
// zebkit-js main.mjs
const view = new zebkit.View('app://main/index.html', {width: 1024, height: 768});
view.grant('app://main', ['app', 'pdf']);
view.bind('save', async (name, text) => {
  await zebkit.fs.writeFile(`${zebkit.args[0]}/${name}`, text);
  return {saved: true};
});
view.on('close', () => zebkit.quit());
```

```js
// zebkit-js examples/ui/todo.mjs: a window of native widgets, styled with
// Tailwind's classes and kept up to date by signals (an excerpt)
const {h, signal, computed, For, window} = zebkit.ui;
const [tasks, setTasks] = signal([]);
const done = computed(() => tasks().filter((t) => t.done).length);

const Task = (task) =>
  h('view', {class: 'flex-row items-center gap-3 p-3 rounded-xl bg-[#141a2e]'},
    h('button', {class: 'w-8 h-8 p-0 rounded-full bg-[#7c5cff] text-white',
                 onClick: () => toggle(task)}, task.done ? '✓' : ''),
    h('text', {class: 'grow text-[#e6e8f2]'}, task.text));

window({title: 'Today', width: 460, height: 680}, () =>
  h('view', {class: 'flex-col gap-4 p-6 bg-[#0b1020]'},
    h('text', {class: 'text-3xl font-bold text-white'}, 'Ship something great'),
    h('text', {class: 'text-sm text-[#8a91aa]'}, () => `${done()} of ${tasks().length} done`),
    h(For, {each: tasks}, Task)));
```

![examples/ui/todo.mjs](docs/images/zebkit-ui-todo.png)

### Agents

Playwright's API runs inside the engine (`docs/AUTOMATION.md`): every
command of Playwright's protocol, in the application's process, with no
CDP and no Node.js. From C it is one call, `zebkit_automation_call(view,
"Frame.click", "{\"selector\": \"#go\"}", done, data)`; Python has it with
Playwright's names:

```python
import zebkit
from zebkit.automation import Page, expect, run

async def test():
    page = Page()
    await page.goto("https://example.com/")
    await expect(page).to_have_title("Example Domain")
    await expect(page.get_by_text("documentation examples")).to_be_visible()
    await page.screenshot(path="example.png")
    zebkit.quit()

zebkit.main(lambda: run(test()), ["python", "--headless"])
```

Playwright's own clients, its test runner and its other languages included,
connect to the engine's Playwright endpoint unchanged:

```sh
tools/zebkit-run --headless --playwright-port=0   # prints "Playwright listening on ws://127.0.0.1:<port>/<token>"
```

```js
const browser = await chromium.connect('ws://127.0.0.1:<port>/<token>');
const page = await (await browser.newContext()).newPage();
```

Agents and tools that speak CDP drive zebkit as they would drive Chrome:

```sh
tools/zebkit-run --headless --remote-debugging-port=9222 https://example.com/
```

Any CDP client connects to `http://127.0.0.1:9222`.

An MCP client gets the engine's capabilities as tools from `tools/zebkit-mcp`, a
separate program, with file access and origins denied until its operator grants
them ([docs/MCP.md](docs/MCP.md)):

```sh
ZEBKIT_DIR=<package> cargo build --release --manifest-path tools/zebkit-mcp/Cargo.toml   # or the archive's
zebkit-mcp --allow-origin https://example.com --allow-write ~/agent-files   # on standard input and output
zebkit-mcp --http 8931 --allow-origin '*'                                   # on 127.0.0.1, with a token
```

### The examples

```sh
mise example:linux:basic    # examples/window.c: a browser window
mise example:rust:window    # the same in Rust
mise example:ffmpeg         # examples/ffmpeg.cpp: a library inside the engine
(cd examples/gpui-browser && cargo run --release)   # a tabbed browser in GPUI-KIT
```

## Benchmark

Against the latest stable Electron, 45.2.1 (Chromium 156), measured the same way:
one harness, the same pages, two thin hosts that do the same thing, every process
counted, medians of 5 to 11 runs taking turns, Linux x86-64, 2026-11-06 and 07
(`scripts/electron-compare.sh`, `docs/reports/electron-compare.md`).

| | zebkit 0.2.0 | Electron 45.2.1 | |
|---|---:|---:|---|
| As an application ships it, uncompressed / `.tar.xz` | **171.2 / 59.4 MiB** | 260.5 / 87.1 MiB | 34% smaller |
| Start, cold, to first paint | **2.3 s** | 6.6 s | 66% less |
| Start, warm, to first paint | **116 ms** | 236 ms | 51% less |
| Memory, a blank page | **179 MB** | 250 MB | 29% less |
| A call from the page to the host and back, 1 MiB / 16 MiB | **3.3 / 58 ms** | 4.3 / 66 ms | 23% / 12% less |
| DOM, 20,000 elements made and laid out | 280 ms | 278 ms | level |
| JavaScript and DOM, ten workloads | 1139 ms | 1193 ms | level |
| Text layout, a chapter of a book | 8.1 ms | 7.6 ms | level, within noise |
| A 756-page PDF in each one's viewer: CPU / memory | **0.75 s / 261 MB** | 1.6 s / 399 MB | 53% / 35% less |
| Ten popular sites: CPU loading / memory | **21.7 s / 4756 MB** | 25.2 s / 5060 MB | 14% / 6% less |
| Processes, a page | 7 | **6** | one more: storage sandboxed in its own, as Chrome |

- **Size.** zebkit keeps the whole web platform applications use: HTML, CSS,
  JavaScript with every JIT tier, WebAssembly, WebGL, media with H.264 and AAC,
  HTTP/3, PDF.
- **Speed.** Chrome's own profile-guided optimization reaches Blink because
  zebkit is built with CFI as Chrome is; every speed change is kept only when it
  gains more than it costs in size (`docs/SIZE_AND_SPEED.md`).
- **Where Electron is ahead**: one process fewer a page, and memory on two of the
  ten sites, YouTube and The Verge, where advertising and video decide.
- How each number is made: `docs/SIZE_AND_SPEED.md`.

The same Playwright commands three ways, headless, medians
(`docs/reports/automation-bench.md`, `scripts/automation-bench.sh`):

| | zebkit's API, in-process | Your Playwright scripts, connected to zebkit | Playwright with Chrome 156 |
|---|---:|---:|---:|
| `locator.click()` | **2.0 ms** | 3.5 ms | 33.3 ms |
| `locator.fill()` | 2.1 ms | **2.0 ms** | 2.9 ms |
| `locator.press('Enter')` | **0.59 ms** | 0.98 ms | 2.6 ms |
| `locator.textContent()` | **0.23 ms** | 0.70 ms | 0.81 ms |
| `allTextContents()` of 200 | **0.34 ms** | 1.9 ms | 1.9 ms |
| `page.goto()` | **11.2 ms** | 13.0 ms | 18.2 ms |
| `page.screenshot()` | **12.4 ms** | 16.7 ms | 33.8 ms |
| `page.screenshot({type: 'jpeg'})` | **13.9 ms** | 14.4 ms | 32.9 ms |
| the screenshot's pixels, unencoded | **9.3 ms** | | |

- **zebkit's API, in-process**: your program calls the command through
  `<zebkit/automation.h>`, Python's `zebkit.automation` or Rust's
  `zebkit::automation`; it runs inside the engine, with no Node.js and no protocol.
- **Your Playwright scripts, connected to zebkit**: Playwright's own Node.js
  client, unchanged, with `chromium.connect()` to zebkit's endpoint; its test
  suite (v1.64.1) passes 4,046 of its tests there, Chrome 4,196
  (`docs/AUTOMATION.md`, section 7).
- **Playwright with Chrome**: Playwright as usual, over CDP.
- **Why it is faster**: one call in the renderer where Playwright's server makes
  several round trips over CDP, no JSON between processes, no Node.js process
  (Playwright's alone reached 175 MiB); and the frames a click's checks wait for
  are made at once instead of at 60 Hz on a page without a display.
- **A screenshot is 2.7 times faster**: the fresh frame it takes is made at
  once instead of at the next 60 Hz tick, the PNG is deflated at level 1 with
  the Up filter (2 ms where Chrome's default level takes 13, for 59 KB
  instead of 40 KB on this page), and the picture's shared memory is made in
  one call instead of a page fault at a time. What is left of the 12 ms is the
  page's frame (4 ms), copying the picture out of the compositor (4 ms) and
  encoding it (4 ms). The pixels themselves, with no encoding
  (`zebkit_automation_screenshot_pixels()`, zebkit's own), take 9 ms. Over CDP
  zebkit does what Chrome does: frames at 60 Hz, Chrome's PNG.

## Reference

### Documentation

| Document | What it covers |
|---|---|
| [docs/API.md](docs/API.md) | Everything an application can call, in C, Rust, Python and JavaScript |
| [docs/BUILD.md](docs/BUILD.md) | Fetching Chromium, building, packaging, testing, measuring and releasing; profiles and patches |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | How the engine is made, and what in this repository is what |
| [docs/AUTOMATION.md](docs/AUTOMATION.md) | Playwright's API without CDP: how Playwright works, what zebkit does instead, the endpoint, what it costs |
| [docs/MCP.md](docs/MCP.md) | `tools/zebkit-mcp`: the engine as MCP tools for agents, its bounds, what is weak |
| [docs/SIZE_AND_SPEED.md](docs/SIZE_AND_SPEED.md) | Where the size goes, what was cut and kept, the compiler against speed, the Electron baseline |
| [docs/MACOS.md](docs/MACOS.md) | The macOS framework, native and cross builds |
| [docs/WINDOWS.md](docs/WINDOWS.md) | The Windows DLL, its sandbox, cross-building on Linux, the state of the port |
| [docs/SANDBOX.md](docs/SANDBOX.md) | The sandbox on each system, and running without one |
| [docs/LICENSING.md](docs/LICENSING.md) | zebkit's license, the third-party licenses inside the engine, and what shipping it involves |
| [docs/ROADMAP.md](docs/ROADMAP.md) | The library and the engine: requirements, what is done, what is next |
| [docs/ROADMAP_HOOKS.md](docs/ROADMAP_HOOKS.md) | Hooks: how an application decides what the engine does, from native code |
| [docs/UI.md](docs/UI.md) | `zebkit.ui`: the engine's own small UI, what it is for and what it is not |
| [bindings/rust/README.md](bindings/rust/README.md) | The Rust crates |
| [bindings/golang/README.md](bindings/golang/README.md) | The Go binding: what it covers, building with cgo |
| `docs/releases/` | Each release: what is in it, what was tested, what is missing |
| `docs/reports/` | Size reports, regenerated by the scripts |

### Repository

| Path | What it holds |
|---|---|
| `upstream.lock` | The Chromium release built, the pinned depot_tools, the Electron release measured against |
| `profiles/` | Build flavours as GN arguments: `slim.gn` (the product), `slim-macos.gn`, `slim-windows.gn`, `baseline.gn` (Chromium's defaults) |
| `patches/` | Changes to Chromium, applied in the order of `patches/series` |
| `src/engine/` | zebkit's own code, linked into Chromium as `//zebkit/engine`: the library, its C API and headers |
| `src/ffmpeg/` | zebkit's FFmpeg configuration, from `scripts/ffmpeg-config.sh` |
| `bindings/rust/`, `bindings/python/`, `bindings/golang/` | The Rust crates, the Python binding and the Go binding |
| `tools/` | `zebkit-run` (open pages, serve CDP or Playwright's endpoint), `zebkit-js` (applications in JavaScript) and `zebkit-mcp` (the engine as MCP tools) |
| `tests/` | Programs that test every layer of the API against a package; speed workloads |
| `examples/` | A browser window in C, `zebkit.ui`, a library inside the engine, the Electron baseline |
| `scripts/` | Every step, one script each; `mise tasks` lists the short forms |

`upstream/` (Chromium's tree, about 30 GB), `out/`, `dist/` and `.cache/`
are generated and not tracked.

zebkit is Chromium plus a small patch set (`patches/`), built from source.
Where Chromium lacks something an application needs, zebkit patches
Chromium rather than working around it (`docs/BUILD.md`).

## License

zebkit is free software under the GNU Lesser General Public License, version
2.1 or (at your option) any later version: [LICENSE](LICENSE). Applications
of any license, open or closed, can use it as a library.

The engine contains Chromium and the libraries it uses (Blink, V8, Skia,
PDFium, FFmpeg in its LGPL configuration, ICU, SQLite, BoringSSL and others),
each under its own license. Every release archive carries `LICENSE`, a
`NOTICE` that says where its source is, and `THIRD_PARTY_NOTICES.txt` with
every third-party license text. [docs/LICENSING.md](docs/LICENSING.md) says
what an application that ships zebkit has to do.

Contributions are accepted under the same license: by sending a pull request
you agree that your contribution is licensed under the LGPL 2.1 or later, as
the rest of zebkit.
