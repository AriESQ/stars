# Videous & Friends

A comprehensive video editing and processing platform with multiple components for video highlight detection, advanced effects, and enhancement.

## Core Components

### Pegasus Editor
Video highlight detection and editing system that automatically identifies key moments in videos.
- Located in `src/pegasus/`
- Main application entry: `src/pegasus/app.py`
- Sports-specific functionality: `src/pegasus/sport.py`

### Videous CHEF (Comprehensive Highlight Enhancement Framework)
Advanced video processing and effects engine for professional-grade video enhancement.
- Located in `src/chef/` and `Videous CHEF/`
- Key modules:
  - `video_effects.py`: Core video effects processing
  - `videousapi.py`: API interface for video processing
  - `videomatting.py`: Video matting and background separation
  - `BGREPLACEVIDEOS.py`: Background replacement functionality
  - `depth_controller.py`: Depth estimation and control

### StarLeague
Video analysis and enhancement system for sports and gaming content.
- Located in `src/starleague/` and `StarLeague/`
- Main application: `StarLeague.py`
- Custom implementation: `StarLeaguecustom.py`

### RobustVideoMatting
Advanced video matting library for precise foreground extraction.
- Located in `RobustVideoMatting/`
- Inference scripts: `inference.py`, `inference_utils.py`
- Model definitions in `model/`

## Supporting Modules

### Core Utilities
- Located in `src/core/`
- `algorithms.py`: Core algorithms for video processing

### Utility Functions
- Located in `src/utils/`
- `config_manager.py`: Configuration management
- `s3_manager.py`: Amazon S3 integration for media storage

### Color Grading
- Located in `70 CGC LUTs/`
- Contains Look-Up Tables (LUTs) for professional color grading

## Media Storage

Media files are stored in Amazon S3:
- Bucket: `videous-media-files`
- Path: `s3://videous-media-files/videos/`
- Models: `s3://videous-media-files/models/`

## Setup and Installation

### Requirements
```
pip install -r requirements.txt
```

### Running the Application
```
python -m src.pegasus.app
```

### Development Environment
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up configuration in `configs/`

## Project Structure

```
videous-friends/
├── configs/                  # Configuration files
├── docs/                     # Documentation
├── models/                   # Model files (stored in S3)
├── scripts/                  # Utility scripts
├── src/
│   ├── chef/                 # Videous CHEF modules
│   ├── core/                 # Core algorithms
│   ├── pegasus/              # Pegasus Editor
│   ├── starleague/           # StarLeague
│   └── utils/                # Utility functions
└── tests/                    # Test suite
```

## Additional Resources

- See the `docs` directory for detailed documentation
- Configuration templates available in `configs/`
- Test suite in `tests/`

## License

Proprietary - All rights reserved
