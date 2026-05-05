# Off-Axis Projection Demo 🎯

A real-time 3D head-tracking demo that creates a realistic "window into a virtual world" effect using your webcam. Built with Three.js and MediaPipe FaceMesh.

![Off-Axis Demo](https://img.shields.io/badge/License-MIT-blue.svg)

## ✨ Features

- **Real-time Head Tracking**: Uses MediaPipe FaceMesh to track your head position via webcam
- **Off-Axis Projection**: Dynamically adjusts the 3D camera frustum based on head position for a "window" effect
- **Deep Virtual Chamber**: Cyberpunk-style grid environment with variable density and electric flow shaders
- **GLTF Model Support**: Load and display custom 3D models
- **Model Animations**: Automatically plays GLTF animations (e.g., running horse)
- **Interactive Controls**: Real-time adjustment of model position, scale, rotation, lighting, and effects

## 📸 Preview

![Demo Preview](./preview.gif)

*The off-axis projection effect creates a realistic "window into a virtual world" - move your head to experience true 3D depth on a 2D screen!*

## 🎬 Demo

Visit the live demo at: [Your Demo URL]

Or run locally:

```bash
# Clone the repository
git clone https://github.com/MindDock/off-axis-demo.git
cd off-axis-demo

# Start a local server (Python 3)
python3 server.py

# Open http://localhost:8000 in your browser
```

## 🎮 Controls

Once the demo is running, you'll have access to:

- **Select Model**: Choose from available 3D models
- **Scale**: Adjust model size
- **Rotation Y**: Rotate model around Y-axis
- **Position Y/Z**: Move model vertically and in depth
- **Light Intensity**: Adjust spotlight brightness
- **Grid Speed**: Control the speed of the electric flow effect
- **Fullscreen Button**: Top-left corner for immersive viewing

## 📦 Adding Custom Models

1. **Download Models**: Visit [Sketchfab](https://sketchfab.com/3d-models/) and download GLTF format models
   - Look for the "Download 3D Model" button
   - Select **glTF** format (not glb, fbx, or others)
   - Download and extract the ZIP file

2. **Add to Project**:
   ```
   models/
   ├── default/           # Default model (included)
   │   └── scene.gltf
   └── your-model-name/   # Your custom model
       ├── scene.gltf
       └── textures/      # If applicable
   ```

3. **Register in Code**: Edit `index.html` and add your model to the `models` object:
   ```javascript
   const models = {
       'Original': './models/default/scene.gltf',
       'Your Model': './models/your-model-name/scene.gltf',
       // ... other models
   };
   ```

## 🛠️ Technical Details

### Technologies Used

- **Three.js**: 3D rendering engine
- **MediaPipe FaceMesh**: Real-time face landmark detection
- **dat.GUI**: Interactive control panel
- **WebGL**: Hardware-accelerated graphics

### How It Works

1. **Face Tracking**: MediaPipe detects iris landmarks (468, 473) to estimate head position in 3D space
2. **Off-Axis Projection**: The camera's projection matrix is recalculated each frame using `makePerspective()` with asymmetric frustum parameters based on head position
3. **Depth Perception**: Variable grid density and shader-based fog effects create a sense of deep space
4. **Smooth Tracking**: Exponential smoothing (LERP) reduces jitter in head tracking

### Configuration

Key parameters in `index.html`:

```javascript
const SCREEN_WIDTH_CM = 30.0;   // Virtual screen width
const SCREEN_HEIGHT_CM = 20.0;  // Virtual screen height
const BOX_DEPTH_CM = 80.0;      // Chamber depth
const SENSITIVITY = 2.5;        // Head tracking sensitivity
```

## 🎨 Customization

### Environment

The cyberpunk grid environment can be customized by modifying the `createEnvironment()` function:
- Grid density: Adjust `stepX` and `numZLines`
- Colors: Change `gridUniforms.color` (default: `0x00ffff` cyan)
- Depth effect: Modify the fragment shader's `distFade` calculation

### Lighting

Three light sources are configurable:
- **Main Spotlight**: Front-facing key light
- **Ambient Light**: Global illumination
- **Rim Light**: Cyan accent from below

## 📝 Browser Compatibility

- ✅ Chrome/Edge (Recommended)
- ✅ Safari
- ⚠️ Firefox (may have MediaPipe compatibility issues)

**Requirements**:
- WebGL 2.0 support
- Webcam access
- Modern browser (last 2 versions)

## 📄 License

This project is licensed under the MIT License - see the [license.txt](license.txt) file for details.

## 🙏 Credits

- **MediaPipe**: Google's ML framework for face tracking
- **Three.js**: 3D graphics library
- **Default 3D Model**: [Specify source if applicable]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Project Link: [https://github.com/MindDock/off-axis-demo](https://github.com/MindDock/off-axis-demo)

---

**Note**: This demo works best when viewing from a distance of 40-80cm from your screen. Move your head around to experience the 3D effect!
