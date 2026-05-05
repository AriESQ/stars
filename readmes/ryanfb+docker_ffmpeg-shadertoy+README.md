# docker_ffmpeg-shadertoy

Dockerfile for [ffmpeg_shadertoy_filter](https://gitlab.com/kriwkrow/ffmpeg_shadertoy_filter) with `xfvb` and Mesa rendering configured.

What's this mean? You can run FFmpeg with GLSL shadertoy filters inside a headless Docker container with software rendering. Combine with [`ffmpeg-gl-transition`](https://github.com/transitive-bullshit/ffmpeg-gl-transition) for GLSL transitions between videos for extra fun.

## Usage

Clone this repository then:

    docker build -t ffmpeg-shadertoy .
    docker run -ti -v $(pwd):/data ffmpeg-shadertoy /bin/bash
    xvfb-run ./ffmpeg -i /data/input.mp4 -vf "shadertoy=example/shader.glsl" -c:v libx264 -preset slow -crf 25 -f mp4 -c:a copy -y /data/output.mp4

Try out other shaders from [Shadertoy](https://www.shadertoy.com/), experiment and enjoy!
