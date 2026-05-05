Frame extractor
===============

No additional Python libraries are needed, so a venv is not required.

Help:

```
$ ./unpack.py --help
...
$ ./repack.py --help
...
```

Unpacking
---------

Output frames 1 to 10 of `clip.mkv` to the directory `frames` (creating the directory if necessary):

```
$ ./unpack.py 1 10 clip.mkv frames
```

The interval is closed, i.e. the result will be frames 1 to 10 inclusive.

The resulting files will be named `frames/frame-0001.png` to `frames/frame-0010.png`.

It's convention whether the first frame in the video is called frame 1 or frame 0.

By default, numbering starts from 1. If you prefer to start from 0 - you can extract the same set of frames like so:

```
$ ./unpack.py --zero-based 0 9 clip.mkv frames
```

The resulting files will be named `frames/frame-0000.png` to `frames/frame-0009.png`.

If omitted, `start` defaults to the first frame and `end` defaults to the last frame.

Note: the output file name numbering always starts from 1 (or 0 if using `zero-based`), i.e. the original frame number is not used. 

Numbering
---------

If you want the frame number to be overlayed as text onto each output image:

```
$ ./unpack.py --numbered 10 20 clip.mkv frames
```

Note: the overlayed frame number will always starts from 1 (or 0 if using `zero-based`), i.e. the original frame number is not used. 


Repacking
---------

To repack the frames into a high quality H.264 video file:

```
$ ./repack.py --frame-rate=24 --output=repacked.mkv 'frames/*.png'
```

**Important:** the final argument in _not_ a glob to be expanded by the shell, it's a glob that will be passed to `ffmpeg`, so it must be enclosed in quotes.

`ffmpeg` requires that the glob contains a file extension - so it will accept e.g. `frames/*.png` but not `frames/*`.

If required, you can specify the frame rate as a fraction:

```
$ ./repack.py --frame-rate=24000/1001 --output=repacked.mkv 'frames/*.png'
```

Minor bug
---------

There seems to be a bug in Python's `argparse` help output (in Python 3.8.10 at least). It `-f` and `--foo` style arguments as optional even if you specified them as mandatory.

E.g. here it claims the `--frame-rate` and `--output` are optional:

```
$ ./repack.py --help
usage: repack.py [-h] --frame-rate FRAME_RATE --output OUTPUT frames_glob

positional arguments:
  frames_glob           glob for input frames, e.g. 'frames/*.png' (don't forget the quotes)

optional arguments:
  -h, --help            show this help message and exit
  --frame-rate FRAME_RATE
                        output frame rate, e.g. 25 or 24000/1001
  --output OUTPUT       the output video file name, e.g. video.mkv
```

But if you omit them, it complains (as expected):

```
$ ./repack.py 'frames/*.png'
usage: repack.py [-h] --frame-rate FRAME_RATE --output OUTPUT frames_glob
repack.py: error: the following arguments are required: --frame-rate, --output
```

Blender and frame 0 or 1
------------------------

Blender seems a bit schizophrenic when it comes to whether things start at frame 0 or 1.

Go to _New / Video Editing_ and in the lower _Video Sequencer_ - the playhead weirdly is set to 00:00+01 rather than 00:00+00 and if you untick _View / Show Seconds_, it's clear that this point in time is frame 1 (and that you can move the playhead back to 0).

I suppose you _could_ think of the playhead seconds as indicating the end time of the current frame but then I'd have shown it either as a rectangle (rather than a line) that's covers the portion of time covered by the frame or I'd have put the line at the end (or possibly the middle) of rectangle that represents the current frame.

If you go to _Add / Movie_ and select a clip and then the _Start_ frame stays as 1 and if you select _View / Range / Set Frame Range to Clips_ then _End_ frame is set to the count of frames in your clip.

If you then select the clip (or clips if there's also a separately represented audio track) and drag them back two frames the you might expect _Start_ to either go to -1 or stay at 1 (i.e. the first two frames become ignored) if you select _Set Frame Range to Clips_ again but actually _Start_ goes to 0, i.e. decreases by one one frame, but _End_ decreases by 2 frames.

I.e. your video has only become 1 frame shorter despite shifting it back two frames over the apparent start point.

Now, if you press left _Jump to Endpoint_ button then you jump to 0. Whereas previous, it would have jumped to 1. So it's at least consistent with the current _Start_ value.

If you ask it to render a frame range, e.g. 20 to 30 then the resulting files file end up numbered `0020.png` to `0030.png`, i.e. their names reflect their frame number as shown on the Blender playhead. If you e.g. slid things such the sixth frame of your video is now frame 1 and specify the range 1 to 10 then this sixth frame will be output as `0001.png`.
