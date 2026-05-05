# ImageData Planar Image Coder

Decodes image data stored in planar format for use with `ImageData` objects and encodes `ImageData` back to planar format. This package also contains helpers for encoding and decoding the following planar image formats:

* Crack Art
* Degas / Degas Elite
* IFF
* NEOChrome / NEOChrome Master
* Tiny Stuff
* Spectrum 512
* STOS packed images

## Installation
```
npm i git+https://github.com/keithclark/imagedata-planar.git
```

## Examples

### Decoding planar data to `ImageData`

```js
import { decode, IndexedPalette } from '@keithclark/imagedata-planar';

// Create a single plane, 320 x 200 image filled with random pixels
const buffer = Uint8Array.from({ length: 320 * 200 / 8 }, () => Math.random() * 255);

// Create an indexed palette for our pixels
const palette = IndexedPalette.fromValueArray([0xdd0000ff, 0x0000ddff]);

// Decode the image using the dimensions and palette
const imageData = decode(buffer, 320, 200, palette);

// Draw the decoded output to a canvas so we can see it
const canvas = document.createElement('canvas');
canvas.width = imageData.width;
canvas.height = imageData.height;
canvas.getContext('2d').putImageData(imageData, 0, 0);
document.body.appendChild(canvas);
```

### Encoding `ImageData` to planar data

```js
import { encode, IndexedPalette } from '@keithclark/imagedata-planar';

// Create an image and fill it with random white pixels
const imageData = new ImageData(320, 200);
const pixelView = new DataView(imageData.data.buffer);
for (let c = 0; c < 1000; c++) {
  const index = Math.floor(Math.random() * pixelView.byteLength / 4);
  pixelView.setUint32(index, 0xffffffff);
}

// Create an indexed palette from the image
const palette = IndexedPalette.fromImageData(imageData);

// Encode the image
const buffer = encode(imageData, palette);
```

# Supported Image Formats

In addition to the general purpose planar `encode` and `decode` methods, coders for various image formats are also provided. You can use these by importing the relevant `encode`/`decode` methods as shown below. 

As well as the decoded `ImageData`, these format-specific functions expose an additional metadata object for the image, allowing them to be re-encoded later.

```js
// Import the IFF decode method
import decode from '@keithclark/imagedata-planar/formats/iff/decode.js';

// Fetch the image and decode it
const buffer = await fetch('image.iff');
const { imageData, meta } = decode(buffer);

// Draw the image to a canvas
const canvas = document.getElementById('myCanvas');
canvas.width = imageData.width;
canvas.height = imageData.height;
canvas.getContext('2d').putImageData(imageData, 0, 0);
```
