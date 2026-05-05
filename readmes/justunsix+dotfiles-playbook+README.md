# Dotfiles-Playbook

Ansible playbooks for Managing my Linux (Ubuntu, Fedora, Arch), Windows, MacOS
Machines

## Prerequisites

Works on Linux (Fedora, Ubuntu, Arch distributions) and Windows Subsystem for
Linux (WSL2) Ubuntu.

## Usage

Run `bootstrap.sh`.

- When run on a Linux machine, Ansible configures the system it is run on
- When run in WSL, Ansible will configure Windows hosting WSL

### What the Script Does

- Script will check the Linux distribution and run the appropriate Ansible
  playbook and install required software and Ansible requirements for the target
  system.
- Playbook is designed to work with a repository containing dotfiles and
  configuration files like my [dotfiles](https://github.com/justunsix/dotfiles)
  repository. These are configured in the configuration `yaml` files in the
  `group-vars` and `host-vars` folders.

### Overriding Defaults

- Variables used by Ansible can be overridden with a `config.yml` file in the
  root of the repository. Optionally, another configuration `yaml` file
  specified in a repository that contains vars files such as `dotfiles-overlay`
  defined in the `default-config.yml`.
- These files can be helpful to override variables for different machines or
  environments and manage secrets outside of this repository.

## Roadmap

- Make Ansible vars and tasks more flexible instead of hardcoding values with:
  - Use
    [`ansible.builtin.setup`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/setup_module.html)
    settings
    - `ansible_facts['distribution']` for conditionals on Fedora and Ubuntu playbook
  - Build on `default_config.yaml` and override for other Linux distributions
- Set up
  [Ansible logging](https://docs.ansible.com/automation-controller/latest/html/administration/logging.html)
  to more easily read output outside the terminal
- Improve README to describe repository structure and tasks

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

### Built With

- [Ansible](https://www.ansible.com/)
- Inspired by
  [geerlingguy/mac-dev-playbook](https://github.com/geerlingguy/mac-dev-playbook)
  and
  [dotfiles Ansible role](https://github.com/geerlingguy/ansible-role-dotfiles)
