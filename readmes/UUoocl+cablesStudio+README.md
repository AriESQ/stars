# Cables Studio Standalone Patches

A collection of specialized patches and operators designed for the Cables Studio Electron environment, enabling integration with local hardware, external frameworks, and system-level APIs.

## Available Patches

### 1. MediaPipe Local Standalone
Provides offline, high-performance computer vision capabilities using Google's MediaPipe framework.
- **FaceLandmarker**: Detects detailed face landmarks and blendshapes from a video or image texture.
- **HandLandmarker**: Tracks hand positions, skeletal structures, and gestures in real-time.
- **PoseLandmarker**: Performs full-body skeletal tracking for motion analysis and interaction.
Video example

https://github.com/user-attachments/assets/94d5deb8-cff3-42bc-ac68-60818ae5247b

### 2. OBS WebSocket Standalone
Enables direct control and automation of OBS Studio via the WebSocket v5 protocol.
- **ObsLaunch**: Starts OBS Studio with the necessary command-line arguments for remote control and debugging.
- **ObsConnect**: Establishes a persistent connection to OBS and broadcasts real-time server events.
- **ObsRequest**: Composes and sends arbitrary requests to control scenes, sources, and settings in OBS.

https://github.com/user-attachments/assets/23b2c86b-44c5-4024-9fc8-cf518a19ee42

### 3. P5.js Standalone
Integrates the creative coding power of P5.js directly into the Cables GL rendering pipeline.
- **P5Instance**: Executes P5.js sketches in instance mode and shares the resulting canvas as a high-performance texture.

### 4. Python Pynput Standalone
Bridges Cables with Python to access system-wide input monitoring and specialized hardware control.
- **PythonConfig**: Defines the local environment settings and paths for the Python bridge execution.
- **PythonGlobalKeyboardMonitor**: Listens for system-wide keyboard events and keystrokes regardless of window focus.
- **PythonGlobalMouseMonitor**: Tracks global mouse coordinates and button clicks across the entire desktop.
- **PythonUvcPtzControl**: Manages Pan, Tilt, and Zoom operations for UVC-compatible cameras through native commands.

https://github.com/user-attachments/assets/29ab12af-3d3f-43de-bddc-a37ac925ef1f

### 5. Syphon In/Out Standalone (macOS)
Facilitates real-time video sharing between Cables and other macOS creative software.
- **SyphonIn**: Ingests video streams from external applications like Resolume, MadMapper, or OBS.
- **SyphonOut**: Publishes the Cables GL viewport or textures to the local Syphon server for external use.

---

*AI Disclaimer: This project and its documentation were developed with the assistance of AI tools to ensure compatibility and maintain rigorous architectural standards across the standalone ecosystem.*
