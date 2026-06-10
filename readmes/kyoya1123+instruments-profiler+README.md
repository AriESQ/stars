# Instruments Profiler

[![License: MIT](https://img.shields.io/github/license/kyoya1123/instruments-profiler)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/kyoya1123/instruments-profiler)](https://github.com/kyoya1123/instruments-profiler/stargazers)
![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)

[日本語版はこちら / Read in Japanese](README.ja.md)

A Claude Code Skill that fully automates Xcode Instruments profiling for iOS/macOS apps — from recording to analysis to actionable recommendations.

## What It Does

This skill automates the entire Instruments profiling workflow:

1. **Device Selection** — Automatically detects simulators and connected devices
2. **Release Build** — Builds optimized Release configuration (Debug builds give inaccurate measurements)
3. **Profiling** — Runs `xctrace record` with SwiftUI or App Launch templates
4. **Symbolication** — Resolves your app's symbols using dSYM for readable stack traces
5. **Analysis** — Parses trace data and generates detailed Markdown reports
6. **Recommendations** — Identifies hot frames, hangs, hitches, and suggests fixes

## Why This Matters

Xcode Instruments is powerful but painful:

- Complex GUI with steep learning curve
- Manual template selection and configuration
- Raw trace data requires expertise to interpret
- No automatic actionable insights

**This skill eliminates all of that.** Just say "profile this app" and get a complete performance report with specific optimization recommendations.

## Installation

### Quick Install (3 steps)

```bash
# 1. Clone to your Skills directory
git clone https://github.com/kyoya1123/instruments-profiler.git ~/.claude/skills/instruments-profiler

# 2. Restart Claude Code
```

## Usage

### Basic Commands

Just tell Claude what you want to measure:

```
/instruments-profiler
```

```
Profile this app with Instruments
```

```
Measure the app launch time
```

```
Run Instruments profiling
```

### Profiling Modes

| Mode | Template | Best For |
|------|----------|----------|
| **SwiftUI** | SwiftUI + Time Profiler + Hangs + Hitches | View updates, CPU usage, UI responsiveness |
| **App Launch** | App Launch | Startup time, library loading, initialization |
| **Time Profiler** | Time Profiler | General CPU profiling |
| **Leaks** | Leaks | Memory leak detection |
| **Allocations** | Allocations | Memory allocation analysis |
| **Animation Hitches** | Animation Hitches | Frame drop detection, scroll performance |
| **Energy Log** | Energy Log | Battery consumption analysis (physical device only) |

## Requirements

- Claude Code
- iOS Simulator or connected iOS device (physical device recommended for stable operation)

## How It Works

```
Device Selection → Release Build → Profiling → Symbolication → Analysis → Report
```

1. **Device Selection** — Detects simulators and connected devices, asks you to choose
2. **Release Build** — Builds optimized Release configuration (Debug builds give inaccurate measurements)
3. **Profiling** — Runs `xctrace record` with your selected template
4. **Symbolication** — Resolves symbols using dSYM for readable stack traces
5. **Analysis** — Parses trace data and generates a detailed Markdown report
6. **Report** — Identifies hot frames, hangs, hitches, and suggests specific fixes

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Permission denied | Developer tools not authorized | System Settings → Privacy → Developer Tools |
| Device not found | Invalid device name/UDID | Run `xctrace list devices` |
| Empty trace | Recording too short | Interact with the app during profiling |
| Symbols show as "unknown" | Missing dSYM | Ensure Release build includes dSYM |
| Cannot find process | Process search failed | Use `--launch` instead of `--attach` |

## Contributing

Issues and pull requests welcome! Please file issues in both English or Japanese.

## License

MIT License - see [LICENSE](LICENSE)
