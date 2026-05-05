# Hyperpowers

Workflow guidance for Claude Code and Codex.

Hyperpowers provides repo-local skills, hooks, commands, and specialized agents that help AI coding agents stay aligned with a real engineering workflow. The active workflow is markdown-first: shape the work, create a local task directory, then execute in small reviewed slices.

## Workflow Model

- Active work is now tracked in local markdown task directories under `plans/active/`.
- `plan.md` holds the approved spec.
- `context.md` captures discoveries and resume notes.
- `tasks.md` is the rolling backlog with `Now`, `Next`, `Later`, `Blocked`, and `Done`.
- Finished task directories are deleted from `plans/active/`; they are not archived in the repo.

## Features

### Skills

Core workflow skills:
- `brainstorming` shapes rough ideas into an approved spec
- `writing-plans` distills the spec into task docs
- `executing-plans` works the current slice and updates docs
- `review-implementation` audits the implementation against the spec
- `verification-before-completion` requires evidence before completion claims
- `managing-task-docs` handles splitting, deleting finished local task dirs, and re-prioritizing task docs

Supporting skills:
- `test-driven-development`
- `debugging-with-tools`
- `fixing-bugs`
- `refactoring-diagnosis`
- `refactoring-design`
- `refactoring-safely`
- `dispatching-parallel-agents`
- `building-hooks`
- `skills-auto-activation`

### Commands

- `/hyperpowers:brainstorm`
- `/hyperpowers:write-plan`
- `/hyperpowers:execute-plan`
- `/hyperpowers:update-task-docs`
- `/hyperpowers:review-implementation`

### Agents

- `code-reviewer`
- `codebase-investigator`
- `internet-researcher`
- `test-runner`

### Hooks

Hooks support:
- skill activation suggestions
- session-start context injection
- task-doc truncation guards
- edit tracking
- stop-time reminders for verification and task-doc updates

See [HOOKS.md](/Users/ryan/src/hyper/HOOKS.md) for details.

## Task Directory Workflow

For substantial work:

1. Shape the work with `brainstorming`.
2. Create `plans/active/<slug>/plan.md`.
3. Use `writing-plans` to fill `context.md` and `tasks.md`.
4. Use `executing-plans` to work only the current `Now` slice.
5. Review and verify before completion.
6. Delete the finished local directory from `plans/active/`.

## Installation

Claude Code plugin:

```text
/plugin marketplace add withzombies/hyperpowers
/plugin install hyperpowers@withzombies-hyper
```

Codex skills:
- Repo-local skills live in `.agents/skills/`
- Cross-tool policy lives in [AGENTS.md](/Users/ryan/src/hyper/AGENTS.md)
- Codex-specific notes live in [CODEX.md](/Users/ryan/src/hyper/CODEX.md)

## Philosophy

- Shape first, code second
- Keep strategy in repo docs
- Keep execution slices small
- Update task docs as reality changes
- Verify before claiming completion

## Contributing

- Use `writing-skills` when editing skills
- Use `building-hooks` when editing hook behavior
- Prefer local markdown task docs

## License

MIT
