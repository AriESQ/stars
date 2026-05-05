# VCPKG repository for modified FFmpeg port

This repository contains the vcpkg port for FFmpeg, which is modified to include additional features required by Resolume.

### Versions

`master` branch contains the latest version that might still be in internal development

date tags refer to the version from vcpkg that was pulled and modified, version number tags report the first version of Resolume to include this version of FFmpeg.
This does not update with every release of the Resolume software.

### Superseeded repositories

This superseeds the vcpkg-public-registry repository, which was used to host the FFmpeg port before we changed our maintence mode. That repo was in use up until Resolume 7.20.x.

# Notes on how this repo is upgraded by team Resolume

## Upgrade vcpkg and FFmpeg

As we use a custom modified version of FFmpeg, we need to upgrade this port manually. We still like to use the updates from upstream vcpkg so we need to extract those changes and apply our changes on top of that.

## Extract changes from vcpkg

```bash
# Inside the vcpkg repo
git subtree split -P ports/ffmpeg -b ffmpeg-port

# checkout our public registry
git clone https://github.com/resolume/vcpkg-ffmpeg.git
cd vcpkg-ffmpeg

# assuming our modifications on ffmpeg are latest commit on master
git checkout -B ffmpeg-port master^1
git subtree pull <path-to-vcpkg-repo> ffmpeg-port --prefix ports/ffmpeg
git checkout -B ffmpeg-update master
git rebase -i --autosquash ffmpeg-port

### Fix conflicts (probably version in vcpkg.json)

# update version files
git rev-parse HEAD:ports/ffmpeg

# copy this commit and update `versions/f-/ffmpeg.json` to include this version (with new port file version)

# update baseline.json port-version to match

# Then commit these changes
git commit --amend --no-edit versions
git remote add forpr git@github.com/sandercox/vcpkg-ffmpeg.git
git push forpr ffmpeg-update

# Head over to github to start a PR with these changes
```
