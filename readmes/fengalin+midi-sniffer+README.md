# midi-sniffer ![CI](https://github.com/fengalin/midi-sniffer/workflows/CI/badge.svg)

`midi-sniffer` is portable GUI to inspect MIDI messages on up to 2 ports.

![midi-sniffer UI](assets/screenshot_20220408.png "midi-sniffer UI")

## Dependencies

Also this application should work on Linux, macOS and Windows, it has only been
tested on Linux so far. Portability is made possible thanks to the Rust Standard
Library and the following crates:

- [`egui`](https://crates.io/crates/egui) / [`eframe`](https://crates.io/crates/eframe) / [`winit`](https://crates.io/crates/winit).
- [`midir`](https://crates.io/crates/midir).
- [`rfd`](https://crates.io/crates/rfd), when the `save` (default) feature is enabled.

### Linux

Minimum dependencies include development libraries for:

- X11 or Wayland.
- `alsa` (`alsa-lib-devel`, `libasound2-dev`, ...)

Message list saving support is available using the `save` feature, which
requires:

- `gtk3` (`gtk3-devel`, `libgtk-3-dev`, ...)

`jack` audio support is available using the `jack` feature, which requires:

- `libjack-dev`, `jack-audio-connection-kit-devel` or
`pipewire-jack-audio-connection-kit-devel`, ...

## Build

You need a stable Rust toolchain for the target host. Get it from [this page](https://www.rust-lang.org/fr/tools/install).
On a Unix-like system, you should be able to install `rustup` from your packet
manager.

Clone the git tree and run the following command in an environment where
`cargo` is available:

```
cargo b --release
```

This will compile the executable **without** `jack` support. If you need `jack`
support, use the following command:

```
cargo b --release --features=jack
```

## Run

After a successful compilation, launch the executable with:

```
target/release/midi-sniffer
```

## LICENSE

This crate is licensed under MIT license ([LICENSE-MIT](LICENSE-MIT) or
http://opensource.org/licenses/MIT)
