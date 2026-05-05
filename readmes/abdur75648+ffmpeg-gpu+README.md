# ffmpeg-gpu

This repository provides a Dockerized setup for using GPU-based video decoding and encoding with FFmpeg and NVIDIA's NVDEC/NVENC, integrated with TorchAudio.
It includes the necessary setup to leverage GPU acceleration for video processing and a Python script to compare the performance of GPU vs CPU-based video processing.

* Based on the instructions provided by the official PyTorch documentation for FFmpeg integration with GPU support, available [here](https://pytorch.org/audio/main/build.ffmpeg.html#checking-the-intallation).

## Getting Started

Follow these steps to clone the repository, build the Docker image, run the container, and test GPU vs CPU performance.

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/abdur75648/ffmpeg-gpu.git
cd ffmpeg-gpu
```

### 2. Build the Docker Image

Build the Docker image containing FFmpeg with GPU support and TorchAudio:

```bash
docker build -t ffmpeg-gpu .
```

### 3. Run the Docker Container

Run the Docker container interactively:

```bash
docker run --gpus all -it --rm ffmpeg-gpu /bin/bash
```

This command ensures that the Docker container uses GPU acceleration (via `--gpus all`) and allows you to access the container’s shell.

### 4. Verify FFmpeg Installation

Inside the Docker container, verify that FFmpeg supports hardware acceleration for decoding and encoding by running:

```bash
src="https://download.pytorch.org/torchaudio/tutorial-assets/stream-api/NASAs_Most_Scientifically_Complex_Space_Observatory_Requires_Precision-MP4_small.mp4"
ffmpeg -hide_banner -y -vsync 0 \
  -hwaccel cuvid \
  -hwaccel_output_format cuda \
  -c:v h264_cuvid \
  -resize 360x240 \
  -i "${src}" \
  -c:a copy \
  -c:v h264_nvenc \
  -b:v 5M test.mp4
```

This command downloads a sample video from the internet, decodes it using NVDEC (`h264_cuvid`), resizes it, and then re-encodes it with NVENC (`h264_nvenc`). The output is saved as `test.mp4`.

If the command works without errors, FFmpeg has been correctly configured with GPU support.

### 5. Run the Performance Test Script

Next, you can compare the speed of GPU-based video processing vs CPU-based processing using the included Python script.

To run the test, execute:

```bash
python test_FFMPEG_VS_CPU.py
```

This script will run the same video processing pipeline (as shown above) on both the GPU and the CPU and provide a performance comparison.

## Benchmark Results

For a **30-second, 1920x1080** video using a **Testal T4 GPU** and **Intel Xeon Platinum 8259CL CPU**, the following are the results:

- **OpenCV (CPU):** 6.45 sec.
- **Stream Writer (CPU):** 8.45 sec.
- **Stream Writer (GPU):** 2.70 sec.

These benchmarks demonstrate the significant performance improvement when using GPU for video decoding and encoding compared to CPU-based processing

## Requirements

- **NVIDIA GPU** with CUDA support
- **Docker** with GPU support
- **CUDA Toolkit** and NVIDIA drivers installed on your system

## License

This repository is licensed under the [MIT License](LICENSE.md).