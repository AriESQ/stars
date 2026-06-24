# autonice

Automatically renice processes the moment they exec, driven by eBPF.

A tracepoint on `sched_process_exec` streams every exec to a userspace daemon,
which matches the binary against a config and calls `setpriority(2)`.
**eBPF detects, userspace acts** — there's no BPF helper to renice a task, so the
kernel side only reports execs and the daemon does the reniceing.

## How it works

```
 kernel                          userspace (tokio)
 ┌──────────────────────┐        ┌────────────────────────────┐
 │ sched_process_exec   │  ring  │ match path against config  │
 │  → pid + exec path   │ ─────► │  → setpriority(pid, nice)  │
 └──────────────────────┘  buf   └────────────────────────────┘
```

Two kinds of match:

- **Single binaries** (`[rules]`) — by basename; opt in to path-substring
  matching with the table form `{ nice = N, substring = true }`.
- **Subtree roots** (`[subtree]`) — renice each configured root (`cargo`,
  `make`, …) *and everything it spawns* (rustc, sub-makes, `cc`, `ld`), tracked
  by parent pid so standalone `rustc`/`cc` outside a root are left alone.
  Descendants are seeded race-free from a `sched_process_fork` hook.

## Requirements

**To run** — any modern Linux distro (Arch, Debian, Ubuntu, …):

- Linux ≥ 5.8 with BTF and tracefs at `/sys/kernel/tracing`. Debian bookworm+
  and current Arch both qualify.
- Root, or the capabilities `CAP_BPF`+`CAP_PERFMON` (load BPF) and `CAP_SYS_NICE`
  (renice others / set negative nice).

The released binary is a **fully static musl build** — no glibc dependency, so
the *same* binary runs on every distro. Most users can grab it and skip the
build toolchain entirely (see [Running as a service](#running-as-a-service)).

**To build from source** — only if you're not using a released binary:

- Rust nightly with `rust-src`, the `x86_64-unknown-linux-musl` target, and
  [`bpf-linker`] (the eBPF crate is compiled by `build.rs`).
- A C linker (`build-essential` on Debian, `base-devel` on Arch).

```sh
make deps   # rustup: rust-src + musl target; cargo install bpf-linker
```

Install the system prerequisites first (on Debian, `rustup` is packaged only on
trixie+ — `apt install rustup`; elsewhere get it from https://rustup.rs):

```sh
# Debian / Ubuntu
sudo apt install build-essential
# Arch
sudo pacman -S --needed base-devel rustup
```

If `cargo install bpf-linker` complains about LLVM, install it too
(`apt install llvm clang` / `pacman -S llvm clang`).

## Build & run

```sh
make build                       # or: cargo build
sudo RUST_LOG=info ./target/debug/autonice
# or:  make run                  # wraps the binary in `sudo -E`
```

`make` on its own lists every target.

### Quick test in a container

[`docker-compose.yml`](docker-compose.yml) runs the host-built **static** binary
in a thin container to watch it act on the host's execs — one service per distro,
so you can confirm the same binary works on each:

```sh
make docker-arch     # archlinux:base
make docker-debian   # debian:trixie-slim   (alias: make docker)
```

Each target builds the static binary (`make build-static`) and runs it; the
image itself builds nothing (the binary already embeds the eBPF object). It needs
`privileged` and — critically — `pid: host`, because the eBPF reports global pids
that `setpriority`/`/proc` only resolve in the host pid namespace. That makes it
barely isolated from the host: a convenience harness, not a sandbox. See the
file's header for the full rationale.

## Configuration

Read from `./autonice.toml` then `/etc/autonice.toml`. Nice ranges from `-20`
(highest priority) to `19` (lowest). If no config exists, uses internal default.

```toml
[subtree]
nice = 19                    # each root + its whole build subtree
roots = ["cargo", "make"]    # cargo, make, and everything they spawn

[rules]
dd = 19                                 # <basename> = <nice>; matches basename only
ffmpeg = { nice = 15, substring = true } # also matches any path substring
# pipewire = -10                        # negative nice needs CAP_SYS_NICE
```

## Layout

| Crate              | Role                                                          |
| ------------------ | ------------------------------------------------------------ |
| `autonice-ebpf`    | eBPF program: tracepoint → ring buffer (`#![no_std]`)        |
| `autonice-common`  | `ExecEvent` shared kernel ↔ userspace                        |
| `autonice`         | daemon: drain ring buffer, match config, `setpriority`       |

Built with [Aya]. The userspace `build.rs` compiles the eBPF crate via
`aya-build` (cargo-in-cargo with `-Z build-std`) and embeds the object.

## Running as a service

The binary self-installs on any systemd distro (Debian, Arch, …): the unit file
and a default config are baked in (`include_str!`), so `autonice install` copies
the running binary to `/usr/local/bin`, writes the unit + `/etc/autonice.toml`
(kept if it already exists), and enables the service with just the capabilities
it needs (see [`autonice.service`](autonice.service)) instead of full root.

The release binary is static, so building it (below) and downloading it from the
CI release are interchangeable — either way it's a single file:

```sh
make release   # -> target/x86_64-unknown-linux-musl/release/autonice
sudo ./target/x86_64-unknown-linux-musl/release/autonice install
journalctl -u autonice -f
```

Equivalently, by hand:

```sh
BIN=target/x86_64-unknown-linux-musl/release/autonice
sudo install -Dm755 "$BIN"           /usr/local/bin/autonice
sudo install -Dm644 autonice.toml    /etc/autonice.toml
sudo install -Dm644 autonice.service /etc/systemd/system/autonice.service
sudo systemctl daemon-reload && sudo systemctl enable --now autonice
```

## Setup notes

- **Pinned for reproducibility.** The `aya` deps are git (no `rev`), so the
  committed `Cargo.lock` is what pins them — keep it committed.
  `rust-toolchain.toml` pins the nightly + `rust-src`, since the eBPF crate's
  `-Z build-std` is sensitive to the exact nightly.
- **`rust-src` must be *installed*, not just available** —
  `rustup component add rust-src --toolchain nightly` (in `make deps`).
- **`AYA_BUILD_SKIP=1`** skips the eBPF rebuild when iterating on userspace only.
- **Userspace builds on stable**; only the eBPF crate needs nightly, and
  `aya-build` invokes it via `rustup run nightly` — no need to switch defaults.
- **Static musl release.** `make release` targets `x86_64-unknown-linux-musl` —
  a fully static binary with no glibc dependency, so one artifact runs on every
  distro. `cargo build`/`test`/`run` stay native (glibc) for fast local dev.
- **Introspect a running daemon** with `bpftool prog show` and
  `bpftool map dump name EVENTS`.
- Verifier errors only appear on a *privileged* load; use `RUST_LOG=debug` for
  aya's verifier log.

## Caveats

- Subtree descendants are seeded race-free from a `sched_process_fork` hook (the
  child is recorded the instant it's forked, before it execs). A `/proc/<pid>/stat`
  parent lookup at exec time remains as a fallback — for fork events not yet
  drained, and for forks from a non-leader thread (whose tracepoint `parent_pid`
  is a TID, but whose `/proc` ppid is the tracked process).
- Tracepoint field offsets are hardcoded (exec: `filename` @ 8, `pid` @ 12;
  fork: `parent_pid` @ 24, `child_pid` @ 44); verify on your kernel with
  `make tracepoint-format`.

## License

GPL2.0

[Aya]: https://aya-rs.dev
[`bpf-linker`]: https://github.com/aya-rs/bpf-linker
