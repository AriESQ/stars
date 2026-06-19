# bgbgone-app

<p align="center">
  <img src="design/reference-screenshots/v0.1.1-app-icon.png" width="200" alt="bgbgone-app icon">
</p>

**Background, be gone!** — the macOS GUI for [`bgbgone`](https://github.com/Arthur-Ficial/bgbgone).

Drop a folder of images. Watch it process. End up with a folder of clean cutouts. 100% on-device (Apple Vision via the `bgbgone` CLI), batchable, never touches the network.

`bgbgone-app` is a thin SwiftUI wrapper around the `bgbgone` CLI — there is **no image-processing logic in this repo** (architecturally enforced; see [CLAUDE.md](CLAUDE.md)). The GUI exists to make the same UNIX tool ergonomic for visual workflows: bulk product photography, headshot batches, content cleanup. For automation, scripting, and pipelines, use the CLI directly.

## Install

```bash
brew tap Arthur-Ficial/tap
brew install --cask bgbgone-app
```

Or grab the signed + notarised `.zip` from the [latest release](https://github.com/Arthur-Ficial/bgbgone-app/releases/latest).

The cask ships with `bgbgone` embedded as a fallback, so it works out of the box. If you already have `bgbgone` installed via `brew install Arthur-Ficial/tap/bgbgone`, the app uses your installed version (keeping the CLI and GUI in lockstep).

## v0.2 — "Finder, but for background removal"

v0.2 is a ground-up rewrite of the UI shell around the same proven CLI engine. The window is now a real `NSWindow` with a real Apple title bar, a real sidebar, a real `Table` for the file list, a real `Form` for configuration, and a real `.inspector` pane on the right with the dual preview. If you've used Finder, you know how it works.

Plus **Demo Mode**: an empty-state button that downloads 10 public-domain images from Wikimedia Commons (full attribution shown before any byte hits disk) and runs them end-to-end through `bgbgone` — a one-click way to see the whole pipeline without finding your own files.

What changed under the hood:

- Real `NSWindow` chrome — no more app-in-an-app (v0.1 painted a second title bar inside the real one).
- Real `NSImage` previews — the dual preview pane decodes your actual pixels via `ImageIO` thumbnails, instead of drawing grey-blob silhouettes.
- Real elapsed-ms timing — the status pill shows the wall-clock time `bgbgone` actually took.
- Stock SwiftUI everywhere: `NavigationSplitView` / `Table` / `Form` / `Picker(.segmented)` / `.fileImporter` / `ColorPicker`.
- System fonts, system semantic colours (`.primary` / `.secondary` / `.tertiary`), system `.accentColor` (follows your macOS accent preference), system `.regularMaterial` / `.thinMaterial` backgrounds.
- TDD enforcement: the new `NoFakeUITests` suite fails any future PR that re-introduces fake chrome, stub runners, silhouette placeholders, baked-in demo files, or aspirational labels.

## How it works

1. Drop a folder (or images) onto the window — or click **Try Demo** to pull 10 public-domain images from Wikimedia Commons.
2. The app scans recursively, surfaces a batch in the sidebar, populates the file table with sortable columns (Name / Status / Size / Dimensions / Modified).
3. Right inspector pane: select a row → live dual preview (Original / Removed) above the config form. Configure output folder, name pattern, background (Transparent / Color / Image), format (PNG / JPEG / HEIC / TIFF).
4. Hit **Remove background from N** in the toolbar. Each file runs through `bgbgone <input> -o <output> --json --quiet` as a separate `Process`; up to 4 in parallel.
5. Outputs appear at your chosen folder, named by your chosen pattern. Right-click → **Show in Finder** to jump there.

## Demo Mode — what gets downloaded

`scripts/demo-manifest.json` lists the 10 public-domain images and their licenses + attribution. On first **Try Demo** click, the GUI shows the attribution sheet, you click **Download & Run**, and `scripts/fetch-demo-images.sh` downloads each into `~/Library/Caches/bgbgone-app/demo/`. Idempotent — subsequent runs use the cache.

The demo cross-section exercises the matrix of `bgbgone --type` modes: animal, product, portrait, botanical, vehicle, food, translucent, already-transparent PNG, statue/architectural, graphic.

## Apple Silicon, macOS 26+

SwiftUI 6.3 / macOS 26 single-window app. It carries no media libraries beyond `ImageIO` (used only to read thumbnails and `width × height × bytes`). All segmentation work is delegated to the embedded `bgbgone` binary. Architecturally enforced by `NoBusinessLogicTests` — any `import Vision|CoreImage|CoreML|Metal|Accelerate|MetalKit|VideoToolbox|MetalPerformanceShaders` under `Sources/` fails the build.

## Project family

| Tool | What | Framework |
|------|------|-----------|
| [apfel](https://github.com/Arthur-Ficial/apfel) | LLM | FoundationModels |
| [auge](https://github.com/Arthur-Ficial/auge) | Vision / OCR | Vision |
| [bgbgone](https://github.com/Arthur-Ficial/bgbgone) | Background removal CLI | Vision + CoreImage |
| **bgbgone-app** (this) | GUI for bgbgone | SwiftUI |

## Development

See [CLAUDE.md](CLAUDE.md) for project rules. TL;DR:

```bash
git submodule update --init --recursive   # fetch the pinned bgbgone CLI (vendor/bgbgone)
make vendor         # build the pinned bgbgone v1.2.23 helper (also done by make app/test)
make test           # swift test — incl. the real-binary e2e against the pinned CLI
make app            # builds build/bgbgone-app.app (embeds + version-asserts the helper)
make run            # build + open
make screenshots    # capture build/screenshots/<state>.png for every UI state
make release        # bump .version, sign, notarize, release, update tap (Arthur only)
```

The `bgbgone` CLI is a **pinned git submodule** (`vendor/bgbgone` @ v1.2.23), built and
embedded into the app bundle — never scavenged from your `PATH`. After cloning, run the
`git submodule update --init --recursive` line above (or just `make vendor` / `make app`,
which initialise it for you).

The design source-of-truth lives in [`design/`](design/) — open `design/project/bgbgone.html` in a browser to step through every UI state. The Swift implementation matches those mockups via real macOS chrome (no painted facsimiles).

## License

MIT — see [LICENSE](LICENSE).

## Made by

A project by **[Franz Enzenhofer](https://github.com/franzenzenhofer)** ([Full Stack Optimization](https://www.fullstackoptimization.com)), built by his AI assistant **[Arthur Ficial](https://github.com/Arthur-Ficial)**.
