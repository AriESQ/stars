# FFmpeg Static Build Script

A comprehensive bash script to build a fully static FFmpeg binary on Ubuntu-based systems with support for modern codecs including x264, x265, VP8/VP9, AV1, MP3, Opus, and NVENC hardware acceleration.

## Features

- Creates a **fully static** FFmpeg binary for maximum portability
- Compiles all dependencies from source to ensure compatibility
- Supports modern video codecs:
  - H.264 (via libx264)
  - H.265/HEVC (via libx265)
  - VP8/VP9 (via libvpx)
  - AV1 (via SVT-AV1)
- Supports audio codecs:
  - MP3 (via libmp3lame)
  - Opus
- Includes NVIDIA hardware acceleration (NVENC) support
- Handles pre-existing directories and partial builds
- Automatically resolves common build issues

## Requirements

- Ubuntu or Debian-based Linux distribution
- sudo privileges
- Internet connection
- Basic build tools (will be installed by the script)
- NVIDIA GPU and drivers (optional, for NVENC support)

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ffmpeg-static-build.git
   cd ffmpeg-static-build
   ```

2. Make the script executable:
   ```bash
   chmod +x build_ffmpeg_static.sh
   ```

3. Run the script:
   ```bash
   ./build_ffmpeg_static.sh
   ```

4. Wait for the compilation to complete (this may take a while depending on your system)

5. The static FFmpeg binary will be available at `$HOME/ffmpeg_build/ffmpeg/ffmpeg`

## Configuration

You can modify the following variables at the beginning of the script:

- `INSTALL_DIR`: Where to install the libraries (default: `/usr/local`)
- `SRC_DIR`: Where to download and compile the source code (default: `$HOME/ffmpeg_build`)
- `FFMPEG_VERSION`: Which version of FFmpeg to compile (default: `git` for the latest version)

## Troubleshooting

### Common Issues

#### Missing dependencies
If you encounter errors about missing dependencies, try running:
```bash
sudo apt update
sudo apt install -y build-essential git cmake yasm nasm pkg-config unzip wget
```

#### x265 not found
If the script reports `x265 not found using pkg-config`, the script includes automatic detection and resolution mechanisms. If this still fails, you can manually install x265 development files:
```bash
sudo apt install libx265-dev
```

#### NVENC support
NVENC support requires NVIDIA drivers to be installed. The script attempts to install them if not found, but you may need to install them manually for your specific GPU.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FFmpeg team for their amazing work
- Developers of all the codec libraries
- Everyone who contributed to testing and improving this script