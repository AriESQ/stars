RTSP_To_VirtualCam
RTSP_To_VirtualCam is a Python application that streams Real-Time Streaming Protocol (RTSP) video feeds to a virtual camera on your system. This allows you to use any RTSP-compatible camera as a virtual webcam in various applications such as Cables.gl Zoom, VDMX, OBS Studio, and more. The application features a user-friendly graphical interface built with PyQt5, automatic reconnection with exponential backoff, and a test pattern display when the RTSP stream is unavailable.

![Screenshot 2024-10-18 193446](https://github.com/user-attachments/assets/df957d41-6266-4126-80dd-8420f38cbdc7)

Features
RTSP Stream Integration: Connect to and stream video from RTSP-compatible cameras.
Virtual Camera Output: Send video frames to a virtual camera device, making it accessible to any application that supports webcam input.
Graphical User Interface (GUI): Intuitive interface built with PyQt5 for easy configuration and control.
Automatic Reconnection: Implements exponential backoff strategy to automatically reconnect to the RTSP stream in case of disconnection.
Test Pattern Display: Shows a test pattern on the virtual camera when the RTSP stream is unavailable.
RTSP URL History: Maintains a history of the last 10 RTSP URLs for quick access.
Logging: Detailed logs are maintained in both the console and a log file (virtual_cam_app.log) for troubleshooting and monitoring.
Prerequisites
Before installing and running RTSP_To_VirtualCam, ensure that your system meets the following requirements:

Operating System: Windows, macOS ( need to fix issues with pyvirtualcam library, not working for now in Mac OS 14/15), or Linux.
Python Version: Python 3.10 
FFmpeg: Required by the av library for handling RTSP streams.
Virtual Camera Support:
Windows: Typically supported out of the box, but ensure you have the latest drivers.
macOS: May require additional permissions or software to create virtual cameras.
Linux: You might need to set up virtual camera devices manually (e.g., using v4l2loopback).
Installation
Follow the steps below to set up RTSP_To_VirtualCam on your system.

1. Clone the Repository
First, clone the repository to your local machine using git.


git clone https://github.com/dabulina/RTSP_to_VirtualCam.git
cd RTSP_To_VirtualCam

2. Create a Virtual Environment (Optional but Recommended)
Creating a virtual environment helps manage dependencies and avoid conflicts with other Python projects.


python -m venv venv
Activate the virtual environment:

Windows:


venv\Scripts\activate
macOS/Linux:


source venv/bin/activate
3. Install FFmpeg
FFmpeg is required by the av library to handle RTSP streams.

Windows:

Download the latest FFmpeg build from the official website.
Extract the downloaded archive.
Add the bin folder of the extracted FFmpeg to your system's PATH environment variable.
macOS (Using Homebrew):


brew install ffmpeg
Linux (Debian/Ubuntu-based):


sudo apt-get update
sudo apt-get install ffmpeg
4. Install Python Dependencies
Ensure that pip is updated to the latest version.


pip install --upgrade pip
Install the required Python packages using the provided requirements.txt file.

requirements.txt
numpy>=1.21.0
opencv-python>=4.5.0
av>=10.0.0
PyQt5>=5.15.0
pyvirtualcam>=0.3.0
Install the dependencies:


pip install -r requirements.txt
5. (Optional) Verify Installation
To ensure that all dependencies are installed correctly, you can run the main application to check for errors.


python RTSP_To_VirtualCam.py
Usage
Follow the steps below to use RTSP_To_VirtualCam:

Launch the Application

Run the main Python script:


python RTSP_To_VirtualCam.py
Configure RTSP Stream

Add RTSP URL: Enter your RTSP URL in the input field. Click Connect to start streaming.
RTSP URL History: The application maintains a history of the last 10 RTSP URLs entered for quick access.
Connect to RTSP Stream

Click the Connect button to start streaming from the specified RTSP URL.
The application will attempt to establish a connection. If successful, the status will update to Connected.
If the connection fails, the application will display a test pattern and attempt to reconnect automatically using an exponential backoff strategy.
Disconnect from RTSP Stream

Click the Disconnect button to stop streaming and revert the virtual camera to display the test pattern.
Virtual Camera Output

The virtual camera can be selected as a webcam source in any application that supports webcam input.
For example, in Zoom:
Go to Settings > Video.
Select RTSP_To_VirtualCam as the camera source.
Configuration
RTSP URL Input
The application allows users to input their RTSP URLs manually. No default RTSP URL is pre-populated, enhancing security and flexibility.

RTSP URL History
The application maintains a history of the last 10 RTSP URLs entered. This allows for quick access and reconnection to frequently used streams.

Logging
Logs are maintained in both the console and a log file named virtual_cam_app.log located in the project's root directory. These logs are useful for monitoring the application's behavior and troubleshooting issues.

License
This project is licensed under the GNU General Public License v3.0.

Important: Since PyQt5 is licensed under GPLv3, your project must also be licensed under GPLv3 to comply with its terms.

GPLv3 License Overview
Freedom to Use: You can use the software for any purpose.
Freedom to Modify: You can modify the software to suit your needs.
Freedom to Distribute: You can distribute copies of the original software.
Copyleft: Any distributed modified versions must also be licensed under GPLv3.
For more details, please refer to the GNU GPLv3 License.

Contributing
Contributions are welcome! If you'd like to contribute to RTSP_To_VirtualCam, please follow these steps:

Fork the Repository

Click the Fork button at the top right of this page to create a copy of the repository under your GitHub account.

Clone the Forked Repository


git clone https://github.com/yourusername/RTSP_To_VirtualCam.git
cd RTSP_To_VirtualCam
Create a New Branch


git checkout -b feature/YourFeatureName
Make Your Changes

Implement your feature or bug fix.

Commit Your Changes


git commit -m "Add feature: YourFeatureName"
Push to Your Fork


git push origin feature/YourFeatureName
Create a Pull Request

Go to the original repository and click Compare & pull request to submit your changes for review.

Acknowledgements
PyQt5: For providing the framework to build the graphical user interface.
pyvirtualcam: For enabling virtual camera support.
OpenCV: For handling video processing and frame manipulation.
PyAV: For interfacing with FFmpeg and handling RTSP streams.
NumPy: For efficient numerical operations on video frames.
Troubleshooting
FFmpeg Not Found: Ensure that FFmpeg is installed and added to your system's PATH environment variable.
Virtual Camera Not Detected: Verify that the virtual camera driver is installed correctly. On some systems, you may need to install additional software or drivers.
RTSP Stream Issues: Check the RTSP URL for correctness and ensure that the camera is accessible over the network. Refer to the logs in virtual_cam_app.log for detailed error messages.

Enjoy Martins Dabolins
