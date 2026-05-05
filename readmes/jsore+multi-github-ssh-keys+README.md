# Multiple SSH Keys For Separate GitHub Accounts

As an example, let's say you have two GitHub accounts:

1. One for personal projects: `jsore@email.com`
2. One for work related projects: `jsore.work@email.com`

You have one machine to develop on but want to use separate SSH keys for each account

This is building on GitHub's articles for [setting up GitHub SSH access on a Mac](https://help.github.com/en/articles/checking-for-existing-ssh-keys)

<br>





## Create the keys

Run `ssh-keygen`, supplying your GitHub account's email address as a comment ( `-C` )

```
( running cd with no arguments moves you $HOME )
~ $ cd
~ $ ssh-keygen -t rsa -b 4096 -C "jsore@email.com"
> Generating public/private rsa key pair.
```

<br>



You'll be asked what to name the keys and where to create them ( include the
whole path with the name )

The names can be anything, just make sure you can tell them apart

```
> Enter file in which to save the key (/Users/jsore/.ssh/id_rsa):
>     /Users/jsore/.ssh/github_personal_rsa
```

<br>



Repeat for however many GitHub accounts you want SSH keys for

```
~ $ ssh-keygen -t rsa -b 4096 -C "jsore.work@email.com"
> Generating public/private rsa key pair.
> Enter file in which to save the key (/Users/jsore/.ssh/id_rsa):
>     /Users/jsore/.ssh/github_work_rsa
```

<br>



I also went ahead and built a key pair to be a 'default' key for single-use VM's

```
~ $ ssh-keygen -t rsa -b 4096 -C "jsore.private@email.com"
> Generating public/private rsa key pair.
> Enter file in which to save the key (/Users/jsore/.ssh/id_rsa):
>     /Users/jsore/.ssh/default_ssh_rsa
```

<br>



Your keys can be checked with `ssh-add -l` and deleted with `ssh-add -D`

<br>





## Dealing with the `ssh-agent`

For macOS 10.12.2 or later, you'll need to update the `~/.ssh/config` file

<br>



Start the agent then open the config file, `touch ~/.ssh/config` first if it doesn't exist

```
~ $ eval "~ $(ssh-agent -s)"
~ $ open .ssh/config "Sublime Text"
```

<br>



This is the config GitHub mentions in their SSH article

```bash
Host *
    AddKeysToAgent yes    # auto-load keys into ssh-agent
    UseKeychain yes       # store the passphrases ( keys ) in your keychain
    IdentityFile ~/.ssh/id_rsa    # <-- equivalent to my github_personal_rsa
```

<br>



Instead, don't default all SSH connections to our GitHub keys, define specific hosts

```bash
Host *
    AddKeysToAgent yes
    UseKeychain yes
    #IdentityFile ~/.ssh/id_rsa
    IdentityFile ~/.ssh/default_ssh_rsa    # for my temporary VM's

# will be used in conjunction with git clone Host variable
# the -Host should be the same as your GitHub account's username
Host github.com-jsore
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_personal_rsa    # this is the private key, not .pub

Host github.ibm.com-sorensen
    HostName github.ibm.com
    User git
    IdentityFile ~/.ssh/github_work_rsa
```

<br>



Add the private keys to the `ssh-agent` and use mac-specific `-K` flag for keychain storage

```
~ $ ssh-add -K ~/.ssh/github_personal_rsa
> Identity added: /Users/jsore/.ssh/github_personal_rsa (jsore@email.com)
~ $ ssh-add -K ~/.ssh/github_work_rsa
> Identity added: /Users/jsore/.ssh/github_work_rsa (jsore.work@email.com)
~ $ ssh-add -K ~/.ssh/default_ssh_rsa
> Identity added: /Users/jsore/.ssh/default_ssh_rsa (jsore.private@email.com)
```

<br>



## Configuring your repos

Add your **public** keys to each of your GitHub accounts - **NEVER** share the private

Copy them to your clipboard then paste them in `github.com/settings/keys` `New SSH key`

```
~ $ pbcopy < ~/.ssh/github_personal_rsa.pub
( paste in GitHub )
~ $ pbcopy < ~/.ssh/github_work_rsa.pub
( paste in Enterprise GitHub )
```

<br>



Now, I only have a couple work-related repos - the majority of my projects are on
my personal account - so, I have a `--global` config setting to use my personal
account's login info and SSH key ( defined in the `.ssh/config` `Host` ) and set
manual definitions for my couple of work repos

```
~ $ git config --global user.name "jsore"
~ $ git config --global user.email "jsore@email.com"
~ $ cd some/dir/for/work
```

<br>



Let's assume I'm making a new pointer to an existing repo in my work GitHub account
and need to `git clone` down to my local machine: I'll need to use the `-Host` variable
I mentioned in the comments in `.ssh/config`

```
work $ git clone git@github.ibm.com-sorensen:sorensen/some/work/project.git
work $ cd project
```

<br>



The `-sorensen` portion is the `-Host` portion, it specifies which `.ssh/config`
`Host` to use

<br>



Just set local username options and you're good to go using your normal dev flow

```
work/project $ git config user.name "sorensen"
work/project $ git config user.email "jsore.work@email.com"

( make some changes to something )

work/project $ git add .
work/project $ git commit -m "some comments"
work/project $ git push -u origin master

( pushes without bugging for a password because auth happens with key pair )
```

<br>



You can check out your local git config options and confirm your remote maps to
the correct SSH `Host` key

```
work/project $ git config --list
> ...
> user.name=jsore                   <-- global settings listed first
> user.email=jsore@email.com        <-- global settings listed first
> ...
> remote.origin.url=git@github.ibm.com-sorensen:sorensen/some/work/project.git  <-- yup, right -Host
> ...
> user.name=sorensen                <-- then overrides to globals are listed
> user.email=jsore.work@email.com   <-- then overrides to globals are listed
> ...
```

<br>



Now I can work on a new project and have the project mapped to my personal account
automatically just by specifying the correct `-Host` when initially connecting it to GitHub

<br>



New project from a local directory:

```
work/project $ cd some/personal/projects
projects $ mkdir new-hotness
projects $ cd new-hotness
projects/new-hotness $ echo "# test text so that file isn't blank" >> README.md
projects/new-hotness $ git init
projects/new-hotness $ git add README.md
projects/new-hotness $ git commit -m "some comments"

( create a new repo on GitHub titled new-hotness, then: )

projects/new-hotness $ git remote add origin git@github.com-jsore:jsore/new-hotness.git
projects/new-hotness $ git push -u origin master

( pushes without bugging for a password because auth happens with key pair )
```

<br>



Cloning a project previously created and backed up on GitHub:

```
$ cd some/personal/projects
projects $ git clone git@github.com-jsore:jsore/another-new-hotness.git
projects $ cd another-new-hotness

( do some changes )

projects/another-new-hotness $ git commit -a -m "some comments"
projects/another-new-hotness $ git push -u origin master
```

<br>



If you happen to forget to assign the correct `-Host` when cloning a project or
adding a new remote, just update the project's `.git/config` file to use the right one

```
...
[remote "origin"]
    url = git@github.com:jsore/this-was-created-wrong.git
...
```

To:

```
[remote "origin"]
    url = git@github.com-jsore:jsore/this-was-created-wrong.git
```

<br><br>