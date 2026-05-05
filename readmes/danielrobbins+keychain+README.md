
Introduction to Keychain
========================

`Keychain` helps you to manage SSH and GPG keys in a convenient and secure
manner. It acts as a frontend to `ssh-agent` and `ssh-add`, but allows you
to easily have one long running `ssh-agent` process per system, rather than
the norm of one `ssh-agent` per login session.

This dramatically reduces the number of times you need to enter your
passphrase. With `keychain`, you only need to enter a passphrase once every
time your local machine is rebooted. `Keychain` also makes it easy for remote
cron jobs to securely "hook in" to a long running `ssh-agent` process,
allowing your scripts to take advantage of key-based logins.

`Keychain` also integrates with `gpg-agent`, so that GPG keys can be cached
at the same time as SSH keys.

Bash Completion
===============

Keychain includes bash completion support for command-line options, SSH keys,
GPG keys, and the `--extended` key format (`sshk:`, `gpgk:`, `host:`).

Most Linux distributions will install the completion script automatically when
you install keychain via your package manager.

For manual installation:

- **System-wide** (requires `bash-completion` package and root access):
  ```
  sudo make install-completions
  ```
  This installs to `/usr/local/share/bash-completion/completions/` by default.
  Use `PREFIX=/usr` for `/usr/share/bash-completion/completions/`.

- **User-only** (no root required):
  ```
  mkdir -p ~/.local/share/bash-completion/completions
  cp completions/keychain.bash ~/.local/share/bash-completion/completions/keychain
  ```

After installation, restart your shell or run:
```
source /etc/bash_completion
```

**Tip:** If pressing tab doesn't show all possible completions when there are
multiple matches (e.g., `sshk:id_<tab>` completes to common prefix but doesn't
list all keys), add this to your `~/.inputrc`:
```
set show-all-if-ambiguous on
```
Then restart your shell or run `bind -f ~/.inputrc`.

Support This Project
====================

Keychain is maintained by [BreezyOps](https://breezyops.com) -
Daniel Robbins' Open Source Innovation Lab. If you find it useful, please consider:

- Starring the repository ⭐
- Joining [Discussions](https://github.com/danielrobbins/keychain/discussions) to share tips and ask questions 💬
- [Supporting development](https://paypal.me/breezyops) to help maintain and improve keychain! ❤️

Your support helps keep this project alive and actively maintained, and supports the creation of future projects. Thank you!

IMPORTANT - GitHub Contributors
===============================

Please submit pull requests against the `master` branch which should track official
releases. Before submitting your PR, please:

1. Make sure that you have [ShellCheck](https://shellcheck.net) enabled in your
   IDE and that your changes don't introduce any bashisms or other non-POSIX things.
   For any *intended* exceptions, such as non-quoting of expanded variables, please
   insert a commented ShellCheck exception to disable the warning, and if not totally
   obvious, then add a comment to the exception like this:

       # shellcheck disable=SC2086 # this is intentional:

   If you do not understand a ShellCheck warning, then don't just blindly disable it.
   Do some research first, make any necessary changes, and then submit your PR.
2. Please use tabs for initial indentation, not spaces.
3. Don't use tabs at the end of lines, such as to align comments. Either use a full
   line to add a comment or add a short comment at the end of a command, separating
   the "#" from the actual command with just a single space.
4. For any new features or options, update `keychain.pod` with documentation on how
   to use the new feature.
