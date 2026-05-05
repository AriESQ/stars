# double-pendulum
A simultaneous double pendulum simulation.

This was used to make [this video](https://www.youtube.com/watch?v=FFyvYNuKZmA). Each pixel in the
generated images represents a double pendulum. The location of each pixel determines the starting angle of each
leg of the pendulum.

## Build Instructions

This code should all be self-contained. The Makefile by default uses **g++** as the C++ compiler, but that variable can be changed
to **clang++** or any other C++ compiler.

### To build, run:

```
make
```

This will generate an executable file called **pendulums** and when run, this will output `.png` files into the `rendered/` directory.

### To create a video:

I used **ffmpeg** to create a `.mp4` video after rendering has completed.

The command that I ran inside of the `rendered/` directory was:

```
ffmpeg -framerate 30 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4
```
