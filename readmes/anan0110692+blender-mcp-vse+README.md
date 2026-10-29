# BlenderMCP-VSE - Blender Video Editing with AI

<p align="center">
  <img src="assets/hammer-icon.png" alt="BlenderMCP-VSE" width="120"/>
</p>

**BlenderMCP-VSE** extends the original [BlenderMCP](https://github.com/ahujasid/blender-mcp) project with a complete **Video Sequence Editor (VSE)** integration, enabling AI-powered video editing through Claude and the Model Context Protocol (MCP).

This fork transforms Blender into an AI-controllable video editing suite, allowing you to edit videos, add effects, manage audio, and render outputs - all through natural language commands.

---

## What's New in This Fork

### Video Sequence Editor (VSE) Integration

This fork adds **30+ new tools** for complete video editing capabilities:

| Category | Tools |
|----------|-------|
| **Strip Management** | Add movie, sound, image, image sequence, scene, color, and text strips |
| **Strip Editing** | Move, trim, cut, duplicate, delete strips |
| **Effects & Transitions** | Cross-fade, wipe, gamma cross, and other transitions |
| **Audio Control** | Volume, pan, and audio strip management |
| **Advanced Effects** | Speed control, adjustment layers, effect strips |
| **Timeline Control** | Frame navigation, preview range, playback control |
| **Organization** | Meta strips for grouping, multi-strip selection |
| **Export** | Render settings, codec selection, animation rendering |

---

## Features

### Original BlenderMCP Features
- **Two-way Communication**: Connect Claude AI to Blender through socket-based server
- **3D Object Manipulation**: Create, modify, and delete 3D objects
- **Material Control**: Apply and modify materials and colors
- **Scene Inspection**: Get detailed information about the current scene
- **Code Execution**: Run Python code in Blender from Claude
- **Poly Haven Integration**: Download HDRIs, textures, and 3D models
- **Hyper3D Rodin**: AI-generated 3D models
- **Sketchfab Integration**: Search and download 3D models
- **Hunyuan3D Support**: Additional AI model generation

### New VSE Features
- **Import Media**: Add videos, audio, images, and image sequences
- **Non-Linear Editing**: Cut, trim, move, and arrange clips on the timeline
- **Transitions**: Add cross-fades, wipes, and other transitions between clips
- **Text Overlays**: Add text strips with customizable properties
- **Color Strips**: Create solid color backgrounds or overlays
- **Audio Editing**: Control volume, pan, and audio timing
- **Speed Effects**: Reverse playback, slow motion, speed ramping
- **Adjustment Layers**: Apply effects across multiple strips
- **Meta Strips**: Group strips together for organization
- **Render Output**: Configure resolution, FPS, codec, and export video

---

## Installation

### Prerequisites

- **Blender 4.0+** (compatible with Blender 5.x)
- **Python 3.10+**
- **uv package manager**

#### Install uv

**macOS:**
```bash
brew install uv
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Add uv to PATH (Windows):
```powershell
$localBin = "$env:USERPROFILE\.local\bin"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$userPath;$localBin", "User")
```

**Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### Step 1: Install the Blender Addon

1. Download `addon.py` from this repository
2. Open Blender
3. Go to **Edit > Preferences > Add-ons**
4. Click **"Install..."** and select the `addon.py` file
5. Enable the addon by checking **"Interface: Blender MCP"**

### Step 2: Configure MCP Server

#### Claude Desktop

Edit your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/anan0110692/blender-mcp-vse", "blender-mcp"]
        }
    }
}
```

#### Claude Code CLI

```bash
claude mcp add blender -- uvx --from git+https://github.com/anan0110692/blender-mcp-vse blender-mcp
```

#### Cursor

Add to your MCP settings (Settings > MCP):

**macOS/Linux:**
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/anan0110692/blender-mcp-vse", "blender-mcp"]
        }
    }
}
```

**Windows:**
```json
{
    "mcpServers": {
        "blender": {
            "command": "cmd",
            "args": ["/c", "uvx", "--from", "git+https://github.com/anan0110692/blender-mcp-vse", "blender-mcp"]
        }
    }
}
```

---

## Usage

### Enabling VSE Integration

1. In Blender, open the **3D View sidebar** (press `N`)
2. Find the **"BlenderMCP"** tab
3. Check **"Use Video Editing (VSE)"** to enable video editing tools
4. Click **"Connect to Claude"**

### Example Commands

#### Video Editing
- *"Import the video from E:\Videos\clip.mp4 and add it to the timeline"*
- *"Cut the video at frame 100"*
- *"Trim the first 2 seconds from the beginning of the clip"*
- *"Add a cross-fade transition between the two clips"*
- *"Reverse the video playback"*
- *"Set the video to play at half speed"*

#### Audio
- *"Add background music from music.mp3 on channel 2"*
- *"Set the audio volume to 50%"*
- *"Mute the original video audio"*

#### Text & Graphics
- *"Add a title that says 'Welcome' at the beginning"*
- *"Create a black color strip for 30 frames as an intro"*
- *"Add a fade-in effect to the first clip"*

#### Export
- *"Set the output resolution to 1920x1080"*
- *"Set the frame rate to 30 fps"*
- *"Render the video as H.264 MP4"*

#### 3D + Video Workflow
- *"Create a 3D scene with a rotating cube, then render it as a video strip"*
- *"Add the 3D render to the timeline and add music underneath"*

---

## VSE Tools Reference

### Media Import
| Tool | Description |
|------|-------------|
| `add_movie_strip` | Add video file to timeline |
| `add_sound_strip` | Add audio file to timeline |
| `add_image_strip` | Add single image as strip |
| `add_image_sequence` | Add image sequence as strip |
| `add_scene_strip` | Add Blender scene as strip |
| `add_color_strip` | Add solid color strip |
| `add_text_strip` | Add text overlay strip |

### Strip Editing
| Tool | Description |
|------|-------------|
| `get_strip_info` | Get detailed strip information |
| `move_strip` | Move strip to different position/channel |
| `trim_strip` | Trim strip start/end points |
| `cut_strip` | Split strip at specific frame |
| `duplicate_strip` | Create copy of strip |
| `delete_strip` | Remove strip from timeline |
| `set_strip_properties` | Modify strip properties |

### Effects & Transitions
| Tool | Description |
|------|-------------|
| `add_transition` | Add transition between strips |
| `add_effect_strip` | Add visual effect |
| `add_adjustment_layer` | Add adjustment layer |
| `add_speed_control` | Control playback speed/reverse |

### Audio
| Tool | Description |
|------|-------------|
| `set_strip_volume` | Adjust audio volume |
| `set_strip_pan` | Adjust stereo panning |

### Timeline
| Tool | Description |
|------|-------------|
| `get_vse_info` | Get timeline overview |
| `set_frame_current` | Jump to specific frame |
| `set_frame_range` | Set start/end frames |
| `set_preview_range` | Set preview range |
| `get_strips_at_frame` | Find strips at frame |

### Organization
| Tool | Description |
|------|-------------|
| `make_meta_strip` | Group strips together |
| `unmake_meta_strip` | Ungroup meta strip |
| `select_strips` | Select specific strips |
| `select_all_strips` | Select all strips |

### Rendering
| Tool | Description |
|------|-------------|
| `set_render_settings` | Configure output settings |
| `render_animation` | Render video output |

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BLENDER_HOST` | `localhost` | Blender socket server host |
| `BLENDER_PORT` | `9876` | Blender socket server port |
| `DISABLE_TELEMETRY` | `false` | Disable anonymous telemetry |

### Disabling Telemetry

```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/anan0110692/blender-mcp-vse", "blender-mcp"],
            "env": {
                "DISABLE_TELEMETRY": "true"
            }
        }
    }
}
```

---

## Compatibility

- **Blender 4.x**: Full support
- **Blender 5.x**: Full support (API compatibility layer included)
- **Operating Systems**: Windows, macOS, Linux

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| VSE tools not appearing | Enable "Use Video Editing (VSE)" in the BlenderMCP panel |
| Connection failed | Ensure Blender addon is running and connected |
| Strip not found | Check strip name with `get_vse_info` |
| Render fails | Verify output path is writable |
| Audio not playing | Check if audio strip is muted |

---

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

## Credits

- **Original BlenderMCP**: [Siddharth Ahuja](https://github.com/ahujasid/blender-mcp)
- **VSE Extension**: [anan0110692](https://github.com/anan0110692)

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Disclaimer

This is a community project and not officially affiliated with Blender Foundation or Anthropic.
