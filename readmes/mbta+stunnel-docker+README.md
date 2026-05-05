# Stunnel Docker images

[Stunnel](https://www.stunnel.org/) is a "proxy designed to add TLS encryption
functionality to existing clients and servers without any changes in the
programs' code".

This Dockerfile allows it to run on an Alpine Linux container.


## Usage

``` sh
cd alpine
docker build -t stunnel .
docker run -p <container port>:<local port> -e "STUNNEL_CONF=<configuration>" stunnel
```

## New Versions

If a [new version of Stunnel](https://www.stunnel.org/NEWS.html) ([Alpine package](https://pkgs.alpinelinux.org/package/edge/community/x86_64/stunnel)) or [new version of Alpine Linux](https://alpinelinux.org/releases/) is released, update [.github/workflows/build_alpine_images.yml](https://github.com/mbta/stunnel-docker/blob/main/.github/workflows/build_alpine_images.yml) to include the new versions in the build matrix.
