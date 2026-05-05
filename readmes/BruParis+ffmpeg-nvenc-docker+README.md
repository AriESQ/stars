# FFmpeg with NVIDIA NVENC Docker Image

This repository contains a Dockerfile to build a Docker image for FFmpeg with NVIDIA NVENC support. The image is based on `nvidia/cuda:11.8.0-base-ubuntu20.04` and includes support for hardware acceleration using NVIDIA GPUs.

## Features

- CUDA 11.8
- FFmpeg 5.1
- NVIDIA NVENC hardware acceleration

## Prerequisites

- A machine with an NVIDIA GPU
- NVIDIA drivers installed
- Docker installed

## Build Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/ffmpeg-nvenc-docker.git
   cd ffmpeg-nvenc-docker
   ```
2. Build the Docker image:
   ```bash
   docker build -t ffmpeg-nvenc .
   ```

## Usage

### Example FFmpeg Commands
```bash
docker run --rm --gpus all ffmpeg-nvenc:latest ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset slow -b:v 5M output.mp4
```

### Verify NVENC Support
```bash
docker run --rm --gpus all ffmpeg-nvenc:latest ffmpeg -encoders | grep nvenc
```

### Note for NixOS Users

On NixOS, the --gpus all option may not work as expected. Instead, you can use the --device nvidia.com/gpu=all option to enable GPU access for the container. Additionally, ensure your NixOS system is configured with the hardware.nvidia-container-toolkit module to support NVIDIA GPU containers.

Here’s an example of the adjusted command:
```bash
docker run --rm --device nvidia.com/gpu=all ffmpeg-nvenc:latest ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset slow -b:v 5M output.mp4
```
