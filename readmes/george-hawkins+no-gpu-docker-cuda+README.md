Compiling CUDA binaries on a machines without GPUs
==================================================

CUDA is not simply a set of libraries, it also involves it's own compiler called `nvcc` (for more details see the [CUDA LLVM Compiler page](https://developer.nvidia.com/cuda-llvm-compiler) and, more usefully, the _CUDA Compilation Trajectory_ section of the [CUDA Compiler Driver NVCC page](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/) where you can see the interaction between `nvcc` and the host C++ compiler).

I've included a tiny CUDA sample [`add.cu`](add.cu) here (taken from this [NVIDIA blog post](https://developer.nvidia.com/blog/even-easier-introduction-cuda/)).
On a machine set up for compiling CUDA code, you would compile and execute it like so:

```
$ nvcc add.cu -o add_cuda
$ ./add_cuda
Max error: 0.000000
```

However, getting a system to the point where you can run `nvcc` is quite complicated (as can be gauged from the size of the [CUDA installation instructions for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)).

The nature of CUDA means that a surprising number of elements come into play. The different generations of GPUs have characteristics, e.g. a [compute capability](https://developer.nvidia.com/cuda-gpus), that affects what driver can be installed and this in turn determines the compatible CUDA versions. Parsing the necessary information out of the [CUDA toolkit release notes](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html) requires a degree in cryptology (it's easier to search SO for _hopefully_ up-to-date compatibility matrices).

By default, Nvidia drivers will refuse to install on a system that does not have the necessary hardware but you can force installation. This is also true of other CUDA components - the complexity of all the interactions mean that Nvidia try to stop you installing things if the system does not match expectations.

An easier approach is to use one of the Nvidia's [`nvidia/cuda`](https://hub.docker.com/r/nvidia/cuda) Docker images (look for the latest `devel` tag in the "Supported tags" sections of the Docker Hub page).

Docker compose solution
-----------------------

I've included a small `docker-compose` setup here to demonstrate this. Just clone this repo and then:

```
$ cd no-gpu-docker-cuda
$ docker-compose build
```

This may take a long time as several of the necessary Docker layers are over 1GiB.

Once built, you can compile the `add.cu` sample, included here, even if you're running on a machine that has no GPUs (the compilation time will several seconds even for this tiny sample):

```
$ export UID
$ export GID=$(id --group)
$ docker-compose run interactive-cuda nvcc add.cu -o add_cuda
                                      ^^^^ ^^^^^^
...
WARNING: The NVIDIA Driver was not detected.  GPU functionality will not be available.
...
$ ls
Dockerfile  add.cu  add_cuda*  docker-compose.yml
                    ^^^^^^^^^
```

Through the magic of `docker-compose`, this runs `nvcc` within a container on our local `add.cu` file.

Note: `UID` and `GID` need to be made available so that `docker-compose.yml` can pick them up. `UID` already exists as a shell variable, so just needs to be exported, while `GID` needs a value and needs to be exported.

When you run the `nvcc` step, you'll see that the container outputs the warning:

```
WARNING: The NVIDIA Driver was not detected.  GPU functionality will not be available.
   Use the NVIDIA Container Toolkit to start this container with GPU support; see
   https://docs.nvidia.com/datacenter/cloud-native/ .
```

So, obviously, we can't run the resulting `add_cuda` binary locally and unfortunately the Docker magic also runs out at this point. Compiling things didn't require a GPU but running the executable requires giving the Docker container access to a real GPU. If you try it without doing so, it'll fail like this:

```
$ docker-compose run interactive-cuda ./add_cuda
...
WARNING: The NVIDIA Driver was not detected.  GPU functionality will not be available.
...
$ echo $?
139
```

It actually fails silently, you just see the normal `WARNING` message from the container and no output. But our executable segfaulted and Docker communicates that to us via its exit code, i.e. `139`.

To get things to work, you'd need to be running on a system with a GPU and make this GPU available to `dockerd` by setting up the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html) - in particular you need to add the `nvidia-container-runtime` runtime.

Then you would need to update the [`docker-compose.yml`](docker-compose.yml) file to reserve the necessary GPU capability as covered in the [Enabling GPU access with Compose page](https://docs.docker.com/compose/gpu-support/).

This step is simpler if you're doing everything with plain `docker` and within a container, then you just need to add `--gpus all` when running things (as shown in the next section).

Running the raw docker image
----------------------------

If you want to use the `nvidia/cuda` image interactively without `docker-compose`, you have to tell it that the image's platform is `linux/amd64` (assuming you're using a Mac with a non-Intel CPU):

```
$ docker run --interactive --tty --platform linux/amd64 nvidia/cuda:12.1.0-devel-ubuntu22.04
```

I don't know why this isn't required for `docker-compose`.

Once running within the container, you can try things out like so:

```
root@ea43e27ffa9b:/# cd
root@ea43e27ffa9b:~# cat > add.cc
> Paste in the contents of add.cc and enter ctrl-D to finish.
root@ea43e27ffa9b:~# nvcc add.cu -o add_cuda
root@ea43e27ffa9b:~# ./add_cuda 
qemu: uncaught target signal 11 (Segmentation fault) - core dumped
Segmentation fault
```

Here you see both QEMU and the container complaining about the resulting segmentation fault.

If you were on an Intel machine with a GPU (and with Docker configured with the `nvidia-container-runtime` runtime), you could get things to work by using `--gpus all` to give the container access to the host GPU:

```
$ docker run --gpus all --interactive --tty --platform linux/amd64 nvidia/cuda:12.1.0-devel-ubuntu22.04
             ^^^^^^^^^^
```

CUDA assets
-----------

If you want to look at the various assets that make up a CUDA installation, you'll find them under the symbolic link `/usr/local/cuda` in the container:

```
$ docker run --interactive --tty --platform linux/amd64 nvidia/cuda:12.1.0-devel-ubuntu22.04
root@4251c1754915:~# ls -F /usr/local/cuda/include/
CL/         cuda_surface_types.h    cusparse.h                   nvJitLink.h
Openacc/    cuda_texture_types.h    cusparse_v2.h                nvPTXCompiler.h
Openmp/     cuda_vdpau_interop.h    device_atomic_functions.h    nvToolsExt.h
...
root@4251c1754915:~# ls -F /usr/local/cuda/bin
__nvcc_device_query*  compute-sanitizer*  cu++filt*  cuda-gdbserver*  cuobjdump*  nvcc*         nvdisasm*  nvprof*   ptxas*
bin2c*                crt/                cuda-gdb*  cudafe++*        fatbinary*  nvcc.profile  nvlink*    nvprune*
```

As you can see, there are CUDA specific versions of GDB and other tools, not just the compiler.
