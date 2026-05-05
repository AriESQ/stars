# tl;dr

Running the same script in a containe using `arm64` and `amd64` based images to compare performance impact on an M1.

Running the script in a native image, taking advantage of hypervirtualization, took 5 mins on average. Emulating another platform, using `qemu`, took 25 mins.

# Context

Looking into the impact of `qemu` when using Docker on the M1.

The M1 is an ARM based platform:

```sh
 $ uname -m
arm64
```

Docker Desktop leverages hypervisors to achieve virtualization with the better performance. Container images can be multi-architecture, meaning, you can use the same `Dockerfile` to build images for different platforms.

Docker on the M1 ends up using MacOS hypervisor.framework for arm based images - `arm64` and  `qemu` for intel (`amd64`) ones.

This repository will create an image for each platform, execute an script and measure the time it takes to complete.

Using as base images:

* `node:14.18.0`
* `cypress/included:8.7.0`

Node project releases a multi-arch image, meaning, there're images available for both platforms. Cypress mades available only a intel based image: `amd64` ([no plans for an `arm64`](https://github.com/cypress-io/cypress-docker-images/issues/431)). 

Run `make` commands for building the images first, then execute the benchmark test.

Base images platform:

```sh
$ for i in $(docker images | egrep "node|cypress" | awk '{print $1":"$2}') ; do printf "%s\t%s\n" "$(docker inspect $i | jq -r '.[].Architecture')" "$i" ; done | sort
amd64	cypress/included:8.7.0
arm64	node:14.18.0
✔ ~/src/github.com/osvaldotoja/benchmarking-yarn [main|✔]
13:24 $
```

# Usage

```sh
$ make
build-node                     Build using node base image
build-cypress                  Build using cypress base image
test-node                      Run benchmark using node base image
test-cypress                   Run benchmark using cypress base image
```

# Results

```sh
# time make test-node
|-----------------------------------------|
|------------ RESULTS (seconds) ----------|
|-----------------------------------------|
|                          |        react | 
|     npm_with_empty_cache |       23.360 | 
|      npm_with_all_cached |       15.730 | 
|    yarn_with_empty_cache |       38.450 | 
|     yarn_with_all_cached |       20.043 | 
|-----------------------------------------|

# time make test-cypress
|-----------------------------------------|
|------------ RESULTS (seconds) ----------|
|-----------------------------------------|
|                          |        react | 
|     npm_with_empty_cache |      115.987 | 
|      npm_with_all_cached |       95.997 | 
|    yarn_with_empty_cache |      138.007 | 
|     yarn_with_all_cached |       60.970 | 
|-----------------------------------------|
# 25m
```

second round

```sh
# time make test-node
|-----------------------------------------|
|------------ RESULTS (seconds) ----------|
|-----------------------------------------|
|                          |        react | 
|     npm_with_empty_cache |       23.367 | 
|      npm_with_all_cached |       16.377 | 
|    yarn_with_empty_cache |       40.713 | 
|     yarn_with_all_cached |       22.200 | 
|-----------------------------------------|
aarch64
real    6m28.795s

# time make test-cypress
|-----------------------------------------|
|------------ RESULTS (seconds) ----------|
|-----------------------------------------|
|                          |        react | 
|     npm_with_empty_cache |      122.050 | 
|      npm_with_all_cached |       98.560 | 
|    yarn_with_empty_cache |      136.767 | 
|     yarn_with_all_cached |       60.190 | 
|-----------------------------------------|
x86_64
real    25m4.190s
```

```sh
# time make test-node
|-----------------------------------------|
|------------ RESULTS (seconds) ----------|
|-----------------------------------------|
|                          |        react | 
|     npm_with_empty_cache |       20.277 | 
|      npm_with_all_cached |       13.160 | 
|    yarn_with_empty_cache |       41.310 | 
|     yarn_with_all_cached |       20.573 | 
|-----------------------------------------|
Running on aarch64

real    5m42.122s

# time make test-cypress
|-----------------------------------------|
|------------ RESULTS (seconds) ----------|
|-----------------------------------------|
|                          |        react | 
|     npm_with_empty_cache |      102.847 | 
|      npm_with_all_cached |       86.597 | 
|    yarn_with_empty_cache |      123.123 | 
|     yarn_with_all_cached |       56.497 | 
|-----------------------------------------|
Running on x86_64

real    21m44.595s

Images size:

```sh
12:03 $ docker images | head -n 3
REPOSITORY                                                  TAG                                IMAGE ID       CREATED          SIZE
test-node                                                   14.18.0                            4c5061c6542a   8 minutes ago    910MB
test-cypress/included                                       8.7.0                              76a5b8c01b81   35 minutes ago   2.91GB
```

Images platform:

```sh
$ for i in $(docker images | egrep "^test" | awk '{print $1":"$2}') ; do printf "%s\t%s\n" "$(docker inspect $i | jq -r '.[].Architecture')" "$i" ; done | sort
amd64   test-cypress/included:8.7.0
arm64   test-node:14.18.0
```