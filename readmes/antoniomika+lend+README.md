# lend

Give a remote shell or coding agent access to selected commands and SSH keys on your laptop, with local approval. Tools such as `gh` and `op` can stay on the laptop. Remote command execution and MCP use `lend`. SSH tools use the forwarded agent socket directly.

lend wraps your existing SSH agent. One local config controls command execution, key visibility, SSH signing, and agent management. The proxy checks each request before invoking a local command or asking the upstream agent to act. The upstream agent keeps the private keys and can require its own approval after lend approves. A remote agent can explain why it needs command access through the CLI or an MCP tool.

```text
Remote: lend exec -- command args
                  |
          forwarded SSH agent socket
                  |
Laptop: lend agent -> policy + local approval -> local command
                                           -> original SSH agent (signing)
```

The docs site lives in [docs](docs/README.md), with a [getting started guide](docs/posts/getting-started.md), [CLI reference](docs/posts/cli.md), and guides for policies, approval, and MCP. Run `make docs-serve` to browse it at `http://127.0.0.1:3000`.

## Install

Homebrew on macOS or Linux:

```sh
brew install antoniomika/tap/lend
```

Install the latest binary into `~/.local/bin`:

```sh
curl -fsSL https://github.com/antoniomika/lend/releases/latest/download/install.sh | sh
```

Choose a version and installation directory:

```sh
curl -fsSL https://github.com/antoniomika/lend/releases/latest/download/install.sh \
  | sh -s -- --version vX.Y.Z --dir "$HOME/.local/bin"
```

The installer selects macOS or Linux and amd64 or arm64, verifies the archive's SHA256 checksum, and replaces the binary only after verification. It requires curl, tar, and either `sha256sum` or `shasum`. It uses no sudo and does not edit shell configuration. Add `~/.local/bin` to your `PATH` if needed. Run the same installer to upgrade, or use `brew upgrade antoniomika/tap/lend` for a Homebrew installation.

Release archives and `checksums.txt` are also available on the GitHub release page for manual installation. macOS release binaries include native approval and require macOS 13 or later. Linux binaries have no Go runtime dependency. Install the binary on both the laptop and remote hosts, then check it:

```sh
lend version
lend doctor --remote
```

Use `doctor --remote` on a remote host after forwarding the laptop's lend proxy. Use the local checks below on the laptop.

## Build from source

Requires Go 1.24 or later. There are no Go module dependencies.

```sh
go build -buildvcs=false -o bin/lend ./cmd/lend
```

Build on macOS with cgo enabled and the Xcode Command Line Tools installed to include native approval:

```sh
CGO_ENABLED=1 go build -buildvcs=false -o bin/lend ./cmd/lend
```

Build the same program on the remote host, or cross-compile a Linux client:

```sh
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -buildvcs=false -o bin/lend-linux-amd64 ./cmd/lend
```

Use `GOARCH=arm64` for an ARM Linux host. Put the corresponding binary on each machine's `PATH`.

`make build` builds the local binary. Go is needed only to build from source. Python 3 is used by the maintainer's packaging and installer tests.

## Doctor

On the laptop:

```sh
lend doctor --config ./policy.json
lend doctor --config ./profiles.json --profile development
lend doctor --config ./policy.json --approval terminal --json
```

Doctor checks policy parsing, configured executables, the local working directory, upstream socket access, available upstream identities, proxy extension support, socket permissions, the local approval backend, required device authentication or biometrics, and history paths. If the policy enables leases, it also checks desktop lock tracking. `--upstream PATH`, `--socket PATH`, and `--dir PATH` select the locations to inspect. `--timeout` bounds each socket or desktop probe.

On a remote host:

```sh
lend doctor --remote
```

Remote mode reads `SSH_AUTH_SOCK`, or an explicit `--socket PATH`, and checks that the forwarded agent advertises the lend execution extension. It skips laptop policy and desktop checks, so it works on a headless VM without local credentials or a desktop session.

Doctor does not execute configured tools, fetch credential values, request signatures, open lend approval dialogs, create directories, or change agent state. Backend detection cannot prove that a future approval will succeed. Config checks use the file on disk; a running daemon keeps its loaded policy until restarted. Text and JSON reports use `ok`, `warn`, and `error`. Exit status is 0 with no errors, 1 when a check fails, and 2 for invalid command-line arguments. A stopped local proxy is a warning so you can check setup before starting it.

## Command policy

Start the laptop agent with either `--config FILE` or `--allow-all`. A config defaults to denying unlisted commands, SSH keys, and management operations. `--allow-all` permits any executable, SSH key, and supported management operation while keeping approval for each request.

[examples/policy.json](examples/policy.json) allows `op read` with biometric approval and `gh pr view` with a confirmation prompt. It includes rules for SSH authentication, Git signing, adding or removing the selected key, and locking or unlocking the agent. Copy it to a local policy file, set the executable paths for your laptop, and replace the key fingerprint. Inspect executable paths with `command -v op` and `command -v gh`, and list fingerprints with `lend keys` while `SSH_AUTH_SOCK` points at the original agent.

```json
{
  "default": "deny",
  "require_reason": true,
  "commands": [
    {
      "executable": "/opt/homebrew/bin/op",
      "args_prefix": ["read"],
      "approval": "biometric"
    },
    {
      "executable": "/opt/homebrew/bin/gh",
      "args_prefix": ["pr", "view"],
      "approval": "prompt"
    }
  ],
  "ssh": {
    "default": "deny",
    "keys": [
      {
        "fingerprint": "SHA256:REPLACE_WITH_FINGERPRINT_FROM_LEND_KEYS",
        "label": "SSH login and Git signing",
        "approval": "biometric",
        "purposes": ["ssh", "sshsig"],
        "namespaces": ["git"],
        "max_signatures": 10
      }
    ]
  }
}
```

Executable paths are absolute and resolved through symlinks when loading the policy and when receiving a request. A matched rule runs the program with its configured path as `argv[0]`, so a multi-call binary behaves as the alias you allowed. Prefixes match complete arguments: `["pr", "view"]` allows further arguments after those two. The longest matching prefix determines approval. An omitted prefix permits every argument to that executable. Duplicate rules and unknown config fields are rejected. Policy changes take effect after restarting the agent.

| Approval | Requirement |
| --- | --- |
| auto | Platform default: macOS device authentication or a Linux prompt |
| prompt | Explicit local confirmation |
| authenticate | macOS device owner authentication, which can use a password |
| biometric | macOS biometric authentication with no password fallback |
| none | No approval. The request runs as soon as policy admits it |

`authenticate` and `biometric` requests fail on Linux, in macOS builds without cgo, and when using `--approval=terminal`. A biometric request also fails when biometry is unavailable, unenrolled, or locked out. The remote caller cannot select a weaker approval requirement. Every command needs local approval or an explicitly approved lease for its scope, unless its rule sets `none`.

`none` works anywhere an approval is set: command rules, `default_approval`, SSH keys, and management. Anyone who can reach the forwarded socket can then make matching requests without a prompt, which is the same trust as forwarding your upstream agent directly. Those requests still appear in activity and history with the decision `policy`, and `lend doctor` warns about each rule and default that uses `none`. A rule with `none` cannot also set a `lease`.

Set `"default": "allow"` and `"default_approval": "biometric"` to permit every command with biometric approval. `require_reason` requires a nonempty requester-supplied reason for both CLI and MCP calls. Reasons are displayed as untrusted text and do not establish identity or change policy.

Argument prefixes control which command requests are admitted. They do not restrict the capabilities of an approved executable. Further arguments, configuration files, plugins, and stdin can affect what it does. Every admitted request still receives its required approval.

## SSH key policy

The `ssh` section uses the same approval modes as command rules. Its default is `deny`, independently of the command policy's default. A missing `ssh` section exposes no keys and refuses all signatures. Each allowed signature needs fresh lend approval or a valid local lease. Upstream approval caching does not satisfy lend approval.

Before starting the proxy, inspect the original agent:

```sh
lend keys --socket "$SSH_AUTH_SOCK"
```

Each line shows a fingerprint, key type, and escaped upstream comment. Copy the fingerprint into a key rule. Key selection uses the fingerprint of the exact public key blob supplied by the agent. Comments are not used for authorization. Plain key fingerprints match OpenSSH SHA256 fingerprints. Certificate blobs have their own fingerprints and require separate rules, so use `lend keys` for certificates too.

| Key field | Meaning |
| --- | --- |
| fingerprint | Exact SHA256 fingerprint to expose and authorize |
| label | Local name displayed during approval |
| approval | Required local approval mode |
| purposes | Allowed signing formats, defaults to SSH authentication |
| namespaces | Allowed SSHSIG namespaces, defaults to all |
| max_signatures | Successful signatures allowed per daemon run, zero means unlimited |
| lease | Optional duration and use limit offered during local approval |

Purposes are `ssh` for a structurally valid SSH user authentication payload, `sshsig` for an SSHSIG signing payload, and `raw` for other data. An SSH authentication payload must contain the same key as the signing request. A Git-only signing key can use `"purposes": ["sshsig"]` and `"namespaces": ["git"]`. A namespace restriction requires the `sshsig` purpose and applies to those signatures. The namespace alone does not restrict other explicitly enabled purposes.

The signature cap is shared across connections and reserves capacity while approval is pending. Local denials and upstream signing failures release the reservation. A valid signature returned by the upstream agent consumes one use, even if the remote client disconnects before receiving it. Restarting lend resets the counters. These counters are held in memory.

Unlisted keys are removed from identity listings, and direct signing requests for their blobs are refused. Management operations require their own permissions described below. Legacy agent operations and unknown extensions are refused. OpenSSH session binding messages continue on the same upstream connection as listing, signing, and management requests, preserving its existing restrictions.

To allow every upstream key with biometric approval, use `"ssh": {"default": "allow", "default_approval": "biometric"}`. Explicit key rules still apply to matching fingerprints. Key policies govern requests made through this proxy. They do not change the original agent's socket or the restrictions it enforces.

## Agent management

The `ssh.management` section controls changes to the original agent. It defaults to `deny` independently of command and signing defaults. Each permitted operation requires the same local approval modes used for commands and signatures.

```json
{
  "ssh": {
    "management": {
      "default": "deny",
      "operations": [
        {"operation": "add-key", "approval": "biometric"},
        {"operation": "remove-key", "approval": "biometric"},
        {"operation": "remove-all-keys", "approval": "biometric"},
        {"operation": "lock", "approval": "prompt"},
        {"operation": "unlock", "approval": "biometric"},
        {
          "operation": "add-provider",
          "approval": "biometric",
          "providers": ["/example/provider.so"]
        },
        {
          "operation": "remove-provider",
          "approval": "biometric",
          "providers": ["/example/provider.so"]
        }
      ]
    }
  }
}
```

Add this section to your local policy and use provider identifiers appropriate for your upstream agent. `providers` matches exact identifiers; it does not expand globs or resolve filesystem aliases. For OpenSSH these identifiers usually name provider libraries. Provider loading can load local code and expose multiple keys.

| Operation | Effect on the upstream agent |
| --- | --- |
| add-key | Add a key or replace its existing constraints |
| remove-key | Remove the selected key |
| remove-all-keys | Remove every key, including keys hidden by lend |
| lock | Lock the shared agent with a requester-supplied passphrase |
| unlock | Unlock the shared agent with a requester-supplied passphrase |
| add-provider | Load a provider or token's keys |
| remove-provider | Remove keys associated with a provider or token |

`add-key` and `remove-key` rules can include a `fingerprints` array to select exact keys. The example policy demonstrates this. An omitted array permits any target for that operation, subject to approval. Fingerprint selectors are rejected on operations such as `remove-all-keys` because those operations affect the entire agent. Add-key rules can also restrict requested security-key provider identifiers with `providers`. Provider selectors apply when a request explicitly specifies a provider; plain key imports remain eligible for the rule.

One rule is allowed per operation. A rule that rejects a fingerprint or provider does not fall back to the management default. To allow all supported management operations with biometric approval, set `"management": {"default": "allow", "default_approval": "biometric"}` inside `ssh`. The `--allow-all` flag also enables management with platform-default approval.

Management prompts show the operation, target key fingerprint or provider identifier, requested lifetime, confirmation requirement, and recognized constraint extension names. Private keys, passphrases, PINs, and security-key handles are omitted from the approval context. Processed management packet buffers are cleared after forwarding or refusal. Caller and connection context appear when available.

Management permissions are separate from key-use permissions. Adding a key does not admit it for listing or signing through lend; its `ssh.keys` rule or signing default still applies. Removing and re-adding a key does not reset lend's signature counters. Changes affect the actual upstream agent and its other local or forwarded users.

Key loading supports RSA, Ed25519, the NIST P-256/P-384/P-521 ECDSA curves, DSA, OpenSSH security-key formats, and their certificate variants. Software private keys are checked against their public components before selecting a fingerprint. Security-key handles remain opaque and are passed to the upstream agent. RSA integers are limited to 16384 bits, DSA moduli to 3072 bits, and DSA subgroup orders to 256 bits. Unsupported encodings and unknown constraint extensions are refused before approval. Supported constraints include lifetime, confirmation, `sk-provider@openssh.com`, `restrict-destination-v00@openssh.com`, and provider-associated certificates. Destination constraint contents and certificate signatures are validated by the upstream agent. Requests are forwarded unchanged after local approval.

The upstream agent remains responsible for supporting or rejecting management operations. Its own restrictions can refuse an approved request, including remote provider-loading restrictions. Use standard tools such as `ssh-add` through the proxy:

```sh
SSH_AUTH_SOCK="$HOME/.lend/agent.sock" ssh-add -t 1h /local/key
SSH_AUTH_SOCK="$HOME/.lend/agent.sock" ssh-add -d /local/key.pub
SSH_AUTH_SOCK="$HOME/.lend/agent.sock" ssh-add -x
```

## Use

Start a session with a dedicated proxy and policy profile:

```sh
lend ssh --config ./profiles.json --profile development -- agent-vm
```

For a manually managed proxy, keep this agent running in a local terminal. Its upstream defaults to the current `SSH_AUTH_SOCK`, which can point to OpenSSH, 1Password, or another compatible agent.

```sh
lend agent --config ./policy.json --socket "$HOME/.lend/agent.sock"
```

From another laptop terminal, forward the proxy socket:

```sh
SSH_AUTH_SOCK="$HOME/.lend/agent.sock" ssh -A remote-host
```

Agent-based authentication for this connection also goes through the proxy. Its login key needs permission in the `ssh` policy.

On the remote host:

```sh
lend exec --reason "Inspect the pull request before reviewing it" -- \
  gh pr view 123 --repo example/project

lend exec --reason "Fetch the credential needed by this task" -- \
  op read op://vault/item/field
```

Commands run with the laptop user's privileges, environment, and `PATH`, with `SSH_AUTH_SOCK` set to lend's socket so their SSH operations also use its key policy. Their working directory defaults to the laptop user's home directory and can be set with `lend agent --dir /local/directory`. Relative executable paths containing `/` resolve against that directory. Arguments pass directly to the executable. To use shell syntax, explicitly request a shell allowed by your policy.

With a laptop policy allowing those requests, `gh` performs the operation using its local authentication. `op read` sends the requested secret back to the remote caller. Keep the tools and their desktop integrations configured on the laptop. The VM can make requests while your SSH session exposes the forwarded socket.

For unrestricted command, key, and supported management selection with approval, start `lend agent --allow-all --socket "$HOME/.lend/agent.sock"`. You can then run examples such as `lend exec -- hostname` or, with a Mac laptop, `printf 'clipboard content' | lend exec -- pbcopy`.

The remote process receives streamed stdout and stderr and the command's exit code. A command terminated by a signal returns `128 + signal`. Approval, transport, and startup failures return 125.

## Profiles and SSH sessions

The top-level `profiles` object contains independent policies. Selecting `--profile development` uses that policy in full, including commands, keys, management, credential reader, and history settings. Profiles inherit no permissions from the root policy and cannot contain other profiles. `lend agent --config FILE --profile NAME` also selects a profile.

[examples/profiles.json](examples/profiles.json) provides development and cluster profiles. Replace executable paths, fingerprints, the history path, and credential references for your laptop. On Linux, use `prompt` approval in place of the example's macOS biometric requirement.

`lend ssh` starts a separate local daemon and a private socket for each connection. The wrapper labels prompts with the locally selected profile and SSH target. SSH uses that proxy for authentication and forwarding. The wrapper disables connection sharing, persistence, and backgrounding so its lifetime follows the SSH process. Ports, users, jump hosts, and other SSH settings come from `~/.ssh/config`. Optional arguments after the host become the remote command.

```sh
lend ssh --config ./profiles.json --profile development -- agent-vm
lend ssh --config ./profiles.json --profile cluster -- rack
```

Each session prints its local socket path. Closing SSH stops its daemon, cancels pending and running requests, and discards its leases and signature counters. A parent lifetime pipe also stops the daemon if the wrapper exits unexpectedly. The local session label describes the connection selected on the laptop. It does not establish the identity of a remote process or prevent socket relaying on the remote machine.

## Approval leases

Add `lease` to a command rule or SSH key rule to offer an optional grant:

```json
"lease": {"duration": "5m", "uses": 3}
```

The prompt offers Allow once and Allow lease. Terminal approval accepts separate request-specific `allow` and `lease` phrases. The lease choice requires the rule's configured authentication. Allow once leaves caching disabled for that approval.

Leases are offered only inside supervised `lend ssh` sessions with available desktop lock tracking. Standalone agents and unavailable lock tracking fall back to individual approvals. A lease lasts until its duration or use limit is reached, the session ends, lend observes a device lock or loses lock tracking, or you revoke it. Configurations allow up to one hour and 100 uses. The initial approved request counts as one use. Attempts consume lease uses even if execution or upstream signing later fails.

Command leases match the resolved executable, exact argv, local working directory, credential references, and approval requirement. Stdin can vary between uses. Signing leases match the key, purpose, namespace, signature flags, and approval requirement. Local socket peer details and accepted binding hints further restrict reuse. Caller-supplied metadata never grants access. Signing leases do not establish a destination identity. Signature quotas and upstream restrictions apply to every use. Management operations never use leases. They require fresh approval unless their rule sets `none`, and they clear existing leases when the upstream operation succeeds.

On Linux, lock tracking checks the active X11 or Wayland session's logind `LockedHint` through `loginctl`. It polls once per second and checks again before using a grant. A lock and unlock entirely between polls can be missed. On macOS, the cgo build checks console state and screen lock notifications. macOS builds without cgo cannot offer leases. Use individual approvals when your desktop cannot report its lock state reliably.

## Local credentials

Command rules can inject secrets from a local reader into the approved process. `secret_reader` is the absolute path to a program that prints a secret, and `secret_reader_args` are the arguments placed before the reference. For each variable, lend runs the reader with those arguments followed by the configured reference, and uses its stdout as the value. Without `secret_reader_args`, the reference is the only argument.

For 1Password, run [`op read --no-newline`](https://developer.1password.com/docs/cli/reference/commands/read/):

```json
{
  "secret_reader": "/opt/homebrew/bin/op",
  "secret_reader_args": ["read", "--no-newline"],
  "commands": [
    {
      "executable": "/opt/homebrew/bin/gh",
      "args_prefix": ["pr", "view"],
      "approval": "biometric",
      "secrets": {"GH_TOKEN": "op://Development/github/token"}
    }
  ]
}
```

Other readers work the same way when they take the secret's name last, such as `pass show`, `gopass show -o`, or `security find-generic-password -w -s` on macOS. lend keeps the reader's output exactly, including a trailing newline, so use a no-newline option where the reader has one.

lend reads credentials after the request is admitted and approved, and passes the values through the command environment. The remote request cannot choose environment variables or secret references. The prompt shows variable names and references; values remain hidden. Credential reads use the same command timeout and proxy socket. Failures refuse execution without returning the reader's output. Values are fetched again for each command, including leased requests, with a 64 KiB limit per value and 32 variables per rule.

The command can use the credential to perform an operation and return its result. Its output still goes to the requester, so an executable or arguments that print the environment can disclose injected values. Select arguments and executables accordingly. Credential values are never added to approval summaries or history. Existing explicit `op read` command grants still return their output to the requester.

The longest matching command prefix selects the whole rule, including its credentials and lease. Rules do not combine their settings.

## Activity and revocation

Inspect local sessions and requests:

```sh
lend status --all --watch
lend status --all --json
lend pause --all
lend resume --all
```

The live terminal view shows socket connections, queued and active requests, caller context when available, running commands, leases, lock tracking availability, and used or reserved signature quota. `--json` includes the full active approval summaries. Active summaries can contain sensitive command arguments. Completed history has separate logging settings.

Pause cancels active and queued work, clears leases, and refuses new connections until resume. `--all` visits the default agent and supervised sessions under lend's runtime directory. Use `--socket PATH` for an individual session or a custom agent location. Newly started daemons begin unpaused.

```sh
lend pause --socket /path/printed/by/lend/agent.sock
lend revoke --socket /path/printed/by/lend/agent.sock REQUEST_ID
lend clear-leases --socket /path/printed/by/lend/agent.sock
lend clear-leases --socket /path/printed/by/lend/agent.sock LEASE_ID
```

Revoking a request cancels that request and clears the daemon's leases. Revoking a socket connection also cancels its current request. A remote process can open another channel while its session remains enabled; pause that session to refuse further requests. Revocation cannot undo an operation already completed by an upstream agent or command.

Controls use a separate private Unix socket beside the proxy. The agent forwarding protocol does not expose these operations. Local control commands use the local default socket or an explicit path and never select the remote `SSH_AUTH_SOCK` automatically.

## Policy explanations and history

Check a local rule without running the command, fetching credentials, or opening an approval prompt:

```sh
lend explain --config ./profiles.json --profile development \
  --reason "Inspect the pull request" -- gh pr view 123 --repo example/project
lend explain --config ./profiles.json --profile development \
  --key SHA256:KEY_FINGERPRINT --purpose sshsig --namespace git
lend explain --config ./profiles.json --profile development --operation lock
```

The JSON result reports admission, the resolved executable and matching argument prefix for commands, approval requirement, lease configuration, and credential variable names. It evaluates the config on disk. It does not inspect live quotas, lease availability, or the upstream agent. A running agent keeps its loaded policy until restarted.

```sh
lend history --all
lend history --all --json
lend history --file /absolute/private/directory/history.jsonl
```

Each daemon keeps the latest 256 completed request records in memory. Records include local session and request IDs, executable or key fingerprint, operation, approval decision, completion state, duration, and command exit status. Caller text, reasons, stdin, stdout, stderr, credential references, and credential values are omitted.

Enable persistent JSON Lines history in a policy or profile:

```json
"history": {"path": "/absolute/private/directory/history.jsonl"}
```

The history directory must belong to the laptop user with mode `0700`; files use `0600`. The journal rotates at 8 MiB and retains one previous file. Shared writers coordinate through a local file lock. Each daemon reloads the latest records from the current file at startup and adds its own completions to its history view. `lend history --file PATH` reads completed records from the file after the session ends and can also inspect the rotated `.1` file. A history write failure appears in status. Persistent history is disabled by default.

Arguments are omitted by default. `"log_arguments": true` inside `history` opts into storing complete command arguments. Those arguments can contain secrets; lend does not infer which arguments are safe. This setting never enables output, environment, or stdin logging.

## Approval

| Platform | auto approval |
| --- | --- |
| macOS | Native request review, then Touch ID or another method accepted by macOS device owner authentication |
| Linux desktop with Zenity | Local Allow once / Deny dialog |
| Linux without Zenity | Prompt in the agent's controlling terminal |

Command prompts show the resolved executable, every argument, and the local directory. SSH signing prompts show the key fingerprint, local label, key type, signing format, namespace, payload size, SHA256 payload digest, and signature flags. Management prompts show the operation and its target. SSH requests do not carry a requester-supplied reason or a verified destination name.

CLI and MCP command requests automatically include caller context. The remote lend process reports its hostname, user and UID, working directory, executable path, PID, parent PID, parent executable when available, and `SSH_CONNECTION` when set. MCP requests also include the client name and version from initialization, the tool name, and the request ID. Working directory and process details describe the remote lend process, including the MCP bridge when using MCP.

An example of the caller portion of an MCP approval prompt:

```text
Caller (requester supplied, unverified):
  Interface: "mcp"
  Host: "agent-vm"
  User: "user"
  Working directory: "/work/project"
  MCP client: "example-agent"
  MCP client version: "1"
  Tool: "run_local_command"
  Request ID: "7"
  PID: 123
  Parent PID: 12
```

Caller context is informational and cannot change command or key authorization. A remote process can spoof these fields, including the MCP client name. lend escapes their contents and labels them as requester supplied. Older clients and ordinary SSH signing requests show caller details as unavailable when no metadata is present. Process context collection reads selected metadata; it does not collect parent command arguments or a complete environment.

The laptop also inspects its connected Unix socket peer. Linux provides a connection-time PID and UID; macOS provides a PID. The prompt labels those as local kernel-reported credentials and shows a best-effort local process lookup separately. With SSH forwarding, this identifies the laptop's SSH process. It does not identify the remote process. Failed or unsupported peer inspection leaves the details unavailable.

For both commands and SSH signatures, up to eight session-binding host-key fingerprints are shown when the upstream agent accepted those bindings on that connection. They are labeled as session hints unverified by lend. They do not establish a destination name or authorize the caller. Refused bindings are omitted, and metadata is scoped to its connection.

Desktop prompts let you scroll through long requests. The Linux dialog requires checking the approval box before Allow once is enabled. Control characters and non-ASCII text are escaped so request fields cannot insert terminal controls or change the prompt's layout. Terminal approval requires typing the displayed `allow` phrase with its request code. Each request gets a different code to prevent stale input from approving another request.

macOS authentication uses a fresh `LAContext` for each request. Cancellation, authentication failure, and unavailable authentication deny the request. A macOS binary built without cgo requires `--approval=terminal` for `auto` or `prompt` rules. Linux biometric integration is outside this first version.

Use `lend agent --config ./policy.json --approval=terminal` to select terminal approval explicitly on either platform for `auto` or `prompt` rules. Approval reads the laptop's `/dev/tty`. The remote session cannot answer the prompt. Without a usable local desktop or controlling terminal, approval fails.

Each daemon queues commands, SSH signatures, and management requests behind one local approval dialog. The approval timeout includes queue time. Cancelled or disconnected requests leave the queue, and expired requests cannot reach the prompt. The server admits up to 32 socket connections; excess connections are refused. Approved commands can run concurrently while another request waits for approval. Approval expires after one minute and commands time out after five minutes. Both `lend agent` and `lend ssh` accept timeout overrides:

```sh
lend agent --config ./policy.json --approval-timeout=90s --command-timeout=10m
```

The socket lives in a directory owned by the laptop user with mode `0700`, and the socket has mode `0600`. The default is `$XDG_RUNTIME_DIR/lend/agent.sock` when `XDG_RUNTIME_DIR` is set, otherwise `~/.lend/agent.sock`. lend removes its socket on normal shutdown and refuses to replace any existing path. After a crash, verify the old agent has stopped before removing its stale socket.

## MCP

Run `lend mcp` as a stdio MCP server inside the remote SSH session. It reads `SSH_AUTH_SOCK` from its environment, or accepts `--socket PATH`. The agent client must launch it with access to the current forwarded socket.

For an MCP client using a `mcpServers` configuration:

```json
{
  "mcpServers": {
    "laptop": {
      "command": "lend",
      "args": ["mcp"]
    }
  }
}
```

The server exposes one tool, `run_local_command`:

```json
{
  "args": ["gh", "pr", "view", "123", "--repo", "example/project"],
  "reason": "Inspect this pull request before preparing a review"
}
```

The reason is required for MCP calls and appears in the laptop approval prompt beside caller context. The bridge attaches caller information from its process and the MCP handshake; caller fields are not tool arguments. Optional `stdin` accepts up to 64 KiB of UTF-8 input. Results include the exit code and separate stdout and stderr, each capped at 64 KiB with an explicit truncation flag. Binary output uses base64. Command failure or refusal sets the MCP result's `isError` field. Cancelling the tool or closing the MCP session closes its command channel.

The MCP adapter supports the initialization-based stdio protocol revisions `2025-11-25` and `2025-06-18`. It does not implement the newer per-request metadata protocol, HTTP transports, resources, or prompts. It emits JSON-RPC exclusively on stdout. CLI and MCP requests use the same laptop policy and approval path.

## Agent approvals

`lend approve` asks the laptop for a decision without running anything there. Topics are allowed in the policy's `approvals` section, each with its own approval:

```json
{"approvals": {"topics": [{"name": "claude-code", "approval": "biometric:inline"}, {"name": "deploy", "approval": "biometric"}]}}
```

```sh
lend approve --topic deploy --title "terraform apply (staging)" --details-file plan.txt && terraform apply plan.out
```

`lend approve --hook claude-code|codex|agy|pi` answers a coding agent's permission hook from the laptop. `--hook json` reads a neutral format that any agent can produce, and `--hook claude-compatible` serves agents that copy Claude Code's hook format. [examples/pi/lend-approval.ts](examples/pi/lend-approval.ts) is the pi extension. See [Agent approvals](https://lend.antonio.cx/agent-approvals.html) for each agent's hook configuration.

## Scope and trust

This is an initial implementation for macOS and Linux. It supports pipes and binary streams. It does not allocate a PTY, forward terminal input, resize terminals, or support interactive programs such as editors. When the remote caller's stdin is a terminal, the command receives EOF; pipe or redirect input to send it to the laptop.

Forwarding the proxy grants the ability to request local execution, use admitted SSH keys, and request permitted management changes. Local policy checks every request. Commands, signatures, and management require approval unless their rule or default sets `none`. Commands and signatures can also use a valid explicit lease. The upstream agent's restrictions and approval requirements also apply. Approving a shell, interpreter, or command that consumes instructions on stdin can authorize arbitrary local execution. Stdin is streamed after approval and is not reviewed by the prompt.

Requests are labeled with an unverified origin. This version preserves OpenSSH session binding messages for the upstream agent, but does not verify those bindings itself or map them to hostnames. Signing format classification does not prove the remote destination or enforce host allowlists. Anyone able to access the forwarded socket, including an administrator on the remote host, can request execution or relay the socket elsewhere. The local policy and approval prompt govern each request.

Commands run directly as the local user and can access local files, credentials, and environment variables. Their output goes to the requester. Approval is not an execution sandbox. An approved program can access the original agent socket directly if it knows its path, so an arbitrary command grant also grants that program the local user's access. Disconnects and timeouts cancel execution and kill the command's process group. Pipelined requests or a blocked stdin stream can delay disconnect detection until a timeout; descendants that detach from the process group can outlive cancellation.

## Development

```sh
go test -race ./...
go vet ./...
```

`make check` also checks formatting and runs the installer and release packaging tests. GitHub CI runs on Linux and macOS, on both amd64 and arm64, and checks the minimum Go version on Linux. macOS CI builds the cgo backend against the native SDK. See [releasing](docs/releasing.md) for publishing releases and updating the Homebrew tap.

Tests cover profile isolation, exact lease scope, expiry and revocation, unavailable lock tracking, approval queue cancellation, credential injection and failures, persistent history and rotation, local controls, management permissions, secret redaction, private-key identity checks, packet clearing, caller display, spoofed metadata, binding hints, key filtering, signing policy and quotas, upstream denial, command policies, reason forwarding, MCP lifecycle and cancellation, output limits, streaming, argv handling, timeouts, framing limits, and socket directory checks. Plain key fingerprints are checked against `ssh-keygen`. Unix socket, peer credential, and OpenSSH agent integration tests skip when the environment denies socket creation. Native macOS dialogs, authentication, and lock notifications need validation on a Mac with an interactive desktop session. Desktop lock integration and the complete SSH wrapper lifecycle also need validation on unrestricted desktop hosts.

The transport and execution packages have in-memory tests, so the core tests can also run in restricted environments. See [the protocol](docs/protocol.md) for the experimental wire format.

## Prior art

- [ssh-rev-exec](https://github.com/KOBA789/ssh-rev-exec) carries local execution requests through an SSH agent proxy.
- [op-forward](https://github.com/ekovshilovsky/op-forward) forwards 1Password CLI commands to a machine with desktop authentication.

lend uses the SSH agent extension transport and adds its own local approval before launching a command. It is an independent implementation.
