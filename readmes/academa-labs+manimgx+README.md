<p align="center">
  <a href="https://manimgx.academa.ai">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/logo-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/logo-light.svg">
      <img alt="ManimGX" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/logo-light.svg" width="640">
    </picture>
  </a>
</p>

<p align="center">
  <b>Blazingly fast 3D animation engine for agents, compatible with <a href="https://www.manim.community">Manim CE's API</a>.</b><br>
  Powered by Rust and wgpu. Install with a prompt or pip. Run in the browser.
</p>

<p align="center">
  <b><a href="https://manimgx.academa.ai">Documentation</a></b> ·
  <a href="https://manimgx.academa.ai/user-guide/quickstart/">Quickstart</a> ·
  <a href="https://manimgx.academa.ai/gallery/">Examples</a> ·
  <a href="https://manimgx.academa.ai/reference/">API Reference</a>
</p>

<p align="center">
  <a href="https://coverage.manimgx.academa.ai"><img alt="Test coverage" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fcoverage.manimgx.academa.ai%2Fbadge.json&label=coverage"></a>
  <a href="https://pypi.org/project/manimgx/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/manimgx?color=58c4dd&label=PyPI"></a>
  <a href="https://www.npmjs.com/package/manimgx"><img alt="npm version" src="https://img.shields.io/npm/v/manimgx?color=58c4dd"></a>
  <a href="https://pepy.tech/projects/manimgx"><img alt="PyPI total downloads" src="https://img.shields.io/pepy/dt/manimgx?color=58c4dd&label=PyPI%20downloads"></a>
  <a href="https://www.npmjs.com/package/manimgx"><img alt="npm monthly downloads" src="https://img.shields.io/npm/dm/manimgx?color=58c4dd&label=npm%20downloads"></a>
</p>

<p align="center">
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/quadratic_formula.py"><img alt="The quadratic formula: completing a square by moving colored rectangles and equation terms" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/quadratic_formula.gif" width="32%"></a>
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/fourier_pi.py"><img alt="Fourier series: a chain of rotating arrows draws the outline of π" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/fourier_pi.gif" width="32%"></a>
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/linear_maps.py"><img alt="A matrix moves the plane: a grid, basis arrows and a unit square transform together" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/linear_maps.gif" width="32%"></a>
  <br>
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/derivative.py"><img alt="A tangent slides along a curve as its slope traces the derivative" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/derivative.gif" width="32%"></a>
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/complex_maps.py"><img alt="Complex functions bend a grid into parabolas, circles and rays" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/complex_maps.gif" width="32%"></a>
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/lorenz_attractor.py"><img alt="The Lorenz attractor: nearby trajectories separate as they trace a butterfly in three dimensions" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/lorenz_attractor.gif" width="32%"></a>
  <br>
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/heavy_top.py"><img alt="Three spinning tops precess and nod as their axes trace curves on glass spheres" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/heavy_top.gif" width="32%"></a>
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/hopf_fibration.py"><img alt="The Hopf fibration: colorful linked circles form nested tori as beads travel along them" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/hopf_fibration.gif" width="32%"></a>
  <a href="https://github.com/academa-labs/manimgx/blob/main/examples/catenoid_helicoid.py"><img alt="A rainbow helicoid bends into a catenoid while preserving its intrinsic curvature" src="https://raw.githubusercontent.com/academa-labs/manimgx/main/docs/content/showcase/catenoid_helicoid.gif" width="32%"></a>
</p>

**36.2 seconds of video, rendered in 3.08 seconds.** Across five scenes at 1080p60 on an Apple M4 Pro, ManimGX is **90.6× faster than ManimCE**, **11.5× faster than ManimGL**, and **18.7× faster than Blender Workbench**, from launch to finished MP4. [How it was measured](https://github.com/academa-labs/manimgx/tree/main/benchmarks): the scenes, the settings and every run.

<figure class="mx-benchmark">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://manimgx.academa.ai/images/benchmark-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://manimgx.academa.ai/images/benchmark-light.svg">
    <img alt="Total render times: ManimGX 3.08 s, ManimGL 35.28 s, Blender Workbench 57.61 s, ManimCE 278.83 s, Blender EEVEE 601.40 s" src="https://manimgx.academa.ai/images/benchmark-light.svg" width="100%">
  </picture>
  <p align="center"><sub>All engines use the fastest encoding preset available. Lower is better.</sub></p>
</figure>

**Compare the same scene.** Linked rings at 2.5 seconds, rendered by each engine.

| ManimGX | ManimCE | ManimGL | Blender Workbench | Blender EEVEE |
| :---: | :---: | :---: | :---: | :---: |
| ![Eight linked rings rendered by ManimGX at 2.5 seconds](https://manimgx.academa.ai/images/benchmark-quality/manimgx-light.png) | ![Eight linked rings rendered by ManimCE at 2.5 seconds](https://manimgx.academa.ai/images/benchmark-quality/manim_ce-light.png) | ![Eight linked rings rendered by ManimGL at 2.5 seconds](https://manimgx.academa.ai/images/benchmark-quality/manimgl-light.png) | ![Eight linked rings rendered by Blender Workbench at 2.5 seconds](https://manimgx.academa.ai/images/benchmark-quality/blender_workbench-light.png) | ![Eight linked rings rendered by Blender EEVEE at 2.5 seconds](https://manimgx.academa.ai/images/benchmark-quality/blender_eevee-light.png) |

## Get started

**With a prompt.** Paste into Claude Code, Codex, or Cursor. Your agent handles setup:

```text
Follow https://manimgx.academa.ai/llms.txt.
Install ManimGX, make a 3D animation of the solar system, and open it.
```

**With pip.** Install on macOS, Linux or Windows with Python 3.13+:

```sh
pip install manimgx
```

Fonts, typesetting and video encoding are included.
For editor setup and a guided first animation, follow the
[Quickstart](https://manimgx.academa.ai/user-guide/quickstart/).

## From Python to MP4

Save this as `scene.py`:

```python
import manimgx as m


class Hello3D(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=65 * m.DEGREES, theta=-45 * m.DEGREES)
        self.begin_ambient_camera_rotation(rate=0.5)
        cube = m.Cube(side_length=3, fill_opacity=0.3, stroke_width=2)
        self.play(m.Create(cube), run_time=2)
        self.wait(4)
```

Render it:

```sh
manimgx render scene.py
```

You get `Hello3D.mp4`, a 1080p60 video:

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://manimgx.academa.ai/films/readme-Hello3D.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://manimgx.academa.ai/films/readme-Hello3D-light.svg">
    <img alt="A blue cube is drawn as the camera circles it" src="https://manimgx.academa.ai/films/readme-Hello3D-light.svg#readme" width="100%">
  </picture>
</p>

## Why ManimGX?

**An API for 3D video in the age of agents.** Your agent writes Python using
[Manim CE's API](https://www.manim.community).
ManimGX's Rust + wgpu engine renders the MP4, blazingly fast.

- **Fully statically typed.** Keyword arguments and `.animate` chains included.
- **2D and 3D together.** Surfaces, meshes and moving cameras alongside text, equations
  and plots.
- **Runs in the browser.** `npm install manimgx`. [Pyodide](https://pyodide.org) runs
  Python in a Web Worker; WebGPU renders the scene.
  [Embed a scene](https://manimgx.academa.ai/user-guide/rendering/#embed-in-a-web-page) with no render server.
- **Agent feedback.** [`manimgx inspect`](https://manimgx.academa.ai/user-guide/rendering/#inspect): storyboards and 2D layout checks, at play endings or times you choose.
- **Text and math.** Write LaTeX or Typst. No LaTeX installation needed.
- **Speech in sync.** [Match animations to spoken words](https://manimgx.academa.ai/user-guide/sound-and-voice/)
  with `self.say()`.

## Documentation

**[manimgx.academa.ai](https://manimgx.academa.ai)** has the guides, rendered examples
with source code, and API reference:

- [Quickstart](https://manimgx.academa.ai/user-guide/quickstart/): install, set up your
  editor, and render your first scene.
- [User Guide](https://manimgx.academa.ai/user-guide/the-basics/): learn scenes,
  animations, 3D, text and sound, one idea at a time.
- [Examples](https://manimgx.academa.ai/gallery/): watch complete films and read the
  Python that makes them.
- [API Reference](https://manimgx.academa.ai/reference/): look up classes, methods
  and their typed parameters.
- [Coming from Manim CE](https://manimgx.academa.ai/user-guide/coming-from-manim-ce/):
  adapt existing scenes and check where behavior differs.

For agents, [llms.txt](https://manimgx.academa.ai/llms.txt) provides setup instructions
and links to the documentation as Markdown.

## On the shoulders of giants

[Grant Sanderson](https://www.3blue1brown.com) created
[Manim](https://github.com/3b1b/manim). ManimGX targets the API of
[Manim Community Edition](https://www.manim.community), the widely used
community-maintained fork.

The Rust renderer uses [wgpu](https://wgpu.rs) for native GPU rendering and WebGPU in
the browser. Its 3D lighting is adapted from Google's
[Filament](https://github.com/google/filament): physically based materials,
image-based lighting, ambient occlusion, bloom and AgX tone mapping.
[Typst](https://typst.app) typesets text and math, with
[mitex](https://github.com/mitex-rs/mitex) translating LaTeX input to Typst.
[x264](https://www.videolan.org/developers/x264.html) encodes native video exports as
H.264; [FFmpeg](https://ffmpeg.org) decodes imported audio, using
[libopus](https://opus-codec.org) for Opus.

[Pyodide](https://pyodide.org) runs Python scenes in a browser worker. Linux wheels
bundle [Mesa](https://mesa3d.org)'s lavapipe for Vulkan rendering on the CPU when no
suitable GPU is available.

## Community

Questions, bug reports and feature requests start with an
[issue](https://github.com/academa-labs/manimgx/issues/new/choose).
To contribute, read [Contributing](https://github.com/academa-labs/manimgx/blob/main/.github/CONTRIBUTING.md)
and the [Developer Guide](https://manimgx.academa.ai/developer-guide/).

[Changelog](https://manimgx.academa.ai/changelog/) ·
[Citing ManimGX](https://github.com/academa-labs/manimgx/blob/main/CITATION.cff)

Everyone participating follows the
[Code of Conduct](https://github.com/academa-labs/manimgx/blob/main/.github/CODE_OF_CONDUCT.md).
Report vulnerabilities privately through the
[security policy](https://github.com/academa-labs/manimgx/blob/main/.github/SECURITY.md).

## License

ManimGX's own code is [MIT-licensed](https://github.com/academa-labs/manimgx/blob/main/LICENSE).
Native wheels include x264 and are GPL-3.0-or-later as a whole.

Bundled components retain their licenses: see the
[third-party notices](https://github.com/academa-labs/manimgx/blob/main/LICENSE-THIRD-PARTY),
[Linux renderer notices](https://github.com/academa-labs/manimgx/blob/main/LICENSE-LAVAPIPE),
and the [Noto](https://github.com/academa-labs/manimgx/blob/main/fonts/manimgx-fonts/LICENSE)
and [Noto CJK](https://github.com/academa-labs/manimgx/blob/main/fonts/manimgx-fonts-cjk/LICENSE) font licenses.

This software uses code of [FFmpeg](https://ffmpeg.org) licensed under
[LGPL-2.1-or-later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).
Complete source, including FFmpeg, is in `manimgx-X.Y.Z-source.tar.xz` on each
[GitHub release](https://github.com/academa-labs/manimgx/releases).
