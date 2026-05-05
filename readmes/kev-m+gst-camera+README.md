# GStreamer Video as WMF Virtual Camera
This project was inspired by the fact that modern video conference tools, such as Teams or Google Meet, do not allow me to select a lower camera resolution.

My webcam has a wide-angle lens which is very suited to a conference room with multiple participants, but in a one-on-one video call, I occupy only a small portion of the video.

My solution? Create a virtual camera with a reduced video resolution and use that for video conferencing.

## Windows Virtual Camera
The Windows [IMFVirtualCamera interface]([url](https://learn.microsoft.com/en-us/windows/win32/api/mfvirtualcamera/nn-mfvirtualcamera-imfvirtualcamera)) supports 
creating a software camera that can be discovered and used by apps as if it was a hardware capture device.

## Gstreamer
[GStreamer]([url](https://gstreamer.freedesktop.org/)) is a fantastic mdeia processing framework that supports constructing arbitrary pipelines to achieve a variety of tasks.

My idea is to create a virtual camera from a gstreamer pipeline:
```DOS
C:> gst-launch-1.0.exe mfvideosrc ! "video/x-raw, format=NV12, width=800, height=600, framerate=30/1" ! queue ! mf_camera
```

This plugin, once it works, will open up a host of fun media sources that can be published as a camera for other apps to use.

# Installation
Bare-bones instructions. You need to know what you are doing before you start!
- Install Visual Studio (I use VS 2022).
- Checkout this project and load the solution.
- Build the DLL.
- Register the DLL with `regsvr32 gst-camera\x64\Debug\mf_camera.dll` (you must run this as administrator).

# Problems

*Full Disclosure:* I have no practical experience with WMF! I'm relying on online help, tutorials and gut instinct. 
Gemini, DeepSeek, ChatGPT, Copilot, etc seem to be completely out of date and their input is worse than useless.

Right now, the code does not work.

## Example Startup
```DOS
Call to DllMain(DLL_PROCESS_ATTACH)
mf_camera_init: 1
RegisterVirtualCamera '{CBA38424-2226-419C-9705-60D59BE792D3}' ok!
Error: Access is denied.
StartVirtualCamera: Cannot start VCam!
Failed to register virtual camera.
Use Windows high-resolution clock, precision: 1 ms
Setting pipeline to PAUSED ...
Pipeline is live and does not need PREROLL ...
gst_mfcamera_sink_event: 10254
gst_mfcamera_sink_event: 12814
Pipeline is PREROLLED ...
Setting pipeline to PLAYING ...
.
.
/GstPipeline:pipeline0/GstMFVideoSrc:mfvideosrc0.GstPad:src: caps = video/x-raw, format=(string)NV12, width=(int)800, height=(int)600, framerate=(fraction)30/1, pixel-aspect-ratio=(fraction)1/1, colorimetry=(string)1:4:0:1
.
.
I'm plugged, therefore I'm in!!
I'm plugged, therefore I'm in!!
handling interrupt.
Interrupt: Stopping pipeline ...
Execution ended after 0:00:01.083334400
Setting pipeline to NULL ...
Freeing pipeline ...
Call to DllMain(DLL_PROCESS_DETACH)
```

1. The virtual camera can not start.
2. The `MediaSourceActivate` is not being invoked.
3. The virtual camera is not available to other applications.

My suspicion is that I need to determine the video format details (size and colour space) and prime the media source with this 
information BEFORE trying to start the virtual camera.

## Questions

1. When is the most appropriate place in the gstreamer life-cycle to *register* the virtual camera?
2. When the is most appopriate place in the gstreamer life-cycle to *start* the virtual camera?
3. How do I set up the `MediaSource` and `MediaSourceActivate` class with the media format coming from the gstreamer pipeline?
4. How do I synchronise adding frames from the gstreamer pipeline with generating them in the `MediaSource`?
