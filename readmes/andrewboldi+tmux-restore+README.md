<p align="center">
  <img src="assets/logo.svg" alt="" width="132">
</p>

<h1 align="center">tmux-restore</h1>

<p align="center"><b>Reboot-proof tmux. Your coding agents pick up mid-conversation.</b></p>

<p align="center">
  <a href="https://github.com/andrewboldi/tmux-restore/actions/workflows/test.yml"><img alt="tests" src="https://img.shields.io/github/actions/workflow/status/andrewboldi/tmux-restore/test.yml?branch=main&label=tests&style=flat-square"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/github/license/andrewboldi/tmux-restore?style=flat-square"></a>
  <a href="https://github.com/tmux-plugins/tpm"><img alt="tmux plugin" src="https://img.shields.io/badge/tmux-plugin-1bb91f?style=flat-square&logo=tmux&logoColor=white"></a>
</p>

<p align="center">
  <a href="#what-it-does">What it does</a> ·
  <a href="#install">Install</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="docs/agents.md">Agents</a> ·
  <a href="docs/caveats.md">Caveats</a> ·
  <a href="CONTRIBUTING.md">Contributing</a>
</p>

Ever rebooted and lost a dozen tmux windows, along with the agent conversations running in them?
tmux-restore saves everything every minute and right before shutdown, and puts it back when tmux
starts. Panes running Claude Code, Codex, Gemini CLI, opencode or pi reopen the exact
conversation they were in.

<p align="center">
  <img src="assets/demo.gif" alt="A tmux window with Claude Code, vim and a dev server. tmux is killed and started again: the conversation, vim and the layout come back, and the dev server's command waits on the prompt." width="820">
</p>

## What it does

- **Everything comes back.** Sessions, windows, splits, working directories and scrollback.
- **Agents resume mid-conversation.** Each one reopens its own conversation, with the same flags.
- **Saved at shutdown, not just on a timer.** Every minute, plus once more as the machine goes down.
- **Nothing risky re-runs.** Editors and monitors restart. Anything else (a deploy, a dev server)
  comes back typed on the prompt, waiting for Enter.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/andrewboldi/tmux-restore/main/install.sh | bash
```

It installs whatever is missing (tmux, TPM, the plugins) and turns everything on. Run it again to
update. Rather not run a script? [Install by hand](docs/install-manually.md).

## How it works

1. **Save.** Every minute, [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)
   records every session, window, pane and its scrollback.
2. **Rewrite.** For each pane running an agent, a small adapter finds the conversation's id in
   the agent's own session files and saves the command that resumes it.
3. **Shutdown.** A background service (systemd on Linux, launchd on macOS) saves once more the
   moment the machine starts going down.
4. **Restore.** When tmux starts, [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum)
   puts it all back, and the agents reopen their conversations.

More in [how it works](docs/how-it-works.md). Using another agent? An adapter is one short file;
see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. Built on tmux-resurrect and tmux-continuum by Bruno Sutic and contributors.
