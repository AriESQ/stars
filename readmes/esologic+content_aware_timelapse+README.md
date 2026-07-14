# Content-Aware Timelapse

![](./assets/art.png)

Create timelapses from video that change speed based on the content found in the video. There are a
few primary modes:

1. Content Mode: boring sections are sped over.
2. Content Cropped: Adds a crop to the most interesting region of the input.

## Usage

The `catcli.py` script hosts the commands to create timelapses.

```
(.venv) devon@ESO-3-DEV-VM:~/Documents/misc/content_aware_timelapse$ python catcli.py --help
Usage: catcli.py [OPTIONS] COMMAND [ARGS]...

  Uses the contents of the frames in source files to create timelapses.

Options:
  --help  Show this message and exit.

Commands:
  benchmark        Utility to benchmark image processing throughput.
  classic          Evenly down-selects the input, taking every N frames until
                   the desired output length is reached.
  content          Numerically scores the input frames based on their
                   contents, then selects the best frames.
  content-cropped  Crops the input to the most interesting region, then
                   selects the best frames of cropped region.
```

Each of the commands have their own `--help` pages as well:

```
(.venv) devon@ESO-3-DEV-VM:~/Documents/misc/content_aware_timelapse$ python catcli.py content-cropped --help
Usage: catcli.py content-cropped [OPTIONS]

  Crops the input to the most interesting region, then selects the best frames
  of cropped region.

Options:
  -bp, --batch-size-pois INTEGER RANGE
                                  Scaled frames for Points of Interest
                                  calculation are sent to GPU for processing
                                  in batches of this size.  [env var:
                                  CAT_BATCH_POIS; default: 600; x>=1;
                                  required]
  -bs, --batch-size-scores INTEGER RANGE
                                  Scaled frames for scoring are sent to GPU
                                  for processing in batches of this size.
                                  [env var: CAT_BATCH_SCORES; default: 100;
                                  x>=1; required]
  -bu, --frame-buffer-size INTEGER RANGE
                                  The number of frames to load into an in-
                                  memory buffer. This makes sure the GPUs have
                                  fast access to more frames rather than have
                                  the GPU waiting on disk/network IO.  [env
                                  var: CAT_FRAME_BUFFER_SIZE; default: 0;
                                  x>=0]
  --backend-scores TEXT           Sets which frame scoring backend is used.
                                  Options below. Either provide index or value:
                                     0: vit-cls
                                     1: vit-attention
                                     2: clip  [env var: CAT_BACKEND_SCORES; default: vit-cls]
  --backend-pois TEXT             Sets which Points of Interest discovery backend is used.
                                  Options below. Either provide index or value:
                                     0: vit-attention  [env var: CAT_BACKEND_POIS; default: vit-attention]
  -de, --deselect INTEGER RANGE   Frames surrounding high scores will be
                                  dropped by a radius that starts with this
                                  value.  [env var: CAT_DESELECT; default:
                                  1000; x>=0]
  -vp, --vectors-path-pois FILE   Intermediate POI vectors will be written to
                                  this path. Can be used to re-run.
  -vs, --vectors-path-scores FILE
                                  Intermediate scoring vectors will be written
                                  to this path. Can be used to re-run.
  -z, --viz-path FILE             A visualisation describing the timelapse
                                  creation process will be written to this
                                  path if given
  -g, --gpu [0|1]                 The GPU(s) to use for computation. Can be
                                  given multiple times.
  Crop Config: [mutually_exclusive, required]
                                  Configures how the video will be cropped.
    -ar, --aspect-ratio ASPECT-RATIO
                                  Crop by aspect ratio in the format
                                  WIDTH:HEIGHT (e.g., 16:9, 4:3, 1.85:1).
    -cr, --crop-resolution WIDTHXHEIGHT
                                  Crops to the most interesting video section
                                  of this size.
  -lo, --layout UNIQUE-INT-MATRIX-2D
                                  If given, this will cut the input into
                                  multiple high scoring regions and composite
                                  the input into a single output video. For
                                  example, setting the aspect ratio to 1:1 and
                                  then setting this variable to 1;0;2 will
                                  created a vertical video, three squares tall
                                  with the best scoring region in the center.
                                  [default: 0; required]
  -ri, --resize-inputs BOOLEAN    If inputs are of different resolutions, the
                                  larger videos are shrunk to the smallest
                                  input resolution for analysis.  [env var:
                                  CAT_RESIZE_INPUTS; default: True]
  Configures the audio that will be put under the resulting video: [mutually_exclusive]
    --audio FILE                  If given, these audio(s) will be added to
                                  the resulting video.  [env var: CAT_AUDIO]
    --audio-directory-random DIRECTORY
                                  The audio files in this directory will be
                                  sorted in a random order and added to
                                  resulting video.  [env var:
                                  CAT_AUDIO_DIRECTORY_RANDOM]
  -or, --output-resolution WIDTHXHEIGHT
                                  Desired resolution of the output video.
                                  Video is resized as the final output step so
                                  resizing will occur after any cropping etc.
                                  [env var: CAT_OUTPUT_RESOLUTION]
  -f, --output-fps FLOAT RANGE    Desired frames/second of the output video.
                                  [default: 60.0; x>=1; required]
  -d, --duration FLOAT RANGE      Desired duration of the output video in
                                  seconds.  [default: 30.0; x>=1; required]
  -o, --output-path FILE          Output will be written to this file.
                                  [required]
  -i, --input FILE                Input file(s). Can be given multiple times.
                                  [required]
  --help                          Show this message and exit.

```

Here's a sample usage. With the virtual env activated, run: 

```
python catcli.py content \
--input "/home/devon/Desktop/Overhead Camera/pwm_driver_module/pwm_drive_module_v1.2.0_1.mp4" \
--input "/home/devon/Desktop/Overhead Camera/pwm_driver_module/pwm_drive_module_v1.2.0_2.mp4" \
--input "/home/devon/Desktop/Overhead Camera/pwm_driver_module/pwm_drive_module_v1.2.0_3.mp4" \
--duration 30 \
--output-fps 60 \
--batch-size 1200 \
--vectors-path ./pwm_module_assembly.hdf5 \
--output-path ./big_mean.mp4
```

## Getting Started

### GPU Acceleration

You need to have NVidia drivers and a CUDA development environment to be able to use GPU
acceleration. These are the steps I ran:

```
wget https://developer.download.nvidia.com/compute/cuda/12.3.0/local_installers/cuda_12.3.0_545.23.06_linux.run
wget https://developer.download.nvidia.com/compute/cudnn/9.4.0/local_installers/cudnn-local-repo-ubuntu2004-9.4.0_1.0-1_amd64.deb
sudo dpkg -i cudnn-local-repo-ubuntu2004-9.4.0_1.0-1_amd64.deb
sudo cp /var/cudnn-local-repo-ubuntu2004-9.4.0/cudnn-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cudnn cudnn-cuda-12
```

Eventually, it'd be great to wrap this in a docker container so only the driver is required. 

### Python Dependencies

Poetry is required to manage Python dependencies. You can install it easily by following the
operating system specific instructions [here](https://python-poetry.org/docs/#installation).

`pyproject.toml` contains dependencies for required Python modules for building, testing, and 
developing. They can all be installed in a [virtual environment](https://docs.python.org/3/library/venv.html) 
using the follow commands:

```
python3.10 -m venv .venv
source ./.venv/bin/activate
poetry install
```

There's also a bin script to do this, and will install poetry if you don't already have it:

```
./tools/create_venv.sh
```

## Problems & Roadmap

1. A massive inefficiency in the application is how fast video can be read from disk. Currently,
for the video that we're working with, I'm able to read the video at ~250 frames per second. I
have tried a few things to make this go faster:

* Using `ffmpeg` over openCV.
* Creating worker processes to parallelize the read.
* Reading from the video in the background and writing the frames to disk as HDF5 arrays, then
loading the HDF5 files back into memory when required.

Nothing has been faster than just straight openCV. An in-memory buffer is also used to do this
load in the background, but then you run into memory limits.

## Developer Guide

The following is documentation for developers that would like to contribute
to Content-Aware Timelapse.

### Pycharm Note

Make sure you mark `content_aware_timelapse` and `./test` as source roots!

### Testing

This project uses pytest to manage and run unit tests. Unit tests located in the `test` directory 
are automatically run during the CI build. You can run them manually with:

```
./tools/run_tests.sh
```

### Local Linting

There are a few linters/code checks included with this project to speed up the development process:

* Black - An automatic code formatter, never think about python style again.
* Isort - Automatically organizes imports in your modules.
* Pylint - Check your code against many of the python style guide rules.
* Mypy - Check your code to make sure it is properly typed.

You can run these tools automatically in check mode, meaning you will get an error if any of them
would not pass with:

```
./tools/run_checks.sh
```

Or actually automatically apply the fixes with:

```
./tools/apply_linters.sh
```

There are also scripts in `./tools/` that include run/check for each individual tool.


### Using pre-commit

Upon cloning the repo, to use pre-commit, you'll need to install the hooks with:

```
pre-commit install --hook-type pre-commit --hook-type pre-push
```

By default:

* black
* pylint
* isort
* mypy

Are all run in apply-mode and must pass in order to actually make the commit.

Also by default, pytest needs to pass before you can push.

If you'd like skip these checks you can commit with:

```
git commit --no-verify
```

If you'd like to quickly run these pre-commit checks on all files (not just the staged ones) you
can run:

```
pre-commit run --all-files
```
