dotfiles
========

A collection of *dotfiles* for the applications I use, to configure
them the way I like.

Currently a work-in-progress.

### Local Git configuration

Each machine can have its own local Git configuration under `~/.gitconfig.d`.

Either create a file `~/.gitconfig.d/local.gitconfig` which will be ignored
by this Git repository; or set up a symlink to an existing versioned file.

For example, to use the config for the personal laptop, set up a symlink like
this:

```shell
cd "${HOME}/.gitconfig.d"
ln -sv 'bradfeehan@MacBook.VJ7DN4LW5F.gitconfig' 'local.gitconfig'
```
