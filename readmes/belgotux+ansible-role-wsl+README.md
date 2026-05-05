WSL
=========

Role to add all the necessary to use wsl correctly : configure global git, configure ssh keys with keychain at login, install minimal required tools, no password for sudo, configure ansible, docker-compose ans aliases if docker desktop is installed on windows

Requirements
------------
- Install Ubuntu via wsl : `wsl --install -d ubuntu`
- Put a username and password
- Install Ansible on the fresh WSL : `sudo apt update && sudo apt install ansible -y`
- Copy the archive or get it directly from ansible-galaxy : `ansible-galaxy install belgotux.wsl`
- Copy the example playbook
- Run the playbook with sudo password ask : `ansible-playbook wsl.yml -K`

Role Variables
--------------

### Needed : 
- `id_rsa_files` : list of ssh keys in the format : `[src_priv: "/mnt/c/Users/$myuser/.ssh/id_rsa", src_pub: "/mnt/c/Users/$myuser/.ssh/id_rsa", dest: "~/.ssh/id_rsa"]`
- `collections_to_install` : list of the ansible collections to install (default `community.docker`)

### Optionnel :
- `links_list` : list of src en dest link to create, for link your personnel script to files folder in ansible for example, format list of src and dest.
- `dns_server` : to set manual DNS server and not take the automatic dns 172.21.32.1
- `my_hostname` : to set a hostname for the distribution
- `dns_search_suffix` : set search DNS suffix

### Automatic : 
- `myuser`: the user defined at installation (default `"{{ ansible_env.HOME }}"`)

Example Playbook
----------------

```yml
- hosts: localhost
  vars:
    myuser: belgotux
    git_global: 
    - param1: user
      param2: name
      value: "belgotux"
    - param1: user
      param2: email
      value: "belgotux@monlinux.net"
    - param1: init
      param2: defaultBranch
      value: "main"
    - param1: core
      param2: editor
      value: "code"
    - param1: credential
      param2: helper
      value: "cache --timeout=57600"
    my_windows_user: "{{myuser}}"
    bash_alias_dir_share: /usr/share
    id_rsa_files:
    - src_priv: "/mnt/c/Users/belgotux/Nextcloud/keys/belgotux"
      src_pub: "/mnt/c/Users/belgotux/Nextcloud/keys/belgotux.pub"
      dest: "$HOME/.ssh/belgotux"
  connection: local
  roles:
    - name: wsl
```


License
-------

[GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

Author Information
------------------

Belgotux
[MonLinux](https://www.monlinux.net)