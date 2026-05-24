# TouchDeisgner OKLCh

This is a set of Toxes that make it easy to use the OKLCH color space in TouchDesigner.

## Lightness, Chroma, and Hue

OKLCh is based on the OKLAB perceptual color space, designed to be uniform in how humans perceive color differences.

- **Lightness (L)**: Perceived brightness from 0 (black) to 1 (white). Perceptually uniform—equal steps look equally different.

- **Chroma (C)**: Colorfulness/saturation intensity. Capped at ~0.3 because sRGB monitors can only display colors up to about 0.3-0.4 chroma. Higher values produce out-of-gamut colors that clip when converted to RGB.

- **Hue (h)**: Angular position on the color wheel, expressed in radians (-π to π). Radians are used because GLSL trig functions (`atan2`, `sin`, `cos`) work natively in radians, avoiding conversion overhead.

## Toxes

### LChPicker

A simple LCH color picker.

### LChAdjust

This tox supports a few of the common options of the native HSVAdjust top, and supports clamping the lightness and chroma, which can be useful especially in feedback loops.

### LChFeedbackEdge

Based on the same FeedbackEdge from the palette, but with the HSVAdjust swapped out for LCHAdjust. I've left the chroma and lightness capped, as they tend to become way too strong and wash out the image. I've also replaced the default edge color from a normal red to one within the color space.

I find this to be more visually pleasing in comparison to the orginal. The color space in general seems to create far fewer ugly color combinations when compared to hsv.

## Credits

Big thanks to percolated_ for the orginal td implementation, you can pick up the toxes from [his patreon.](https://www.patreon.com/c/percolated/about)

[Checkout his youtube channel](https://www.youtube.com/@percolated_/videos)

Conversion function from <https://bottosson.github.io/posts/oklab/>
