# PolicyWitness

>Read the [user guide](PolicyWitness.md) for more detail.

PolicyWitness is a macOS harness for observing differences between `sandbox_check`'s userland sandbox-prediction API and the kernel's actual enforcement. It does so by evaluating SBPL policy applied to a sandboxed worker plus a probe plan, exercising both the prediction and the kernel. Each run produces one JSON envelope describing both channels per probe step, with the policy bytes, the runner's entitlements, and unified-log deny evidence attached.

Measuring `sandbox_check`'s prediction about a process against policy enforcement requires managing process lifecycles. `sandbox_check` answers for an existing PID, and sandbox application is one-way — a process gets exactly one sandbox. Evaluating a policy therefore means a fresh process per evaluation: compile and apply the policy to it once, aim both the prediction and the attempted operation at that PID while it lives, and carry the answer out through a channel the policy under test cannot sever.

## Flow

>Specimens -> Runs -> Steps -> Evidence

PolicyWitness operates on specimens: an SBPL policy plus a probe plan. The controller launches a fresh runner per specimen. The runner is an unsandboxed XPC host plus two short-lived children: `pw-probe-runner`, a sandboxed C worker that applies the specimen policy to itself and runs the probe plan and `sb_api_validator --batch` which queries `sandbox_check` for each probe against the worker's sandboxed PID. The host stays unsandboxed so the XPC reply path survives even under a strict `(deny default)` profile, joins both children's outputs into one JSON envelope, and replies.

Each step records two parallel verdicts plus the cross-channel comparison:

- **Attempt** (`steps[].attempt`): in-band kernel response — `rc`, `errno`, mach `kr` — from actually performing the operation inside the sandboxed worker.
- **Prediction** (`steps[].sandbox_check`): the userland `sandbox_check` verdict for the same operation + filter against the same PID, supplied by the validator.
- **Drift** (`steps[].drift`): the validator-vs-attempt comparison. `true` when they disagree about allow/deny with strong-evidence backing; `false` when they agree; `null` when no comparison is possible (validator skipped, attempt didn't produce a verdict, DAC/sandbox ambiguity, etc.).

Unified-log evidence for kernel denies is attached out-of-band (best-effort).

## Entitlements + SBPL

macOS sandboxing isn't just SBPL: a process's effective sandbox is its SBPL profile applied on top of the entitlements its binary was codesigned with. The same SBPL can yield different kernel behavior depending on which entitlements are granted, so a specimen has to describe both halves to be a faithful witness.

By default SBPL is applied to a process holding no entitlements. To observe a different combination, copy the bundled XPC service, sign it with your own entitlements plist (Developer ID or ad-hoc), and install it via `policy-witness runner install --kind byoxpc`. Specimens then select it via `runner.id` or `runner.service`. See the user guide ([PolicyWitness.md](PolicyWitness.md)) for the install recipe.

## What ships

This repo builds a single distributable app bundle:

- `dist/PolicyWitness.app`
  - `Contents/MacOS/policy-witness` (Rust controller)
  - `Contents/MacOS/pw-runner-client` (Swift NSXPCConnection wrapper)
  - `Contents/MacOS/sandbox-log-observer` (Rust unified-log capture helper)
  - `Contents/MacOS/sbpl-preflight` (SBPL compile/preflight helper)
  - `Contents/MacOS/sb_api_validator` (diagnostic copy of the validator CLI)
  - `Contents/XPCServices/PWRunner.xpc` (Swift XPC host; one host + two short-lived children per specimen)
    - `Contents/MacOS/pw-probe-runner` (bundle-local C worker that applies the policy and runs probe attempts)
    - `Contents/MacOS/sb_api_validator` (bundle-local validator launched once per run for sandbox_check verdicts)
  - `Contents/Resources/Evidence/*` (generated manifests: hashes/entitlements, `symbols.json`)

Build the app bundle with `./build.sh` (sign with `IDENTITY=...`; see [SIGNING.md](SIGNING.md)).

## Documentation

- Using the app:
  - User guide: [PolicyWitness.md](PolicyWitness.md)
  - FAQ: [QUESTIONS.md](QUESTIONS.md)
  - Signing/distribution: [SIGNING.md](SIGNING.md)
- Implementation details:
  - CLI contract and controller behavior: [controller/README.md](controller/README.md)
  - Runner service architecture: [runner/README.md](runner/README.md)
- Contributing:
  - Repo orientation: [AGENTS.md](AGENTS.md)
  - Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
  - Testing: [tests/README.md](tests/README.md)
