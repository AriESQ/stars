# Gradient Fitter

![Gradient Fitter](public/screenshot.png)

**Live Version:** https://www.bernhard-hoffmann.com/gradient-fitter/

## Examples

- **GLSL** • [ShaderToy](https://www.shadertoy.com/view/sf23zh)
- **JS** • [p5.js Web Editor](https://editor.p5js.org/bhoffmann93/sketches/KP6EBi5KO)

## Description

A browser tool for extracting color gradients from images. Upload an image, draw a sample line or extract a palette, and the tool fits the colors to a mathematical function. The output is a `palette(float t)` function, which returns normalized (0.0-1.0) RGB Values for t (0.0-1.0). Available as GLSL, HLSL, JavaScript, or TypeScript.

### Two modes:

**Line Sample** – drag a line across the image to sample colors along it. Fits either a polynomial (least-squares, configurable degree) or a cosine palette ([Inigo Quilez Cosine Palette](https://iquilezles.org/articles/palettes/)).

**Palette Extract** – extracts dominant colors from the whole image (dominant, generative, or via Colormind AI API), then fits them using one of four methods:

- **Catmull-Rom** smooth spline that passes exactly through each color
- **Linear** straight segments between stops
- **Polynomial** least-squares fitting, can overshoot
- **Cosine** smooth, option to loop perfectly ([Inigo Quilez Cosine Palette](https://iquilezles.org/articles/palettes/))

Both modes support **interpolation in Linear RGB** for Linear and Catmull modes – avoids the dark muddy midpoints you get when interpolating in sRGB space. The output includes the sRGB conversion.
See: [What every coder should know about gamma](https://blog.johnnovak.net/2016/09/21/what-every-coder-should-know-about-gamma/).

**Stops Mode** (Weighted/Uniform) available for Catmull-Rom and Linear – places the stops in relation to the dominance of colors extracted.

## Curve Fitting

**Polynomial** – least-squares fit per RGB channel. Degree 1–6, configurable.

**Cosine** – random search across multiple restarts, best fit by MSE is kept.

**Linear** – direct interpolation between color stops. Stops mode weighted spaces stops by pixel area.

**Catmull-Rom** – smooth spline through the color stops. Stops mode weighted applies area-based spacing.

## About

This project was built with [Claude Code](https://claude.ai/code).

## Stack

- React 19 + Vite
- Tailwind CSS
- [lucide-react](https://lucide.dev/) – icons
- [extract-colors](https://github.com/Namide/extract-colors) – dominant color extraction
- [Colormind API](http://colormind.io/) – AI palette generation (API mode)

## Run locally

```bash
npm install
npm run dev
```
