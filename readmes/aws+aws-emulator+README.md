# AWS Emulator README

AWS Emulator is a local emulator of the AWS APIs. You use it to test your software without calling AWS, on your own machine, on a development server, or in continuous integration (CI). You don’t need an AWS account. Your requests go to the emulator, not to AWS. So you work with emulated resources instead of AWS resources. AWS Emulator has no additional service fee. You pay only for AWS resources when you deploy on AWS.

The emulator is a local program that serves an AWS API endpoint. It has no graphical interface. After you start the emulator, you set environment variables to point the AWS CLI or an AWS SDK at its endpoint. Then you run your code as usual. In embedded mode, you pass the emulator’s HTTP client to your SDK instead.

AWS Emulator is for building and testing. Don’t use it for production workloads or to test security. See [Security in AWS Emulator](https://docs.aws.amazon.com/emulator/latest/userguide/security.html).

**Documentation:** [AWS Emulator User Guide](https://docs.aws.amazon.com/emulator/latest/userguide/what-is-service.html)

## Quick start

### With an AI coding agent

Install the `aws-emulator` skill, then ask your agent to set up the emulator. This needs the AWS CLI version 2.35.0 or later. See [Getting started with an AI coding agent](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-agent.html).

```bash
aws agent-toolkit add-skill --skill-name aws-emulator --region us-east-1
```

### Server mode (CLI and any SDK)

- **Linux:** install the RPM or Debian package and run `aws-emulator`. See [Getting started on Linux](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-linux.html).
- **Windows / macOS:** run the emulator in a container built from a short Dockerfile. See [Getting started with Docker](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html).

Point your SDK at a running emulator by setting environment variables. See [Pointing your AWS SDK at AWS Emulator](https://docs.aws.amazon.com/emulator/latest/userguide/point-sdk-to-emulator.html).

### Embedded mode (Rust tests)

Add the emulator as a dev-dependency and run it in-process, one isolated instance per test. There is no endpoint URL, certificate, or environment variable to set. Your test wires the emulator's HTTP client straight into the SDK client. See [Getting started with embedded mode](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-embedded.html), and [Building from source](#building-from-source) below for its build cost.

## Known issues

To see how closely each service matches AWS, check the fidelity scores published with each release on the [releases page](https://github.com/aws/aws-emulator/releases). To check whether your own project is expected to work, see [Checking whether your project works with AWS Emulator](https://docs.aws.amazon.com/emulator/latest/userguide/check-project.html).

Individual gaps are tracked in the repository's `issues/` directory. APIs and behaviors that don't work yet are under `issues/things-that-do-not-work/`, and ones that have since been fixed move to `issues/things-that-now-work/`.

## Building from source

You need this if you are modifying the emulator, running it from a checkout, or using embedded mode. Embedded mode compiles the emulator into your test binary, so the prerequisites and build-cost guidance below apply to it too. Most other users install a prebuilt package instead (see [Quick start](#quick-start)). Building from source is supported on **Linux (x86_64 and aarch64)**; on Windows and macOS, use the Docker path above.

### Prerequisites

- A Rust toolchain with Cargo (install via [rustup](https://rustup.rs)).
- A C compiler, such as GCC or clang. Some dependencies build C code.
- At least 100 GB of free disk for `target/`. The workspace has one crate per AWS service, so a debug build of everything is large, and it grows as services are added.
- A multi-core machine. A cold full build compiles every service crate, so the first build takes a while; fewer cores take proportionally longer. After that, rebuilding after a change to one service is much faster.

### Build and run

```bash
cargo build -p aws-emulator-router
cargo run   -p aws-emulator-router
```

The emulator serves HTTPS on `127.0.0.1:9297` (self-signed certificate).

### Embedded mode build cost

Embedded mode compiles the emulator into your test binary, so your project's first `cargo test` builds the emulator's service crates alongside your own code. Budget a first build and `target/` on the same order as building from source above, then fast incremental builds. Recommendation: reuse one `CARGO_TARGET_DIR` across projects, cache `target/` (or use sccache) in CI, and pin the emulator to a release commit so it isn't rebuilt on every change.

## Repository layout

```
.
├── Cargo.toml              # workspace: one member per service, plus the core crates
├── services/
│   └── service-<name>/     # ONE CRATE PER SERVICE
│       ├── smithy-model/   # <name>.json — the Smithy model that drives the wire protocol
│       ├── build.rs        # generates the service declaration from the model
│       ├── src/
│       │   ├── service.rs  # request routing and refusal overrides
│       │   ├── state.rs    # this service's in-memory state
│       │   └── ops/        # one file per operation
│       └── tests/
├── core/
│   ├── router/             # the emulator binary: mounts every service on one endpoint
│   └── embedded/           # the in-process (embedded mode) facade
├── vendor/                 # framework crates — do not edit (replaced on update)
└── issues/                 # tracked fidelity issues
```

## Telemetry

AWS Emulator is configured to collect and report usage data to AWS, to gain insight into how AWS Emulator is used. Telemetry is on by default. AWS Emulator collects telemetry data with strict data minimization in mind, preventing identification or attribution to specific users, accounts, or organizations. Its records never include what’s in your requests or responses, your code, your credentials, or personal data. We don’t share telemetry with third parties.

For details on what is collected and how the data is handled, see [Telemetry in AWS Emulator](https://docs.aws.amazon.com/emulator/latest/userguide/telemetry.html). To turn telemetry off, use one of the following options.

### Use a command-line option

Start the emulator with the `--telemetry` option (short form `-t`) set to `off`. This setting applies only to that emulator process.

```bash
aws-emulator --telemetry off
```

In a container, add `--telemetry off` after the image name in the `docker run` command.

### Use an environment variable

Set `EMULATOR_TELEMETRY` to `off` before you start the emulator. This setting applies to every emulator that you start from that shell.

`EMULATOR_TELEMETRY` accepts `on`, `true`, or `1` to turn telemetry on, and `off`, `false`, or `0` to turn it off. Values aren’t case sensitive. Any other value turns telemetry off, and the startup notice shows a warning.

```bash
export EMULATOR_TELEMETRY=off
aws-emulator
```

### Use a configuration file

To turn telemetry off for every run on a machine, add these lines to the emulator settings file, `config.toml`. The file is `~/.aws/emulator/config.toml` on Linux and macOS, and `%USERPROFILE%\.aws\emulator\config.toml` on Windows. To use a different file, set the `EMULATOR_CONFIG` environment variable to its path.

```toml
[telemetry]
enabled = false
```

### Use the embedded configuration API

In embedded mode, turn off telemetry in the options that you pass when you create the emulator.

```rust
use aws_emulator_embedded::{AwsEmulatorEmbedded, EmbeddedOptions, Telemetry};

fn main() {
    let emulator = AwsEmulatorEmbedded::new(EmbeddedOptions::default().telemetry(Telemetry::Off));
    let _http_client = emulator.http_client();
}
```

You might build a tool that includes the emulator, such as a test framework that other people run. If you do, tell your users about telemetry and give them a way to turn it off. You can also ship your tool with telemetry off.

## Reporting issues and contributing

Report bugs and fidelity gaps in [GitHub Issues](https://github.com/aws/aws-emulator/issues). The most useful report names the service, the operation, your SDK and version, the request you sent, and how the response differed from real AWS. This repository does not take PRs.

## License

This software is licensed under the CC0 1.0 Universal (CC0-1.0) License, except the code in the `vendor/` directory, which is under the Apache License 2.0. See [LICENSE](LICENSE) for details, and [vendor/README.md](vendor/README.md) for the license of the code in `vendor/`.
