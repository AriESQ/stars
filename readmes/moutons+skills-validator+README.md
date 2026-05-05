# skills-validator

[![CI](https://github.com/moutons/skills-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/moutons/skills-validator/actions/workflows/ci.yml)
[![CodeQL](https://github.com/moutons/skills-validator/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/moutons/skills-validator/actions/workflows/github-code-scanning/codeql)
[![Crates.io](https://img.shields.io/crates/v/skills-validator)](https://crates.io/crates/skills-validator) [![OpenSSF Best Practices](https://www.bestpractices.dev/projects/12600/badge)](https://www.bestpractices.dev/projects/12600)

A validation tool for [Agent Skills](https://agentskills.io/specification) — the emerging standard for packaging reusable instructions that AI coding agents can discover and follow. skills-validator checks skill directories for spec compliance,
content quality, reference integrity, and security concerns using a five-pass analysis pipeline.

> Validates skills according to the Agent Skills specification, informed by the [OpenCode](https://opencode.ai/docs/skills/) and [Claude Code](https://code.claude.com/docs/en/skills) implementations.

## Installation

From [crates.io](https://crates.io/crates/skills-validator):

```bash
cargo binstall skills-validator --locked
# or
cargo install skills-validator --locked
```

From source:

```bash
git clone https://github.com/moutons/skills-validator.git
cd skills-validator
cargo install --path . --locked
```

## Quick Start

```bash
# Validate a skill directory
skills-validator validate path/to/skill

# Scan all known agent tool directories for skills
skills-validator scan --all

# JSON output for CI pipelines
skills-validator validate path/to/skill --output-format json
```

## Usage

### Validating Skills

```bash
# Basic validation
skills-validator validate path/to/skill

# Strict mode — exit 1 on warnings and suggestions, not just errors
skills-validator validate path/to/skill --strict

# Filter output by minimum severity
skills-validator validate path/to/skill --severity warning

# JSON output
skills-validator validate path/to/skill --output-format json

# Read skill properties (outputs YAML)
skills-validator read-properties path/to/skill

# Generate <available_skills> XML for agent prompts
skills-validator to-prompt path/to/skill-a path/to/skill-b
```

### Scanning for Skills

The `scan` command discovers and validates skills across agent tool directories (Claude Code, OpenCode, Cursor, Windsurf, and 20+ others).

```bash
skills-validator scan --all                    # Scan repo + user home
skills-validator scan --user                   # Scan user home only
skills-validator scan --repo                   # Scan repo root only
skills-validator scan --tool claude-code       # Scan specific tool(s)
skills-validator scan --all --dry-run          # Discover without validating
```

### Shell Completions

```bash
skills-validator completions bash
skills-validator completions zsh
skills-validator completions fish
```

### CLI Flags

| Flag                                          | Description                                          |
| --------------------------------------------- | ---------------------------------------------------- |
| `--strict`                                    | Exit 1 on warnings or suggestions (not just errors)  |
| `--output-format human\|json`                 | Output format (default: `human`)                     |
| `--severity info\|suggestion\|warning\|error` | Only show diagnostics at or above this severity      |
| `--json`                                      | **Deprecated.** Alias for `--output-format json`     |
| `--verbose`                                   | Show detailed output                                 |
| `--dry-run`                                   | Discover skills without validating (scan subcommand) |

### Exit Codes

| Code | Meaning                                    |
| ---- | ------------------------------------------ |
| `0`  | All skills valid (warnings may be present) |
| `1`  | One or more skills invalid                 |
| `2`  | Scan or configuration error                |

## Configuration

### Config File

Generate a default config file:

```bash
skills-validator setup
```

This creates `$XDG_CONFIG_HOME/skills-validator/config.toml` (typically `~/.config/skills-validator/config.toml`) with all options commented out showing their defaults:

```toml
# skills-validator configuration
# Override order: compiled defaults -> this file -> env vars -> CLI flags
# Env var naming: SKILLS_VALIDATOR_<SECTION>_<KEY> (uppercase)

# [sizeyness]
# moderate_file_threshold = 3
# hefty_file_threshold = 6
# moderate_subdir_threshold = 1
# hefty_subdir_threshold = 3

# [content]
# body_line_limit = 300
# known_models = ["claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"]

# [references]
# markdown_hop_limit = 5
# orphan_exclusions = ["LICENSE*", "CHANGELOG*", "README*", ".gitignore", ".*"]

# [security]
# semgrep_enabled = true
# semgrep_path = "semgrep"
# custom_rules_dir = ""
```

### Configuration Sections

**`[sizeyness]`** — Thresholds for classifying skills as Simple, Moderate, or Hefty. Larger skills are held to higher standards (suggestions escalate to warnings or errors).

| Field                       | Default | Description                        |
| --------------------------- | ------- | ---------------------------------- |
| `moderate_file_threshold`   | `3`     | File count to classify as Moderate |
| `hefty_file_threshold`      | `6`     | File count to classify as Hefty    |
| `moderate_subdir_threshold` | `1`     | Subdirectory count for Moderate    |
| `hefty_subdir_threshold`    | `3`     | Subdirectory count for Hefty       |

**`[content]`** — Body length limits and model validation.

| Field             | Default                    | Description                                   |
| ----------------- | -------------------------- | --------------------------------------------- |
| `body_line_limit` | `300`                      | Maximum body lines before warning             |
| `known_models`    | `["claude-opus-4-6", ...]` | Valid model identifiers for the `model` field |

**`[references]`** — Link validation and orphan detection.

| Field                | Default                           | Description                                 |
| -------------------- | --------------------------------- | ------------------------------------------- |
| `markdown_hop_limit` | `5`                               | Maximum link chain depth before stopping    |
| `orphan_exclusions`  | `["LICENSE*", "CHANGELOG*", ...]` | Glob patterns for files that aren't orphans |

**`[security]`** — Semgrep integration and security scanning.

| Field              | Default     | Description                                 |
| ------------------ | ----------- | ------------------------------------------- |
| `semgrep_enabled`  | `true`      | Enable semgrep analysis of embedded scripts |
| `semgrep_path`     | `"semgrep"` | Path to semgrep binary                      |
| `custom_rules_dir` | `""`        | Additional semgrep rules directory          |

### Environment Variables

Every config field can be overridden with an environment variable using the pattern `SKILLS_VALIDATOR_<SECTION>_<KEY>`:

| Environment Variable                                   | Config Field                          |
| ------------------------------------------------------ | ------------------------------------- |
| `SKILLS_VALIDATOR_SIZEYNESS_MODERATE_FILE_THRESHOLD`   | `sizeyness.moderate_file_threshold`   |
| `SKILLS_VALIDATOR_SIZEYNESS_HEFTY_FILE_THRESHOLD`      | `sizeyness.hefty_file_threshold`      |
| `SKILLS_VALIDATOR_SIZEYNESS_MODERATE_SUBDIR_THRESHOLD` | `sizeyness.moderate_subdir_threshold` |
| `SKILLS_VALIDATOR_SIZEYNESS_HEFTY_SUBDIR_THRESHOLD`    | `sizeyness.hefty_subdir_threshold`    |
| `SKILLS_VALIDATOR_CONTENT_BODY_LINE_LIMIT`             | `content.body_line_limit`             |
| `SKILLS_VALIDATOR_REFERENCES_MARKDOWN_HOP_LIMIT`       | `references.markdown_hop_limit`       |
| `SKILLS_VALIDATOR_SECURITY_SEMGREP_ENABLED`            | `security.semgrep_enabled`            |
| `SKILLS_VALIDATOR_SECURITY_SEMGREP_PATH`               | `security.semgrep_path`               |
| `SKILLS_VALIDATOR_SECURITY_CUSTOM_RULES_DIR`           | `security.custom_rules_dir`           |

Boolean values accept `true`/`false`, `1`/`0`, or `yes`/`no` (case-insensitive). Invalid values emit a warning and fall back to the previous value.

### Override Order

Configuration is resolved in this order (later wins):

1. Compiled defaults
2. Config file (`config.toml`)
3. Environment variables
4. CLI flags

## Validation Pipeline

Validation runs as a five-pass pipeline. Each pass can emit diagnostics at any severity level.

| Pass | Name           | What it checks                                                     |
| ---- | -------------- | ------------------------------------------------------------------ |
| 1    | **Parse**      | YAML frontmatter parsing via pulldown-cmark AST                    |
| 2    | **Structure**  | File inventory, sizeyness classification, binary file detection    |
| 3    | **Content**    | Frontmatter field validation, body quality, positive reinforcement |
| 4    | **References** | Markdown link chain walking (up to 5 hops), orphan file detection  |
| 5    | **Security**   | Remote execution patterns, optional semgrep integration            |

### Diagnostic Severity Tiers

| Tier           | Purpose                                       | Exit code             |
| -------------- | --------------------------------------------- | --------------------- |
| **Info**       | Positive reinforcement for good practices     | 0                     |
| **Suggestion** | Gentle nudge to consider adding something     | 0 (1 with `--strict`) |
| **Warning**    | Real quality concern affecting agent behavior | 0 (1 with `--strict`) |
| **Error**      | Broken, spec-violating, or dangerous          | 1 always              |

### Sizeyness Escalation

Skills are classified by sizeyness (Simple, Moderate, Hefty) based on file count, total size, and body length. A check that produces a **suggestion** for a simple skill may escalate to a **warning** or **error** for a moderate or hefty one. Larger,
more complex skills are held to a higher standard.

### Frontmatter Validation

Validates against the [Agent Skills specification](https://agentskills.io/specification):

| Field           | Required | Constraints                                                                                                                                                                   |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. Must not contain consecutive hyphens (`--`). Must match directory name. |
| `description`   | Yes      | Max 250 characters. Non-empty.                                                                                                                                                |
| `license`       | No       | License name or reference to a bundled license file.                                                                                                                          |
| `compatibility` | No       | Max 500 characters. Indicates environment requirements.                                                                                                                       |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                                                                                                          |
| `allowed-tools` | No       | Space-delimited list of pre-approved tools. (Experimental)                                                                                                                    |

**Unknown fields** produce warnings (demoted from errors in 0.2.0).

### Content Quality

Warns when skill content is missing key directive words:

| Keyword   | Guidance                                                                                                                                                       |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `never`   | A well-written skill includes clear directives to NEVER do something and preferably ALWAYS do an alternative. See <https://agentskills.io/what-are-skills>     |
| `always`  | A well-written skill includes clear directives to ALWAYS do something in certain circumstances. See <https://agentskills.io/what-are-skills>                   |
| `when`    | A well-written skill contains 'when' statements to inform the agent of what conditions trigger certain behaviors. See <https://code.claude.com/docs/en/skills> |
| `example` | A well-written skill contains examples to inform the agent of what to do in commonly encountered circumstances. See <https://opencode.ai/docs/skills>          |

### Claude Code Extensions

Claude Code supports additional fields beyond the official spec. These generate **warnings** but not errors:

- `argument-hint` - Hint shown during autocomplete
- `disable-model-invocation` - Prevent automatic loading
- `user-invocable` - Hide from / menu
- `model` - Model to use when skill is active
- `context` - Run in forked subagent context
- `agent` - Which subagent type to use
- `hooks` - Hooks scoped to skill lifecycle

See <https://code.claude.com/docs/en/skills> for details.

## Rust API

```rust
use skills_validator::{run_pipeline, read_properties, to_prompt};

fn main() {
    // Validate a skill directory using the five-pass pipeline
    let result = run_pipeline("my-skill");
    for diagnostic in &result.diagnostics {
        println!("[{}] {}", diagnostic.severity, diagnostic.message);
    }

    // Read skill properties
    let props = read_properties("my-skill").unwrap();
    println!("Skill: {} - {}", props.name, props.description);

    // Generate prompt for available skills
    let prompt = to_prompt(&["skill-a", "skill-b"]);
    println!("{}", prompt);
}
```

> **Migration note:** `validate()` and `ValidationResult` are deprecated. Use `run_pipeline()` and `PipelineResult`/`Vec<Diagnostic>` instead. See CHANGELOG.md for the full migration guide.

## Agent Prompt Integration

Use `to-prompt` to generate the suggested `<available_skills>` XML block for your agent's system prompt:

```xml
<available_skills>
<skill>
<name>
my-skill
</name>
<description>
What this skill does and when to use it
</description>
<location>
/path/to/my-skill/SKILL.md
</location>
</skill>
</available_skills>
```

## Security Considerations When Building Skills

Script execution introduces security risks. Consider:

- **Sandboxing**: Run scripts in isolated environments
- **Allowlisting**: Only execute scripts from trusted skills
- **Confirmation**: Ask users before running potentially dangerous operations
- **Logging**: Record all script executions for auditing

The validator's security pass detects remote execution patterns (curl-pipe-bash, etc.) and can optionally run semgrep for deeper script analysis. Configure semgrep integration in the `[security]` section of the config file.

See <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#security-considerations> for more details.

## Background

This project draws inspiration from the [agentskills/skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) Python reference library, extending it with a layered validation pipeline, configurable severity tiers, and
sizeyness-aware escalation.

## License

Apache 2.0
