<p align="center">
  <img src="docs/social-preview.png" alt="Gander: take a gander at any file. Open source Android file viewer for PDF, DOCX, XLSX, PPTX, JPG, MP4, MP3 and Markdown. 100% offline, 15 MB APK, zero permissions, no ads or trackers.">
</p>

# Gander 🪿

**Take a gander at any file.** A tiny, open source, fully offline **file viewer for Android** that opens
PDF, Word (`.docx`), Excel, PowerPoint (`.pptx`), photos, videos, audio, Markdown, text and code
in one app, with **zero permissions, no ads, no tracking and no internet access at all**.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/mokshablr/gander)](../../releases/latest)
[![Build](https://img.shields.io/github/actions/workflow/status/mokshablr/gander/build.yml?branch=main)](../../actions)
![Min API](https://img.shields.io/badge/minSdk-26%20(Android%208)-brightgreen)
![Kotlin](https://img.shields.io/badge/Kotlin-100%25-purple)

Every phone ships with a dozen half-viewers that bounce your documents to cloud services.
Gander is the opposite: one small APK (about 15 MB) that renders everything **on the device**.
It cannot phone home because it does not even hold the INTERNET permission.

<p align="center">
  <img src="docs/demo.gif" width="300" alt="Gander demo: thumbnail recents, folder browsing, PDF, Word, Excel and Markdown viewing">
</p>

## Screenshots

| Home: recents and folders | Folder browsing | PDF |
| :---: | :---: | :---: |
| ![Recent files with thumbnail previews and granted folders](docs/screenshots/home.png) | ![Browsing a granted folder with previews](docs/screenshots/folder.png) | ![PDF viewer](docs/screenshots/pdf.png) |

| Word (.docx) | PowerPoint (.pptx) | Excel (.xlsx) |
| :---: | :---: | :---: |
| ![Word document viewer](docs/screenshots/docx.png) | ![PowerPoint slides viewer](docs/screenshots/pptx.png) | ![Excel spreadsheet viewer with sheet tabs](docs/screenshots/xlsx.png) |

## Features

- **One viewer for everything**: documents, spreadsheets, slides, images, video, audio, Markdown, code
- **Pinch zoom and smooth scrolling** everywhere, with deep zoom into huge photos (tiled decoding)
- **Recent files** with thumbnail previews (image, video frame, PDF first page)
- **Folder browsing** through one-time system grants, still without any storage permission
- **Share sheet and "Open with" integration**: share a file from any app (chat, mail, browser) into Gander, or tap it in a file manager
- **Find in document**: search inside Word, Excel, slides, Markdown, text and code with match navigation
- **Share and locate**: send the open file to any app, or jump to its folder in the file manager
- **Private by construction**: no permissions, no INTERNET, no analytics, no accounts, nothing leaves the phone
- **Modern Android**: Material 3, dark mode, edge to edge, works on Android 8.0+

## Supported formats

| Category | Formats | Renderer |
| --- | --- | --- |
| Documents | PDF | Pdfium (native) |
| | Word `.docx` | docx-preview, offline in a sandboxed WebView |
| Spreadsheets | `.xlsx` `.xls` `.xlsm` `.xlsb` `.csv` `.ods` | SheetJS, offline |
| Slides | PowerPoint `.pptx` | PPTXjs, offline |
| Photos | JPG, PNG, WebP, BMP, HEIC/HEIF | Tiled deep-zoom image view, EXIF aware |
| | GIF (animated), SVG, AVIF, ICO | WebView |
| Video | MP4, M4V, MOV, MKV, WebM, 3GP, AVI, FLV, MPEG-TS | Media3 ExoPlayer |
| Audio | MP3, M4A, AAC, FLAC, WAV, OGG, Opus, AMR | Media3 ExoPlayer |
| Markdown | `.md` rendered as formatted HTML | marked + DOMPurify, offline |
| Text and code | `.txt` `.json` `.xml` logs, most source files | Text viewer |

Legacy binary `.doc` and `.ppt` are not supported (no faithful offline renderer exists);
the app explains this and suggests re-saving as `.docx` / `.pptx`. Binary `.xls` works.

## Install

Runs on **Android 8.0 (API 26) and up**.

1. Download the latest APK from [Releases](../../releases/latest):
   `Gander-x.y-arm64.apk` fits practically every phone from 2017 onward
   (use the `universal` APK for very old or x86 devices).
2. Copy it to your phone, tap it, and allow "install unknown apps" when asked.
3. Optional: Play Protect may warn about an unknown developer; that is what
   sideloaded open source looks like. Tap "Install anyway".

Updating: install the new APK over the old one; recents and folder grants survive.

**Automatic updates without a store**: install
[Obtainium](https://github.com/ImranR98/Obtainium) and add
`https://github.com/mokshablr/gander` as an app source. It follows the tagged
GitHub releases here and updates Gander like a store would.

**Verify before installing**: every release is signed with the same key, so you can
confirm an APK really came from this repo. Obtainium can pin the fingerprint below,
and for a file you have already downloaded:

```sh
apksigner verify --print-certs Gander-x.y-arm64.apk
```

Signing certificate SHA-256:

```
5B:5C:F6:4A:94:23:7C:D5:F0:E0:85:76:00:38:BC:1C:EB:DF:18:DA:BA:5C:B3:EA:CA:7C:15:9F:22:A7:E2:4B
```

## How the zero-permission trick works

Gander receives files through the Storage Access Framework and "Open with" intents,
so the OS hands it exactly the documents you chose and nothing else. Office formats
render inside a locked-down WebView whose every request is intercepted by
`WebViewAssetLoader`: bundled JS libraries load from app assets and the document
streams from the content URI. No network stack is ever touched, and the app does
not declare the INTERNET permission, so there is nothing to audit or trust.

Folder browsing uses `ACTION_OPEN_DOCUMENT_TREE` grants. Note that Android itself
refuses to grant the Downloads root to any app; grant Documents, DCIM or a
subfolder of Downloads instead.

## Build from source

To build it yourself you need JDK 17+ and the Android SDK (platform 35). These are
build requirements only. The installed app runs on Android 8.0 (API 26) and up.

```sh
./gradlew assembleDebug        # installable debug build
./gradlew assembleRelease      # unsigned without a keystore
```

Release signing expects a local, untracked keystore at `keystore/gander.jks`
(store and key password `gander-local`, alias `gander`); generate one with:

```sh
keytool -genkeypair -keystore keystore/gander.jks -alias gander \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass gander-local -keypass gander-local -dname "CN=Gander"
```

The keystore is gitignored on purpose: it is a personal signing key and must
never land in a public repo.

## Architecture in one paragraph

`ViewerActivity` routes by file extension first, MIME type second (`FileKind.kt`),
into one of four surfaces: a native Pdfium view for PDF, a tiled
`SubsamplingScaleImageView` for photos, Media3 ExoPlayer for video and audio, or a
sandboxed WebView for everything rendered by vendored JS libraries
(`app/src/main/assets/viewer/`). The home screen (`MainActivity`) lists recents
(persisted SAF grants) and granted folders (DocumentsContract child queries), with
thumbnails generated off-thread and cached (`Thumbs.kt`).

Vendored viewer libraries and their licenses: JSZip (MIT), docx-preview
(Apache-2.0), SheetJS CE (Apache-2.0), PPTXjs + divs2slides (MIT), jQuery 1.11
(MIT), D3 3.x + NVD3 (BSD/Apache), marked (MIT), DOMPurify (Apache-2.0/MPL).

## Roadmap

- F-Droid listing
- Legacy `.doc` / `.ppt` support if a usable offline renderer appears
- iOS companion (thin QuickLook wrapper)

## Contributing

Issues and small PRs are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).
If Gander is useful to you, a star helps other people find it.

## License

[MIT](LICENSE). Vendored viewer libraries keep their own licenses, listed above;
all are MIT/Apache/BSD and compatible.
