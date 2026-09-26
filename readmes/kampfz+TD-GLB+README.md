# TD-GLB

TouchDesigner C++ plugins for importing GLB (binary glTF) files.

## Plugins

### GLBImportSOP — GLB Geometry Importer
A CPlusPlus **SOP** node that parses a GLB file and outputs its triangle mesh geometry to the GPU via the VBO path (`directToGPU = true`).

**Features:**
- Imports positions, normals, and UV coordinates (TEXCOORD_0) from all triangle primitives in the file
- Flips V (glTF V=0 is top-left; TD/OpenGL V=0 is bottom-left)
- Handles indexed and non-indexed primitives, and interleaved/strided buffer views
- Supports FLOAT, UNSIGNED_BYTE, and UNSIGNED_SHORT UV component types
- File is parsed once on load and cached; use the **Reload** pulse to force re-parse
- GPU-resident VBO (Static mode) — no per-frame CPU cost after initial upload

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| GLB File  | Path to the `.glb` file |
| Reload    | Pulse to re-parse the file without changing the path |

**Usage:**
1. Set the **GLB File** parameter
2. Add the SOP to a **Render TOP** via a Geometry COMP and apply a Phong, PBR, or Constant material

> Because `directToGPU = true`, this SOP outputs directly to the GPU and cannot be wired into other SOP nodes. It is intended for rendering via a Render TOP.

---

### GLBTextureTOP — GLB Texture Extractor
A CPlusPlus **TOP** node that extracts an embedded PBR texture from a GLB file and outputs it as an RGBA8 texture.

**Features:**
- Extracts any of the five standard PBR texture slots from a material
- Converts any channel count (R, RG, RGB, RGBA) to RGBA8
- File is parsed once on load and cached; use the **Reload** pulse to force re-parse

**Parameters:**
| Parameter      | Description |
|----------------|-------------|
| GLB File       | Path to the `.glb` file |
| Material Index | Which material in the file to read from (0-based) |
| Texture Slot   | Base Color / Normal / Metallic-Roughness / Emissive / Occlusion |
| Reload         | Pulse to re-parse the file without changing the path |

---

## Building

### Requirements
- Visual Studio 2022 (v143 toolset)
- TouchDesigner installed at `C:\Program Files\Derivative\TouchDesigner\`
- [tinygltf](https://github.com/syoyo/tinygltf) headers placed in `third_party/tinygltf/`
  - `tiny_gltf.h`
  - `json.hpp`
  - `stb_image.h`
  - `stb_image_write.h`

### Steps
1. Open `GLBImportSOP.sln` in Visual Studio
2. Select **Release | x64**
3. Build → Rebuild Solution
4. Output DLLs are placed in `Release/`
   - `Release/GLBImportSOP.dll`
   - `Release/GLBTextureTOP.dll`

If TouchDesigner is installed in a non-default location, update the `TDSamplesDir` property in each `.vcxproj` file.

---

## Installation as Custom Node Types

These plugins can be installed as first-class TouchDesigner node types that appear in the OP Create dialog alongside built-in nodes.

1. Copy the built DLLs to your TouchDesigner plugins folder:
   ```
   %USERPROFILE%\Documents\Derivative\TouchDesigner\Plugins\
   ```
   Create the `Plugins` folder if it doesn't exist.

2. Restart TouchDesigner.

**GLB Import** will appear in the SOP family and **GLB Texture** in the TOP family — no need to use a generic CPlusPlus SOP/TOP node.

For per-project installation instead of global, set a custom path via **Edit → Preferences → DATs → Custom OP Path**.
