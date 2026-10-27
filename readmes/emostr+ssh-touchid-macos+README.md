# ssh-touchid

`ssh-touchid` keeps an SSH private-key passphrase in the local macOS Keychain
and requires Touch ID through `LocalAuthentication` before passing it to the
system `ssh-add`. The passphrase is never placed in a command-line argument or
written to a file.

The Keychain item uses the classic macOS Keychain and its application ACL. This
is intentional: Apple's biometric Keychain ACL uses the Data Protection
Keychain, which is unavailable to a standalone command-line executable unless
it is packaged as an app-like bundle and signed with a provisioning profile.
This project can therefore be built locally without an Apple Developer account.

## Requirements

- macOS 13 or newer
- A Mac with Touch ID configured
- Xcode Command Line Tools (`xcode-select --install`); Swift is not required

## Build and install

```sh
make
sudo make install
```

Homebrew on Apple Silicon commonly uses `/opt/homebrew/bin`; either location is
fine as long as it is in `PATH`.

## Use

Enroll a private key once:

```sh
ssh-touchid enroll ~/.ssh/id_ed25519
```

Add it to the current `ssh-agent` with Touch ID:

```sh
ssh-touchid unlock ~/.ssh/id_ed25519
```

Normal `ssh`, `git`, and `scp` commands then use the unlocked key through the
agent. Touch ID is requested once per `ssh-add`, not for every signature. To
forget the key in the agent, run `ssh-add -d ~/.ssh/id_ed25519`; to delete the
stored passphrase as well, run:

```sh
ssh-touchid remove ~/.ssh/id_ed25519
```

For a shorter command, add an alias to your shell configuration:

```sh
alias ssh-unlock='ssh-touchid unlock ~/.ssh/id_ed25519'
```

## Security notes

- The passphrase briefly exists in the memory of the askpass helper and
  `ssh-add`; that is inherent in unlocking a conventional encrypted key.
- Touch ID is enforced by this executable immediately before its Keychain read;
  it is not an atomic biometric policy attached to the Keychain item. The
  Keychain's own ACL restricts direct access by other executables.
- Once loaded, the standard `ssh-agent` can use the key without another Touch
  ID prompt until the key is removed or the agent exits.
- If you need biometric approval for *every SSH signature*, use an SSH agent
  designed around Secure Enclave keys instead. Conventional OpenSSH private-key
  files cannot be made non-exportable retroactively.
