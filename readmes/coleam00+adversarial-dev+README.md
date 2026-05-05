# Adversarial Dev

A GAN-inspired three-agent harness that separates **planning**, **building**, and **evaluation** into distinct AI agents with distinct contexts. The evaluator's job is to **break** what the generator builds -- creating adversarial tension that drives quality far beyond what a single agent can achieve. Built with both the **Claude Agent SDK** and **Codex SDK** so you can run the same architecture on either platform.

Based on Anthropic's engineering article: [Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps).

## What This Demonstrates

Most AI coding agents fail on complex tasks not because the model is bad, but because nobody separated the work into specialized roles. A single agent that plans, builds, and evaluates its own work will reliably praise its own mediocre output. This is called **self-evaluation bias**, and it's the quiet killer of ambitious AI coding projects.

This project implements the fix: three agents, each with a focused job and its own context window.

| Agent | Role | Analogy |
|-------|------|---------|
| **Planner** | Expands a short prompt into a full product spec with sprints | Product manager |
| **Generator** | Builds one feature at a time, commits to git | Software engineer |
| **Evaluator** | Actively tries to break what the generator built, scores ruthlessly | Adversarial QA |

The evaluator doesn't just review code -- it's an adversary. It runs the application, probes for failures, tests edge cases the generator didn't think of, and scores each criterion on a 1-10 scale with a hard pass threshold. If any criterion fails, the sprint goes back to the generator with detailed, unforgiving feedback. The generator has to fight its way past the evaluator to advance. This adversarial pressure is what turns AI-generated code from "looks right" into "actually works."

## Quick Start

### Prerequisites

- [Bun](https://bun.sh) runtime installed
- Claude CLI authenticated (`claude auth login`)
- Codex CLI authenticated (`codex auth login`)

### Install

```bash
git clone https://github.com/coleam00/adversarial-dev.git
cd adversarial-dev
bun install
```

### Run the Claude Harness

```bash
bun run claude-harness/index.ts "Build a personal task manager with a REST API, interactive dashboard with charts, task categories, priority levels, due dates, and search functionality"
```

Or pass a detailed prompt from a file:

```bash
bun run claude-harness/index.ts --file prompt.md
```

### Run the Codex Harness

```bash
bun run codex-harness/index.ts "Build a personal task manager with a REST API, interactive dashboard with charts, task categories, priority levels, due dates, and search functionality"
```

Both harnesses write their output to `workspace/claude/` and `workspace/codex/` respectively. The built application lives in `workspace/{sdk}/app/`.

## Configuration

Defaults are in `shared/config.ts`:

| Setting | Default | Description |
|---------|---------|-------------|
| `maxSprints` | 10 | Maximum number of sprints |
| `maxRetriesPerSprint` | 3 | Max evaluation retries before failing a sprint |
| `passThreshold` | 7 | Minimum score (out of 10) for each criterion |
| `CLAUDE_MODEL` | `claude-sonnet-4-6` | Model for Claude harness |
| `CODEX_MODEL` | `gpt-5.4` | Model for Codex harness |

## How It Works

When you run a harness, here's what happens step by step:

### 1. Planning Phase
The planner takes your short prompt and generates a comprehensive product specification with features organized into sprints, a design language, and tech stack decisions. This spec is written to `spec.md`.

### 2. Contract Negotiation (per sprint)
The generator proposes what it will build and how success should be measured. The evaluator reviews the criteria, making them more specific, adding edge cases, and raising the bar. They iterate until locked in. The contract is saved as JSON.

### 3. Build Phase (per sprint)
The generator reads the spec and contract, then implements features one at a time with git commits after each. It has full access to create files, run commands, install dependencies, and test code.

### 4. Evaluation Phase (per sprint)
The evaluator reads the contract criteria, examines the code, **runs the application**, and tries to break it. It scores each criterion on a 1-10 scale. If all criteria pass (score >= 7/10), the sprint survives. If any fail, detailed feedback goes back to the generator -- with file paths, line numbers, and exact failure descriptions.

### 5. Retry Loop
The generator reads the adversarial feedback, decides whether to refine or pivot, and rebuilds. This cycles up to 3 times per sprint. If a sprint can't survive the evaluator after all retries, the harness stops.

### 6. Completion
Once all sprints pass, you have a working application built incrementally with quality gates at every step -- every feature tested by an agent whose job was to break it.

## The Architecture

```
User Prompt (1-4 sentences)
         |
         v
   +-----------+
   |  PLANNER  |  --> writes spec.md (features, sprints, design language)
   +-----------+
         |
         v  (for each sprint)
   +---------------------+
   | CONTRACT NEGOTIATION |  Generator proposes criteria,
   | Generator <-> Eval   |  Evaluator tightens the screws,
   +---------------------+  both lock in "done"
         |
         v
   +-----------+     fail + feedback     +------------+
   | GENERATOR | <---------------------- | EVALUATOR  |
   | (build)   | ----------------------> | (attack)   |
   +-----------+     implementation      +------------+
         |                                      |
         v              pass                    |
    Next Sprint <-------------------------------+
```

### Sprint Contracts

Before any code is written, the generator and evaluator negotiate a **sprint contract**: a JSON document defining exactly what "done" means. Each criterion is specific and testable -- not "works well" but "PUT /frames/reorder returns 200 and reorders frames in the database."

The evaluator uses contract negotiation to set traps -- adding edge cases, tightening thresholds, and demanding specifics that force the generator to build robust code from the start. This is directly from Anthropic's approach. They found that JSON contracts work better than markdown because models are less likely to tamper with structured JSON.

### File-Based Communication

Agents communicate through files, not shared conversation history. This keeps each agent's context focused on its role:
- `spec.md` -- Product specification from the planner
- `contracts/sprint-{n}.json` -- Sprint contracts
- `feedback/sprint-{n}-round-{m}.json` -- Evaluator feedback per attempt
- `progress.json` -- Harness state tracking

## The GAN Connection

This architecture is inspired by **Generative Adversarial Networks** (GANs), where a generator creates outputs and a discriminator tries to reject them, iterating until quality emerges from the tension between the two.

| GANs | This Harness |
|------|-------------|
| Generator vs. discriminator | **Generator vs. evaluator** |
| Gradient descent | **Hard pass/fail thresholds** |
| Two networks | **Three agents** (adds planner) |
| Continuous training | **Sprint-based iteration** |
| Zero-sum game | **Asymmetric adversarial** -- evaluator tries to break, generator tries to survive |

The core insight is the same: **separate generation from evaluation, then pit them against each other**. A generator that evaluates its own work converges on mediocrity. A separate evaluator with the explicit mandate to find failures creates the adversarial pressure that forces quality upward. The generator doesn't just build -- it builds knowing an adversary is waiting.

## Why This Is the Future of AI Coding

We're at an inflection point. In 2025, the focus was on making individual agents smarter. In 2026, the focus has shifted to **harness design** -- the scaffolding around agents that makes them reliable.

Here's the key principle from Anthropic's article:

> "Every component in a harness encodes an assumption about what the model can't do on its own."

As models improve, harnesses simplify. When Opus 4.5 shipped, Anthropic removed context resets from their harness because the model could maintain coherence natively. When Opus 4.6 shipped with 1M tokens, they removed sprint decomposition entirely because the model could sustain coherent work across two-hour builds.

But the frontier doesn't shrink -- it moves. Better models make previous scaffolding unnecessary while opening new possibilities for harnesses that achieve more complex tasks. The **pattern** of separating planning, building, and evaluation is durable even as the implementation details evolve.

Two principles that matter most:
1. **Separate evaluation from generation.** Don't let the agent grade its own homework.
2. **Define "done" before you start.** Sprint contracts are how you turn vibing into engineering.

## Project Structure

```
adversarial-dev/
├── shared/              # Shared types, config, prompts, utilities
│   ├── types.ts         # TypeScript interfaces
│   ├── config.ts        # Model and threshold defaults
│   ├── prompts.ts       # Agent system prompts (identical for both SDKs)
│   ├── logger.ts        # Colored console output
│   └── files.ts         # File I/O for specs, contracts, feedback
├── claude-harness/      # Claude Agent SDK implementation
│   ├── index.ts         # CLI entry point
│   ├── harness.ts       # Orchestration loop
│   ├── planner.ts       # Planner agent
│   ├── generator.ts     # Generator agent
│   └── evaluator.ts     # Evaluator agent
├── codex-harness/       # Codex SDK implementation
│   ├── index.ts         # CLI entry point
│   ├── harness.ts       # Orchestration loop
│   ├── planner.ts       # Planner agent
│   ├── generator.ts     # Generator agent
│   └── evaluator.ts     # Evaluator agent
└── workspace/           # Runtime output (gitignored)
    ├── claude/          # Claude harness working directory
    └── codex/           # Codex harness working directory
```

Both harnesses share the same prompts, types, and orchestration flow. The only differences are the SDK-specific agent implementations -- `query()` async generators for Claude, `Codex` threads for Codex.
