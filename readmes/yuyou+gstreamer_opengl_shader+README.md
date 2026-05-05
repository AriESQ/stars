# gstreamer opengl shader samples

```
GST_DEBUG=1,glshader:6 gst-launch-1.0 gltestsrc is-live=true ! glshader vertex="\"`cat vertex.gstreamer`\"" fragment="\"`cat fragment.gstreamer`\"" ! glimagesink sync=false
```


The script above works for GStreamer 1.20.*/1.22.*. But 1.22.8 complains errors about the GLSL version (`#version 330`)

*NOTE*:  The change to make it work is to change

`#version 330`

to

`#version 330 core`
