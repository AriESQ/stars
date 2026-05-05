<h1 align="center">FFmpeg - drawvg</h1>

<div align="center">

**[Website] │ [Playground] │ [Documentation](#documentation) │ [Installation](#installation)**

</div>

---

<!-- landing:intro -->

drawvg is a [FFmpeg filter], available since [8.1], to render vector graphics
on top of video frames.

[FFmpeg filter]: https://ffmpeg.org/ffmpeg-filters.html
[8.1]: http://ffmpeg.org/index.html#pr8.1

The render is done by executing a script written in its own language, called VGS
(*Vector Graphics Script*). The script consists of a series of commands to
describe 2D graphics, which are rasterized using the [Cairo][libcairo] library.

[libcairo]: https://www.cairographics.org/

VGS is not intended to be used as a general-purpose language. Since its scope is
limited, it prioritizes being concise and easy to use. The syntax is heavily
inspired by languages like [Magick Vector Graphics][MGV], or
[SVG's `<path>`][svg-path]. Some features of the syntax (like using whitespaces
to separate arguments) are also present in languages like
[TCL](https://en.wikipedia.org/wiki/Tcl) or
[shell scripts](https://en.wikipedia.org/wiki/Shell_script).
Many command names are taken from [PostScript]. VGS is fully documented in the
[language reference][langref].

[svg-path]: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/path
[MGV]: https://imagemagick.org/script/magick-vector-graphics.php
[PostScript]: https://en.wikipedia.org/wiki/PostScript
[langref]: https://ayosec.github.io/ffmpeg-drawvg/playground/docs/langref.html

Scripts can use [FFmpeg expressions] to describe graphics dynamically, so they
can compute coordinates based on frame dimensions, frame metadata, generate
random values, read pixel colors, etc.

[FFmpeg expressions]: https://ffmpeg.org/ffmpeg-utils.html#Expression-Evaluation

<!-- /landing:intro -->

For example, to draw a blue circle in the middle of a frame:

```
circle (w / 2) (h / 2) 100
setcolor blue
fill
```

You can experiment with  drawvg scripts in the [playground]. It also has a
gallery of more complex examples, to show most of the capabilities of the
interpreter.

There are other examples in the [repository's website][website], to show how
drawvg can be combined with other FFmpeg filters to modify video frames.

[website]: https://ayosec.github.io/ffmpeg-drawvg/
[playground]: https://ayosec.github.io/ffmpeg-drawvg/playground/

## Documentation

* [Language Reference for VGS][langref]

* [Playground Help](https://ayosec.github.io/ffmpeg-drawvg/playground/docs/manual.html)

## Implementation

The implementation is in the [`drawvg-filter` branch](/../drawvg-filter/) of
this repository.

## Installation

To use the drawvg filter, [you have to compile][ffbuild] the FFmpeg fork in the
[`drawvg-filter` branch](/../drawvg-filter/), and configure FFmpeg with
`--enable-cairo`.

[ffbuild]: https://trac.ffmpeg.org/wiki/CompilationGuide

```console
$ git clone --filter tree:0 -b drawvg-filter https://github.com/ayosec/ffmpeg-drawvg.git

$ cd ffmpeg-drawvg

$ ./configure --enable-cairo ...

$ make -j"$(nproc)"

$ ./ffmpeg ...
```

### Container Image

If you have a container runtime (like Docker or Podman) in a x86-64 machine,
instead of building it locally, you can use the container image built in this
repository:

```console
$ podman pull ghcr.io/ayosec/ffmpeg-drawvg:latest ...
```

For example, to create a video (in the file `output.mp4`) with a rotating
square in the center:

```bash
podman run --rm --volume "$PWD:/mnt" \
    ghcr.io/ayosec/ffmpeg-drawvg \
    ffmpeg \
        -y -f lavfi -i '
            color=teal:qhd:60:5,

            drawvg=
                translate (w/2) (h/2)
                rotate t
                rect -100 -100 200 200
                fill,

            format=yuv420p
        ' \
        -c:v libx265 -crf 18 \
        /mnt/output.mp4
        ```
