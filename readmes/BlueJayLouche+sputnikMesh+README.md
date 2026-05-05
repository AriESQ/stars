# SputnikMesh Configuration Guide

## First and foremost all credit goes to [Andrei Jay](https://andreijaycreativecoding.com/) Show him some love and visit his [Patreon](https://www.patreon.com/andrei_jay)

This document explains how to configure SputnikMesh through the `settings.xml` file. You can adjust MIDI mappings, audio reactivity, FFT bin configuration, video settings, performance mode and more without changing the source code.

## Understanding settings.xml Structure

The `settings.xml` file contains several main sections:

```xml
<toggles>          <!-- Boolean switches for different features -->
<parameters>       <!-- Numeric values for various effect parameters -->
<lfo>              <!-- Low Frequency Oscillator configurations -->
<transform>        <!-- 3D transformation settings -->
<mesh>             <!-- Mesh rendering options -->
<plocks>           <!-- Parameter lock automation data -->
<midiMappings>     <!-- MIDI controller assignments -->
<audioReactivity>  <!-- Audio input and frequency analysis settings -->
<video>            <!-- Video device and format settings -->
<performance>      <!-- Performance optimization settings -->
```

## Parameter Reference Table

Below is a comprehensive table of all parameters with their keyboard shortcuts and default MIDI mappings:

| Parameter          | Description               | Keyboard Shortcut | Default MIDI CC | Range       | XML Parameter ID    |
|--------------------|---------------------------|-------------------|-----------------|-------------|---------------------|
| **Basic Parameters** |                         |                   |                 |             |                     |
| Luma Key Level     | Luma key threshold       | A/Z               | CC 16           | 0.0 - 1.0  | luma_key_level      |
| X Displacement     | Horizontal displacement  | Q/W               | CC 17           | -1.0 - 1.0 | x_displace          |
| Y Displacement     | Vertical displacement    | E/R               | CC 18           | -1.0 - 1.0 | y_displace          |
| Z Frequency        | Z-axis noise frequency   | S/X               | CC 19           | 0.0 - 0.1  | z_frequency         |
| X Frequency        | X-axis noise frequency   | G/B               | CC 20           | 0.0 - 0.1  | x_frequency         |
| Y Frequency        | Y-axis noise frequency   | K/,               | CC 21           | 0.0 - 0.1  | y_frequency         |
| Zoom               | Zoom level               | O/P               | CC 22           | 0.0 - 1.0  | zoom                |
| Scale/Resolution   | Mesh resolution          | [/]               | N/A             | 50 - 200   | scale               |
| Center X           | Center X offset          | T/Y               | N/A             | -1.0 - 1.0 | center_x            |
| Center Y           | Center Y offset          | U/I               | N/A             | -1.0 - 1.0 | center_y            |
| **LFO Parameters** |                          |                   |                 |             |                     |
| Z LFO Argument     | Z LFO speed              | D/C               | N/A             | 0.0 - 1.0  | z_lfo_arg           |
| Z LFO Amplitude    | Z LFO intensity          | F/V               | N/A             | 0.0 - 1.0  | z_lfo_amp           |
| X LFO Argument     | X LFO speed              | H/N               | N/A             | 0.0 - 1.0  | x_lfo_arg           |
| X LFO Amplitude    | X LFO intensity          | J/M               | N/A             | 0.0 - 1.0  | x_lfo_amp           |
| Y LFO Argument     | Y LFO speed              | L/.               | N/A             | 0.0 - 1.0  | y_lfo_arg           |
| Y LFO Amplitude    | Y LFO intensity          | ;/,               | N/A             | 0.0 - 1.0  | y_lfo_amp           |
| **Transformation** |                          |                   |                 |             |                     |
| Rotate X           | X-axis rotation          | N/A               | N/A             | -180 - 180 | rotate_x            |
| Rotate Y           | Y-axis rotation          | N/A               | N/A             | -180 - 180 | rotate_y            |
| Rotate Z           | Z-axis rotation          | N/A               | N/A             | -180 - 180 | rotate_z            |
| Global X Displace  | Global X displacement    | N/A               | N/A             | -1.0 - 1.0 | global_x_displace   |
| Global Y Displace  | Global Y displacement    | N/A               | N/A             | -1.0 - 1.0 | global_y_displace   |
| Stroke Weight      | Line thickness           | N/A               | N/A             | 0.5 - 5.0  | stroke_weight       |

## Toggle Controls Table

| Toggle Feature     | Description               | Keyboard Shortcut | Default MIDI CC | XML Toggle ID       |
|--------------------|---------------------------|-------------------|-----------------|---------------------|
| Debug Overlay      | Show debug information    | ` (backtick)      | N/A             | debug               |
| Luma Key           | Enable luma key effect    | 1                 | CC 57           | lumaKey             |
| Bright Mode        | Brightness boost          | 2                 | CC 53           | bright              |
| Invert             | Invert colors             | 3                 | CC 54           | invert              |
| Black & White      | Monochrome mode           | 5                 | CC 56           | blackAndWhite       |
| Stroke Weight      | Use custom stroke weight  | N/A               | CC 55           | strokeWeight        |
| Wireframe          | Wireframe rendering       | N/A               | N/A             | wireframe           |

## Mesh Types Table

| Mesh Type          | Description               | Keyboard Shortcut | Default MIDI CC | Mesh Type Value     |
|--------------------|---------------------------|-------------------|-----------------|---------------------|
| Triangle Grid      | Filled triangular mesh    | - (minus)         | CC 49           | 0                   |
| Horizontal Lines   | Horizontal line grid      | 0                 | CC 50           | 1                   |
| Vertical Lines     | Vertical line grid        | 9                 | CC 51           | 2                   |
| Triangle Wireframe | Wireframe triangular mesh | = (equals)        | CC 52           | 3                   |

## LFO Controls Table

| LFO Setting         | Description              | Keyboard Shortcut | Default MIDI CC | XML LFO ID          |
|---------------------|--------------------------|-------------------|-----------------|---------------------|
| Z LFO Shape         | Z wave shape             | 6                 | N/A             | zShape              |
| X LFO Shape         | X wave shape             | 7                 | N/A             | xShape              |
| Y LFO Shape         | Y wave shape             | 8                 | N/A             | yShape              |
| Z Ring Modulation   | Z ring mod toggle        | !                 | N/A             | zRingMod            |
| X Ring Modulation   | X ring mod toggle        | @                 | N/A             | xRingMod            |
| Y Ring Modulation   | Y ring mod toggle        | #                 | N/A             | yRingMod            |
| Z Phase Modulation  | Z phase mod toggle       | $                 | N/A             | zPhaseMod           |
| X Phase Modulation  | X phase mod toggle       | %                 | N/A             | xPhaseMod           |
| Y Phase Modulation  | Y phase mod toggle       | ^                 | N/A             | yPhaseMod           |

## System Controls Table

| Function            | Description                 | Keyboard Shortcut     | Default MIDI CC | Notes                       |
|---------------------|-----------------------------|-------------------|-----------------|----------------------------|
| Reset Parameters    | Reset to defaults           | Shift+R           | CC 58           | Resets all parameters      |
| Toggle Audio        | Audio reactivity on/off     | Shift+A           | N/A             |                            |
| Cycle Audio Device  | Switch audio input device   | Shift+D           | N/A             |                            |
| Audio Smoothing     | Adjust audio smoothing      | Shift+[/]         | N/A             | Lower/higher smoothing     |
| Audio Sensitivity   | Adjust audio sensitivity    | Shift+−/=         | N/A             | Lower/higher sensitivity   |
| FFT Normalization   | Toggle normalization        | Shift+N           | N/A             |                            |
| Performance Mode    | Toggle performance mode     | Shift+P           | N/A             | Optimizes for weaker CPUs  |
| Cycle Video Device  | Switch video input device   | Shift+V           | N/A             |                            |
| Cycle Video Format  | Switch video format         | Shift+F           | N/A             | YUYV, MJPEG, etc.          |
| Cycle Resolution    | Switch video resolution     | Shift+Z           | N/A             |                            |
| Camera Framerate    | Adjust camera FPS           | Shift+Ctrl+−/=    | N/A             | Decrease/increase FPS      |
| Recording           | Start/stop parameter recording | N/A            | CC 60           | For parameter lock system  |
| MIDI Map Template   | Generate MIDI template      | Shift+M           | N/A             | Creates mapping_template.xml |
| Video Info          | Print video device info     | Shift+I           | N/A             | Outputs to console         |

## 1. Configuring MIDI Channel Mappings

The `<midiMappings>` section allows you to map MIDI controllers to specific parameters. Here's how to configure it:

```xml
<midiMappings>
  <mapping>
    <controlNumber>16</controlNumber>   <!-- MIDI CC number -->
    <channel>0</channel>                <!-- MIDI channel (0-15) -->
    <paramId>luma_key_level</paramId>   <!-- Parameter to control -->
    <minValue>0.0</minValue>            <!-- Minimum parameter value -->
    <maxValue>1.0</maxValue>            <!-- Maximum parameter value -->
    <bipolar>false</bipolar>            <!-- Center at 0 for -1 to 1 range -->
  </mapping>
  <!-- Add more mappings as needed -->
</midiMappings>
```

## 2. Configuring Audio Reactivity and FFT Bins

The `<audioReactivity>` section controls audio input and analysis:

```xml
<audioReactivity>
  <enabled>1</enabled>                   <!-- 0 = disabled, 1 = enabled -->
  <sensitivity>2.000000000</sensitivity> <!-- Amplification of audio input -->
  <smoothing>0.800000012</smoothing>     <!-- Smoothing factor (0.0-0.99) -->
  <numBands>8</numBands>                 <!-- Number of frequency bands -->
  <deviceName>Built-in Microphone</deviceName> <!-- Audio input device -->
  <deviceIndex>0</deviceIndex>           <!-- Device index in system list -->
  <normalizationEnabled>1</normalizationEnabled> <!-- Enable FFT normalization -->
  
  <!-- Frequency band configuration -->
  <bandRanges>
    <range>
      <minBin>0</minBin>     <!-- Starting FFT bin -->
      <maxBin>3</maxBin>     <!-- Ending FFT bin -->
    </range>
    <!-- more ranges... -->
  </bandRanges>
  
  <!-- Parameter mappings for audio reactivity -->
  <mappings>
    <mapping>
      <band>6</band>                 <!-- Which frequency band (0-7) -->
      <paramId>x_displace</paramId>  <!-- Parameter to modulate -->
      <scale>2.000000000</scale>     <!-- Scaling factor -->
      <min>-0.500000000</min>        <!-- Minimum output value -->
      <max>0.500000000</max>         <!-- Maximum output value -->
      <additive>0</additive>         <!-- 0 = replace, 1 = add to value -->
    </mapping>
    <!-- more mappings... -->
  </mappings>
</audioReactivity>
```

### Understanding FFT Bins:

The FFT (Fast Fourier Transform) bins represent different frequency ranges. With the default 1024 FFT size and 44100Hz sample rate, each bin represents about 43Hz. The `<bandRanges>` section maps groups of bins to logical frequency bands.

Default frequency bands:
1. Band 0 (bins 1-2): Sub bass (20-60Hz)
2. Band 1 (bins 3-5): Bass (60-250Hz)
3. Band 2 (bins 6-11): Low mids (250-500Hz)
4. Band 3 (bins 12-46): Mids (500-2000Hz)
5. Band 4 (bins 47-92): High mids (2-4kHz)
6. Band 5 (bins 93-139): Presence (4-6kHz)
7. Band 6 (bins 140-278): Brilliance (6-12kHz)
8. Band 7 (bins 279-511): Air (12-20kHz)

Adjust these ranges to focus on specific frequency areas that you want to react to.

### Audio Normalization

The `<normalizationEnabled>` tag controls whether FFT values are normalized relative to the maximum value:

- When enabled (`1`), the audio reactivity will be consistent regardless of the overall volume level
- When disabled (`0`), the audio reactivity will directly reflect the raw audio levels, showing more variation between quiet and loud sections

## 3. Configuring Video Devices and Formats

The `<video>` section allows you to configure video input settings:

```xml
<video>
  <devicePath>/dev/video0</devicePath>   <!-- Device path (Linux) or device:// (macOS) -->
  <deviceID>0</deviceID>                 <!-- Device index in system list -->
  <format>yuyv422</format>               <!-- Video format (e.g., yuyv422, mjpeg) -->
  <width>640</width>                     <!-- Desired capture width -->
  <height>480</height>                   <!-- Desired capture height -->
  <frameRate>30</frameRate>              <!-- Desired frame rate -->
</video>
```

### Available Video Formats:

Depending on your camera, these formats may be available:
- `yuyv422` or `YUYV` - Common uncompressed format (default)
- `mjpeg` or `MJPG` - Motion JPEG (often higher resolution at good framerates)
- `rgb565` - RGB format
- `bayer_rggb8`, `bayer_bggr8`, etc. - Various Bayer pattern formats
- `h264` - H.264 compressed video (if supported by camera)

On Raspberry Pi with V4L2 support, the actual available formats will be printed to the console when starting the application.

## 4. Performance Mode

The `<performance>` section lets you configure the performance optimization settings:

```xml
<performance>
  <enabled>0</enabled>                    <!-- 0 = off, 1 = on -->
  <scale>50</scale>                       <!-- Mesh resolution in performance mode (lower = faster) -->
  <noiseUpdateInterval>4</noiseUpdateInterval> <!-- Update noise every N frames -->
  <highQuality>1</highQuality>            <!-- 1 = high quality, 0 = optimize for speed -->
</performance>
```

Performance mode applies multiple optimizations for lower-powered devices like Raspberry Pi:
- Reduces mesh resolution
- Updates noise textures less frequently
- Uses smaller noise textures
- Processes fewer pixels in noise generation
- Limits camera resolution and framerate
- Reduces audio processing frequency

Toggle performance mode with `Shift+P` during runtime.

## Advanced Tips

### Generating a MIDI Mapping Template

The application includes a feature to generate a template MIDI mapping file. Press Shift+M while running the application to generate a `mapping_template.xml` file in the data folder. This template contains all available parameters with default settings, which you can customize and then copy into your settings.xml file.

## Raspberry Pi Optimization

For best performance on Raspberry Pi:

1. Enable performance mode with `Shift+P` or set it in settings.xml: `<performance><enabled>1</enabled></performance>`
2. Choose MJPEG format if available for your camera (`Shift+F` to cycle formats)
3. Use lower resolutions (640x480 or 320x240)
4. Set a lower framerate (24fps is usually sufficient)
5. When running headless, launch with: `DISPLAY=:0 ./SputnikMesh`

## Troubleshooting

1. **Invalid XML**: Ensure your XML is properly formatted. Missing closing tags or improper nesting can prevent the application from loading settings.

2. **Device Not Found**: If an audio or video device is no longer available, the application will fall back to the default device.

3. **Parameter Out of Range**: If you set values outside the expected ranges, the application will clamp them to valid values.

4. **Missing Sections**: If you remove entire sections from settings.xml, the application will use default values for those settings.

5. **Audio Not Working**: Check that your audio input device is properly connected and that the correct device is selected in settings.xml.

6. **Video/Camera Issues**: 
   - On Linux/Raspberry Pi, ensure you have proper permissions for the video device (`sudo usermod -a -G video $USER`)
   - Check if the format and resolution are supported by your camera
   - Try using `v4l2-ctl --list-formats-ext` in a terminal to see supported formats
   - In debug mode (press \` key), check the video device information

7. **MIDI Not Responding**: Ensure your MIDI device is connected before starting the application. Check the debug overlay to confirm MIDI messages are being received.

8. **Performance Issues**:
   - Enable performance mode with `Shift+P`
   - Reduce mesh scale/resolution
   - Use simpler mesh types (horizontal or vertical lines)
   - Disable audio reactivity if not needed
   - Lower the camera resolution and framerate
