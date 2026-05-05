# WebAV

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/WebAV-Tech/WebAV)
![NPM downloads](https://img.shields.io/npm/dm/@webav/av-cliper)
[![Release](https://github.com/WebAV-Tech/WebAV/actions/workflows/release.yml/badge.svg)](https://github.com/WebAV-Tech/WebAV/actions/workflows/release.yml)

English | [中文](./README_CN.md)

WebAV is an SDK for **creating/editing** video files on the web platform, built on WebCodecs.

_Visit [WebAV Pro](https://github.com/WebAV-Tech/WebAV-Pro) for more advanced features. You can purchase Pro licenses or request custom outsourcing if needed, which also helps support the ongoing maintenance of this project._

### Features

- Cross-platform: Supports running on Edge and Chrome browsers, as well as in Electron.
- Zero Cost: Fully utilizes client-side computation, eliminating server costs.
- Privacy and Security: No user data is uploaded.
- High Performance: 20x faster than ffmpeg.wasm. For a comparison with native performance, see [WebCodecs Performance Benchmark](https://hughfenghen.github.io/posts/2024/07/27/webcodecs-performance-benchmark/).
- Easy to Extend: Developer-friendly for web developers, easily integrates with Canvas and WebAudio for custom functionality.
- Small Size: Approximately 50KB (MINIFIED + GZIPPED, before tree-shaking).

_Compatible with Chrome 102+_

### Use Cases

- Batch audio and video file processing, such as adding watermarks, dubbing, embedding subtitles
- Building audio and video related products, such as video editing, live streaming, video animation production

## DEMO

The WebAV project offers a variety of quick DEMO experiences. Visit the [DEMO Homepage](https://webav-tech.github.io/WebAV/demo) to check the compatibility of your current device, or click here to experience [Pro advanced features online](https://webav-tech.github.io/WebAV-Pro/demo).

_Tip: The test video resources are hosted on GitHub Pages. Starting a DEMO may require some network loading time._

Here are some feature demos you might be interested in:

- [Video Concatenation](https://webav-tech.github.io/WebAV/demo/2_1-concat-video)
- [Video Editing](https://webav-tech.github.io/WebAV/demo/6_4-video-editor)
- [Live Recording](https://webav-tech.github.io/WebAV/demo/4_2-recorder-avcanvas)
- WebAV + Canvas + WebAudio [Decode and Play Video](https://webav-tech.github.io/WebAV/demo/1_1-decode-video)

## Packages Introduction

### [av-cliper](https://webav-tech.github.io/WebAV/_api/av-cliper/)

`av-cliper` is the foundational SDK for audio and video data processing. It provides basic classes and functions to help developers quickly achieve their target functionalities.

Here is a brief introduction to the core API of `av-cliper`:

- `IClip` is an abstraction for audio/video materials. It parses audio/video, image, and subtitle resources, and provides data for other modules.
- `Sprite<IClip>` attaches spatial and temporal attributes to materials, allowing you to control the spatial position and time offset of the video in the material. This enables multi-material collaboration, animation, and more.
- `Combinator` can add multiple Sprites and, based on their positions, layers, and time offsets, synthesize and output a video file.

<details>
<summary style="cursor: pointer;"> Code Demo: Add a Moving Semi-transparent Watermark to a Video </summary>

```js
import {
  ImgClip,
  MP4Clip,
  OffscreenSprite,
  renderTxt2ImgBitmap,
  Combinator,
} from '@webav/av-cliper';

const spr1 = new OffscreenSprite(
  new MP4Clip((await fetch('./video/bunny.mp4')).body),
);
const spr2 = new OffscreenSprite(
  new ImgClip(
    await renderTxt2ImgBitmap(
      'Watermark',
      `font-size:40px; color: white; text-shadow: 2px 2px 6px red;`,
    ),
  ),
);
spr2.time = { offset: 0, duration: 5e6 };
spr2.setAnimation(
  {
    '0%': { x: 0, y: 0 },
    '25%': { x: 1200, y: 680 },
    '50%': { x: 1200, y: 0 },
    '75%': { x: 0, y: 680 },
    '100%': { x: 0, y: 0 },
  },
  { duration: 4e6, iterCount: 1 },
);
spr2.zIndex = 10;
spr2.opacity = 0.5;

const com = new Combinator({
  width: 1280,
  height: 720,
});

await com.addSprite(spr1);
await com.addSprite(spr2);

com.output(); // => ReadableStream
```

</details>

### [av-canvas](https://webav-tech.github.io/WebAV/_api/av-canvas/)

`av-canvas` relies on the basic capabilities of `av-cliper` and provides a canvas that responds to user operations on Sprites (dragging, scaling, rotating), enabling quick implementation of products like video editing and live streaming workstations.

<details>
<summary style="cursor: pointer;"> Code Demo: Add Video and Text to the Canvas </summary>

```js
import {
  ImgClip,
  MP4Clip,
  VisibleSprite,
  renderTxt2ImgBitmap,
} from '@webav/av-cliper';
import { AVCanvas } from '@webav/av-canvas';

const avCvs = new AVCanvas(document.querySelector('#app'), {
  width: 1280,
  height: 720,
});

const spr1 = new VisibleSprite(
  new MP4Clip((await fetch('./video/bunny.mp4')).body),
);
const spr2 = new VisibleSprite(
  new ImgClip(
    await renderTxt2ImgBitmap(
      'Watermark',
      `font-size:40px; color: white; text-shadow: 2px 2px 6px red;`,
    ),
  ),
);

await avCvs.add(spr1);
await avCvs.add(spr2);

// Export user-edited materials into a video
// (await avCvs.createCombinator()).output()

// Capture stream from the canvas (MediaStream) for live streaming or video recording
// avCvs.captureStream()
```

</details>

### [av-recorder](https://webav-tech.github.io/WebAV/_api/av-canvas/)

`av-recorder` records `MediaStream` and outputs the video file stream in MP4 format.

<details>
<summary style="cursor: pointer;"> Code Demo: Record Camera and Microphone, Output MP4 File Stream </summary>

```js
import { AVRecorder } from '@webav/av-recorder';
const mediaStream = await navigator.mediaDevices.getUserMedia({
  video: true,
  audio: true,
});

const recorder = new AVRecorder(mediaStream);
recorder.start(); // => ReadableStream
```

</details>

## Contributing

### Running the Project

1. Clone the current project locally
2. Execute `pnpm install && pnpm build` in the root directory
3. Change directory to the specific package (e.g., av-cliper) and run `pnpm dev`
4. The path is the filename in the DEMO directory, such as `concat-media.html`
5. Open the DEMO URL in the browser, such as `http://localhost:6066/concat-media.html`
6. Run unit tests for the package with `pnpm test`

### Running the WebAV Site

1. Clone the current project locally
2. Execute `pnpm install && pnpm build` in the root directory
3. Change directory to `doc-site` and run `pnpm dev`
4. Follow the terminal prompts to visit the specified URL

If you are a beginner in the field of web audio and video, you can start by learning the basics:

[Articles by the Author](https://webav-tech.github.io/WebAV/article)  
[Web Audio and Video Knowledge Graph](https://github.com/hughfenghen/WebAV-KnowledgeGraph)

## Sponsor Author

If this project has been helpful to you, please sponsor the author to a milk tea ：）

[Paypal.me](https://paypal.me/hughfenghen)

## Sponsors

We would like to thank our GitHub sponsors who support the development of WebAV:

<div>
  <a href="https://github.com/425776024"><img src="https://github.com/425776024.png" width="50" height="50" alt="425776024" /></a>
  <a href="https://github.com/CheckCoder"><img src="https://github.com/CheckCoder.png" width="50" height="50" alt="CheckCoder" /></a>
  <a href="https://github.com/chunpu"><img src="https://github.com/chunpu.png" width="50" height="50" alt="chunpu" /></a>
  <a href="https://github.com/jundaychan"><img src="https://github.com/jundaychan.png" width="50" height="50" alt="jundaychan" /></a>
</div>

Your support helps us continue to improve and maintain this project!
