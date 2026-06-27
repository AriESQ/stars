# claudemd

> A **personal AI-coding discipline harness**: one developer's opinionated **AI-CODING-SPEC v6.14**, encoded as Claude Code shell hooks and shipped with the plugin. Built and dogfooded on my own repos — fork and adapt, don't adopt wholesale.

[![CI](https://github.com/sdsrss/claudemd/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sdsrss/claudemd/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/claudemd-cli.svg)](https://www.npmjs.com/package/claudemd-cli)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

claudemd plugs into the Claude Code hook system to **block commits, pushes, and bash commands** that violate AI-CODING-SPEC v6.14 — banned vocabulary in commit messages, `rm -rf $VAR` without variable validation, ship-on-red-CI, unread `MEMORY.md` entries during release flows, and more. The spec itself (`CLAUDE.md` + `CLAUDE-extended.md` + `CLAUDE-changelog.md` + `OPERATOR.md`) ships with the plugin and installs into `~/.claude/`, so the rules Claude Code reads at session start match the rules the hooks enforce. (`OPERATOR.md` is the human-only spec-maintenance handbook — Agent-loaded files are the CLAUDE trio.)

A standalone CLI (`npx claudemd-cli`) reuses the same `banned-vocab.patterns` source for git pre-commit hooks, GitHub Actions, and other agents that don't run inside Claude Code.

> **Status & scope.** This is a single-maintainer tool that encodes one developer's working discipline — not a general-purpose product. It's exercised almost entirely on my own repositories, the spec is opinionated, and the defaults reflect my preferences rather than a consensus. If you install it, expect to fork `CLAUDE.md` and tune the rules to your own workflow. Treat it as a reference implementation of "spec-as-enforced-hooks," not a turnkey solution. Issues and PRs are welcome.

---

## Quick start

Run **both** slash commands inside Claude Code:

```
/plugin marketplace add sdsrss/claudemd
/plugin install claudemd@claudemd
```

Then bootstrap the **current** session (skip the wait-for-next-session restart) + verify:

```
/claudemd-install
/claudemd-status
/claudemd-doctor
```

`install` copies the spec into `~/.claude/`, writes the hook manifest, and evicts legacy entries — idempotent, safe to re-run. (Background: Claude Code does not fire `postInstall`, so without `/claudemd-install`, `install.js` runs on the next `SessionStart` instead.) `status` reports plugin version, shipped vs installed spec version, kill-switch state, and rule-hits row count. `doctor` runs 9+ health checks with `[✓] / [△] / [✗]` markers.

Fallback (no slash command — e.g. scripting outside CC): `node ~/.claude/plugins/cache/claudemd/claudemd/<version>/scripts/install.js`. Find `<version>` with `ls ~/.claude/plugins/cache/claudemd/claudemd/ | sort -V | tail -1`.

> ⚠️ **`~/.claude/CLAUDE.md` is shared real estate.** Claude Code reads this file as your user-global instructions across every project. If you've hand-written personal instructions there (`Always reply in 中文`, `My name is X`, etc.), install moves your existing files to `~/.claude/backup-<ISO>/` (last 5 kept automatically) before writing the spec. Since v0.5.3, install prints a `[claudemd] WARN: …` line to stderr when the existing file does not look like a claudemd spec. To bring your personal instructions back on uninstall, run `CLAUDEMD_SPEC_ACTION=restore /claudemd-uninstall`.

---

## Prerequisites

| Tool | Required | Why |
|---|---|---|
| `node >= 20` | yes | install / status / doctor / update scripts (`package.json` engines) |
| `jq` | yes | every hook parses Claude Code event JSON via `jq` — without it hooks silently fail-open |
| `git` | yes | `ship-baseline-check` reads HEAD body; `session-start-check` runs `git ls-remote`; manual upgrade fallback |
| `gh` | recommended | `ship-baseline-check` calls `gh run list` — if absent, the hook fail-opens silently and shipping on red CI is no longer blocked |
| `coreutils` | macOS only | hooks need GNU `timeout`. Install with `brew install coreutils`, then prepend `$(brew --prefix coreutils)/libexec/gnubin` to your `PATH` |

Verify in one command (Linux): `node --version && jq --version && gh --version && git --version && timeout --version | head -1`. macOS users can swap `timeout` for `gtimeout` if `coreutils` is bottle-installed without the `gnubin` shim.

---

## What it installs

| Layer | Contents |
|---|---|
| 16 shell hooks | `banned-vocab-check` · `pre-bash-safety-check` · `ship-baseline-check` · `residue-audit` · `memory-read-check` · `memory-prompt-hint` · `mid-spine-yield-scan` · `sandbox-disposal-check` · `session-start-check` · `session-extended-read` · `session-summary` · `session-end-check` · `transcript-vocab-scan` · `transcript-structure-scan` · `version-sync` · `mem-audit` |
| 13 slash commands | `/claudemd-install` · `/claudemd-status` · `/claudemd-update` · `/claudemd-audit` · `/claudemd-toggle` · `/claudemd-doctor` · `/claudemd-analyze` · `/claudemd-uninstall` · `/claudemd-rules` · `/claudemd-clean-residue` · `/claudemd-sparkline` · `/claudemd-sampling-audit` · `/claudemd-bypass-audit` |
| 1 standalone CLI | `claudemd-cli lint` · `claudemd-cli audit` ([npm: `claudemd-cli`](https://www.npmjs.com/package/claudemd-cli)) |
| Spec v6.14 | `~/.claude/CLAUDE.md` · `CLAUDE-extended.md` · `CLAUDE-changelog.md` · `OPERATOR.md` (backup-before-overwrite) |

Install moves any existing `~/.claude/CLAUDE*.md` to `~/.claude/backup-<ISO>/` (last 5 kept automatically). Uninstall offers `keep / restore / delete`; `delete` requires an extra confirmation.

> Since v0.1.5, hook registration lives in the plugin's own `hooks/hooks.json` — the Claude Code harness expands `${CLAUDE_PLUGIN_ROOT}` there automatically on every invocation, so hooks track the active plugin version without manual re-registration. `install.js`'s remaining jobs are (1) copy `spec/CLAUDE*.md` into `~/.claude/` (with backup-before-overwrite), (2) evict any legacy claudemd hook entries from prior installs (≤0.1.1 absolute-path form, 0.1.2-0.1.4 `${CLAUDE_PLUGIN_ROOT}`-in-settings.json form), and (3) write the installed manifest. It never touches other-plugin hooks. Claude Code's plugin-lifecycle `postInstall` field is not honored, so the script runs from `SessionStart` instead.

---

## Hooks (what fires when)

Once installed, hooks run silently in the background. Verbose log: `~/.claude/logs/claudemd.jsonl` (one row per hook decision). Aggregate via `/claudemd-audit`.

| Trigger | Hook | What happens |
|---|---|---|
| `git commit` with banned vocab (e.g. `significantly`, `70% faster`, `should work`) | `banned-vocab-check` | Blocks the commit with a message pointing to the §10-V spec rule. |
| Bash command with `rm -rf $VAR` (unvalidated expansion) or unpinned `npx <pkg>` | `pre-bash-safety-check` (v0.5.0+) | Blocks at PreToolUse:Bash per §8 SAFETY. Bypass via `[allow-rm-rf-var]` / `[allow-npx-unpinned]` token in the command, or pin/validate the variable. |
| `git push` while base-branch CI is red | `ship-baseline-check` | Blocks the push (2-second `gh run list` timeout; fail-open if `gh` absent or times out). |
| Bash command matching ship/push/deploy/release with an unread matched `MEMORY.md` entry | `memory-read-check` | Blocks the command with a list of memory files to Read first. |
| Session end with `~/.claude/tmp/` growth > 20 entries | `residue-audit` | Advisory stderr warning; never blocks. |
| Session end with fresh `tmp.XXXXXX`-style directories | `sandbox-disposal-check` | Advisory stderr warning. |
| Stop event with `Why:`-less hard-rule citations in the assistant turn | `mem-audit` (v0.9.4+) | Detects spec-citation patterns missing the `Why:` rationale token; advisory log. |
| Session end | `session-summary` (v0.8.0+) | Writes `~/.claude/.claudemd-state/last-session-summary.json`; banner emit at next `SessionStart`. |
| New session start with GitHub remote tag newer than local cache max version | `session-start-check` (v0.4.0+) | Injects an "upgrade available" banner via `additionalContext`. Rate-limited to once per 24h via `~/.claude/.claudemd-state/upstream-check.lastrun` sentinel. 3-second `git ls-remote` timeout, fail-open. |
| First `UserPromptSubmit` after a mid-session `/plugin install` upgrade | `version-sync` (v0.3.1+) | Backgrounds `install.js` once per session when the manifest version diverges from the active plugin's `package.json`. Sentinel-gated; fail-open. |
| `PostToolUse` after assistant text containing banned vocab | `transcript-vocab-scan` | Advisory; logs to rule-hits without blocking. |
| Session end with last assistant turn carrying §10 four-section out of order, `Done:` lines lacking evidence fingerprints, or `Uncertain:` short hedges without `because` | `transcript-structure-scan` (v0.9.10+) | Stop advisory — closes the audit gap that ~7 self-enforced HARD rules (§iron-law-2 / §10-four-section-order / §10-honesty) had no hook-side feedback signal. Opt-in (`TRANSCRIPT_STRUCTURE_SCAN=1`, default OFF) for FP signal collection; FP-tightened so single-section `Done:` lines never trigger. |

### Execution order (PreToolUse:Bash)

CC runs all configured PreToolUse hooks for `Bash` sequentially in declaration order. **First deny stops the rest** and the tool call is denied. The 4 Bash hooks fire in this order (declared in `hooks/hooks.json`):

1. `pre-bash-safety-check` (§8 SAFETY immutable) — `rm -rf $VAR`, unpinned `npx <pkg>`. First so a §8 violation can never be overridden by a downstream hook.
2. `banned-vocab-check` (§10-V) — `git commit` message scan.
3. `ship-baseline-check` (§7) — `git push` while base CI is red.
4. `memory-read-check` (§11) — ship/release/deploy commands matching unread MEMORY.md tags.

Per-hook timeout (3-5s in `hooks.json`); timeout = treated as exit 0 (pass) per fail-open contract. Stop / SessionStart / UserPromptSubmit / PostToolUse hooks run all declared hooks regardless (none can block; advisories accumulate). Internal hook errors (missing `jq`, malformed event JSON, unreadable patterns file) fail-open; failures do NOT propagate to subsequent hooks.

**Readonly fast-path** (v0.8.3 introduced opt-in default-OFF; **v0.20.0 promoted to default-ON** via §13.3 advisory→enforce gate): hooks 1, 2, and 4 short-circuit when the command is a definitely-read-only shape (no shell-meta, first token in safe-reader whitelist — `ls`, `cat`, `git log`, `git status`, `git diff`, `git rev-parse`, `pwd`, `echo`, `head`, `tail`, etc.). Hook 3 only fires on `git push` so the fast-path doesn't apply. Opt-out: `export BASH_READONLY_FAST_PATH=0` (or any other value than the literal `0` is treated as ON).

## Commands

| Command | Purpose |
|---|---|
| `/claudemd-install` | Bootstrap the current session right after `/plugin install` (copy spec into `~/.claude/`, write manifest, evict legacy entries). Idempotent. CC does not fire `postInstall`, so without this command `install.js` waits until the next `SessionStart`. |
| `/claudemd-status [--verbose]` | Plugin version + spec version + kill-switch state + logs line count. `--verbose` adds per-hook env-var × event × effective vs persisted state table + 5 escape-token reference. |
| `/claudemd-update` | Interactive diff against plugin-shipped spec, then apply-all or cancel (4-file spec set is lockstep — per-file select would dangle §EXT cross-references). |
| `/claudemd-audit [--days N]` | Aggregate rule-hits over last N days (default 30). Top banned-vocab patterns, per-hook deny counts. |
| `/claudemd-toggle <hook-name>` | Enable/disable a specific hook by toggling `DISABLE_*_HOOK` in `settings.json` env. |
| `/claudemd-doctor [--prune-backups=N]` | Health checks; optionally prune `~/.claude/backup-*` dirs older than N. v0.7.1+ also flags rule sections whose bypass:deny ratio > 50% (R-N6 §0.1 demotion candidates). |
| `/claudemd-rules [N]` | v0.8.0+ — audit `spec/hard-rules.json` manifest over last N days (default 30 — lowered from 90d in v0.13.1 after the 90d gate was structurally unreachable under typical log retention). Surfaces `demoteCandidates` (hook-enforced rules with 0 hits) and `staleReviews` (rules whose `last_demote_review` is null/old). |
| `/claudemd-sparkline [--days=A,B,C]` | v0.8.4+ R-N9 — per-`spec_section` cumulative counts of signal events across 3 windows (default 30/60/90d). Trend arrow compares per-period rate; `(newly active)` / `(silenced)` annotations flag activation/deactivation transitions. Markdown block suitable for CHANGELOG header pre-release. |
| `/claudemd-clean-residue [--apply]` | Dry-run-by-default cleanup of stale `claudemd-sync-*` sentinels and historical `claudemd-(mockgh\|work).*` test sandboxes. |
| `/claudemd-uninstall` | Pre-uninstall cleanup: clears manifest + state + log + legacy `settings.json` hook entries. Run BEFORE `/plugin uninstall claudemd@claudemd` (see [Uninstall](#uninstall)). |

---

## Standalone CLI

The same `banned-vocab.patterns` source the in-CC hook uses is also exposed as a Node CLI for **git pre-commit hooks, GitHub Actions, and other agents** (Codex, Cursor, OpenClaw) — anywhere outside the Claude Code process.

```bash
# After npm publish (operator-driven, not part of plugin install):
npx claudemd-cli lint "your commit message here"
npx claudemd-cli lint --stdin < message.txt
npx claudemd-cli audit ~/.claude/projects/<encoded>/<session>.jsonl
npx claudemd-cli audit transcript.jsonl --json

# Dev mode (this repo, before npm publish):
node bin/claudemd-lint.js lint "your commit message here"
node bin/claudemd-lint.js audit ~/.claude/projects/<encoded>/<session>.jsonl
```

| Subcommand | Purpose |
|---|---|
| `lint <text>` / `--stdin` | Scan commit-message text for §10-V banned vocab. Exit 0 clean / 1 hits. |
| `audit <jsonl-path>` | Scan all assistant-text turns in a Claude Code transcript jsonl. Skips `@ratio` patterns by default (chat prose has different baseline conventions); pass `--include-ratio` to include them. |
| `--json` | JSON output (machine-readable for CI). |
| `--version` / `--help` | Standard. |

**Pre-commit example (`.git/hooks/commit-msg`)**:

```bash
#!/usr/bin/env bash
npx claudemd-cli lint --stdin < "$1" || exit 1
```

The CLI does NOT depend on `~/.claude/` state — pure stateless input → stdout/stderr + exit code. Same enforcement, anywhere Node 20+ runs.

---

## Kill-switches

All visible in `/claudemd-status`. Three tiers:

**1. Plugin-wide.** Short-circuits every hook before any logic runs:

```bash
export DISABLE_CLAUDEMD_HOOKS=1
```

**2. Per-hook.** Disable one, leave others active:

```bash
export DISABLE_BANNED_VOCAB_HOOK=1               # or
export DISABLE_PRE_BASH_SAFETY_HOOK=1            # or
export DISABLE_SHIP_BASELINE_HOOK=1              # or
export DISABLE_RESIDUE_AUDIT_HOOK=1              # or
export DISABLE_MEMORY_READ_HOOK=1                # or
export DISABLE_MEMORY_HINT_HOOK=1                # v0.11.0+ — UserPromptSubmit MEMORY.md tag pre-matcher (proactive §11 hint)
export DISABLE_SANDBOX_DISPOSAL_HOOK=1           # or
export DISABLE_SESSION_START_HOOK=1              # or
export DISABLE_SESSION_SUMMARY_HOOK=1            # v0.8.0+ — Stop hook writing summary
export DISABLE_USER_PROMPT_SUBMIT_HOOK=1         # version-sync (mid-session upgrade re-install)
export DISABLE_TRANSCRIPT_VOCAB_SCAN_HOOK=1      # PostToolUse §10-V advisory scan
export DISABLE_TRANSCRIPT_STRUCTURE_SCAN_HOOK=1  # v0.9.10+ — Stop §10 four-section advisory
export DISABLE_MEM_AUDIT_HOOK=1                  # v0.9.4+ — Stop Why:-less citation advisory
export DISABLE_SESSION_END_CHECK_HOOK=1          # v0.9.27+ — SessionEnd §11-session-exit mid-SPINE check
export DISABLE_SESSION_EXTENDED_READ_HOOK=1      # v0.10.1+ — PreToolUse:Read §13.1-extended-read denominator signal
export DISABLE_MID_SPINE_YIELD_HOOK=1            # v0.15.0+ — Stop §11-mid-spine-yield advisory (opt-in via MID_SPINE_YIELD_SCAN=1)
```

**2a. Per-sub-feature** (v0.4.0+). Sub-flags inside an enabled hook, named without the `_HOOK` suffix:

```bash
export DISABLE_UPSTREAM_CHECK=1            # only the upstream-tag-check sub-feature
                                           # of session-start-check; bootstrap-on-mismatch
                                           # behavior remains active.

export DISABLE_SESSION_SUMMARY_BANNER=1    # v0.8.0+ — only the SessionStart banner-emit
                                           # half of session-summary; the Stop-side write
                                           # of last-session-summary.json continues so
                                           # the data is captured for /claudemd-audit
                                           # but no additionalContext line is injected.

export DISABLE_BATCH_CADENCE_ADVISORY=1    # v0.19.2+ — only the §13.2 batch-review
                                           # cadence advisory inside session-end-check;
                                           # mid-SPINE warn-on-unvalidated-mutation
                                           # behavior remains active. Threshold also
                                           # configurable via CLAUDEMD_BATCH_THRESHOLD=N
                                           # (positive integer, default 20).

export BANNED_VOCAB_PROSE_SCAN=0           # v0.21.0+ — disable only the Path 2 prose
                                           # scan in banned-vocab-check (the v0.21.0
                                           # §13.3 Gate 2 promotion that denies
                                           # ship-flow commands when the preceding
                                           # assistant turn's prose contains a
                                           # high-fire §10-V pattern). Path 1
                                           # commit-message scan remains active.

export CLAUDEMD_PATH2_DRY_RUN=1            # v0.21.1+ — Path 2 observability mode.
                                           # When set, ship-verb + prior-prose §10-V
                                           # match logs a `deny-prose-dry-run` event
                                           # row to ~/.claude/logs/claudemd.jsonl
                                           # instead of denying. Grep the rows to
                                           # measure true-positive vs false-positive
                                           # rate before committing to live deny.
                                           # Sample: jq -r 'select(.event=="deny-prose-dry-run") | .extra.matched' ~/.claude/logs/claudemd.jsonl
```

**3. Per-invocation escape hatches.** Embed in the command itself, no env var needed:

| Escape | Where | Bypasses |
|---|---|---|
| `[allow-banned-vocab]` | commit message | `banned-vocab-check` |
| `known-red baseline: <reason>` | commit body | `ship-baseline-check` |
| `[skip-memory-check]` | bash command string | `memory-read-check` |
| `[allow-rm-rf-var]` | bash command string | `pre-bash-safety-check` (rm-with-var path only) |
| `[allow-npx-unpinned]` | bash command string | `pre-bash-safety-check` (unpinned npx path only) |

---

## Update

Claude Code has **no** `/plugin update` slash command — it's silently ignored as unrecognized. The canonical upgrade sequence is:

```
/plugin marketplace update claudemd                 # refresh local marketplace clone (git fetch)
/plugin uninstall claudemd@claudemd                 # remove old plugin version
/plugin install claudemd@claudemd                   # install latest from refreshed clone
/reload-plugins                                     # apply changes to current session
```

Or open the interactive UI via `/plugin` → **Installed** tab → select `claudemd` → follow upgrade prompts.

After the plugin upgrade, sync the shipped spec into `~/.claude/`:

```
/claudemd-update
```

The command prints per-file diff summary, then prompts `apply-all` or `cancel`. Per-file select is intentionally not supported — the 4-file spec set (`CLAUDE.md` + `CLAUDE-extended.md` + `CLAUDE-changelog.md` + `OPERATOR.md`) evolves lockstep, and mixing versions would dangle `§EXT §X-EXT` cross-references in Core. Backup is automatic (retained to 5). `/claudemd-update` never fetches from GitHub — it only diffs the plugin-cache spec against your `~/.claude/CLAUDE*.md` + `~/.claude/OPERATOR.md`. The network fetch is Claude Code's job (via `/plugin marketplace update`).

---

## Uninstall

Claude Code's marketplace lifecycle does not fire `preUninstall`, so `/plugin uninstall claudemd@claudemd` alone leaves orphan state behind (`~/.claude/.claudemd-manifest.json`, `~/.claude/.claudemd-state/`, `~/.claude/logs/claudemd.jsonl`). Use the **two-step flow**:

```
/claudemd-uninstall                    # clear manifest + state + log (plugin still installed)
/plugin uninstall claudemd@claudemd    # CC removes plugin cache itself
```

Reversing the order is the orphan-state vector — `${CLAUDE_PLUGIN_ROOT}` and `scripts/uninstall.js` are gone after `/plugin uninstall`, with no in-tree tool to clean up afterwards. `/claudemd-doctor` flags `[△] plugin cache: orphan manifest …` if you've already hit this.

### Spec disposition

`/claudemd-uninstall` defaults to `keep` (leaves `~/.claude/CLAUDE*.md` in place). Override via env vars before the slash command:

| Option | Env vars | Behavior |
|---|---|---|
| `keep` (default) | (none) | `~/.claude/CLAUDE*.md` left in place; settings.json hook entries cleared. |
| `restore` | `CLAUDEMD_SPEC_ACTION=restore` | Copies the most recent `~/.claude/backup-<ISO>/*.md` back to `~/.claude/`. Use this if your install-time stderr showed `[claudemd] WARN: existing ~/.claude/CLAUDE.md does not look like a claudemd spec` — your hand-written user-global instructions are sitting in the backup waiting to be brought back. |
| `delete` | `CLAUDEMD_SPEC_ACTION=delete CLAUDEMD_CONFIRM=1` | Hard-AUTH: removes all four spec files (`CLAUDE*.md` + `OPERATOR.md`). |

`CLAUDEMD_PURGE=1` (env var) on `/claudemd-uninstall` also drops `~/.claude/.claudemd-state/` and your rule-hits log.

### Direct script invocation (advanced fallback)

If `/claudemd-uninstall` is unavailable (you already ran `/plugin uninstall` first and want to clean up by reaching into the cache before it gets pruned, or you need to script the uninstall outside CC):

```bash
CLAUDEMD_SPEC_ACTION=keep     node ~/.claude/plugins/cache/claudemd/claudemd/<version>/scripts/uninstall.js
CLAUDEMD_SPEC_ACTION=restore  node ~/.claude/plugins/cache/claudemd/claudemd/<version>/scripts/uninstall.js
CLAUDEMD_SPEC_ACTION=delete CLAUDEMD_CONFIRM=1 node ~/.claude/plugins/cache/claudemd/claudemd/<version>/scripts/uninstall.js
```

The slash command and the script are equivalent — the slash command just supplies `${CLAUDE_PLUGIN_ROOT}` for you.

---

## Troubleshooting

**`Plugin "claudemd" not found in any marketplace`** — you forgot the `/plugin marketplace add sdsrss/claudemd` step. Re-run it, then retry install.

**Hooks don't fire / `~/.claude/CLAUDE*.md` not present after install** — Claude Code's `postInstall` lifecycle is not honored, so `install.js` runs from the `SessionStart` hook on your next session, not at install time. Three options:

1. **Recommended**: run `/claudemd-install` in your current session. Wraps `scripts/install.js` exactly the same way `SessionStart` does — idempotent, prints a JSON summary.
2. Start a fresh Claude Code session (`SessionStart` fires the bootstrap automatically).
3. Run the script manually outside CC (e.g. shell scripting): `node ~/.claude/plugins/cache/claudemd/claudemd/<version>/scripts/install.js` (find `<version>` with `ls ~/.claude/plugins/cache/claudemd/claudemd/ | sort -V | tail -1`).

Verify with `/claudemd-status` — the "log.lines" count should increment after the next hook fires.

**`/plugin update claudemd` does nothing / empty stdout** — `/plugin update` is not a valid Claude Code slash command; CC silently ignores unrecognized commands. Use the canonical sequence in the [Update](#update) section: `/plugin marketplace update claudemd` → `/plugin uninstall claudemd@claudemd` → `/plugin install claudemd@claudemd` → `/reload-plugins`. If that also fails (marketplace clone refuses to refresh), manually `git -C ~/.claude/plugins/marketplaces/claudemd fetch origin main --tags && git merge --ff-only origin/main`, then `git archive v<version> | tar -x -C ~/.claude/plugins/cache/claudemd/claudemd/<version>/`, then run that version's `scripts/install.js`.

**`Hook command references ${CLAUDE_PLUGIN_ROOT} but the hook is not associated with a plugin`** (5 errors on every `Bash` tool call + every session end) — you're on claudemd 0.1.2 / 0.1.3 / 0.1.4. Those releases wrote hook commands into `~/.claude/settings.json` under the literal `${CLAUDE_PLUGIN_ROOT}` token, but the CC harness only expands that variable for hooks defined in a plugin's own `hooks/hooks.json` — never in `settings.json`. The fix is v0.1.5+, which moves hook registration into the plugin's `hooks/hooks.json` (where the token expands correctly) and evicts the stale settings.json entries on install. Upgrade via the canonical sequence in the [Update](#update) section, then restart the Claude Code session to clear the cached hook registry.

**`ship-baseline-check` silently passes on red CI** — `gh` CLI is not installed, or authentication failed. Install with `brew install gh` / `apt-get install gh` and run `gh auth login`. Check with `/claudemd-doctor` — it reports `gh: missing` if absent.

**CI matrix fails on macOS** — our own CI installs `coreutils` for GNU `timeout`. If you're running hooks outside the bundled CI, ensure `timeout` is on PATH (`brew install coreutils && export PATH="$(brew --prefix coreutils)/libexec/gnubin:$PATH"`).

**`/claudemd-doctor` reports backup growth** — run `/claudemd-doctor --prune-backups=5` to keep only the 5 most recent.

**`PreToolUse:Bash hook error ... No such file or directory`** pointing at `~/.claude/hooks/banned-vocab-check.sh` — Claude Code loaded `settings.json` at session start and cached the old hand-install hook entry in memory. `install.js` migrated the on-disk entry to the cache path and moved the original shell file to `~/.claude/backup-*/hooks/`, but the running session's hook registry is still stale. Exit and restart the Claude Code session — settings.json is re-read from disk, and the error stops. (This applies to any mid-session `settings.json` change, not just claudemd.)

---

## Project layout

```
claudemd/
├── .claude-plugin/
│   ├── plugin.json           # minimal manifest (name, version, author, license, keywords)
│   └── marketplace.json      # marketplace catalog entry
├── hooks/                    # 16 shell hooks + hooks/lib/ (hook-common, rule-hits, platform)
│   └── hooks.json            # authoritative hook registration (v0.1.5+); CC expands ${CLAUDE_PLUGIN_ROOT} here
├── commands/                 # 12 slash-command markdown files
├── bin/                      # standalone CLI entrypoint (claudemd-lint.js → `npx claudemd-cli` on npmjs.org)
├── scripts/                  # 16 Node.js management scripts + scripts/lib/ (single-source registry, lint, etc.)
├── spec/                     # shipped v6.14.1 CLAUDE*.md trio + OPERATOR.md + hard-rules.json manifest
├── tests/                    # hook shell tests + Node.js tests + integration + fixtures
├── docs/                     # ADDING-NEW-HOOK.md + RULE-HITS-SCHEMA.md + superpowers/
└── .github/workflows/        # ci.yml (ubuntu+macOS × node 20) + npm-publish.yml (tag-triggered)
```

---

## Extending

- **Add a new hook** — see [`docs/ADDING-NEW-HOOK.md`](docs/ADDING-NEW-HOOK.md) for the 5-step guide (hook script + test + plugin registration + doc + version bump).
- **Rule-hits log schema** — [`docs/RULE-HITS-SCHEMA.md`](docs/RULE-HITS-SCHEMA.md) for the JSONL row format used by `/claudemd-audit`.
- **Design rationale + decisions log** — [`docs/superpowers/specs/2026-04-21-claudemd-plugin-design.md`](docs/superpowers/specs/2026-04-21-claudemd-plugin-design.md).

---

## License

MIT — see [LICENSE](LICENSE).
