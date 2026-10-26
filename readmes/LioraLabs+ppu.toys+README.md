# ppu

`ppu` is the Rust engine behind [ppu.toys](https://ppu.toys): an emulated SNES
Picture Processing Unit and S-DSP sound chip driven from Lua. This repository
holds the engine crate, the `ppu` command-line tool for authoring toys offline,
and the authoring guides.

Write Lua, render frames to PNG, check a toy for errors, pack it, then open the
packed file in the ppu.toys Studio to play it with sound, edit it live, and
publish it.

## Install

Prebuilt binaries for macOS and Linux, Intel and ARM:

```sh
brew install lioralabs/tap/ppu   # macOS and Linux
yay -S ppu-cli-bin               # Arch Linux, from the AUR
cargo install ppu-cli            # from crates.io
```

Or build from this repository, or grab a tarball from the
[releases page](https://github.com/LioraLabs/ppu.toys/releases):

```sh
cargo install --git https://github.com/LioraLabs/ppu.toys.git --locked ppu-cli
```

## Quick start

```sh
ppu new my-demo
ppu render my-demo --at 0,2,4,6 -o previews
ppu check my-demo --duration 8 --loop 8
ppu pack my-demo -o my-demo.ppu.json
```

Then open `my-demo.ppu.json` at [ppu.toys](https://ppu.toys). `ppu docs` prints
the same guides that live in [crates/ppu-cli/docs/](crates/ppu-cli/docs/). Start with
[the authoring loop](crates/ppu-cli/docs/cli.md) and [the PPU pipeline](crates/ppu-cli/docs/registers.md).

To run a toy on a real SNES, open it in the [ppu.toys](https://ppu.toys) Studio:
its SNES panel checks it against the console's limits as you type, and
**Export to ROM** builds a cartridge image for an emulator or flash cart.

To have Claude Code author toys with you, install the `creating-demos` skill:

```sh
claude plugin marketplace add LioraLabs/claude-plugins
claude plugin install ppu-toys@lioralabs
```

## Layout

- `crates/ppu-core` is the emulator: tile modes 0 to 4, Mode 7, sprites,
  windows, color math, HDMA, the S-DSP, PNG import, and the Lua bindings. It
  also builds to WebAssembly for the site.
- `crates/ppu-cli` is the `ppu` binary: new, pack, unpack, check, render, docs.
- `vendor/piccolo` is the Lua VM, crates.io 0.3.3 plus one backported fix. Its
  README says when to drop it.
- `crates/ppu-cli/docs/` holds the authoring guides, embedded into both the CLI and the site.
- `plugin/` is the Claude Code plugin: the `creating-demos` skill and its
  effect recipes. The LioraLabs marketplace installs it from here.

## Develop

```sh
cargo test --workspace
```

The Lua fences in `crates/ppu-cli/docs/audio.md` are executed by the test suite, so doc edits
are covered by `cargo test`.

## Releasing

Maintainers cut releases with cook: `cook bump`, `cook release`, then `cook tap`,
`cook aur`, and `cook publish` once the Release workflow is green. The Cookfile
has the details.

## License

MIT. See [LICENSE](LICENSE).
