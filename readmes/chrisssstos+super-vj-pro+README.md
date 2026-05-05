# Super VJ Pro - README

## Overview
Super VJ Pro is an educational game designed to teach aspiring Visual Jockeys (VJs) the fundamentals of VJing through a gamified, interactive learning experience. The game integrates a custom MIDI controller (BitchBoy) with Processing-based software to provide hands-on practice with real-time feedback. It bridges the gap between traditional learning methods (e.g., tutorials) and professional VJ software like Resolume Arena.

## Features
- **Level-Based Progression**: Seven levels introduce core VJing skills, from basic clip launching to advanced effect manipulation.
- **Performance-First Approach**: Learn by doing, with immediate feedback on actions.
- **Rhythm-Based Challenges**: Synchronize visuals with beats to develop timing skills.
- **Real-Time Feedback**: Visual and auditory cues (e.g., "NICE" or "FAIL") guide performance.
- **Minimalistic UI**: Reduces cognitive load, focusing on essential tasks.
- **Integration with Resolume**: Uses OSC (Open Sound Control) and Spout to mirror actions in Resolume Arena.
- **Custom MIDI Controller**: BitchBoy provides tactile input for clip triggering, slider adjustments, and more.
- **Scoring & Leaderboard**: Tracks performance and provides qualitative feedback (e.g., "YOU ARE A TRUE VJ").

## Requirements
### Hardware
- **BitchBoy Controller**: Custom MIDI device with buttons, sliders, and LEDs.
- **Computer**: Running Windows/macOS/Linux with USB support.

### Software
- **Processing**: Download from [Processing.org](https://processing.org/).
- **Resolume Arena**: For backend VJing. Necessary to use with the template that's provided
- **Libraries**:
  - `themidibus` (MIDI communication)
  - `oscP5` (OSC messaging)
  - `spout` (video streaming)
  - `processing.sound` (audio playback/beat detection)

## Installation
1. **Download** the `super_vj_pro.pde` file.
2. **Install Processing** and required libraries via `Sketch > Import Library > Add Library`.
3. **Connect BitchBoy** via USB.
4. **Launch Resolume Arena** (if using integration) and ensure OSC/Spout are enabled.

## Usage
1. **Run the Sketch**: Open `super_vj_pro.pde` in Processing and click "Run."
2. **Follow On-Screen Instructions**: Each level introduces new skills:
   - **Levels 1–2**: Basic clip triggering.
   - **Level 3**: On-beat synchronization.
   - **Levels 4–6**: Slider controls for opacity/effects.
   - **Level 7**: Freestyle mode.
3. **Interact with BitchBoy**: Buttons trigger clips; sliders adjust effects.
4. **View Feedback**: Real-time messages and scores reflect performance.

## Controls
- **Buttons**: Map to clip triggers in Resolume (e.g., buttons 52–55 for Layer 1 clips).
- **Sliders**:
  - Slider 1: Controls opacity (Level 4).
  - Sliders Horizontal: Control effects (Level 6).
- **Encoders**: Adjust effect parameters (e.g., hue, rotation).


![SVP1](/images/LVLS.png)
![SVP2](/images/processing_arena.png)
![SVP3](/images/svp_interact.jpg)
## Credits
Developed by Christos Constantinou (University of Twente, 2025).  
Supervisor: M. A. Gómez Maureira, Eggink Wouter.

## License
Open-source for educational use. Contact author for commercial applications.

For more details, refer to the full thesis: [Super VJ Pro](/Super_VJ_Pro_Final_Project.pdf) and [Super VJ Pro Research](/Super_VJ_Pro_Research_Topics.pdf) 