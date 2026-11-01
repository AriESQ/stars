<img alt="veilocity-logo" src="./assets/images/logo.png" style="margin-left:auto; margin-right:auto; display:block; width:200px;"/>

# Veilocity

**Messages in Motion**

Veilocity is a web-based tool for creating motion-defined text using random-dot kinematogram techniques. Hidden messages become visible only through motion, appearing as random noise when paused.

## Features

- **Motion-Defined Text**: Messages revealed through coherent dot motion
- **Random-Dot Kinematogram**: Classic perceptual effect where static frames look like noise
- **Dual Dot Fields**:
  - Foreground: Persistent dots that drift coherently inside text mask
  - Background: Dynamic noise (white noise, static drift, or still)
- **Customizable Text**:
  - Multi-line text support
  - Choice of standard fonts
  - Custom font file upload (TTF, OTF, WOFF, WOFF2)
  - Adjustable font size (24-200px)
- **Motion Controls**:
  - Independent drift speed for masked dots
  - Adjustable mask scroll speed
  - Vertical position control
- **Background Noise Types**:
  - White Noise: Randomizes every frame (TV static effect)
  - Static Drift: Slow coherent movement
  - None: Still background
- **Visual Controls**:
  - Dot density adjustment (500-5000 dots)
  - Dot size control (1-5px)
- **Playback**:
  - Play/Pause controls
  - Reset to beginning
- **Video Export**:
  - Frame-by-frame recording for perfect quality
  - Selectable frame rate (24/30/60 FPS)
  - Container format options:
    - WebM (VP9/VP8) - Universal browser support
    - MP4 (H.264) - Professional editing compatibility (Chrome/Edge)
  - 15 Mbps bitrate for high quality
  - Records one complete scroll cycle
  - Progress indicator during recording

## How to Use

1. **Enter Your Message**: Type your text in the "Message Text" field (multi-line supported)
2. **Choose Font**: Select a standard font or upload a custom font file
3. **Adjust Appearance**:
   - Font Size: Control text size
   - Vertical Position: Place text higher or lower on screen
   - Dot Density: More or fewer dots
   - Dot Size: Larger or smaller pixels
4. **Configure Motion**:
   - Text Mask Drift Speed: How fast dots move inside the text
   - Mask Scroll Speed: How fast the text scrolls across screen
   - Background Noise Type: Choose how background behaves
5. **Preview**:
   - Click "Play" to see the animation
   - The text will scroll from left to right
   - Text is visible through coherent dot motion
   - Pause to see it disappear into noise
6. **Configure Recording**:
   - Frame Rate: Choose 24 FPS (cinematic), 30 FPS (standard), or 60 FPS (smooth)
   - Video Container: Select WebM (all browsers) or MP4 (Chrome/Edge, best for editors)
7. **Export**:
   - Click "Start Recording" to begin frame-by-frame capture
   - Watch progress indicator showing percentage and frame count
   - Recording automatically stops after one complete scroll cycle
   - File downloads as .webm or .mp4 depending on selected format

## Technical Details

### Motion Perception

Veilocity exploits the human visual system's sensitivity to coherent motion. When dots move together in a specific region (the text mask), the brain perceives a shape defined purely by motion. In any single frozen frame, the image appears as random noise with no discernible pattern.

### How It Works

1. **Text Mask Generation**: Text is rendered to an offscreen canvas to create a binary mask
2. **Foreground Dots**: Dots within the mask drift coherently in one direction
3. **Background Dots**: Dots outside the mask either randomize (white noise), drift differently, or remain still
4. **Scrolling**: The entire text mask scrolls horizontally across the screen
5. **Perception**: Motion-sensitive neurons in the visual cortex respond to the coherent motion, making the text "pop out"

### Performance

- Runs entirely in the browser
- No server-side processing
- Canvas-based rendering with frame rate control (24/30/60 FPS)
- Frame-by-frame recording for consistent output quality
- Direct ImageData buffer manipulation for fast rendering
- Mask caching with threshold-based regeneration
- Efficient dot rendering with loop unrolling for common sizes

## Browser Compatibility

- Modern browsers with Canvas API support
- MediaRecorder API required for video export
- FontFace API for custom font loading

### Video Export Compatibility

| Browser | WebM (VP9/VP8) | MP4 (H.264) |
|---------|----------------|-------------|
| Chrome 120+ | ✅ Yes | ✅ Yes |
| Edge 120+ | ✅ Yes | ✅ Yes |
| Firefox 120+ | ✅ Yes | ❌ No |
| Safari | ❌ Limited | ✅ Yes (macOS/iOS) |

**Recommendations:**
- **For DaVinci Resolve / Adobe Premiere Pro**: Use MP4 format in Chrome/Edge
- **For universal compatibility**: Use WebM format
- **Safari users**: Limited video export support (Safari has incomplete MediaRecorder implementation)

## Privacy & Security

- **No data uploads**: Everything runs locally in your browser
- **No tracking**: No analytics or external services
- **No dependencies**: Pure vanilla JavaScript, no third-party libraries
- **Offline capable**: Works without internet after initial load

## Use Cases

- **ARG & Puzzle Design**: Create hidden messages for alternate reality games
- **Steganography Education**: Demonstrate motion-based concealment
- **Visual Perception Demos**: Illustrate motion detection in vision science
- **Art & Design**: Create unique motion-based visual effects
- **Security Training**: Show non-traditional information hiding methods

## Technical Specifications

- **Language**: Pure HTML5, CSS3, JavaScript (ES6+)
- **APIs Used**:
  - Canvas API (2D rendering with direct ImageData manipulation)
  - MediaRecorder API (video capture with manual frame control)
  - FontFace API (custom font loading)
  - FileReader API (font file upload)
- **Video Formats**:
  - WebM container with VP9 or VP8 codec
  - MP4 container with H.264 codec (browser-dependent)
- **Recording**:
  - Frame rates: 24, 30, or 60 FPS (user-selectable)
  - Bitrate: 15 Mbps for high quality
  - Method: Frame-by-frame capture with `requestFrame()` for precise timing
  - Aspect ratios: 16:9 (1920x1080), 16:10 (1920x1200), 4:3 (1024x768), 1:1 (1080x1080), 9:16 (1080x1920)
- **No Build Process**: Direct file editing, no transpilation
- **No Dependencies**: Zero third-party libraries

## Known Limitations

- **Video Recording**: Requires MediaRecorder API
  - Safari has limited/incomplete MediaRecorder support
  - MP4 export only available in Chrome/Edge (Firefox supports WebM only)
- **Performance**: High dot densities (>50%) may impact performance on slower devices
- **Custom Fonts**: Must be valid TTF/OTF/WOFF/WOFF2 format files
- **Recording Scope**: Captures exactly one scroll cycle (text entering from right, exiting left)
- **Container Formats**: Limited to browser-native MediaRecorder support (WebM and MP4 only)
  - For other formats (AVI, MOV, etc.), export would require third-party encoding libraries

## License

MIT License - See LICENSE file for details

Copyright (c) 2025 NQR

## Related Projects

- **Lucyra**: Digital flashlight for revealing hidden clues in images
- **Ghostmark**: Steganography tool with LSB encoding
- **Inknigma**: Write in invisible ink with multiple encoding methods
- **SpectroGhost**: Audio spectrogram creator

## Credits

Created by NQR as part of the nqrlabs.com toolkit for puzzle solvers and ARG creators.

Based on classic random-dot kinematogram techniques from visual perception research.
