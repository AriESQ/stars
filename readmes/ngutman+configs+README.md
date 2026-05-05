# configs

Personal dotfiles/configs I can share publicly.

## Structure

- `zsh/.zshrc` — public/shareable zsh config (loads optional local `~/.zshrc.work`)
- `tmux/.tmux.conf.local` — my tmux customizations (performance-tuned status line, pane labels, mouse + copy-mode tweaks)
- `tmux/README.md` — tmux features, helper-script notes, and setup details
- `tmux/scripts/` — helper scripts for tmux battery/status caching
- `ghostty/config` — Ghostty terminal configuration
- `pi/agent/settings.json` — pi agent general settings (no auth)
- `pi/agent/extensions/` — global pi extensions such as the minimal footer
- `CHANGELOG.md` — notable shareable config changes in this repo

## Local symlinks

```bash
# zsh
ln -sfn ~/workspace/configs/zsh/.zshrc ~/.zshrc
# keep private/work-only settings local and untracked:
# ~/.zshrc.work

# tmux (using gpakosz base config)
git clone https://github.com/gpakosz/.tmux.git ~/.tmux
ln -sfn ~/.tmux/.tmux.conf ~/.tmux.conf
ln -sfn ~/workspace/configs/tmux/.tmux.conf.local ~/.tmux.conf.local
mkdir -p ~/.tmux/scripts
ln -sfn ~/workspace/configs/tmux/scripts/tmux-battery-cache.sh ~/.tmux/scripts/tmux-battery-cache.sh
ln -sfn ~/workspace/configs/tmux/scripts/tmux-apply-fast-status.sh ~/.tmux/scripts/tmux-apply-fast-status.sh

# ghostty
mkdir -p ~/.config/ghostty
ln -sfn ~/workspace/configs/ghostty/config ~/.config/ghostty/config

# pi settings (no auth)
mkdir -p ~/.pi/agent ~/.pi/agent/extensions
ln -sfn ~/workspace/configs/pi/agent/settings.json ~/.pi/agent/settings.json
ln -sfn ~/workspace/configs/pi/agent/extensions/minimal-footer.ts ~/.pi/agent/extensions/minimal-footer.ts
# then run /reload inside each active pi session
```

## Safety rules before publishing

- Never commit `.env*`, SSH keys, API tokens, cloud creds, cookies, kubeconfigs, or private certs.
- Review all `#()` shell commands in tmux/zsh for accidental secret output.
- Replace usernames/hostnames if they reveal sensitive internal details.
