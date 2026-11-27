# h9 - Hyper9

h9 runs native Plan 9 (9front) programs on macOS, Linux, and Windows as if
they were host programs. Nothing boots and there's no disk image: you type
`h9 ls`, and 9front's own `ls` binary runs on a virtual CPU from your host's
hypervisor and lists your directory in a few milliseconds.

Each run is a small, complete Plan 9 machine with its own namespace,
processes, console, and `/srv`, and its system calls are answered by a Plan 9
kernel inside the h9 process (the one from drawterm), never by your host's.
That kernel is also the sandbox: a program sees only the host files and
network you give it. h9 runs Linux binaries the same way, so a 9front shell
and an Alpine `sh` can share one machine.

> **Status:** h9 is under active development, hasn't had a release yet, and
> its sandbox hasn't been through a security audit. Don't trust it with
> malicious code yet.

## Quick start

On a Mac with Apple Silicon, Zig 0.17, and Xcode:

```sh
git clone https://github.com/progrium/hyper9 && cd hyper9
. scripts/env.sh       # Zig's cache and tools in .local/; puts zig-out/bin on PATH
./scripts/fetch.sh     # the pinned 9front release and other sources
zig build              # builds and signs zig-out/bin/h9
h9 --check             # which engines work here, and why not
```

That's enough to run h9's built-in root, 44 of 9front's commands inside the
binary itself:

```sh
$ h9 echo hello
hello
$ h9 --rc 'cat /dev/sysname; echo; echo $cputype'
h9
arm64
```

For the full 9front tree (compilers, `mk`, rio, acme, fonts, and the man
pages), extract it from the pinned release image with QEMU:

```sh
brew install qemu
zig build mkroot       # about a minute, ~250 MB in .local/9front/root
```

Linux (KVM, the emulator, or the sud engine in containers and CI),
Windows, and the web host are covered in the manual's
[Installing](MANUAL.md#2-installing) chapter and in
[DEVELOPING.md](DEVELOPING.md).

## A few things to try

Use 9front tools in host pipelines, or start a shell in a fresh machine:

```sh
git log --format=%an | h9 sort | h9 uniq -c | h9 sort -nr | sed 5q
h9 rc                                   # % prompt; your cwd is /mnt/term/cwd
h9 --rc 'ls /bin | wc -l'               # the whole pipeline runs inside Plan 9
```

Sandbox a command. By default the root is a copy-on-write overlay, the cwd is
read-write, and nothing else of the host is visible:

```sh
h9 --write=ephemeral --net=disable --timeout 5m --rc 'mk test'   # every change stays in memory
h9 --sandbox ./work --rc 'touch f && ls'      # only ./work, writable, no network
h9 --net-allow 'tcp!api.example.com!443' ./client   # egress to one host only
h9 --print --profile=tight mk                 # show the compiled plan and exit
```

With `--children`, a machine runs its own `h9`, which starts a child machine
inside it, bounded by the parent's files, network, and limits:

```sh
h9 --children --memory 1g --rc 'h9 --memory 256m --net disable --rc ''mk test'''
```

Run Linux programs, from a single static binary to a whole distribution:

```sh
h9 ./hello                              # a static Linux ELF, no Linux tree needed
h9 --dir ./alpine:#L sh                 # Alpine's minirootfs, or any unpacked image
```

Open rio, Plan 9's window system, in a host window:

```sh
h9 --gfx rio
```

Mount file systems over 9P and WebSocket, or serve a machine's namespace to
other machines:

```sh
h9 --url tcp://fs.example.com:564 ls /        # a 9P server as the root
h9 --url fs.example.com/9p ls /               # the same over wss://
h9 --serve unix!/tmp/h9.sock                  # export this machine's namespace, to Linux too
h9 --url tcp://zerofs.local:5564 ls /         # a 9P2000.L server (ZeroFS, diod) too
```

Build 9front software inside h9 with its own compilers and `mk`, run Go's
`GOOS=plan9` binaries, or embed machines in your own Zig program. The
[recipes](docs/recipes.md) have many more one-liners.

## Learn more

- [MANUAL.md](MANUAL.md): using h9, including a Plan 9 primer for Unix
  users, the full flag reference, sandboxing, and troubleshooting.
- [docs/](docs/): guides that go further, such as
  [recipes](docs/recipes.md), [recreating Docker](docs/containers.md),
  [building your own userland](docs/userland.md),
  [embedding h9](docs/embedding.md),
  [emulator performance](docs/emu-performance.md),
  [ideas for what to build](docs/inspiration.md), and
  [how h9 compares](docs/comparison.md) to containers, sandboxes, and other
  ways to run Plan 9.
- [SPEC.md](SPEC.md): how h9 works inside, as built.
- [design/](design/README.md): proposals for what's next, with their status
  in [design/STATUS.md](design/STATUS.md).
- [DEVELOPING.md](DEVELOPING.md): building every target, running the tests,
  releases, and a map of the source tree.

## License

h9 is MIT licensed, emulator included. See [LICENSE](LICENSE).
