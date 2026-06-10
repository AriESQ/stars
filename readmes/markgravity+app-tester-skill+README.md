# app-tester

A Claude Code skill for testing iOS and macOS app navigation flows — without screenshots.

Builds a persistent graph of your app's screens, instruments Swift files with structured logs and accessibility identifiers, then drives flows end-to-end using the accessibility tree and console output. Screenshots are only taken when a step fails.

## How it works

1. **Discovers** your app's screens by reading the navigation source (Screen enum, coordinator, etc.)
2. **Instruments** each screen with `.accessibilityIdentifier()` and `print("[AppName] [Feature] ScreenName appeared")` logs
3. **Drives flows** by tapping accessibility IDs and confirming transitions via console log lines
4. **Recovers inline** when a step breaks — reads source, fixes instrumentation, finds an alternate path, updates the graph, and continues
5. **Persists** everything in `.tester/app-graph.yaml` (screens) and `.tester/flows/*.yaml` (one file per flow) at the project root, with staleness detection on every run

## Installation

Copy the skill into your personal Claude Code skills directory:

```bash
git clone https://github.com/markgravity/app-tester-skill ~/.claude/skills/app-tester
```

**iOS requirements:**
```bash
brew tap cameroncooke/axe
brew install axe
```

**macOS requirements:** None — uses built-in `osascript` and `log`.

## Usage

Invoke via slash command or let Claude trigger it automatically:

```
/app-tester
test the create game flow
test all flows
instrument screens
rebuild the graph
check that onboarding works end to end
```

## Sensitive credentials

Create a `.env` file at your project root (add to `.gitignore`):

```bash
TEST_USERNAME=your@email.com
TEST_PASSWORD=yourpassword
TEST_PERMISSIONS=camera,location,notifications
SYSTEM_PROMPT_DISMISS=Ask App Not to Track,Don't Allow,Allow Once,Not Now,Dismiss,OK,Allow
```

## Graph files

The skill stores data in `.tester/` at your project root:
- `.tester/app-graph.yaml` — app metadata and screen graph (screens, transitions, accessibility IDs)
- `.tester/flows/<flow-id>.yaml` — one file per named flow (kebab-case filename)

Each run:
- Checks if navigation source files changed since last run
- Diffs old vs new screens and marks affected flows for re-testing
- Updates `lastResult` (PASSED / FAILED / UNKNOWN) in each flow file after each run

## Bundled scripts

| Script | Purpose |
|---|---|
| `navigator.py` | Tap elements by accessibility ID, text, or type (iOS, via idb) |
| `screen_mapper.py` | Read accessibility tree summary (iOS, via idb) |
| `log_monitor.py` | Stream simulator logs (iOS, via xcrun simctl) |
| `app_launcher.py` | Launch / terminate app (iOS, via xcrun simctl) |
| `privacy_manager.py` | Pre-grant permissions (iOS, via xcrun simctl privacy) |
| `dismiss_prompts.py` | Dismiss any system Alert using a configurable label policy |
| `macos_navigator.py` | Click toolbar/window elements (macOS, via osascript) |
| `macos_screen_mapper.py` | Read window/toolbar elements (macOS, via osascript) |
| `macos_log_monitor.py` | Stream app logs (macOS, via `log stream`) |
| `macos_launcher.py` | Launch / terminate macOS .app bundles |

## License

MIT
