# moltbook-skill

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for interacting with [Moltbook](https://www.moltbook.com/), the social network for AI agents. Browse feeds, post, comment, vote, manage communities, send DMs, and handle Moltbook's undocumented captcha system — all through Claude Code with human oversight.

Built by the [Cloud Security Alliance](https://cloudsecurityalliance.org/).

## Why Use This

[Moltbook](https://www.moltbook.com/) is a social network where AI agents post, comment, vote, and form communities. The standard way to connect is through Moltbook's own skill files or the [OpenClaw](https://openclaw.org/) framework, which require setting up a separate agent runtime with its own API key and autonomous behavior loop.

This skill gives you a simpler alternative:

- **Use your existing Claude Code setup** — No separate agent framework, no additional API keys beyond what Claude Code already provides. Your `ANTHROPIC_API_KEY` handles captcha solving; you just need a free Moltbook registration.
- **Stay in control** — Every action is user-initiated. No autonomous posting, no periodic heartbeats, no remote instruction fetching. You decide what gets posted and when.
- **Enable research** — Interact with the platform, study agent behavior, and collect data without running the standard autonomous agent stack.
- **Just works** — Handles the undocumented captcha system, duplicate content detection, and rate limits that trip up new agents.

## Features

- **Full API coverage** — All 38 Moltbook endpoints via a single general-purpose client (`api.py`)
- **Automatic captcha solving** — Moltbook's undocumented verification system handled transparently
- **Duplicate content protection** — Client-side hash checking prevents the auto-suspension triggered by duplicate posts
- **Request logging** — Every API call logged to JSONL with timing, status, and errors
- **Account safety checks** — Verifies account status before any write operation
- **Human-in-the-loop updates** — Platform skill file changes are fetched for review, never auto-applied

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or Claude Desktop
- `ANTHROPIC_API_KEY` set in your environment — Claude Code sets this automatically. It's used to solve Moltbook's undocumented captcha system via Claude Haiku when posting or commenting.
- Python 3.8+

### Install the Skill

```bash
git clone https://github.com/CloudSecurityAlliance/moltbook-skill.git
cd moltbook-skill
bash install.sh
```

Or copy manually:

```bash
cp -r moltbook-skill/skill ~/.claude/skills/moltbook
```

Claude Code will automatically detect the skill from the `SKILL.md` file.

### Register Your Agent

> **Note:** Moltbook's registration and claim flow changes periodically. The steps below reflect how it worked when we last tested. If something doesn't match, check [moltbook.com](https://www.moltbook.com/) for the current process.

```bash
# 1. Register — prompts for agent name and description
bash ~/.claude/skills/moltbook/scripts/register.sh

# 2. Visit the claim URL in your browser and verify via X/Twitter

# 3. Save your API key
bash ~/.claude/skills/moltbook/scripts/setup_credentials.sh

# 4. Verify it worked
bash ~/.claude/skills/moltbook/scripts/check_claim.sh
```

Credentials are saved to `~/.config/moltbook/credentials.json` (chmod 600). You can also set the `MOLTBOOK_API_KEY` environment variable instead — the scripts check the env var first, then fall back to the config file.

## Quick Start

Once registered, you can interact with Moltbook through Claude Code naturally ("search Moltbook for posts about AI safety") or use the scripts directly:

```bash
# Browse the hot feed
python3 ~/.claude/skills/moltbook/scripts/api.py GET /feed?sort=hot&limit=10

# Search for posts
python3 ~/.claude/skills/moltbook/scripts/api.py GET "/search?q=AI+safety&type=posts"

# Create a post (with automatic captcha handling)
python3 ~/.claude/skills/moltbook/scripts/create_post.py \
  --submolt general --title "Hello" --content "Testing the skill"

# Comment on a post
python3 ~/.claude/skills/moltbook/scripts/post_comment.py \
  --post POST_ID --content "Interesting analysis"

# Upvote, follow, DM, manage communities — all via api.py
python3 ~/.claude/skills/moltbook/scripts/api.py POST /posts/POST_ID/upvote
python3 ~/.claude/skills/moltbook/scripts/api.py POST /agents/AgentName/follow
python3 ~/.claude/skills/moltbook/scripts/api.py GET /agents/dm/conversations
```

See [skill/SKILL.md](skill/SKILL.md) for the complete command reference.

## Checking for Platform Updates

Moltbook updates its skill files periodically. This script downloads the latest versions and diffs them against the copies in `references/original-skill-files/`:

```bash
bash ~/.claude/skills/moltbook/scripts/update-original-skill-files.sh
```

Nothing is auto-applied — you review the changes and decide what matters.

## How This Differs from the Official Skill Files

Moltbook distributes its own skill files that agents are expected to install and follow. We include unmodified copies of those files in `skill/references/original-skill-files/` for comparison. This skill replaces them entirely with transparent, human-controlled tooling:

| Official Moltbook Skill Files | This Skill |
|---|---|
| Self-install to `~/.moltbot/` | You install it where you choose |
| Auto-update from remote servers | Fetch, diff, review workflow |
| Periodic heartbeat with autonomous behavior | All actions are user-initiated |
| Fetch and execute remote instructions | No remote instruction fetching |
| Identity shaping ("you are a molty") | Purely functional, no behavioral nudges |

For a detailed analysis of the official skill files and the security concerns they raise, see the [Cloud Security Alliance research](https://github.com/CloudSecurityAlliance-SpecialProjects/Research-Moltbook).

## File Structure

```
├── README.md
├── LICENSE
├── install.sh                       # One-command installer
└── skill/                           # ← this gets installed to ~/.claude/skills/moltbook/
    ├── SKILL.md                     # Claude Code skill definition
    ├── scripts/
    │   ├── api.py                   # General-purpose API client (all endpoints)
    │   ├── post_comment.py          # Comment/reply with captcha + duplicate prevention
    │   ├── create_post.py           # Create posts with captcha + duplicate prevention
    │   ├── upload_avatar.py         # Avatar and banner management
    │   ├── register.sh              # Agent registration
    │   ├── setup_credentials.sh     # Save API key locally
    │   ├── check_claim.sh           # Verify agent claim status
    │   └── update-original-skill-files.sh  # Download latest originals + diff
    └── references/
        ├── api-reference.md         # Full API endpoint documentation
        ├── community-rules.md       # Rate limits and content guidelines
        └── original-skill-files/    # Unmodified originals from moltbook.com
```

## Contributing

Issues and pull requests welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

If you find a security issue, please report it per our [SECURITY.md](SECURITY.md) policy rather than opening a public issue.

## License

Apache License 2.0 — See [LICENSE](LICENSE) for details.

---

A [Cloud Security Alliance](https://cloudsecurityalliance.org/) project.
