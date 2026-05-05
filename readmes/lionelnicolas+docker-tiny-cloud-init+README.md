# Ubuntu docker container running a tiny cloud-init systemd service

This image provides a simple way of faking a cloud-init `systemd` service. I've
developped that mainly for quickly validating shell scripts sent as `user-data`
to cloud-init services.

As this is running `systemd`, it can be used to develop/check systemd services
interactions and dependencies when hacking your deployment scripts (but it only
supports `Ubuntu 16.04 Xenial` packages as this is the base distro).


## How to use it

With this image, it is currently required to start the container using `privileged`
mode to make `systemd` work.

If you want to be able to properly shutdown the container with `docker stop`,
you will need to define a specific stop signal (`SIGRTMIN+3`).

The `user-data` shell script file must be mounted in `/var/lib/cloud/user-data`. To
inject environment variables, you'll need to map it to `/etc/cloud-init.env`.

This repository provides sample files to demonstrate that.

```bash
docker run \
	-it \
	--privileged \
	--stop-signal=SIGRTMIN+3 \
	--volume ${PWD}/sample.user-data:/var/lib/cloud/user-data:ro \
	--volume ${PWD}/sample.env:/etc/cloud-init.env:ro \
	lionelnicolas/tiny-cloud-init \
```


## SSH service

A SSH server is installed (and enabled) in this image. If you want to be able to
log into the container using SSH, you'll need to map your SSH public key file in
`/var/lib/cloud/ssh.pub`.

You just need to add this to your `docker run` command:

```bash
--volume ${HOME}/.ssh/authorized_keys:/var/lib/cloud/ssh.pub:ro
```


## Limits

This *only* support `user-data` shell scripts.

Other `cloud-init` services such as `apt` repositories or packages installation,
hostname configuration, YAML-based cloud-init `user-data` files, or even metadata
servers (`169.254.169.254`) are not supported.


## Build

In order to build this container image instead of using the one on the Docker Hub,
you can use the following command from the root directory of this repository:

```bash
docker build -t lionelnicolas/tiny-cloud-init .
```


## License

This is licensed under the Apache License, Version 2.0. Please see [LICENSE](https://github.com/lionelnicolas/docker-tiny-cloud-init/blob/master/LICENSE)
for the full license text.

Copyright 2016-2017 Lionel Nicolas
