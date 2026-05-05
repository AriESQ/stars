# GPU Accelerated Video Split & Encode

This project provides a Dockerized solution to split a video file into segments and encode each segment using NVIDIA's NVENC hardware acceleration. The setup is based on Ubuntu 20.04 with the NVIDIA CUDA runtime, and it leverages tools such as ffmpeg and OpenCV in Python.

## Features

- **GPU Accelerated Encoding:** Utilizes NVIDIA NVENC (`h264_nvenc`) for fast video encoding.
- **Video Splitting:** Splits a long video into multiple segments of configurable duration.
- **Dockerized Environment:** Ensures a consistent environment with all necessary dependencies pre-installed.

## Files Overview

- **Dockerfile:**  
  Sets up the Docker image based on `nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04`. It installs essential packages such as `ffmpeg`, `python3`, and `pip`, and copies the application code along with a sample `videos` directory.

- **requirements.txt:**  
  Contains the Python dependencies required by the application (e.g., OpenCV, any logging libraries, etc.). _Make sure to define all necessary packages in this file._

- **gpu_split_encode.py:**  
  The main Python script that:
  - Reads the input video using OpenCV to determine frame rate and duration.
  - Calculates the number of segments based on a user-defined segment duration.
  - Uses ffmpeg with NVENC to split and encode each segment.
  - Saves each segment to the specified output directory with sequential filenames.

- **videos Folder:**  
  Contains your video files. The expected structure is:
  ```bash
  videos/ 
  ├── input/ 
  │ └── input_video.mp4 
  └── output/
  ```
Adjust the structure and file names as needed.

## Prerequisites

- **Hardware:** An NVIDIA GPU with supported drivers.
- **Software:**  
- [Docker](https://docs.docker.com/get-docker/)  
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) (to enable GPU support in Docker)

## Building the Docker Image

In the root directory (where the Dockerfile is located), build the Docker image with:

```bash
docker build -t video_splitter_gpu .
```

## Running the Container
Interactive Mode
To launch an interactive bash session inside the container (useful for debugging or manual commands):
```bash
docker run --gpus all -it video_splitter_gpu
```
Once inside, you can manually execute commands or run the Python script as needed.
```bash
python3 gpu_split_encode.py --input /app/videos/input/input_video.mp4 --output /app/videos/output --duration 300
```
If you don't want to run it manually, change CMD of Dockerfild.
```bash
CMD ["python3", "gpu_split_encode.py", "--input", "/app/videos/input/input_video.mp4", "--output", "/app/videos/output", "--duration", "300"]
```

## How It Works
1. Video Analysis: The script opens the input video using OpenCV to determine the frames per second (FPS) and total frame count, which are used to calculate the video's total duration.
2. Segment Calculation: The total video duration is divided by the specified segment duration to determine how many segments will be created.
3. Segment Extraction & Encoding: For each segment, the script uses an ffmpeg command with the following options:
- -ss: Specifies the start time of the segment.
- -t: Sets the duration for the segment.
- -c:v h264_nvenc: Uses the NVIDIA hardware encoder for the video stream.
- -c:a copy: Copies the audio stream without re-encoding.
4. Output: Each segment is saved in the output directory with filenames in the format segment_XXX.mp4.
