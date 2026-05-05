# NVIDIA accelerated ffmpeg with docker

## Build

```
docker build -t ffnvidia .
```

## Usaging

Only use nvidia encoder
```
docker run --runtime=nvidia -v host_path:/video  -it ffnvidia ffmpeg -y -i /video/video.mp4  -c:v h264_nvenc output.mp4
```

Use nvidia decoder and encoder 
```
docker run --runtime=nvidia -v host_path:/video  -it ffnvidia ffmpeg -y -hwaccel_device 0 -hwaccel cuvid -c:v h264_cuvid -i /video/video.mp4 -c:v h264_nvenc output.mp4
```

# Accknowledgement 
Usage the `patch` from `https://github.com/keylase/nvidia-patch`

[NVENC patch](patch.sh) removes restriction on maximum number of simultaneous NVENC video encoding sessions imposed by Nvidia to consumer-grade GPUs.

[NvFBC patch](patch-fbc.sh) allows to use NvFBC on consumer-grade GPUs. It should be applied same way as NVENC `patch.sh`, except you have to use `patch-fbc.sh` instead.

Main target operating system is **GNU/Linux**, but for **Windows** support see [**win** (clickable)](win).

