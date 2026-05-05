Provision macOS systems with Ansible
----

Goal here is to enable easy provisioning of an Apple Mac laptop, etc to be useful.

The only real playbook is `macos.yml`

The roles, etc do NOT consider operating systems outside of macOS with `homebrew` installed at this time. Some settings 
require _root_ or _administrator_ permissions; generally this are flagged ahead of time.

`macos.yml` - playbook to build a macOS system. 

Function group
----
While the basic play will build a useful macOS system (for me at least), there's 
CLI definable `function` host groups. These apply specific roles, values, etc for
my own use cases. Nothing in this depends on host names. The assumption is host names
are an unreliable source of truth for provisioning a system for a given function.

To apply a function, use `--extra-vars 'function=[\"foo\",\"bar\"]'` to the CLI to 
create the host group, then define the group variables in `group_vars`, and the roles
to be applied in the `macos.yml` playbook.

Using the Ansible Playbook
----
To test the playbook:  
    `ansible-playbook --ask-become-pass -vvvv ./macos.yml --check`

To run it:  
    `ansible-playbook --ask-become-pass ./macos.yml`

Explanations of roles
----
`common`: basic pieces of software that are on every macOS system  
`macos`: basic settings for a macOS system. Configure brew, set screensaver behavior, etc  
`desktop`: default utilities for desktop systems  
`laptop`: default utilities for laptops  
`home`: configure home directory and files  
`devel`: install development tools (intellij, etc)  
`wifi`:  install WiFi specific tools  
`utils`: collected tasks for GUI utilities  
`tools`: collected tasks for CLI utilities  
`vm`: install VM utilities (VirtualBox, vagrant)  
`docker`: install Docker for Desktop etc  

Change Log
----
2021-11-03
- fix vlan creation

2021-11-01
- add function host_group support.
- add netadmin role.

2021-10-30
- unify various pieces under tools/utils that are specifically for software, etc.
- have "devel" be the developer role for devices.
- rewrite of the whole thing to be more modular.
- support roles more effectively by creating roles, and using `import_role` with `tasks_from`
