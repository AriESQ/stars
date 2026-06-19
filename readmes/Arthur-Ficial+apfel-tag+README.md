# apfel-tag

![version](https://img.shields.io/badge/version-0.1.0-blue)

**On-device content tagging from the command line.** Pipe text in, get tags out - classified by Apple's on-device content-tagging model. No API keys, no network, 100% local.

`apfel-tag` is a sister tool to [apfel](https://github.com/Arthur-Ficial/apfel) (the on-device FoundationModels CLI + OpenAI-compatible server). Tagging lived briefly inside apfel as `apfel tag`; it was extracted here so apfel stays focused on its two products and tagging gets a proper home of its own.

## Install

```bash
brew install Arthur-Ficial/tap/apfel-tag
```

## Usage

Plain output - one tag per line, pipe-friendly:

```bash
echo "The headphones sound amazing and the battery lasts all day." | apfel-tag
```

JSON output for scripting:

```bash
echo "Kubernetes pods keep crashing under load." | apfel-tag -o json | jq -r '.tags[]'
```

Pick a label category with `--kind` (`tags`, `topics`, `emotions`, `actions`, `all`):

```bash
echo "A thrilling, scary movie night with friends." | apfel-tag --kind emotions
```

All categories at once:

```bash
pbpaste | apfel-tag --kind all -o json
```

Cap the number of tags:

```bash
echo "$(cat article.txt)" | apfel-tag --max-tags 5
```

If benign text is refused by the safety guardrails, relax them:

```bash
echo "Your text" | apfel-tag --permissive
```

## Options

| Flag | Effect |
|------|--------|
| `-o`, `--output <plain\|json>` | Output format (default `plain`). |
| `--kind <kind>` | `tags` (default), `topics`, `emotions`, `actions`, `all`. |
| `--max-tags <n>` | Cap the number of tags. |
| `--permissive` | Relax content guardrails. |
| `-q`, `--quiet` | Suppress non-essential output. |
| `--no-color` | Disable colors (also honors `NO_COLOR`). |
| `-h`, `--help` / `-v`, `--version` | Help / version. |

## Exit codes

`0` tags produced · `1` runtime error (model unavailable / refusal) · `2` no input piped or invalid arguments.

## Requirements

macOS 26 (Tahoe) or newer, Apple Silicon, with Apple Intelligence enabled in System Settings.

## Build from source

```bash
git clone https://github.com/Arthur-Ficial/apfel-tag.git
cd apfel-tag
make install
```

## Development

```bash
make test       # build + unit tests + integration tests
make unit       # unit tests only (pure, no model)
make build      # release binary + man page
```

## License

MIT
