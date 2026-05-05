# claw

A tiny POSIX-sh LLM REPL for any Linux box.

`clawlite.sh` is a single shell script that gives you a streaming chat
loop against OpenAI-compatible or Anthropic APIs, with:

- **Shell tool calls** — the model emits `<shell>...</shell>` blocks and
  claw runs them locally, feeding back `<shell-result exit=N>` chunks.
  YOLO by default; pass `--confirm` to be prompted.
- **Mentor mode (optional)** — run a second assistant pass that critiques
  the first answer against the original request, then asks the first
  assistant to revise based on that feedback.
- **Per-session rolling memory** — user prompts and assistant replies
  are journaled to JSONL files. When entries exceed configurable
  windows, an LLM call compacts the overflow into:
  - durable **session rules** (`~/.config/clawlite/instructions/90-<session>-rules.md`)
  - a per-session **journal** (`~/.local/share/clawlite/journals/<session>.journal.md`).
- **Slash commands** — `/help`, `/list`, `/load NAME`, `/save NAME`,
  `/model X`, `/provider openai|anthropic`, `/tools on|off`,
  `/yolo on|off`, `/journal on|off`, `/md on|off|auto`, `/inst`,
  `/paste`, `/reset`.
- **No dependencies beyond `curl` + `jq` + `awk` + `sh`** — busybox
  ash is fine. Built specifically to run inside the v86 Alpine guest
  used by [LinuxOnTab](https://linuxontab.com).

## Install

### One-liner (any Linux)

```sh
wget -qO /usr/local/bin/claw https://linuxontab.com/local/clawlite.sh \
  && chmod +x /usr/local/bin/claw
```

### Install + seed exact config/data roots

If you need claw to come with seeded prompts/instructions/data under a
specific home path (for example `/Users/kilian`), run:

```sh
TARGET_HOME=/Users/kilian \
  wget -qO- https://raw.githubusercontent.com/kilian-ai/claw/main/scripts/install-and-seed.sh | sh
```

This will:

- install claw to `/usr/local/bin/claw`
- seed `/Users/kilian/.config/clawlite/...`
- seed `/Users/kilian/.local/share/clawlite/...`

If claw is already installed, this explicit seed step is enough:

```sh
XDG_CONFIG_HOME=/Users/kilian/.config \
XDG_DATA_HOME=/Users/kilian/.local/share \
  /usr/local/bin/claw --where >/dev/null
```

This serves the latest committed `clawlite.sh` from the LinuxOnTab
GitHub Pages site (which is auto-synced from this repo via
`scripts/sync-to-linuxontab.sh`).

### From this repo's raw URL

```sh
wget -qO /usr/local/bin/claw \
  https://raw.githubusercontent.com/kilian-ai/claw/main/clawlite.sh \
  && chmod +x /usr/local/bin/claw
```

### Clone for hacking

```sh
git clone https://github.com/kilian-ai/claw ~/claw
ln -sf ~/claw/clawlite.sh /usr/local/bin/claw
```

## Configure

On first run, claw seeds:

- `~/.config/clawlite/config` — provider, models, windows, toggles
- `~/.config/clawlite/instructions/00-default.md` — base system prompt
- `~/.config/clawlite/prompts/*.txt` — external prompt templates used by:
  - shell tool behavior
  - user-memory compaction
  - assistant-journal compaction
  - mentor review and revision flow

If `config.default` exists next to `clawlite.sh` (repo checkout), it is
copied to `~/.config/clawlite/config` on first run.

Set your keys (env or in the config file):

```sh
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
```

Defaults:

| Var              | Default               | Meaning                                    |
|------------------|-----------------------|--------------------------------------------|
| `PROVIDER`       | `openai`              | `openai` or `anthropic`                    |
| `MODEL_OPENAI`   | `gpt-5.5`             |                                            |
| `MODEL_ANTHROPIC`| `claude-sonnet-4-5`   |                                            |
| `TOOLS`          | `1`                   | enable `<shell>` tool calls                |
| `CLAW_YOLO`      | `1`                   | run shell tools without confirmation       |
| `MENTOR`         | `0`                   | enable mentor review + revision pass       |
| `MENTOR_TOOLS`   | `1`                   | allow mentor pass to inspect workspace     |
| `TOOL_MAX_ITERS` | `50`                  | max tool turns per user prompt             |
| `TOOL_OUTPUT_LIMIT` | `32768`            | bytes of stdout/stderr fed back per call   |
| `USER_WINDOW`    | `2000`                | verbatim user-prompt history retained      |
| `ASSIST_WINDOW`  | `2000`                | verbatim assistant-reply history retained  |
| `JOURNAL`        | `0`                   | inject session journal into system prompt  |
| `MARKDOWN`       | `off`                 | re-render replies as ANSI markdown         |

## CLI

```
claw [opts] [prompt]
  -s NAME           load/save session (default: "default")
  -m MODEL          override active provider's model
  -p openai|anthropic
  -i FILE           extra instructions file (repeatable)
  --no-memory       skip rolling history this run
  --no-instructions ignore ~/.config/clawlite/instructions/
  --no-tools        disable <shell> tool calls
  --confirm         prompt before each tool call (default: yolo)
  --no-yolo         alias for --confirm
  --yolo            run tools without confirmation (default)
  --mentor          enable mentor pass (review + revision)
  --no-mentor       disable mentor pass
  --reset           wipe live history for this session (keeps rules+journal)
  --journal         inject session journal into system prompt
  --no-journal      do not inject journal
  --md / --no-md    force markdown rendering on/off
  --user-window N   override verbatim user-prompt window
  --assist-window N override verbatim assistant-reply window
  --where           print resolved config + data dirs and exit
```

## Working from inside a guest (round-trip from LinuxOnTab)

You can clone, edit, and push this repo from the v86 Alpine guest:

```sh
# in the guest
apk add git openssh-client
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"

# Auth: use a Personal Access Token (classic, repo scope) and put it
# in a credential helper that survives reboots:
git config --global credential.helper 'store --file=/root/.git-credentials'
# First push will prompt for username (your GH login) and password
# (the PAT). After that it's cached.

git clone https://github.com/kilian-ai/claw
cd claw
# ...edit clawlite.sh...
git add -A && git commit -m "claw: tweak X" && git push
```

When you push, the deployed `linuxontab.com/local/clawlite.sh` does NOT
auto-update. Run `scripts/sync-to-linuxontab.sh` from a checkout that
has `~/.ai/LinuxOnTab` next to it to bump the deployed copy:

```sh
~/claw/scripts/sync-to-linuxontab.sh
```

(That script copies `clawlite.sh` into `LinuxOnTab/local/clawlite.sh`,
commits, and pushes the LinuxOnTab repo. GitHub Pages then serves the
new file within a minute.)

## Publish greybox page to kilian-ai.com

To sync `greybox.html` into your website repo as `index.html`:

```sh
SITE_DIR=/path/to/kilian-ai.com-repo \
  ./scripts/sync-greybox-to-site.sh
```

Common domain setup with CNAME and auto-push:

```sh
SITE_DIR=/path/to/kilian-ai.com-repo \
CNAME=kilian-ai.com PUSH=1 \
  ./scripts/sync-greybox-to-site.sh
```

Defaults:

- `SITE_DIR=../kilian-ai.com`
- `DEST_PATH=index.html`

## License

MIT — see `LICENSE`.
