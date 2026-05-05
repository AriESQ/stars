# Playder - Player for Shaders 

Playder is a tiny Rust tool for rendering fragment shaders into video files using OpenGL.

![CI](https://github.com/k06a/playder/actions/workflows/ci.yml/badge.svg)

## How it works

1. It starts with parsing input arguments with help of [clap](https://github.com/clap-rs/clap)
    ```
    USAGE:
        playder <shader> <width> <height> <fps> <duration>
    ```
2. Then it setups OpenGL with [gl-rs](https://github.com/brendanzab/gl-rs/) and a bit of [glutin](https://github.com/rust-windowing/glutin).

3. Lastly it renders the shader into a video file patching `uniform vec3 iResolution` and `uniform float iTime` shader parameters, similar to [shadertoy](https://shadertoyunofficial.wordpress.com/).

## Installation

1. Ensure you have [Rust](https://www.rust-lang.org/tools/install) installed.

2. Ensure you have [FFmpeg](https://ffmpeg.org/download.html) installed.

3. Then clone the repository and build the project:

    ```sh
    git clone https://github.com/k06a/playder
    сd playder
    cargo build --release
    ```

## Usage

Run Playder with the following command, replacing the parameters as needed:

```sh
cargo run -- shader.frag 1920 1080 30 10 | ffmpeg -y -f rawvideo -pixel_format rgb24 -video_size 1920x1080 -framerate 30 -i pipe:0 -pix_fmt yuv420p -c:v libx265 -tag:v hvc1 output.mp4
```

- `shader.frag` - path to the shader file
- `1920 1080` - video width and height
- `30` - frames per second
- `10` - video duration in seconds

Expected output of this tool is RGB24 each 3 bytes per pixel per frame. You can use ffmpeg to convert it to any format you want.

Example rendering shader in 1920x1080 30fps HEVC of 10 seconds:
```sh
cargo run -- shader.frag 1920 1080 30 10 | ffmpeg -y -f rawvideo -pixel_format rgb24 -video_size 1920x1080 -framerate 30 -i pipe:0 -pix_fmt yuv420p -c:v libx265 -tag:v hvc1 output.mp4
```

Example rendering shader in 7680x3840 60fps HEVC of 10 seconds:
```sh
cargo run -- shader.frag 7680 3840 60 10 | ffmpeg -y -f rawvideo -pixel_format rgb24 -video_size 7680x3840 -framerate 60 -i pipe:0 -pix_fmt yuv420p -c:v libx265 -tag:v hvc1 output.mp4
```

## Contributing

We welcome contributions! Please create a pull request or open an issue on GitHub. 🤝

## License

This project is licensed under the [MIT License](LICENSE).
