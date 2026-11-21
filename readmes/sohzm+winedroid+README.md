<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://winedroid.soham.sh/assets/logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://winedroid.soham.sh/assets/logo-light.png">
  <img src="https://winedroid.soham.sh/assets/logo-light.png" alt="WineDroid" width="240">
</picture>

An experimental Android compatibility layer for macOS, Linux, and the browser.
Inspired by Wine: run Android APKs without booting an Android OS.

**[Try the browser demo →](https://winedroid.soham.sh/demo/)**

Written in Rust, WineDroid executes DEX bytecode, implements Android framework
behavior, and renders app interfaces with Skia. Desktop builds include a
Cranelift JIT. The WebAssembly build runs the same runtime and renderer in your
browser, using the interpreter.

**Very early development.** Some apps and workflows run; compatibility is
limited. Expect missing APIs and broken apps.

## What runs today

The [AppDB](https://winedroid.soham.sh/appdb/) tracks app compatibility,
screenshots, and known issues:

| App | Version | Rating |
| --- | --- | --- |
| [Weather Overview](https://winedroid.soham.sh/appdb/1783189860.html) | 0.1 | Gold |
| [Candle](https://winedroid.soham.sh/appdb/1783192298.html) | 1.7.1 | Silver |
| [Open Notes](https://winedroid.soham.sh/appdb/1783214748.html) | 1.4.0 | Bronze |
| [Currency](https://winedroid.soham.sh/appdb/1782757383.html) | 1.58 | Bronze |
| [OpenCalc](https://winedroid.soham.sh/appdb/1781784356.html) | 3.2.0 | Bronze |
| [Meditation Timer](https://winedroid.soham.sh/appdb/1718264025.html) | 1.2.0 | Bronze |

See the individual reports for what works and what doesn't, and the
[rating definitions](https://winedroid.soham.sh/about.html#ratings).

## Run locally

Install a recent stable Rust toolchain and native C/C++ build tools. On macOS,
use Xcode Command Line Tools. On Linux, also install `pkg-config` and the
FreeType and Fontconfig development packages; running the desktop app requires
an X11 or Wayland session.

```sh
git clone https://github.com/sohzm/winedroid.git
cd winedroid
cargo build --release --locked --bin winedroid
./target/release/winedroid /path/to/app.apk
```

App data lives in `~/.winedroid/default`. Set `WINEDROID_PREFIX` to use another
directory. See [usage](docs/usage.md) for package management, display settings,
and profiling.

## Run in your browser

With Emscripten's `emcc` on your `PATH` and Python 3 installed:

```sh
rustup target add wasm32-unknown-emscripten
scripts/build_web.sh
python3 -m http.server 4173 --directory web
```

Open [localhost:4173](http://localhost:4173) and choose or drop an APK. App data
is lost on reload. The browser build does not support Android native `.so`
libraries or the Cranelift JIT.

## Contributing

Development is intermittent. Contributions and reproducible bug reports are
welcome. Include the app version, host OS, steps to reproduce, and error output.

Read the [architecture](docs/architecture.md) and [contributor instructions](AGENTS.md)
before changing runtime behavior. Compatibility fixes should implement Android
primitives that benefit other apps too. The validation gate is
`scripts/validate.sh`; benchmark APK setup is described in `AGENTS.md`.

## License

[GPLv3 only](LICENSE). Third-party components retain their respective licenses;
see [third-party notices](THIRD_PARTY_NOTICES.md).

### Missing support during development

Execution is best-effort by default. When a guest method call reaches explicitly
reported missing support, winedroid prints `FIXME` with the primitive identity,
then substitutes void, numeric zero (including false),
or null according to the return type. Existing side effects are not rolled back.
This helps discover multiple missing primitives in one run; output after a
substitution is not evidence of Android compatibility. Guest exceptions and
unrelated runtime failures still propagate, and missing objects can cause later
app failures.

An interrupted caller is reported as `CONTEXT: abandoned ...; caused by: ...`
and grouped under the underlying primitive in the report, rather than counted
as a separate missing API. This relationship comes from the error being handled.
Substituted values are not tracked through later execution, so subsequent null
errors are not automatically attributed to an earlier missing call.

Use `WINEDROID_STRICT=1 cargo run -- /path/to/app.apk` to stop on missing support.
`scripts/validate.sh` forces strict mode. For direct conformance runs, use
`WINEDROID_STRICT=1 cargo test --offline`.

Set `WINEDROID_MISSING_PRIMITIVE_LOG=/path/to/missing.txt` to keep a report of
primitive identities, hit counts and first context. It is updated as discoveries
occur, so a later abnormal exit does not lose earlier reports. `FIXME` output is
emitted on first discovery, with an incomplete-execution summary at normal exit.

### Console output

Normal launches print a short header with runtime and app versions, host,
execution mode and start time. After that, missing support is reported once per
primitive as `FIXME: not implemented: ...`; errors remain visible. Installed
artifacts created before version metadata was recorded show an unknown app
version until the APK is installed again.

Use `--trace launch,runtime,ui,click` before the APK or command for startup,
activity, layout and interaction details. Add `automation` for successful
script-step timing and `missing` for full missing-call context and substitutions.
`--verbose` enables all trace categories. `WINEDROID_TRACE` accepts the same
comma-separated categories. Explicit inspection commands and requested dumps
still print their results. Missing-primitive report files retain full context
regardless of console verbosity.
