# Ansible role to bootstrap Debian and configure schroot

[![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-schroot-blue.svg)](https://galaxy.ansible.com/mejo-/schroot/) [![Build Status](https://travis-ci.org/mejo-/ansible-role-schroot.svg?branch=master)](https://travis-ci.org/mejo-/ansible-role-schroot)

A simple role to bootstrap Debian chroots and configure them in schroot.

# Role variables

```
schroot_location: /srv/chroot

# schroot_chroots:
#   - name: debian_stretch_amd64                # required, no default
#     description: Debian 9 Stretch amd64       # default: <name>
#     type: directory                           # default: directory
#     users: frankie                            # default: empty
#     groups: schroot                           # default: empty
#     root_users:                               # default: empty
#       - alice
#       - bob
#     root_groups:                              # default: empty
#       - alice
#       - bob
#     arch: amd64                               # default: amd64
#     suite: lenny                              # required, no default
#     mirror: http://deb.debian.org/debian      # default: http://deb.debian.org/debian
#     check_gpg: True                           # default: True
#     packages:                                 # default: empty
#       - pck1
#       - pck2
schroot_chroots: []
```

# License

This Ansible role is licensed under the GNU GPLv3 or later.

# Author

Copyright 2018 Jonas Meurer <jonas@freesources.org>
