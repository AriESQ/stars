# WebcamWrapper

A Python application that creates a virtual camera from your physical webcam with real-time image processing capabilities.

## Features

- Captures video from your physical webcam
- Applies real-time image processing (currently grayscale conversion)
- Outputs to a virtual camera that can be used by other applications
- Cross-platform support with optimized Windows compatibility

## Prerequisites

### Virtual Camera Backend

This application requires a virtual camera backend to function. Choose one of the following:

#### Option 1: OBS Studio (Recommended)
1. Download and install [OBS Studio](https://obsproject.com/)
2. Start OBS Studio at least once to initialize the virtual camera
3. The OBS Virtual Camera will be automatically available

#### Option 2: Unity Capture
1. Download [Unity Capture](https://github.com/schellingb/UnityCapture)
2. Run the installer as administrator
3. Register the virtual camera device

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd WebcamWrapper
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure your physical webcam is connected and working
2. Make sure you have installed a virtual camera backend (see Prerequisites)
3. Run the application:
   ```bash
   python app.py
   ```

4. The application will:
   - Display available virtual camera backends
   - Initialize your physical webcam
   - Create a virtual camera with the same resolution and FPS
   - Show a preview window with the processed video
   - Make the virtual camera available to other applications

5. Press 'q' in the preview window to exit

## Troubleshooting

### "No virtual camera backends found"
- Install OBS Studio or Unity Capture (see Prerequisites)
- Restart the application after installation

### "Could not open webcam"
- Check that your webcam is connected and working
- Ensure no other applications are using the webcam
- Verify Windows has permission to access the camera

### Import errors
- Make sure you're in the correct virtual environment
- Run `pip install -r requirements.txt` to install dependencies

## Development

The application currently applies a grayscale filter to the video feed. You can modify the image processing logic in the `main()` function to add different effects such as:

- Color filters
- Blur effects
- Edge detection
- Face detection and effects
- Background replacement

## Requirements

- Python 3.7+
- OpenCV (opencv-python)
- PyVirtualCam
- NumPy
- Windows 10/11 (optimized for Windows, but should work on other platforms)