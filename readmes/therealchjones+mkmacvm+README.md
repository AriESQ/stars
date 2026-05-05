# mkmacvm

Build a simple macOS virtual machine for Parallels Desktop without interaction

## Requirements

mkmacvm is designed and tested to work with:

- macOS 13.1 Ventura
- Paralells Desktop Pro 18.1.1

mkmacvm may work with older, newer, or alternative versions of the above software, but
each release of mkmacvm is only tested with its contemporary versions of macOS
and Parallels Desktop Pro.

Additionally, mkmacvm requires a working `python3` in the path.

## Usage

1. In Terminal, on the macOS host computer:

   ```shell
   sudo ./mkmacvm
   ```

2. There is no step 2.

## Options

Very limited options are available for customization of the virtual machine created by mkmacvm. These are set via environment variables. If the value of the variable is `Y`, then the option is enabled; if it is anything else the option is disabled. These are most easily included on the command line along with the mkmacvm command itself. For example:

```
sudo PASSWORDLESS_SUDO=Y ./mkmacvm
```

### Available options

#### `PASSWORDLESS_SUDO`

Enable the primary (non-root) user to have access to all sudo commands without using their password. Ideal for environments intended to be accessed noninteractively.

## Aims

mkmacvm will provide a simple program that creates a macOS virtual machine on
a macOS host without user interaction beyond initiation.

To meet these aims, mkmacvm should:

- create a macOS virtual machine that is easily accessed and configured from the
  command line (e.g., for scripting and testing)
- itself support a command-line interface (to allow easy inclusion in scripts)
- by default run silently without user interaction
- support very limited options (see #38)
- not require software other than macOS, itself, and the virtual machine
  software
- not leave unnecessary remnants (such as temporary files, mkmacvm
  preferences, etc.) on the host machine
- not unnecessarily change the host system, and not change the host system in
  user-visible ways without interaction
- be a single executable (or script or bundle or similar)
- within the limits of the above, leave virtual machine and macOS system
  settings in their default states

## FAQ

- Why did I get an error that reads:

  ```shell
  Error erasing disk error number (22, 0) An error occurred erasing the disk.
  ```

  I don't know. I don't know what it means or why it happens. However, thanks
  to
  [this post](https://www.blackmanticore.com/659444a81916ef87765c979e4231753d),
  I can tell you that it likely happened after a previous attempt failed, and I
  can recommend rebooting your computer as a reasonable and reliable fix (until
  it happens again).

## Similar Projects

Though it does not share any meaningful source code with them, `mkmacvm` is
heavily inspired by these excellent projects:

- [macdeploystick](https://bitbucket.org/twocanoes/macdeploystick/src/master/):
  configure settings to deploy macOS with minimal interaction and multiple
  hardware and software tools

- [pycreateuserpkg](https://github.com/gregneagle/pycreateuserpkg): create macOS
  user accounts from the command line

Please see [LICENSE](LICENSE) for further acknowledgment of their contributions.

## Contributing

Contributions to `mkmacvm` are encouraged under the guidelines of
the
[Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/)
and the
[GitHub Community Guidelines](https://docs.github.com/en/github/site-policy/github-community-guidelines).
All contributions, discussions, and questions about the project are welcome on the
[issues page](https://github.com/therealchjones/mkmacvm/issues).
