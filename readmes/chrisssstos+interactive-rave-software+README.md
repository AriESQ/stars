# Interactive Rave software

A solution for immersive, interactive EDM live performances controlled remotely.

## Overview
the Interactive Rave software is an interactive audiovisual live show designed for the 360LAB at PLANETART. It combines original music and visuals with audience participation, allowing the audience to influence the performance in real time. The project explores immersion, interactivity, and remote control in live EDM performances.

## Features
- **Interactive Performance**: Audience members can influence the music and visuals using MIDI controllers (Launchpads).
- **Remote Control**: The performer controls the show from a separate studio, enabling a remote live experience.
- **360° Projection**: The 360LAB features 8 beamers and a quadrophonic sound system for a fully immersive environment.
- **Custom Software**: Python scripts control the Launchpads, synchronizing audio (Ableton Live) and visuals (Resolume Arena) via OSC and MIDI protocols.

## Installation
### Prerequisites
- Python 3.x
- `launchpad_py` library
- `rtmidi` library
- Ableton Live 11
- Resolume Arena 7
- LoopMIDI (for virtual MIDI ports)
- Voicemeeter (for audio streaming over VBAN)

### Setup
1. **Hardware**:
   - Connect the Launchpads to the performer's PC.
   - Ensure the 360LAB PC is connected to the projectors and sound system.
   - Set up a camera (e.g., Microsoft Kinect) for live streaming to the studio.

2. **Software**:
   - Install the required Python libraries:
     ```bash
     pip install launchpad_py python-rtmidi
     ```
   - Configure Ableton Live and Resolume Arena to communicate via OSC and MIDI.
   - Use Voicemeeter to stream audio from the performer's PC to the 360LAB PC.

3. **Run the Performance**:
   - Start the Python scripts for the Launchpads:
     ```bash
     python launchpad_out.py
     ```
   - Launch Ableton Live and Resolume Arena, ensuring they are synced.
   - Begin the performance, allowing the audience to interact via the Launchpads.

## Usage
- **FX Launchpad**: Press random buttons to apply audio/visual effects (e.g., bitcrush, flanger).
- **CHAOS Launchpad**: Press buttons to trigger "chaos mode," adding retrigger effects to the music and visuals.
- **Control Panel Launchpad**: Allows the audience to progress the performance or choose different paths.

## Project Structure
- `launchpad_out.py`: Controls the Launchpads and handles MIDI input/output.
- `main.py`: Main script for running the performance, handling events, and logging interactions.
- **Visuals and Audio**: Custom content created in FL Studio, After Effects, Blender, etc.

## Testing & Evaluation
The project was tested in three shows:
1. **Interactive Show**: Audience could interact via Launchpads.
2. **Non-Interactive Show**: No audience interaction.
3. **Free4All**: Open DJ booth in the 360LAB.

![360LAB](/images/360_1.jpg)
![360LAB2](/images/360_2.jpg)
## References
- [Resolume Arena](https://resolume.com/)
- [Ableton Live](https://www.ableton.com/)
- [PLANETART](https://www.planetart.nl/)

## License
This project is part of academic research at the University of Twente. For inquiries, contact the author: Christos Constantinou.

---

For more details, refer to the full thesis: [BLOCK_SYSTEM](/BLOCK_SYSTEM.pdf).