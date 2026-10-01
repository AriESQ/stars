# AMT630A OSD

Arduino/ESP32 library for controlling the hardware on-screen display (OSD) engine in AMT630A-based composite-video LCD monitor boards.

**Version 0.7.0**

## Project video

[![Watch the AMT630A OSD / Robby HUD project on YouTube](https://img.youtube.com/vi/0eQ94DHOay0/maxresdefault.jpg)](https://youtu.be/0eQ94DHOay0)

[Watch on YouTube](https://youtu.be/0eQ94DHOay0)

The library exposes the AMT630A's five hardware OSD windows as a practical Arduino API for text, custom glyphs, 16-color 4bpp bitmaps, palette animation, opacity/video blending, scaling, blink regions, and window movement. It also includes a Python image converter and optional automation for entering the hidden factory menu on one hardware-tested three-button monitor firmware.

> **Hardware status:** This project is based on hardware testing and reverse engineering of real AMT630A monitor boards. AMT630A products are not all guaranteed to use the same firmware, panel timing, keypad circuit, or exposed I2C connections. Features marked as hardware/firmware-specific should be treated accordingly.

## Features

- Five independently positioned AMT630A OSD windows.
- LargeFont (16x22 cell geometry) and SmallFont (10x16 cell geometry).
- Text drawing, foreground/background colors, centered strings, bars, rectangles, and raw glyph IDs.
- Shared 512-cell Index RAM allocation and inspection helpers.
- LargeFont custom glyphs stored in Font RAM.
- 4bpp bitmap resources using 16x22 LargeFont-compatible tiles.
- 4096-word / 8192-byte Font RAM bitmap allocator.
- Global 16-entry bitmap palette, RGB helpers, palette-0 transparency, and palette animation.
- Global OSD/video blending, opacity, and brightness controls.
- Per-window 1x-4x horizontal and vertical scaling.
- Hardware blink-region support.
- Lightweight window movement and batch-update APIs.
- Python GIF/PNG/JPEG/BMP-to-Arduino bitmap converter with RGB444-aware quantization, shared palettes, memory limits, and preview output.
- LargeFont and SmallFont character-set browser examples.
- Optional GPIO-driven factory-menu keypad automation for compatible stock firmware.

## Installation

### Arduino Library Manager

After this repository has been accepted into the Arduino Library Manager registry:

1. Open Arduino IDE.
2. Choose **Sketch > Include Library > Manage Libraries...** (or open Library Manager in Arduino IDE 2.x).
3. Search for **AMT630A OSD**.
4. Select the desired version and click **Install**.

### Install from ZIP

Download the release ZIP, then in Arduino IDE choose **Sketch > Include Library > Add .ZIP Library...** and select it.

### Install from source

Clone or copy the repository into the `libraries` directory of your Arduino sketchbook. Restart Arduino IDE if it was already open.

## Basic wiring

The library communicates with the AMT630A over I2C. The default ESP32 pins used by `begin()` are:

| Signal | Default ESP32 pin |
| --- | ---: |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

Always connect grounds between the ESP32 and monitor electronics. Do **not** assume every AMT630A monitor exposes the same test pads, voltage levels, supply input, or keypad arrangement; verify your own board before connecting it.

Custom pins and I2C clock can be supplied to `begin()`:

```cpp
display.begin(21, 22, 100000);
```

## Minimal text example

```cpp
#include <AMT630A_OSD.h>

AMT630A_OSD display;

void setup() {
  Serial.begin(115200);

  if (!display.begin()) return;
  if (!display.setFontMode(AMT630A_OSD::LargeFont)) return;
  if (!display.configureWindow(0, 160, 44)) return;

  display.setDisplayOrigin(0, 40, 40);
  display.writeString(0, 0, 0, "HELLO", AMT630A_OSD::White);
  display.setVisible(0, true);
  display.forceUpdate();
}

void loop() {
  display.service();
}
```

## Important stock-firmware / C6 ownership note

The AMT630A uses SYS register `C6` to select whether the internal 8051 MCU or external I2C controls internal registers. On the hardware-tested monitor, the stock firmware periodically accesses internal video/decoder registers and normally expects MCU ownership. Repeatedly taking external ownership during normal stock-firmware operation was found to eventually freeze the complete display pipeline, including both OSD and live composite video.

The library still uses the external-I2C mechanism because it is how the OSD is controlled. On the tested three-button monitor, entering the hidden factory menu before sustained external OSD activity prevented the observed contention/freeze during long-duration testing. The `EnterFactoryMode` example automates that procedure using a 74HC4066 connected across the existing keypad switches.

This factory-menu procedure is **firmware-specific**. It is not automatically invoked by `begin()` and is not inserted into the other examples. If your monitor has different firmware, validate its behavior independently.

## Factory-menu automation

The tested monitor has three physical buttons: Menu, `+`, and `-`, implemented as a passive resistor ladder. Three channels of a 74HC4066 can be placed across those button contacts so an ESP32 can electronically press them while leaving the physical buttons usable when the ESP32/4066 circuit is powered.

Tested 74HC4066 mapping:

| Button | 4066 switch pins | 4066 control | Example ESP32 GPIO |
| --- | --- | --- | ---: |
| `+` | 1, 2 | 13 | 5 |
| Menu | 3, 4 | 5 | 18 |
| `-` | 8, 9 | 6 | 19 |
| Power | VCC 14, GND 7 | | 3.3 V / GND |

The default library sequence is:

`Menu, Menu, Menu, -, Menu, +, -, -, +, +, Menu`

On the tested firmware, the sequence must finish while **Brightness** is active and the final Menu press opens the Factory screen. Hardware testing found 100 ms press / 150 ms gap to be the shortest repeatable timing; the example uses 150 ms / 200 ms for margin.

```cpp
display.configureFactoryMenuControl(18, 5, 19); // Menu, Plus, Minus
display.setFactoryMenuTiming(150, 200);
display.enterFactoryMode();
```

A custom sequence can be supplied with `FactoryMenuStep` and `setFactoryMenuSequence()`.

`setFactoryOSDCoexistence(true)` tells visibility management to preserve OSD-enable/blink bits already set by the stock firmware instead of replacing them. It does not itself enter factory mode.

See `examples/EnterFactoryMode`.

## Fonts and character sets

Font mode is global:

```cpp
display.setFontMode(AMT630A_OSD::LargeFont);
display.setFontMode(AMT630A_OSD::SmallFont);
```

Verified cell geometry:

| Mode | Cell size |
| --- | --- |
| LargeFont | 16 x 22 pixels |
| SmallFont | 10 x 16 pixels |

`writeString()` maps common ASCII characters into the AMT630A's built-in ROM. `writeGlyph()` bypasses ASCII mapping and writes a raw 10-bit glyph ID. The bundled `LargeFontCharacterSetBrowser` and `SmallFontCharacterSetBrowser` examples let you explore the monitor's ROM from the Serial Monitor. The verified SmallFont ROM mapping used by ordinary ASCII begins around `0x1C0`; digits begin at `0x1C1` and letters at `0x1CB`.

## Windows and Index RAM

There are five hardware OSD windows, but all five share **512 Index RAM cells**. Windows may overlap visually; their backing Index RAM allocations must fit in the shared 512-cell pool.

```cpp
display.configureWindow(0, 160, 66);  // pixels; converted to cells
display.setDisplayOrigin(0, 30, 30);
```

Inspection helpers:

```cpp
display.getWindowWidth(0);
display.getWindowHeight(0);
display.getColumns(0);
display.getRows(0);
display.getWindowIndexStart(0);
display.getWindowIndexCells(0);
display.getIndexRAMUsed();
display.getIndexRAMFree();
```

`releaseWindow()` frees a window and allows the library to reallocate the remaining Index RAM regions.

## Drawing text and cells

```cpp
display.clearWindow(0);
display.clearRegion(0, 2, 1, 4, 2);
display.fillRect(0, 0, 0, 8, 1, AMT630A_OSD::Blue);

display.setCell(0, 0, 0, glyph,
                AMT630A_OSD::White,
                AMT630A_OSD::Blue);

display.writeGlyph(0, 1, 0, 0x123,
                   AMT630A_OSD::White,
                   AMT630A_OSD::Transparent);

display.writeString(0, 0, 1, "READY",
                    AMT630A_OSD::Green,
                    AMT630A_OSD::Transparent);

display.writeStringCentered(0, 2, "CENTERED");
display.writeBar(0, 0, 3, 75, 100, 10, AMT630A_OSD::Green);
```

Available text colors are `Transparent`, `White`, `Red`, `Green`, `Blue`, `Cyan`, `Yellow`, and `Black`.

Drawing changes the library's RAM copy and marks affected cells dirty. `updateDisplay()` sends dirty cells; `forceUpdate()` sends all cells in the requested window(s).

## Visibility and service

```cpp
display.setVisible(0, true);
display.setOSDVisible(true);
display.updateDisplay();
```

Normal examples call `display.service()` in `loop()`. It periodically reconciles library-managed visibility state with the hardware. The interval can be changed with `setServiceInterval(milliseconds)`.

## Moving windows

For initial placement use `setDisplayOrigin()`. For animation, `moveWindow()` updates only the position bytes that changed and leaves window geometry and Index RAM allocation intact:

```cpp
display.moveWindow(0, x, y);
```

## Batch updates

```cpp
if (display.beginBatchUpdate()) {
  display.moveWindow(0, x0, y0);
  display.moveWindow(1, x1, y1);
  display.endBatchUpdate();
}
```

Batch calls may be nested. They reduce repeated ownership transitions during a group of operations, but batching should **not** be interpreted as eliminating the stock-firmware ownership issue described above.

## Scaling

All five windows expose the same public 1x-4x scale API:

```cpp
display.setWindowScale(0, 2);      // 2x X and Y
display.setWindowScale(1, 3, 2);   // 3x X, 2x Y
```

```cpp
display.getWindowScaleX(0);
display.getWindowScaleY(0);
```

Scaling applies to text and bitmap windows. Window 0 uses different AMT630A scaler hardware internally; the library hides that difference.

## Blink regions

The hardware-tested primary blink engine targets one rectangular region in one selected OSD window. Coordinates are **1-based cell coordinates**.

```cpp
display.configureBlink(0, 1, 1, 3, 1, 0x10);
display.setBlinkEnabled(true);
```

Individual controls:

```cpp
display.setBlinkWindow(0);
display.setBlinkRegion(1, 1, 3, 1);
display.setBlinkRateRaw(0x10);
display.setBlinkEnabled(true);
```

The raw blink rate is six bits (`0x00`-`0x3F`). Hardware testing established that smaller values blink faster; an exact time conversion has not been calibrated.

## Opacity, brightness, and video blending

These are global OSD controls shared by all five windows:

```cpp
display.setBlendingEnabled(true);
display.setOpacity(4);      // 0 transparent, 7 maximum OSD opacity
display.setBrightness(16);  // 0..31
display.setBlendingEnabled(false);
```

Getters are `isBlendingEnabled()`, `getOpacity()`, and `getBrightness()`.

## Custom LargeFont glyphs

Font RAM can be partitioned between custom LargeFont glyph slots and bitmap storage:

```cpp
display.configureFontRAM(10);  // reserve 10 custom-glyph slots first
```

A custom glyph contains 16 row words:

```cpp
uint16_t icon[AMT630A_OSD::CUSTOM_GLYPH_ROWS] = {
  // 16 row values...
};

display.loadCustomGlyph(0, icon);
display.writeCustomGlyph(0, 0, 0, 0, AMT630A_OSD::White);
```

Custom glyphs are supported only in LargeFont mode. The current library deliberately rejects simultaneous custom-glyph and bitmap loading with `CustomGlyphBitmapConflict`; their safe coexistence mapping is not exposed as a supported public feature.

## Bitmaps

Bitmap mode uses the AMT630A's Font RAM as 4bpp image storage. Public bitmap support is intentionally tied to LargeFont's **16x22 tile geometry**, allowing bitmap and LargeFont ROM-text windows to coexist without changing global character geometry.

A source image is padded to a whole number of 16x22 tiles. The original width and height remain in the generated resource, but storage is based on the padded tile grid.

```cpp
#include <AMT630A_OSD.h>
#include "MyLogo.h"

AMT630A_OSD display;
AMT630A_OSD::BitmapHandle logo = AMT630A_OSD::INVALID_BITMAP_HANDLE;

void setup() {
  display.begin();
  display.setFontMode(AMT630A_OSD::LargeFont);
  display.configureFontRAM(0);  // all 8192 bytes available to bitmaps

  if (!display.loadBitmap(MyLogo, logo)) return;
  if (!display.configureBitmapWindow(0, logo)) return;

  display.setDisplayOrigin(0, 100, 60);
  display.setVisible(0, true);
  display.forceUpdate();
}

void loop() {
  display.service();
}
```

### Font RAM accounting

```cpp
display.getBitmapMemoryTotal();       // 16-bit words
display.getBitmapMemoryUsed();
display.getBitmapMemoryFree();
display.getBitmapMemoryTotalBytes();
display.getBitmapMemoryUsedBytes();
display.getBitmapMemoryFreeBytes();
display.getBitmapCount();
```

`clearBitmaps()` clears loaded bitmap-resource bookkeeping when no configured window is using those resources.

### 4bpp packing

Hardware testing verified four palette-index pixels per 16-bit Font RAM word in this order:

```text
bits 15..12 = leftmost pixel P0
bits 11..8  = P1
bits  7..4  = P2
bits  3..0  = rightmost pixel P3
```

Equivalent packing:

```cpp
(P0 << 12) | (P1 << 8) | (P2 << 4) | P3
```

## Bitmap palette

All bitmap windows share one global 16-entry hardware palette.

```cpp
display.setBitmapPaletteColor(1, 255, 0, 0);
display.setBitmapPaletteColor(2, 255, 128, 0);
display.setBitmapPaletteColorRaw(3, 0x0F0);
display.setBitmapPalette0Transparent(true);
```

Raw palette values use the AMT's nominal 12-bit `BBBB GGGG RRRR` layout. `rgbToBitmapColor()` converts normal 8-bit RGB values to the raw representation.

`loadBitmap(bitmap, handle)` applies the resource palette by default. Because the palette is global, loading a second bitmap with a different palette can recolor an already-visible bitmap. For simultaneous resources, convert them against the same shared palette or call `loadBitmap(bitmap, handle, false)` and manage the palette explicitly.

Palette cycling can animate an image without rewriting Font RAM. See `AnimationPaletteDemo1` and `AnimationPaletteDemo2`.

# Bitmap Converter

The converter is included in:

```text
tools/bitmap_converter/amt630a_bitmap_converter.py
```

It converts the **first frame** of GIF files, or PNG/JPEG/BMP images, into a C++ header defining an `AMT630A_OSD::Bitmap`.

## Requirements

- Python 3
- Pillow

Install the Python dependency with:

```bash
python -m pip install -r tools/bitmap_converter/requirements.txt
```

or:

```bash
python -m pip install Pillow
```

## Basic conversion

```bash
python tools/bitmap_converter/amt630a_bitmap_converter.py input.png output.h --name MyLogo
```

Then place `output.h` in the Arduino sketch folder and include it:

```cpp
#include "output.h"
```

The generated symbol is the value supplied to `--name`; if omitted, the converter sanitizes the output filename stem and uses that as the symbol name.

## Converter command line

```text
amt630a_bitmap_converter.py INPUT OUTPUT [options]
```

Positional arguments:

| Argument | Meaning |
| --- | --- |
| `INPUT` | GIF, PNG, JPEG, or BMP source. GIF uses the first frame. |
| `OUTPUT` | Generated Arduino/C++ `.h` file. |

Options:

| Option | Meaning |
| --- | --- |
| `--name NAME` | C/C++ bitmap symbol name. Default: sanitized output filename stem. |
| `--font large` | Target bitmap geometry. Only `large` is currently supported; it means 16x22 tiles. |
| `--max-bytes N` | Reject output if packed Font RAM data exceeds N bytes. Default: 8192. |
| `--max-colors N` | Maximum total palette entries, including transparent index 0. Range 2-16; default 16. |
| `--opaque` | If the source has no transparency, allow palette index 0 to be an opaque color instead of reserving it for transparent padding. |
| `--palette FILE.json` | Map the image to an existing shared JSON palette instead of auto-quantizing a new palette. |
| `--export-palette FILE.json` | Save the final palette as JSON for reuse by other images. |
| `--preview FILE.png` | Write a PNG preview based on the converter's measured AMT/display calibration. Existing preview files are replaced. |

## Memory sizing

The AMT630A Font RAM contains 4096 16-bit words = 8192 bytes. A bitmap uses 4 bits/pixel and is padded to complete 16x22 tiles. The converter reports:

- source dimensions,
- tile grid,
- padded hardware dimensions,
- Font RAM words,
- Font RAM bytes.

Use `--max-bytes` when some Font RAM is unavailable to the bitmap allocator:

```bash
python tools/bitmap_converter/amt630a_bitmap_converter.py robot.png robot.h \
  --name robot \
  --max-bytes 4096
```

The converter exits with an error instead of generating an oversized bitmap.

## Transparency

By default, palette index 0 is reserved for transparent source pixels and transparent tile padding. A source pixel is treated as transparent when its alpha is below 128.

For a fully opaque source, `--opaque` allows index 0 to be used as a visible color:

```bash
python tools/bitmap_converter/amt630a_bitmap_converter.py logo.png logo.h --opaque
```

If the source itself contains transparency, index 0 remains transparent even when `--opaque` is supplied.

## Color quantization and AMT display calibration

The converter does not simply quantize to ordinary 24-bit RGB and then truncate. It first works on colors representable by the AMT RGB444 palette and uses a perceptual CIE Lab distance metric. Its palette selection/refinement is designed to use the available slots where they reduce image error rather than reserving particular colors.

The converter also contains a measured transfer calibration for the tested AMT630A/LCD combination. The observed neutral brightness relationship was approximately:

| Intended brightness | AMT nibble code |
| ---: | ---: |
| 0% | 0 |
| 25% | 2.5 |
| 50% | 3.5 |
| 75% | 5.5 |
| 100% | 15 |

The calibration is interpolated independently for red, green, and blue. Palette optimization therefore works from predicted displayed appearance rather than assuming linear RGB444 output. `--preview` applies the inverse calibration to show the converter's prediction of the resulting display colors.

This calibration is based on the tested display and should not be assumed identical on every LCD panel or AMT630A product.

## Shared palettes for multiple bitmaps

Because every bitmap window shares one hardware palette, multiple images displayed simultaneously should normally be converted against one shared palette.

Create the first image and export its palette:

```bash
python tools/bitmap_converter/amt630a_bitmap_converter.py first.png first.h \
  --name first \
  --export-palette hud_palette.json
```

Map another image to that exact palette:

```bash
python tools/bitmap_converter/amt630a_bitmap_converter.py second.png second.h \
  --name second \
  --palette hud_palette.json
```

The palette JSON contains `palette0_transparent` plus a list of RGB hex colors. The converter accepts colors in `#RRGGBB` form or three-element RGB arrays when reading a palette file.

## Preview output

```bash
python tools/bitmap_converter/amt630a_bitmap_converter.py input.png output.h \
  --preview output_preview.png
```

The preview is reconstructed from the exact palette indexes and calibrated palette values used for the generated header. If the preview path already exists, it is intentionally replaced so repeated conversions do not leave a stale preview.

## Complete converter example

```bash
python tools/bitmap_converter/amt630a_bitmap_converter.py radar.gif radar.h \
  --name radar \
  --max-colors 16 \
  --max-bytes 8192 \
  --export-palette radar_palette.json \
  --preview radar_preview.png
```

# API Reference

## Initialization and global configuration

| API | Description |
| --- | --- |
| `begin(sdaPin=21, sclPin=22, i2cClock=100000)` | Initialize Wire/I2C, capture AMT state, and configure global OSD settings. |
| `setDisplaySize(width, height)` | Set the nominal display bounds used by the library. |
| `setFontMode(mode)` | Select global `LargeFont` or `SmallFont`. |
| `getFontMode()` | Return current font mode. |
| `getDisplayWidth()`, `getDisplayHeight()` | Return configured display dimensions. |

## Window management

| API | Description |
| --- | --- |
| `configureWindow(window, width, height, mode=TextMode)` | Configure a text/general window using pixel dimensions converted to the current cell geometry. |
| `configureBitmapWindow(window, bitmapHandle)` | Configure a bitmap window from a loaded bitmap's tile grid. |
| `releaseWindow(window)` | Release a configured window and its Index RAM allocation. |
| `isWindowConfigured(window)` | Test whether a window is configured. |
| `getWindowMode(window)` | Return `TextMode` or `BitmapMode`. |
| `getWindowBitmap(window)` | Return the bitmap handle associated with a bitmap window. |
| `setDisplayOrigin(window, x, y)` | Set initial/static pixel position. |
| `moveWindow(window, x, y)` | Lightweight position-only update. |
| `getWindowX/Y/Width/Height()` | Inspect window position and dimensions. |
| `getColumns()`, `getRows()` | Inspect cell/tile dimensions. |
| `getCharacterWidth/Height()` | Inspect active cell geometry for the window. |
| `getWindowIndexStart/Cells()` | Inspect Index RAM allocation. |
| `getIndexRAMUsed/Free()` | Inspect shared 512-cell Index RAM usage. |

## Drawing

| API | Description |
| --- | --- |
| `clearWindow(window)` | Clear every cell in a window. |
| `clearRegion(window,x,y,w,h)` | Clear a rectangular cell region. |
| `fillRect(window,x,y,w,h,color)` | Fill cell backgrounds in a region. |
| `setCell(...)` | Set raw glyph and text attributes for one cell. |
| `writeGlyph(...)` | Write a raw glyph ID. |
| `writeString(...)` | Write C string or Arduino `String` with foreground/background colors. |
| `writeStringCentered(...)` | Center text on a window row. |
| `getTextWidth(...)` | Return text width in pixels for the current mode. |
| `writeBar(...)` | Draw a cell-based value bar. |
| `updateDisplay([window])` | Flush dirty cells. |
| `forceUpdate([window])` | Force all cells to hardware. |

## Visibility and maintenance

| API | Description |
| --- | --- |
| `setVisible(window, enabled)` | Show/hide one configured window. |
| `isVisible(window)` | Return library visibility state. |
| `setOSDVisible(enabled)` | Global OSD visibility. |
| `isOSDVisible()` | Return global visibility state. |
| `service()` | Periodic visibility-state reconciliation used by normal examples. |
| `setServiceInterval(ms)` | Change service interval. |
| `setFactoryOSDCoexistence(enabled)` | Preserve factory-managed visibility/blink bits while applying library visibility. |

## Batch updates and movement

| API | Description |
| --- | --- |
| `beginBatchUpdate()` | Begin/nest a group of register operations under one ownership interval. |
| `endBatchUpdate()` | End a batch; outermost call restores ownership. |
| `isBatchUpdateActive()` | Test batch state. |
| `moveWindow(...)` | Efficiently update only changed position bytes. |

## Custom glyph / Font RAM

| API | Description |
| --- | --- |
| `configureFontRAM(customGlyphCount)` | Reserve LargeFont custom-glyph slots; remaining Font RAM is available for bitmaps. |
| `getCustomGlyphCapacity()` | Reserved custom-glyph slot count. |
| `getCustomGlyphCount()` | Number of loaded custom glyphs. |
| `loadCustomGlyph(slot, rows)` | Load a 16-row LargeFont custom glyph. |
| `getCustomGlyphId(slot)` | Return hardware glyph ID for a reserved slot. |
| `writeCustomGlyph(...)` | Draw a loaded custom glyph in a text window. |

## Bitmap resources

| API | Description |
| --- | --- |
| `loadBitmap(bitmap, handle, applyPalette=true)` | Allocate/write a generated bitmap resource. |
| `clearBitmaps()` | Clear bitmap-resource bookkeeping when safe. |
| `getBitmapCount()` | Number of loaded resources. |
| `isBitmapLoaded(handle)` | Validate a bitmap handle. |
| `getBitmapWidth/Height(handle)` | Source image dimensions. |
| `getBitmapStorageBytes(handle)` | Font RAM storage used by one resource. |
| `getBitmapMemoryTotal/Used/Free()` | Bitmap allocation in 16-bit words. |
| `getBitmapMemoryTotalBytes/UsedBytes/FreeBytes()` | Bitmap allocation in bytes. |

## Bitmap palette

| API | Description |
| --- | --- |
| `setBitmapPaletteColor(index,r,g,b)` | Set one palette entry from RGB888. |
| `setBitmapPaletteColorRaw(index,bgr12)` | Set one raw 12-bit AMT palette entry. |
| `getBitmapPaletteColorRaw(index)` | Read library palette state. |
| `applyBitmapPalette(bitmap)` | Apply palette embedded in a generated bitmap. |
| `setBitmapPalette0Transparent(bool)` | Control palette-index-0 transparency. |
| `isBitmapPalette0Transparent()` | Inspect transparency state. |
| `rgbToBitmapColor(r,g,b)` | Convert RGB888 to raw AMT bitmap color. |

## Blend, opacity, brightness

| API | Description |
| --- | --- |
| `setBlendingEnabled(bool)` / `isBlendingEnabled()` | Enable/inspect global OSD/video blending. |
| `setOpacity(0..7)` / `getOpacity()` | Global OSD opacity. |
| `setBrightness(0..31)` / `getBrightness()` | Global OSD brightness. |

## Scaling

| API | Description |
| --- | --- |
| `setWindowScale(window, scale)` | Set equal X/Y scale, 1-4. |
| `setWindowScale(window, scaleX, scaleY)` | Set independent X/Y scales, 1-4. |
| `getWindowScaleX/Y(window)` | Inspect current scale. |

## Blink

| API | Description |
| --- | --- |
| `configureBlink(window,x,y,w,h,rawRate)` | Configure selected window, 1-based region, and rate. |
| `setBlinkWindow(window)` | Change blink target window. |
| `setBlinkRegion(x,y,w,h)` | Change 1-based blink region. |
| `setBlinkRateRaw(rawRate)` | Set six-bit raw blink rate. |
| `setBlinkEnabled(bool)` | Enable/disable blink. |
| `getBlinkWindow/X/Y/Width/Height/RateRaw()` | Inspect blink configuration. |
| `isBlinkEnabled()` | Inspect blink enable state. |

## Factory-menu control

| API | Description |
| --- | --- |
| `configureFactoryMenuControl(menuPin, plusPin, minusPin)` | Configure three active-high GPIO controls for external analog switches. |
| `setFactoryMenuTiming(pressMs, gapMs)` | Set default press/gap timing. |
| `setFactoryMenuSequence(steps,count)` | Install a custom button sequence. |
| `useDefaultFactoryMenuSequence()` | Restore the tested built-in sequence. |
| `enterFactoryMode()` | Execute the configured sequence. |

## Errors

Use:

```cpp
if (!display.someOperation()) {
  Serial.println(AMT630A_OSD::errorToString(display.getLastError()));
}
```

The `Error` enum includes initialization, window, Index RAM, glyph, Font RAM, bitmap, palette, scale, I2C, allocation, and factory-menu errors. `clearError()` clears the stored error state.

# Examples

| Example | Purpose |
| --- | --- |
| `LargeFontHUD` | Five-window LargeFont Robby-style HUD. |
| `SmallFontHUD` | Five-window SmallFont version of the HUD. |
| `LargeFontCharacterSetBrowser` | Browse raw LargeFont glyph IDs with Serial controls. |
| `SmallFontCharacterSetBrowser` | Browse raw SmallFont glyph IDs beginning at the verified ROM range. |
| `EnterFactoryMode` | Automate the tested hidden factory-menu sequence through a 74HC4066. |
| `LargeCustomGlyph` | Load and display a LargeFont custom glyph. |
| `MultipleWindows` | Independently positioned text windows. |
| `AnimatedWindows` | Moving text windows. |
| `MultipleWindowBatchTest` | Batch-update behavior. |
| `BitmapWindow` | Generated bitmap plus LargeFont ROM text. |
| `RobotBitmapTest` | Moving bitmap using the included `robot.h`. |
| `AnimatedBitmaps` | Multiple moving windows sharing a bitmap resource. |
| `MixedAnimatedWindows` | Text and bitmap windows together. |
| `HousePaletteBitmaps` | Multiple resources using one shared palette. |
| `AnimationPaletteDemo1` | Palette-driven bitmap animation. |
| `AnimationPaletteDemo2` | Radar-style palette animation with transparent background. |
| `BitmapOpacityTest` | Bitmap/video blending and opacity. |
| `FiveWindowAlphaTest` | Global blending across five text windows. |
| `BitmapScalingTest` | Bitmap scaling. |
| `FiveWindowScalingTest` | Scaling across all five text windows. |
| `BlinkDemo` | Hardware blink-region control. |

Some bitmap examples intentionally require headers generated from your own images and therefore do not bundle those source-specific headers.

# Arduino Library Manager publication

This repository is laid out in Arduino 1.5 library format: `library.properties` and `keywords.txt` at the repository root, public headers/source under `src/`, and sketches under lowercase `examples/`. Arduino's Library Manager requires the root `library.properties`, a compliant repository, and a Git tag/release; first-time publication requires submitting the repository URL to Arduino's Library Registry. Once registered, later compliant tags are indexed automatically.

The repository includes `.github/workflows/arduino-lint.yml`, which runs Arduino's official lint action in strict Library Manager submission mode.

See `RELEASE_CHECKLIST.md` before publishing the first GitHub tag.

# Credits

AMT630A_OSD was developed by Mike Ogrinz with OpenAI collaboration through extensive hardware experimentation, register analysis, firmware reverse engineering, and iterative library testing.

The hidden factory-menu investigation and the hypothesis that factory mode could avoid stock-MCU/external-I2C contention originated with Mike Ogrinz; firmware analysis and test-program development were performed collaboratively.

Special thanks to [nocash](https://problemkaputt.de/x51specs.htm) for his work on the AMT630A custom firmware.

# Version history

See `CHANGELOG.md`.