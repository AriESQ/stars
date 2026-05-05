# textmode.filters.js

<div align="center">

<!-- Add your banner image here when ready -->
<!-- <img alt="textmode_filters_banner" src="YOUR_BANNER_IMAGE_URL" /> -->

| [![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/) [![WebGL](https://img.shields.io/badge/WebGL2-990000?logo=webgl&logoColor=white)](https://www.khronos.org/webgl/) [![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/) | [![npm version](https://img.shields.io/npm/v/textmode.filters.js.svg)](https://www.npmjs.com/package/textmode.filters.js) [![license](https://img.shields.io/npm/l/textmode.filters.js.svg)](https://github.com/humanbydefinition/textmode.filters.js/blob/main/LICENSE) | [![Discord](https://img.shields.io/discord/1357070706181017691?color=5865F2&label=Discord&logo=discord&logoColor=white)](https://discord.gg/sjrw8QXNks) [![ko-fi](https://shields.io/badge/ko--fi-donate-ff5f5f?logo=ko-fi)](https://ko-fi.com/V7V8JG2FY) [![GitHub-sponsors](https://img.shields.io/badge/sponsor-30363D?logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/humanbydefinition) |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

</div>

textmode.filters.js is a GPU-accelerated image filters plugin for [textmode.js](https://code.textmode.art/). Built with [`WebGL2`](https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext) fragment shaders, it provides a collection of customizable visual effects that run entirely on the GPU for maximum performance.

[Installation](#installation) •
[Usage](#usage) •
[Filters](#filters) •
[Contributing](#contributing)

## Features

- 🚀 **GPU-accelerated** - All filters run on the GPU via WebGL2 fragment shaders
- 🎛️ **Customizable parameters** - Fine-tune each filter to your needs
- 📦 **Lightweight** - Minimal footprint, no external dependencies
- 🤝 **Open to contributions** - Easy to add your own custom filters!

## Installation

```bash
npm install textmode.filters.js
```

You can also use it via CDN:

```html
<!-- ESM -->
<script type="module" src="https://unpkg.com/textmode.js/dist/textmode.esm.js"></script>
<script type="module" src="https://unpkg.com/textmode.filters.js/dist/textmode.filters.esm.js"></script>

<!-- UMD -->
<script src="https://unpkg.com/textmode.js/dist/textmode.umd.js"></script>
<script src="https://unpkg.com/textmode.filters.js/dist/textmode.filters.umd.js"></script>
```

## Usage

### ESM

```javascript
import { textmode } from 'textmode.js';
import { FiltersPlugin } from 'textmode.filters.js';

const t = textmode.create({
	width: 800,
	height: 600,
	plugins: [FiltersPlugin],
});

t.draw(() => {
	// Apply filters to layers
	t.layers.base.filter('brightness', 1.2);
	t.layers.base.filter('contrast', { amount: 1.5 });

	t.background(0);
	// ... draw something ...
});
```

### UMD

```html
<script src="https://unpkg.com/textmode.js/dist/textmode.umd.js"></script>
<script src="https://unpkg.com/textmode.filters.js/dist/textmode.filters.umd.js"></script>
<script>
	const t = textmode.create({
		plugins: [FiltersPlugin],
	});

	t.draw(() => {
		t.layers.base.filter('brightness', 1.3);
	});
</script>
```

## Filters

### `brightness`

Adjust image brightness *(1.0 = normal, >1 = brighter, <1 = darker)*

**Parameters:**

- `amount` - Brightness multiplier  
  Default: `1.0` | Range: `0.0` - `∞`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `contrast`

Adjust image contrast *(1.0 = normal, >1 = more contrast, <1 = less)*

**Parameters:**

- `amount` - Contrast multiplier  
  Default: `1.0` | Range: `0.0` - `∞`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `hueRotate`

Shift colors around the color wheel

**Parameters:**

- `angle` - Rotation angle in degrees  
  Default: `0.0` | Range: `0.0` - `360.0`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `glitch`

Digital glitch effect with RGB channel separation, scanlines, and noise

**Parameters:**

- `amount` - Glitch intensity  
  Default: `0.0` | Range: `0.0` - `∞`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `chromaticAberration`

RGB color channel separation effect that simulates lens distortion

**Parameters:**

- `amount` - Offset amount in pixels  
  Default: `5.0` | Range: `0.0` - `∞`
- `direction` - Direction of the color separation as `[x, y]`  
  Default: `[1.0, 0.0]` (horizontal)

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `pixelate`

Reduce image resolution to create a mosaic/pixelated effect

**Parameters:**

- `pixelSize` - Size of each pixel block in pixels  
  Default: `4.0` | Range: `1.0` - `∞`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `gridDistortion`

Distort a monospaced character grid by varying the width and height of individual cells. Create wave effects, perspective distortions, or other grid warping effects by providing custom factor arrays.

**Parameters:**

- `gridSize` - Grid dimensions as `[columns, rows]`  
  Default: `[80, 40]` | Maximum: `[128, 128]`
- `widthFactors` - Array of distortion values (0-1) for each column  
  Must contain at least as many elements as columns (max 128)
- `heightFactors` - Array of distortion values (0-1) for each row  
  Must contain at least as many elements as rows (max 128)
- `widthVariationScale` - Intensity multiplier for width distortion  
  Default: `0.5` | Range: `0.0` - `∞`
- `heightVariationScale` - Intensity multiplier for height distortion  
  Default: `0.5` | Range: `0.0` - `∞`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `crtMattias`

CRT monitor emulation effect with screen curvature, animated scanlines, blur, vignette, and film grain noise.

**Parameters:**

- `curvature` - Amount of screen curvature/barrel distortion  
  Default: `0.5` | Range: `0.0` - `1.0`
- `scanSpeed` - Speed of the scrolling scanline effect  
  Default: `1.0` | Range: `0.0` - `10.0`
- `time` - Animation time
  Default: `0.0`

**Author:** [@mattiasgustavsson](https://github.com/mattiasgustavsson)  
**Source:** https://github.com/libretro/glsl-shaders/blob/master/crt/shaders/crt-mattias.glsl

---

### `scanlines`

A standalone scanline effect that adds horizontal lines to the image to simulate a CRT display or old monitor. Adjustable density, thickness, and movement speed.

**Parameters:**

- `count` - Number of scanlines
  Default: `300.0` | Range: `10.0` - `∞`
- `lineWidth` - Width of the lines relative to the spacing
  Default: `0.5` | Range: `0.0` - `1.0`
- `intensity` - Opacity of the scanlines
  Default: `0.75` | Range: `0.0` - `1.0`
- `speed` - Scrolling speed of the lines
  Default: `1.0` | Range: `0.0` - `∞`
- `time` - Animation time
  Default: `0.0`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `vignette`

Darkens the edges and corners of the image, drawing focus to the center. Useful for creating a cinematic look or highlighting central content.

**Parameters:**

- `amount` - Intensity of the darkening effect  
  Default: `0.5` | Range: `0.0` - `1.0`
- `softness` - Falloff gradient softness (0 = hard edge, 1 = very soft)  
  Default: `0.5` | Range: `0.0` - `1.0`
- `roundness` - Shape of the vignette (0 = rectangular, 1 = circular)  
  Default: `0.5` | Range: `0.0` - `1.0`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `bloom`

Creates a glow effect around bright areas of the image. Pixels above the brightness threshold emit a soft glow that spreads outward, perfect for creating neon, glowing text, or dreamy effects.

**Parameters:**

- `threshold` - Brightness level above which pixels will glow  
  Default: `0.5` | Range: `0.0` - `1.0`
- `intensity` - Strength of the glow effect  
  Default: `1.0` | Range: `0.0` - `∞`
- `radius` - Size of the glow spread in pixels  
  Default: `4.0` | Range: `1.0` - `∞`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `filmGrain`

Adds an animated film grain/noise texture overlay to simulate vintage film stock or analog video. The multi-layered noise creates an organic, moving grain pattern that's less visible in darker areas, mimicking real film characteristics.

**Parameters:**

- `intensity` - Strength of the grain effect  
  Default: `0.2` | Range: `0.0` - `1.0`
- `size` - Size of grain particles  
  Default: `2.0` | Range: `1.0` - `10.0`
- `speed` - Animation speed of the grain  
  Default: `1.0` | Range: `0.0` - `∞`
- `time` - Animation time parameter  
  Default: `0.0`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `saturation`

Adjust color intensity without affecting luminance. Perfect for creating vivid, oversaturated looks or desaturating to grayscale.

**Parameters:**

- `amount` - Saturation multiplier  
  Default: `1.0` | Range: `0.0` (grayscale) - `∞` (vivid)

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### `posterize`

Reduces the color palette to a limited number of bands, creating a retro quantized look.

**Parameters:**

- `levels` - Number of color levels per channel
  Default: `4.0` | Range: `1.0` - `∞`

**Author:** [@humanbydefinition](https://github.com/humanbydefinition)

---

### Usage examples

```javascript
// Using a single value (shorthand)
t.layers.base.filter('brightness', 1.5);
t.layers.base.filter('hueRotate', 180);

// Using an options object
t.layers.base.filter('contrast', { amount: 0.8 });
t.layers.base.filter('glitch', { amount: 2.0 });

// Chaining multiple filters in sequence
t.layers.base.filter('brightness', 1.2);
t.layers.base.filter('contrast', 1.3);
t.layers.base.filter('hueRotate', 90);

// Chromatic aberration with custom direction
t.layers.base.filter('chromaticAberration', { amount: 10, direction: [1, 1] });

// Pixelate effect
t.layers.base.filter('pixelate', 8);

// Vignette with custom shape
t.layers.base.filter('vignette', { amount: 0.7, softness: 0.4, roundness: 1.0 });

// Bloom for glowing bright areas
t.layers.base.filter('bloom', { threshold: 0.6, intensity: 1.5, radius: 8 });

// Film grain with animation
let time = 0;
t.draw(() => {
	t.layers.base.filter('filmGrain', { intensity: 0.3, size: 2, speed: 1.0, time: time });
	time += 0.016;
});

// Saturation adjustments
t.layers.base.filter('saturation', 0); // Grayscale
t.layers.base.filter('saturation', 1.5); // Vivid colors

// Posterize effect (quantize colors)
t.layers.base.filter('posterize', { levels: 4 });
```

## Adding custom filters

Want to create your own filter? Check out the [Contributing Guide](CONTRIBUTING.md) for detailed instructions on how to add new filters to this library!

The basic structure of a filter shader:

```glsl
#version 300 es
precision highp float;

uniform sampler2D u_texture;    // Input texture
uniform vec2 u_resolution;      // Canvas resolution
uniform float u_yourParam;      // Your custom parameter

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(u_texture, v_uv);

    // Your filter logic here
    vec3 result = color.rgb; // Modify this!

    fragColor = vec4(result, color.a);
}
```

## Contributing

Contributions are welcome and greatly appreciated! 🎉

Whether you want to:

- 🐛 Report a bug
- 💡 Suggest a new filter
- 🔧 Submit a pull request
- 📖 Improve documentation

Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

## Related projects

- **[textmode.js](https://github.com/humanbydefinition/textmode.js)** - The main textmode.js library
- **[code.textmode.art](https://code.textmode.art/)** - Documentation & examples
- **[editor.textmode.art](https://editor.textmode.art/)** - textmode.js web editor

---

<div align="center">

<br />

**[↑ back to top](#textmodefiltersjs)**

</div>
