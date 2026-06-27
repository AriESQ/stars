# /onboard

> Make any legacy project Claude-Code-ready — without forcing AI tooling on your teammates.

[![Release](https://img.shields.io/github/v/release/sdsrss/onboard?label=release&color=blue)](https://github.com/sdsrss/onboard/releases)
[![License](https://img.shields.io/github/license/sdsrss/onboard)](./LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-7c3aed)](https://docs.claude.com/en/docs/claude-code/plugins)
[![Tests](https://img.shields.io/badge/tests-224%20passing-brightgreen)](./tests)

**📖 Read this in other languages: [English](./README.md) · [简体中文](./README.zh-CN.md)**

`/onboard` is a [Claude Code](https://claude.com/claude-code) Skill that walks a *legacy* project through a structured 10-phase onboarding protocol — discovering stacks, generating a token-compact `CLAUDE.md`, configuring guard hooks, aligning CI with local commands — **all offer-only, never auto-installing system tools**. Default `--local-only` mode writes zero project files; team members pulling the branch see nothing.

Current version: **v3.2.0**.

---

## Why?

| Problem | What `/onboard` does |
|---|---|
| Cold-starting Claude Code on a legacy repo takes hours of project archaeology | 10-phase protocol auto-discovers stacks, lockfiles, CI, forbidden zones, behavioral conventions (8-dimension deep analysis in Phase 1.7) |
| A 5KB `CLAUDE.md` chews 5K tokens every turn | Extraction-first template, hard token ceiling at 5000 (soft cap 2500), empty sections omitted entirely |
| AI-tool adoption shouldn't pollute the team's repo by default | `--local-only` is the default — all outputs land in `.claude/local-only/` + `.git/info/exclude`; zero `.gitignore` change, zero commits |
| Letting an LLM `brew install` or `npm i` whatever it wants is a recipe for disaster | Iron Law 7 + meta-rule 19: every system install is **offer-only**, every project dependency change is batch-AUTH'd by a human |
| `--uninstall` should be possible | v2.8+ marker/manifest/snapshot protocol makes every PROJECT write reversible (Iron-level reversibility) |

## Features

- **Multi-language stack support** (v2.4) — first-class for repos like TypeScript frontend + Python backend + ML pipeline; Phase 1 detects each stack, Phase 4 applies lint/format/typecheck per-stack, Phase 7 hook dispatches by file extension via `stacks.json`.
- **Two modes** — `--local-only` (default, zero team pollution) and `--share` (opt-in, OUTPUT files committed).
- **4 guard hooks** wired via `.claude/settings.json` — `guard-bash` (deny dangerous shell), `guard-edit` (forbidden-zone protection), `post-edit-check` (multi-stack format check), `stop-verify` (lint + typecheck on touched files).
- **Doctor mode** (`--doctor`, v2.5+) — D1-D15 health checks, no writes, reports `healthy | drifted | broken`.
- **Reversible by design** (v2.8+) — marker + manifest + snapshot make `--uninstall` precise; `=skill` (L1 only) and `=all` (L1+L2+L3) modes (v2.11+).
- **Plugin marketplace standard** (v2.9+) — `/plugin marketplace add sdsrss/onboard` works natively.
- **Lazy-loaded spec** (v3.0+) — SKILL.md keeps a compact entry; consumer Claude reads `phases/phase-7.md` / `phases/uninstall.md` / `references/state-schema.md` only when entering those scopes (meta-rule 27).
- **Compact plan output** (v3.1+) — Phase 2 / 2.5 cards default to Top-N highlights (Top 3 for plan, Top 1-2 per install category), remainder folded as `+N more`; `--verbose-plan` restores full listing. Phase 0 now emits a first-run session-auth tip. Skill description expanded with English trigger surface for better discovery.
- **Plugin matrix sub-file** (v3.2+) — 15-plugin recommendation matrix extracted to `references/recommendations.md`; SKILL.md keeps a 7-bullet sentinel summary; consumer Claude Reads the sub-file when entering Phase 2.5 (meta-rule 27 enumeration expanded to 4 sub-files). 3/3 Opus subagent dogfood verified the lazy-load contract.

## Quick start

### Option A · Claude Code plugin marketplace (recommended)

```text
/plugin marketplace add sdsrss/onboard
/plugin install onboard
```

Upgrade:

```text
/plugin marketplace update onboard
/plugin update onboard
```

### Option B · `curl | bash` universal installer

```bash
curl -sSL https://raw.githubusercontent.com/sdsrss/onboard/main/install.sh | bash             # install
curl -sSL https://raw.githubusercontent.com/sdsrss/onboard/main/install.sh | bash -s -- update
curl -sSL https://raw.githubusercontent.com/sdsrss/onboard/main/install.sh | bash -s -- doctor
curl -sSL https://raw.githubusercontent.com/sdsrss/onboard/main/install.sh | bash -s -- uninstall
```

Environment overrides: `ONBOARD_TARGET=project|user` · `ONBOARD_REPO` · `ONBOARD_BRANCH` · `ONBOARD_ALLOW_DIRTY=1` · `ONBOARD_CONFIRM_UNINSTALL=yes`.

### Option C · Manual `git clone`

The skill files live at `skills/onboard/` inside the repo (Claude Code plugin convention), so a direct clone to `~/.claude/skills/onboard` would nest `SKILL.md` two levels deep. Clone to a fresh scratch dir, then copy the skill subtree:

```bash
SRC=$(mktemp -d -t onboard-src.XXXXXX)
git clone --depth 1 https://github.com/sdsrss/onboard.git "$SRC"
mkdir -p ~/.claude/skills
cp -r "$SRC/skills/onboard" ~/.claude/skills/
chmod +x ~/.claude/skills/onboard/hooks/*.sh ~/.claude/skills/onboard/scripts/*.sh
rm -rf "$SRC"
```

> Using `mktemp -d` avoids `fatal: destination path … already exists` if you re-run after a typo.

### First run

In a git-initialized project root:

```text
/onboard
```

Claude prints an **execution plan** first — phase list, current mode (`--local-only` by default), file-change budget, size class, total ETA — then waits for your confirmation. Each phase ends with a phase card showing what was changed.

---

## Modes

| Mode | When to use | What gets written |
|---|---|---|
| `--local-only` (default, v2.6+) | Personal use on a team repo · team has no AI policy yet · OSS repo where you're a contributor · trial run | `CLAUDE.local.md` · `.claude/settings.local.json` · `.claude/local-only/*` · `.git/info/exclude` markers. **Zero changes** to tracked files. |
| `--share` (opt-in) | Team has approved AI tooling · solo project where you want multi-machine sync · the team wants `CLAUDE.md` reviewed in PR | `CLAUDE.md` (tracked) · `.claude/settings.json` · `.claude/onboarding-logs/*` · revised `.gitignore` · optionally opens PR / MR via host adapter (`gh` / `glab` / `tea`) |

**Why local-only is the default**: most teams have only a few AI-tool early adopters. Default-commit means one person's experiment forces tooling on the rest of the team. Default-local-only = zero team pollution risk; promote to `--share` after team alignment.

**Mode is not silently switched**: changing modes mid-project requires `/onboard --update [--share|--local-only]` with hard AUTH.

---

## How it works

Full protocol in [`skills/onboard/SKILL.md`](./skills/onboard/SKILL.md). The 10 phases and your role at each:

| Phase | What happens | Your role |
|---|---|---|
| 0 · Preflight | git topology, host detection, tool availability | Resolve dirty tree / submodule / detached HEAD if flagged |
| 0.5 · Migration | Inherit prior `--update` decisions | Skip if first run |
| 1 · Discovery | Multi-stack detection, lockfiles, CI parsing | Review the "Environment Report" |
| 1.5 · Blocking Decisions | Forbidden-zone candidates, lockfile/CI choices | Answer via enumerated DSL |
| 1.7 · Deep Analysis (v2.7) | 8-dimension behavioral profile | Approve / correct findings |
| 2 · Authorization | Touch budget, write scope | `proceed safe` / `approve install <id>` / `skip <id>` |
| 2.5 · Install Plan (v2.7) | dev tools · system CLIs · runtimes · plugins | Batch authorize 4 lists |
| 3 · CLAUDE.md | Extraction template, token-budget enforced | Review draft (hard cap 5000 tokens) |
| 4 · Dev & Lint | Per-stack lint / format / typecheck integration | — |
| 5 · Test | Test runner discovery + sanity | — |
| 6 · Commit & CI Gates | Pre-commit / pre-push hooks | — |
| 7 · Claude Code Hooks | 4 hooks installed via `settings.json` | — |
| 8 · `.gitignore` & Verification | Final wiring; in `--share` mode offers PR/MR | — |

Run a single phase with `/onboard --phase=<n>`. Re-onboard with `--resume` (same version) or `--update` (cross-version migration via Phase 0.5).

---

## Hooks

Four hooks installed in `.claude/settings.json` (share) or `.claude/settings.local.json` (local-only):

| Hook | Event | Purpose |
|---|---|---|
| `guard-bash.sh` | `PreToolUse` / `Bash` | Deny `rm -rf /`, force-push to main, `curl \| sh`, project-defined `ONBOARD_FORBIDDEN_COMMANDS` regex list (v2.12.0+) |
| `guard-edit.sh` | `PreToolUse` / `Edit\|Write\|MultiEdit` | Block edits inside `ONBOARD_FORBIDDEN_PATHS` (confirmed forbidden zones) |
| `post-edit-check.sh` | `PostToolUse` / `Edit\|Write\|MultiEdit` | Log touched file + per-stack format check |
| `stop-verify.sh` | `Stop` | Lint + typecheck on touched files per `ONBOARD_STOP_MODE` (`light` / `standard` / `strict`) |

All four follow **Iron Law 15** (exit 0 + stdout JSON, never mixed) and **Iron Law 19** (warn-only checks must exit 0).

**Third-party hook coexistence** (v2.5+): independent matcher-block strategy — onboard never overwrites existing hooks, both are listed and Claude Code's "deny-first" semantics apply.

**Plugin install path note**: `${CLAUDE_PLUGIN_ROOT}` is ephemeral (changes every plugin update). Onboard's Phase 7 default is to invoke `scripts/mirror-hooks.sh` (v2.10.1+, idempotent) to mirror hooks to a stable `~/.claude/onboard-runtime/hooks/` location; `settings.json` references the mirror.

---

## Doctor / Update / Uninstall

```text
/onboard --doctor              # D1-D15 health check, no writes
/onboard --update              # cross-version migration (Phase 0.5)
/onboard --update --local-only # switch from --share back to local-only
/onboard --dry-run             # preview without writing
/onboard --uninstall           # remove all onboard writes from this project
/onboard --uninstall=skill     # uninstall only L1 user-global skill, preserve project config
```

**Uninstall protocol** (v2.8+, three-layer model in v2.11+): `=skill` clears L1 user-global (`~/.claude/skills/onboard/` + plugin cache + mirror), preserves project-side L2 (settings hook references) and L3 (hook scripts) via keeper-rewrite (`.claude/onboard-keeper/`). `=all` clears all three layers. Marker/manifest/snapshot make every PROJECT write reversible; users can `restore-snapshot` to recover the pre-onboard state.

---

## Requirements

| Platform | Status | Notes |
|---|---|---|
| Linux | First-class | — |
| macOS | First-class (v2.5+) | `brew install coreutils` recommended for `gtimeout` |
| WSL2 | First-class | Treated as Linux |
| Windows native | Not supported | Use WSL2 |

**Tools**: `git`, `bash 3.2+`, `jq` (all required — installer refuses without jq because guard hooks shell out to it; missing jq silently disables `permissionDecision` deny payloads) · `coreutils` on macOS (strongly recommended) · `make` (optional).

**Git host adapters** (Phase 8 PR/MR offer, never auto-execute): GitHub (`gh`), GitLab (`glab`), Gitea/Forgejo/Codeberg (`tea`); Bitbucket and unknown hosts fall back to web URLs.

---

## Verification

After install + first run:

```text
/hooks
```

Should list 4 hook configs (PreToolUse × 2, PostToolUse, Stop). Test a forbidden-zone edit to confirm `guard-edit.sh` denies it; test a deliberate lint error to confirm `stop-verify.sh` blocks the Stop event.

Run the in-repo test suite:

```bash
bash tests/run.sh
# 10 integration tests / 224 assertions / 0 fail
```

---

## Troubleshooting

| Symptom | Check |
|---|---|
| `/onboard` not in command list | SKILL.md frontmatter `disable-model-invocation: true` may hit issue [anthropic#43875](https://github.com/anthropics/claude-code/issues/43875); temporarily remove or switch to Command form |
| Hooks not firing | `/hooks` to confirm loaded; check `${CLAUDE_PROJECT_DIR}` expansion; verify `ls -l .claude/skills/onboard/hooks/` shows executable |
| `guard-edit` false positive | Inspect `ONBOARD_FORBIDDEN_PATHS` env (colon-separated, no quotes, no spaces) |
| `stop-verify` timing out | Lower `ONBOARD_STOP_MODE` to `light`, or tune per-stack `lint_timeout_sec` / `typecheck_timeout_sec` in `stacks.json` (v2.12+) |
| `--update` migration fails | Old state backed up to `.claude/onboarding-state.v<old>.json.bak`; check Phase 0.5 output |

Full troubleshooting + edge cases in [`SKILL.md`](./skills/onboard/SKILL.md) § "异常处理".

---

## Contributing

This repo evolved through **4 simulation-based stress testing rounds** in the v2 series (v2.0 → v2.4 was net-line-decrease; v2.5-v2.12 added features on real-run evidence). The v3 series begins with C1 SKILL.md shallow-split (lazy-load contract). Any change should follow this pattern:

1. Run current version (simulated or real)
2. Number each issue (P-A, P-B, …) with Critical / High / Medium / Low severity
3. Accept-or-reject each with written rationale
4. Roll the accepted set into the next version

No speculative features. See [`CLAUDE.md`](./CLAUDE.md) for full repo-maintainer conventions (Iron Laws, meta-rules, validation commands, file-classification, multi-stack discipline).

**Bug reports**: capture the failing-state evidence (error message, state file, phase card) and open an issue. Evidence-driven PRs welcome.

---

## License

[MIT](./LICENSE) — `Copyright (c) sds`.

---

## Links

- [Full protocol spec (SKILL.md)](./skills/onboard/SKILL.md) · [Phase 7 hooks](./skills/onboard/phases/phase-7.md) · [Uninstall mode](./skills/onboard/phases/uninstall.md) · [State schema](./skills/onboard/references/state-schema.md)
- [Changelog](./CHANGELOG.md) (full history; v3.2.0 = current)
- [Releases](https://github.com/sdsrss/onboard/releases)
- [Issues](https://github.com/sdsrss/onboard/issues)
- [Claude Code documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Claude Code plugins documentation](https://docs.claude.com/en/docs/claude-code/plugins)
