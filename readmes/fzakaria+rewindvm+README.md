<p align="center">
  <img src="site/img/mark.svg" width="64" height="64" alt="" />
</p>

<h1 align="center">Rewind VM</h1>

<p align="center">
  <b>Deterministic Linux VMs you can scrub, rewind and fork.</b><br />
  Catch a flaky build or test once, then replay it exactly, step through it, and branch it.
</p>

<p align="center">
  <a href="https://rewindvm.dev">Website</a> ·
  <a href="docs/tutorial-nix.md">Nix tutorial</a> ·
  <a href="docs/tutorial-container.md">Container tutorial</a> ·
  <a href="docs/design.md">Design</a> ·
  <a href="https://github.com/fzakaria/rewindvm/releases">Releases</a>
</p>

<p align="center">
  <a href="https://nixbot.decio.us/repos/github/fzakaria/rewindvm"><img src="https://nixbot.decio.us/badge/a8904f8f-6ea3-4838-87d7-fab31cba44c9.svg" alt="nixbot" /></a>
</p>

<p align="center">
  <img src="site/img/app-failure.png" alt="The Rewind desktop app on a failing Nix build: the timeline of build phases, the build log up to the playhead, the processes alive at that step, the SIGSEGV that ended the test, a card saying where this run parted from a passing run of the same build, and the Runs panel with the build's runs drawn as a tree of forks." />
</p>

Rewind VM runs a Nix build, a test suite or any Linux command inside a KVM
virtual machine whose every run is a function of its inputs. The same inputs
give the same run, at the same steps, every time. A failure you saw once is a
failure you keep: replay it, scrub through it step by step, read any file as it
was at any step, and fork it with a different thread interleaving from any
point.

```console
$ rewind check --epoch 1790985600 github:fzakaria/rewindvm#mylib
schedule   0: exited:0             6030 steps  a9d703ba8977  run 0a1dae14daee9820
schedule   1: exited:0             7773 steps  a9d703ba8977  run eb388bf93ef00f21
schedule   2: exited:0             7663 steps  a9d703ba8977  run 00555e83e6bab5fb
schedule   3: exited:0             7930 steps  a9d703ba8977  run 6d888ae3d6e366b3
schedule   4: exited:2             6285 steps    run c63ac15c205593ff
...

schedule 4 ends differently from schedule 0; finding the step that decides it
schedule 4 limited to steps 4246..4826 still ends differently
step 4825 decides it: a request to switch threads there makes the run fail

passing: run 9ceb6f28d5ffd7ca, schedule 4 over steps 4246..4825
failing: run aa6759a6362f43a2, schedule 4 over steps 4246..4826
the two are the same run until step 4825

where ./tests/test_pool_shutdown first behaves differently:
  ...
  both           4825   166/171   write(1, "job 17 done: 43360\n")
  failing        4829   166/172   write(1, "job 18 done: 26744\n")
  failing        4830   166/172   write(1, "worker picked job 19\n")
  failing        4839   166/171   SIGSEGV code=1 addr=0x108
  failing        4841   166/166   SIGSEGV code=0 addr=0x0
  passing        4826   166/171   write(1, "worker picked job 19\n")
  ...

$ rewind events aa6759a6 --from 4825 --to 4841
      4825   166/171   write(1, "job 17 done: 43360\n")
...
      4839   166/171   SIGSEGV code=1 addr=0x108
      4841   166/166   SIGSEGV code=0 addr=0x0

$ rewind replay aa6759a6
identical to the recording: 1693 events, 1148 context switches and 1476 read and write records over 4887 steps, and the whole machine at its 4 keyframes
```

## Install

On x86_64 Linux with KVM:

```console
$ curl -fsSL https://rewindvm.dev/install | sh
```

With Nix, run it straight from the flake, or install it into your profile:

```console
$ nix run github:fzakaria/rewindvm -- pmu status
$ nix run github:fzakaria/rewindvm#app
$ nix profile install github:fzakaria/rewindvm github:fzakaria/rewindvm#app
```

On NixOS, add the flake as an input and turn on its module:

```nix
inputs.rewind.url = "github:fzakaria/rewindvm";

# in your configuration, with inputs.rewind.nixosModules.default imported;
# it also adds rewindvm.cachix.org to Nix's substituters
programs.rewind.enable = true;
programs.rewind.app.enable = true;
# AMD only: make the branch counter exact at every boot
programs.rewind.amdBranchCounterWorkaround = true;
```

Or take the tarballs from the
[latest release](https://github.com/fzakaria/rewindvm/releases/latest)
yourself:

```console
# the rewind command, with the VM's kernel
$ curl -L https://github.com/fzakaria/rewindvm/releases/latest/download/rewind-x86_64-linux.tar.gz | tar xz
# the desktop app
$ curl -L https://github.com/fzakaria/rewindvm/releases/latest/download/rewind-app-x86_64-linux.tar.gz | tar xz
# the kernel's debug symbols for rewind gdb, next to the command (150 MB)
$ curl -L https://github.com/fzakaria/rewindvm/releases/latest/download/rewind-debug-x86_64-linux.tar.gz | tar xz
```

`/dev/kvm` must be readable and writable by you. On AMD Ryzen and EPYC, run
`sudo rewind pmu enable` once after each boot so the VM's clock can follow the
work done inside it; [Time inside the VM](docs/pmu.md) explains why.

## Use it

```console
# build a derivation under many thread schedules, and name the step that decides a failure
$ rewind check github:fzakaria/rewindvm#mylib

# the same, with the line of code each thread involved was on
$ rewind check --where github:fzakaria/rewindvm#mylib

# build a derivation in the VM once; the output is checked against the host's
$ rewind nix nixpkgs#hello

# have Nix itself build a derivation in the VM, with the clock, the seed and
# the schedule in its hash (docs/tutorial-derivations.md)
$ nix build --impure --expr 'with builtins.getFlake "github:fzakaria/rewindvm"; lib.x86_64-linux.inRewind { epoch = 1790985600; } packages.x86_64-linux.stamp'

# how many of 16 schedules from a step of a recorded run end differently,
# each a fork of the run
$ rewind check --run <run> --schedule-from <step> --schedules 16 --all --no-narrow

# judge every schedule by what a correct run is: here, a config rewritten in place
$ rewind check --property 'atomic-replace=*.conf' github:fzakaria/rewindvm#config-reload

# vary the program's randomness as well as its schedule
$ rewind check --seeds 8 github:fzakaria/rewindvm#hash-order

# any command in a root filesystem: a directory, an erofs image, or a docker export
$ rewind run --root mylib.tar --cwd /src -- make check

# whether this machine can record runs, and what to fix where it cannot
$ rewind doctor

# list runs and look inside one
$ rewind ls
$ rewind show <run>
$ rewind open <run> <step> --compare <other run>
$ rewind log <run> --steps
$ rewind ps <run> <step>
$ rewind cat <run> <step> /build/env-vars
$ rewind files <run> <step> /build

# a directory out of the VM whole, as a tar: the same bytes on
# any machine
$ rewind cat <run> <step> /build --archive tar | tar -x

# a shell inside the VM at a step, in a throwaway fork; --with brings more
# Nix packages into it
$ rewind shell <run> <step> --pid <pid>
$ rewind shell <run> <step> --pid <pid> --with nixpkgs#strace

# gdb on a fork at a step, with the symbols and sources of the kernel and of
# the process running there; arguments after -- go to gdb
$ rewind gdb <run> <step>
$ rewind gdb <run> <step> -- -batch -ex 'break pool.c:77' -ex continue -ex bt

# every thread of a process, even with the CPU idle, as at a deadlock
$ rewind gdb <run> <step> --pid <pid> -- -batch -ex 'thread apply all bt'

# gdb backwards: where a pointer was last written before the step
$ rewind gdb <run> <step> -- -batch -ex 'watch -l p->queue' -ex reverse-continue

# blame a value in memory: the line, thread and step that last wrote it,
# where the other threads were then; --reads for every access as well
$ rewind blame <run> --at <step> 'p->queue'
$ rewind blame <run> --at <step> 'p->stopping' 'p->queue' --reads

# the line of the program's own code a thread was on, with its arguments,
# locals and callers: by default the thread of the step's event; --json for
# programs
$ rewind where <run> <step>
$ rewind where <run> <step> --tid <tid> --json

# which thread held the CPU at each step of a window, from the run's context switches
$ rewind threads <run> --from <step> --to <step>

# where a run's time went: its critical path, the least it can take on any
# number of CPUs, and what would make it finish sooner; --in for one process
$ rewind time <run>
$ rewind time <run> --in <pid>

# branch a run at a step under another schedule or seed, or replay it exactly
$ rewind fork <run> <step> --schedule 2
$ rewind fork <run> <step> --seed 7
$ rewind replay <run>

# remove a run's forks that ran exactly as an older one did
$ rewind prune <run> --identical --dry-run
$ rewind prune <run> --identical

# remove a run and every fork of it, and forks of those
$ rewind remove <run> --dry-run
$ rewind remove <run>

# remove many runs in one call, here every fork, keeping the runs forked from
$ rewind ls | awk '/fork of/ {print $1}' | xargs rewind remove

# remove the cached images and stored pages no run uses any more
$ rewind gc --dry-run
$ rewind gc

# share a run as one file
$ rewind export <run> --replayable
$ rewind import <file>.rwd
$ rewind import https://github.com/fzakaria/rewindvm/releases/download/case-studies/nix-gc-closure-sigpipe-replayable.rwd
```

A program can say what a correct run is from the inside with the
[Rewind SDK](sdk/README.md), a file or two for C, Rust, Go, Python, Java or
shell: `rewind check` judges every run by its assertions, and the app marks
where one broke.

## The desktop app

The app scrubs a recorded run. Drag the playhead along the timeline and the
build log, process tree and files follow it, or jump to the failure or to
where the run parts from a passing one.

- Click a file to read it as it was at the playhead, syntax colored, or as a
  colored hex dump.
- Show source (`s`) opens the line of the program's own code the thread was
  on, with the stack frames that led there; click a frame to see its line.
  Debug info and sources come from the program itself, or from
  nixseparatedebuginfod2 for Nix packages.
- Search (`Ctrl+F` or `/`) finds text in the build log, the console, file
  paths and events, and takes the playhead to each match.
- Bookmarks (`b`) mark a step with a note, kept with the run and in its
  `.rwd` exports.
- Two runs that differ only in their schedules show the step where the
  schedules part, as a dashed blue mark, and the card says what only one of
  them got there, such as a reschedule.
- The Compare tab sets the two runs' events side by side from just before
  they part, in full, with what differs marked; `x` swaps to the compared
  run at the matching step.
- Show threads (`t`) draws a lane per thread over a window of steps, a bar
  where the thread held the CPU, this run above the compared run.
- Previous and Next can stop at one thread, process, file or kind of event,
  at every context switch, or at the switches that give the thread on the
  CPU at the playhead the CPU and take it away; the menu counts each.
- A band under the timeline is darker where the guest switched tasks more
  often, so contention shows at a glance.
- Open shell and Attach gdb work inside the VM at the playhead.
- Fork from here branches the run under another schedule. Its menu turns it
  into Check from here, which tries 8 to 64 schedules from the playhead and
  counts how they ended, a cell per schedule.
- The Runs panel draws a build's runs as a tree of schedules and forks.

<p align="center">
  <img src="docs/img/app-file-viewer.png" width="70%" alt="The Rewind desktop app with a file open at the playhead: /build/env-vars as of step 4,583, next to the build log and the process tree." />
</p>

<p align="center">
  <img src="docs/img/app-shell.png" width="70%" alt="The Rewind desktop app at the step a test segfaulted, with a terminal pane below the scrubber running a shell inside the VM: ls, type gcc and head work in /build/mylib." />
</p>

<p align="center">
  <img src="docs/img/app-runs.png" width="300" alt="The Runs panel: the mylib build's 170 runs as a tree under the passing schedule 0 run, with twelve forks of it at step 2,713, one crashed fork with forks of its own at steps 4,400 and 4,520 and a fork of a fork at 4,500, one row folding the 53 schedules from boot that passed like the schedule 0 run, then schedule 4, which failed, with a row folding the 88 windows rewind check narrowed it to and the narrowest window that still fails." />
</p>

```console
$ nix run github:fzakaria/rewindvm#app -- ~/.local/share/rewind/runs/<run>
```

It opens `.rwd` exports too, from a file or an https URL, and comes with an
example run and a short tour. See [pricing](https://rewindvm.dev/#pricing) for
licenses.

## Case studies

- [A SIGPIPE in Nix's gc-closure test](docs/case-studies/nix-gc-closure-sigpipe.md):
  Rewind's first run of Nix's functional tests failed in `gc-closure.sh`, a
  flake nobody had reported. A two-line `printf` piped into `head -n1` under
  `pipefail` is two writes, and when `head` exits between them the writer
  dies of SIGPIPE. `rewind threads` shows `head` taking the CPU between those
  writes; on the host the test never failed in 200 runs.
- [A hang in Nix's store schema migration](docs/case-studies/nix-schema-migration-hang.md):
  a known, fixed bug, [NixOS/nix#15693](https://github.com/NixOS/nix/issues/15693),
  reproduced on the version it was reported against. `rewind shell` and gdb
  inside the VM pin it to `SQLITE_BUSY_SNAPSHOT` retried inside an open
  transaction, which explains why the first fix did not stop it and the
  second did.
- [Lost task output in devenv](docs/case-studies/devenv-task-output-race.md):
  a known, fixed bug, [cachix/devenv#2281](https://github.com/cachix/devenv/issues/2281),
  where a task's last lines went missing. A test that passed 2000 times on the
  host failed under 206 of 257 schedules, and `rewind gdb` shows the last line
  still in the reader's buffer when `tokio::select!` took the child's exit.
  The fix passes every schedule.

The derivations they run are in
[examples/case-studies/flake.nix](examples/case-studies/flake.nix).

## How it works

The VM has one vCPU on stock KVM, so code in it runs on the real CPU. Its
Linux kernel carries a small Rewind platform: interrupts arrive only when the
VM hands control to Rewind, the clock moves only then, and the timestamp
counter and hardware RNG are hidden. Each of those handoffs is a step, and the
sequence of steps is the same on every run. Inputs, a Nix closure or a root
filesystem, become a read-only erofs image mapped into the VM's memory.
Keyframes of the VM's memory go into a content-addressed page store, so seeking
to any step restores the nearest keyframe and runs forward.

A GNU hello build from nixpkgs runs at close to native speed in the VM, and its
output is bit for bit the one Nix builds on the host.
[Design](docs/design.md) has the details and the limits.

## Develop

```console
$ nix develop                  # the toolchain, with REWIND_KERNEL and REWIND_INITRD set
$ cargo test --workspace
$ cargo run --release -p rewind -- nix nixpkgs#hello
$ nix flake check              # prose, the NixOS module, and a determinism check that needs /dev/kvm
$ nix fmt                      # Nix, Rust, Python, HTML and Markdown
$ nix run .#serve              # the website on a local port
```

- `guest/linux/`: the kernel patch and config fragment for the VM.
- `crates/rewind-vmm/`: the virtual machine monitor: KVM, boot, steps, time,
  keyframes.
- `crates/rewind-init/`: PID 1 inside the VM, a workspace of its own.
- `crates/rewind-trace/`: reading and querying run traces.
- `crates/rewind-store/`: the content-addressed page store.
- `crates/rewind-core/`: input images, Nix derivations, runs, seeking.
- `crates/rewind/`: the `rewind` command.
- `crates/rewind-app/`: the desktop app, a workspace of its own.
- `examples/mylib/`: the flaky thread pool the tutorials use.
- `nix/`: one file per derivation; `flake.nix` only wires them together.
- `site/`: rewindvm.dev.
- `docs/`: tutorials, the time reference and the design.
- `tools/`: the prose check, the tutorial recorder, the renderer that makes
  the site's pages from `docs/`, the benchmark, the version setter and the
  local site server.

Pushing a `v*` tag that matches `VERSION` publishes a release with three
tarballs, one each for the command, the kernel's debug info and the desktop
app.

## License

| Path                                       | License                                                                                            |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| `crates/rewind-app/`                       | Proprietary to Lunch Time Surf LLC, source available, see [its LICENSE](crates/rewind-app/LICENSE) |
| `crates/rewind-app/vendor/gpui-pre-linux/` | Apache-2.0, a patched copy of Zed's GPUI, see its LICENSE-APACHE                                   |
| `crates/rewind-app/vendor/text-input/`     | Apache-2.0, a text field adapted from GPUI's input example, see its LICENSE-APACHE                 |
| `crates/rewind-app/vendor/syntaxes/`       | Grammars for syntax highlighting, under MIT, the Unlicense and Sublime HQ's terms, see its README  |
| `guest/linux/`                             | GPL-2.0-only, as Linux is, see [guest/linux/LICENSE](guest/linux/LICENSE)                          |
| everything else                            | MIT, see [LICENSE](LICENSE)                                                                        |

The engine and the command are open source. The desktop app's source is here
to read, but copying, modifying or redistributing it needs permission.
