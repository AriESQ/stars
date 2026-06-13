# Nanvix Python

[![CI](https://github.com/nanvix/nanvix-python/actions/workflows/ci.yml/badge.svg)](https://github.com/nanvix/nanvix-python/actions/workflows/ci.yml)

CPython 3.12 distribution for the
[Nanvix](https://github.com/nanvix/nanvix) microkernel — a
self-contained Python runtime with pure Python pip packages.

## Quick Start (Pre-built Release)

Download the latest release artifact from
[Releases](https://github.com/nanvix/nanvix-python/releases) and
run Python under `nanvixd`:

### Linux

```bash
gh release download --repo nanvix/nanvix-python --pattern "*.tar.gz" --clobber
tar -xzf microvm-standalone-256mb.tar.gz
cd microvm-standalone-256mb
./bin/nanvixd.elf -ramfs nanvix_rootfs.img -mount ./mnt -- python3.initrd
```

On startup `nanvixd` mounts the host `mnt/` directory at `/mnt`
inside the guest, then CPython executes `/mnt/bootstrap.py` if
present. Otherwise it drops into an interactive REPL.

### Windows

```powershell
gh release download --repo nanvix/nanvix-python --pattern "*.zip" --clobber
Expand-Archive microvm-standalone-256mb.zip -DestinationPath .
cd microvm-standalone-256mb
.\bin\nanvixd.exe -ramfs nanvix_rootfs.img -mount .\mnt -- python3.initrd
```

#### Fast Start (warm restore via snapshot)

Snapshots let you skip the cold boot + Python initialization on
every run. They are only supported on Windows (via the Windows
Hypervisor Platform — WHP) and are **hardware-specific**, so they
cannot be shipped pre-built: each user must generate one locally
on the host that will restore from it. Cold boot takes ~2 s, so
generation is a one-time cost.

##### Generating a snapshot

From the bundle directory, cold-boot once with `-kernel-args
snapshot` and no `-mount`:

```powershell
mkdir snapshots -ErrorAction SilentlyContinue
.\bin\nanvixd.exe -bin-dir .\bin -ramfs nanvix_rootfs.img `
    -kernel-args snapshot -- python3.initrd
```

The VM exits cleanly after the kernel writes the snapshot. Confirm
success with:

```powershell
Get-ChildItem snapshots\kernel.vmem, snapshots\kernel.whp.cbor
```

##### Restoring from a snapshot

Once a snapshot exists, every subsequent run can warm-restore from
it:

```powershell
.\bin\nanvixd.exe -snapshot snapshots\kernel.whp.cbor `
    -ramfs nanvix_rootfs.img -mount .\mnt `
    -kernel-args snapshot -- python3.initrd
```

##### Regenerating a snapshot

A snapshot is tied to both the host hardware and the contents of
the ramfs image. Regenerate it whenever you:

- move the bundle to a different machine (or change CPU features);
- replace `nanvix_rootfs.img` or `python3.initrd`;
- upgrade to a new release.

Delete `snapshots\` and repeat the generation step above.

### Release Bundle Layout

```
microvm-standalone-256mb/
├── bin/
│   ├── kernel.elf            # Nanvix microkernel
│   └── nanvixd.exe (.elf)    # Host-side hypervisor
├── mnt/                      # Place your workload here
├── nanvix_rootfs.img         # RAMFS with CPython stdlib + packages
├── python3.initrd            # Multi-binary initrd (daemons + CPython)
└── README.md
```

On Windows, generating a snapshot (see *Fast Start* above) creates
a `snapshots/` directory in the bundle containing `kernel.vmem`
and `kernel.whp.cbor`.

### Workload Dispatch

Place your entry point in the `mnt/` directory. The guest warm-start
protocol looks for workloads in this order:

1. **`mnt/bootstrap.py`** — executed directly if present
2. **`mnt/argv.txt`** — one argument per line; supports `-m module`
   syntax or a path to a script inside `/mnt`
3. **Neither** — drops into an interactive Python REPL

Example `bootstrap.py`:

```python
import json
print(json.dumps({"hello": "nanvix"}))
```

### Using Built-in Packages

All pure Python packages are pre-installed. No `pip install` is needed:

```bash
# Place your script in the mnt/ directory
echo 'import json; print(json.dumps({"hello": "nanvix"}))' > mnt/bootstrap.py
./bin/nanvixd.elf -ramfs nanvix_rootfs.img -mount ./mnt -- python3.initrd
```

## Building from Source

All interaction is through the `./z` wrapper script which
auto-bootstraps [nanvix-zutil](https://github.com/nanvix/zutils).

### Prerequisites

- **Python 3.12+** on the host
- **Docker** (for cross-compilation and `.pyc` pre-compilation)
- **KVM** (`/dev/kvm`) on Linux for running Nanvix guests

### Build, Test, and Release

```bash
git clone https://github.com/nanvix/nanvix-python.git
cd nanvix-python

./z setup      # Download Nanvix sysroot and pre-built CPython
./z build      # Install pip packages and generate ramfs image
./z test       # Run smoke test and functional tests
./z release    # Package standalone runtime bundle into dist/
```

On Windows, `./z test` additionally runs a snapshot smoke test
(`test-snapshot`) that cold-boots once to produce a WHP snapshot,
then warm-restores from it to run a hello-world workload. Select
individual targets with:

```bash
./z test -- test-smoke
./z test -- test-snapshot      # Windows + standalone only
./z test -- test-integration
```

On Windows, use the PowerShell wrapper (`.\z.ps1`) or the
cross-platform entry point (`.\z`):

```powershell
.\z setup
.\z build
.\z test
.\z release    # Produces dist\microvm-standalone-256mb.zip
```

### Environment Variables

| Variable                 | Default       | Description                           |
| ------------------------ | ------------- | ------------------------------------- |
| `NANVIX_MACHINE`         | `microvm`     | Target platform                       |
| `NANVIX_DEPLOYMENT_MODE` | `standalone`  | Deployment mode                       |
| `NANVIX_MEMORY_SIZE`     | `256mb`       | Memory configuration                  |
| `TIMEOUT_SECONDS`        | `300`         | Per-test timeout in seconds           |
| `TEST_START` / `TEST_END`| `1` / `999`   | Functional test range (inclusive)     |

## What's Included

- **CPython 3.12.3** — fully functional interpreter
- **Pure Python pip packages** — attrs, requests, flask, jinja2,
  beautifulsoup4, rich, click, and many more (see [packages](doc/packages.md))

## Supported Platform

| Platform   | Mode         | Memory |
| ---------- | ------------ | ------ |
| `microvm`  | `standalone` | 256 MB |

Tested on both Linux (KVM) and Windows in CI.

## Documentation

| Document                                | Description                            |
| --------------------------------------- | -------------------------------------- |
| [Building from Source](doc/building.md) | Full build prerequisites and walkthrough |
| [Supported Packages](doc/packages.md)   | Complete list of pip packages          |
| [Testing](doc/testing.md)               | Smoke and functional test details      |
| [CI / CD](doc/ci.md)                    | GitHub Actions pipeline                |
| [Contributing](doc/contributing.md)     | How to add packages or fixes           |

## Usage Statement

This project is a prototype. As such, we provide no guarantees that it
will work and you are assuming any risks with using the code. We welcome
comments and feedback. Please send any questions or comments to any of
the following maintainers of the project:

- [Pedro Henrique Penna](https://github.com/ppenna) -
  [ppenna@microsoft.com](mailto:ppenna@microsoft.com)

> By sending feedback, you are consenting that it may be used
> in the further development of this project.

## License

This project is distributed under the [MIT License](LICENSE.txt).
