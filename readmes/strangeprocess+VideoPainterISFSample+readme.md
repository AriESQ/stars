# Creating Your Own ISF Shader Libraries

This guide walks you through creating a custom ISF (Interactive Shader Format) visual library for Video Painter. No programming experience is required to get started — we'll begin with the basics and build up from there.

---

## What is an ISF Shader?

An ISF shader is a small program that generates visuals in real time. It runs on your GPU (graphics card), which means it can produce complex, animated visuals at high frame rates. ISF is an open standard used by many VJ and visual performance tools.

In Video Painter, ISF shaders respond to **triggers** — clicks, MIDI notes, or audio inpur (based on dB threshold setting) by drawing shapes, patterns, and effects at each trigger point.

---

## Step 1: Set Up Your Library Folder

Create a folder on your computer with the name you want your library to have. Inside it, you need two files:

```
My Custom Shader/
  library.json
  shader.fs
```

That's it — just two files.

---

## Step 2: Create library.json

This file tells Video Painter about your library. Create a text file called `library.json` with the following content:

```json
{
  "name": "My Custom Shader",
  "type": "ISF Shader",
  "author": "Your Name",
  "description": "A short description of what your shader does",
  "version": "1.0.0"
}
```

| Field | Required? | Description |
|-------|-----------|-------------|
| `name` | Yes | The name shown in the library dropdown |
| `type` | Yes | Must be `"ISF Shader"` |
| `author` | Recommended | Your name or alias |
| `description` | Recommended | A brief description |
| `version` | Recommended | Version number for your own tracking |

---

## Step 3: Create Your Shader (shader.fs)

This is where the magic happens. An ISF shader file has two parts: a **JSON header** that defines your controls, and the **GLSL shader code** that generates the visuals.

Here's a minimal working example — a simple color pulse that responds to triggers:

```glsl
/*{
    "DESCRIPTION": "Colored circles that appear at trigger points",
    "CREDIT": "Your Name",
    "ISFVSN": "2.0",
    "CATEGORIES": ["Generator"],
    "INPUTS": [
        {
            "NAME": "circleSize",
            "TYPE": "float",
            "LABEL": "Circle Size",
            "MIN": 0.1,
            "MAX": 2.0,
            "DEFAULT": 0.5
        }
    ]
}*/

// Video Painter trigger uniforms
uniform int u_active_instances;
uniform vec2 u_instance_centers[30];
uniform float u_instance_ages[30];
uniform float u_scale;
uniform float u_scaleBoost;

void main() {
    vec2 uv = isf_FragNormCoord;
    vec4 finalColor = vec4(0.0, 0.0, 0.0, 1.0);

    for (int i = 0; i < 30; i++) {
        if (i >= u_active_instances) break;

        vec2 center = u_instance_centers[i];
        float age = u_instance_ages[i];
        float dist = distance(uv, center);
        float radius = circleSize * 0.15 * u_scaleBoost * (1.0 - age);

        if (dist < radius) {
            float fade = (1.0 - dist / radius) * (1.0 - age);
            vec3 color = vec3(0.2, 0.6, 1.0);
            finalColor.rgb += color * fade;
        }
    }

    gl_FragColor = finalColor;
}
```

Save this as `shader.fs` in your library folder.

---

## Step 4: Import Into Video Painter

1. Open Video Painter
2. Go to **File > Import Library** in the menu bar (or drag-and-drop your folder into the application window)
3. Select your library folder in via the Library slider or the Library Manager (cmd+L)
4. Your shader will be added the end of the library list
5. Optionally, you can create a 240x160px thumbnail image to represent your library, and include in your library folder. The Library Manager will automatically detect and display one if present.

---

## Understanding the Shader Structure

### The JSON Header

The header is wrapped in `/*{ }*/` at the top of the file. It defines:

- **DESCRIPTION** — What your shader does
- **CREDIT** — Author name
- **ISFVSN** — ISF version (use `"2.0"`)
- **CATEGORIES** — Tags for organization (optional)
- **INPUTS** — The controls that appear as sliders in Video Painter's UI

### Input Types

You can add different types of controls:

**Float (slider):**
```json
{
    "NAME": "speed",
    "TYPE": "float",
    "LABEL": "Animation Speed",
    "MIN": 0.0,
    "MAX": 5.0,
    "DEFAULT": 1.0
}
```

**Boolean (toggle):**
```json
{
    "NAME": "invertColors",
    "TYPE": "bool",
    "LABEL": "Invert Colors",
    "DEFAULT": false
}
```

**Integer (stepped slider):**
```json
{
    "NAME": "segments",
    "TYPE": "long",
    "LABEL": "Segments",
    "MIN": 2,
    "MAX": 16,
    "DEFAULT": 6
}
```

**Color (color picker):**
```json
{
    "NAME": "color1",
    "TYPE": "color",
    "LABEL": "Base Color",
    "DEFAULT": [1.0, 0.0, 0.5, 1.0]
}
```

Color defaults are `[Red, Green, Blue, Alpha]`, each from 0.0 to 1.0.

### Built-In Variables

Video Painter automatically provides these variables — **do not declare them yourself**:

| Variable | Type | Description |
|----------|------|-------------|
| `TIME` | float | Elapsed time in seconds |
| `TIMEDELTA` | float | Time since last frame |
| `RENDERSIZE` | vec2 | Screen resolution in pixels |
| `FRAMEINDEX` | int | Current frame number |
| `isf_FragNormCoord` | vec2 | Current pixel position (0.0 to 1.0) |

Your INPUTS are also auto-declared. If you define an input named `speed`, you can use `speed` directly in your code — no need for a `uniform float speed;` line.

### Trigger Uniforms

These are the uniforms that connect your shader to Video Painter's trigger system (clicks, MIDI, audio). Unlike the built-in ISF variables above, **you must declare these yourself**:

```glsl
uniform int u_active_instances;         // Number of active triggers (0-30)
uniform vec2 u_instance_centers[30];    // Position of each trigger (0-1 range)
uniform float u_instance_notes[30];     // MIDI note value (0-1)
uniform float u_instance_ages[30];      // Age of each trigger (0=new, 1=faded)
uniform float u_instance_ids[30];       // Unique ID for each trigger

uniform float u_scale;                  // Global scale parameter
uniform float u_scaleBoost;             // Scale boost for trigger response
```

You only need to declare the ones you actually use.

---

## Tips and Tricks

### Slider Ordering

ISF sorts inputs **alphabetically** by NAME. To control the order sliders appear in the UI, prefix your names:

```json
{ "NAME": "aaSpeed",    "LABEL": "Speed",   ... },
{ "NAME": "abSize",     "LABEL": "Size",    ... },
{ "NAME": "zzColorR",   "LABEL": "Color R", ... },
{ "NAME": "zzColorG",   "LABEL": "Color G", ... },
{ "NAME": "zzColorB",   "LABEL": "Color B", ... }
```

The LABEL is what users see — the NAME prefix is just for ordering.

### Looping Through Triggers

Always use a fixed loop bound of 30 and break early:

```glsl
for (int i = 0; i < 30; i++) {
    if (i >= u_active_instances) break;
    // ... your trigger code here
}
```

This is required for compatibility with all graphics cards.

### Using Time for Animation

```glsl
// Smooth wave
float wave = sin(TIME * speed) * 0.5 + 0.5;

// Cycling through colors
vec3 color = vec3(
    sin(TIME) * 0.5 + 0.5,
    sin(TIME + 2.094) * 0.5 + 0.5,
    sin(TIME + 4.189) * 0.5 + 0.5
);
```

### Smooth Falloff for Circles

```glsl
float dist = distance(uv, center);
float radius = 0.1;
float glow = smoothstep(radius, 0.0, dist);  // Soft edge
```

---

## Optional: shader.json (Trigger Tuning)

You can add an optional `shader.json` file to your library folder to fine-tune how triggers behave:

```json
{
  "fadeTime": 5.0,
  "scaleBoost": 2.0,
  "maxInstances": 20
}
```

| Field | Default | Description |
|-------|---------|-------------|
| `fadeTime` | 3.0 | How many seconds triggers remain visible |
| `scaleBoost` | 1.0 | Size multiplier for trigger response |
| `maxInstances` | 30 | Maximum simultaneous active triggers |

---

## Complete Example: Rainbow Rings

Here's a complete library you can copy and use as a starting point.

**library.json:**
```json
{
  "name": "Rainbow Rings",
  "type": "ISF Shader",
  "author": "Your Name",
  "description": "Expanding rainbow rings at each trigger point",
  "version": "1.0.0"
}
```

**shader.fs:**
```glsl
/*{
    "DESCRIPTION": "Expanding rainbow rings at trigger points",
    "CREDIT": "Your Name",
    "ISFVSN": "2.0",
    "CATEGORIES": ["Generator", "Color"],
    "INPUTS": [
        {
            "NAME": "ringWidth",
            "TYPE": "float",
            "LABEL": "Ring Width",
            "MIN": 0.005,
            "MAX": 0.1,
            "DEFAULT": 0.02
        },
        {
            "NAME": "expandSpeed",
            "TYPE": "float",
            "LABEL": "Expand Speed",
            "MIN": 0.1,
            "MAX": 3.0,
            "DEFAULT": 1.0
        },
        {
            "NAME": "brightness",
            "TYPE": "float",
            "LABEL": "Brightness",
            "MIN": 0.1,
            "MAX": 2.0,
            "DEFAULT": 1.0
        }
    ]
}*/

uniform int u_active_instances;
uniform vec2 u_instance_centers[30];
uniform float u_instance_ages[30];
uniform float u_instance_ids[30];
uniform float u_scaleBoost;

// Convert hue to RGB
vec3 hue2rgb(float h) {
    return clamp(abs(mod(h * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0);
}

void main() {
    vec2 uv = isf_FragNormCoord;

    // Correct for screen aspect ratio so circles aren't stretched
    float aspect = RENDERSIZE.x / RENDERSIZE.y;
    vec2 uvCorrected = vec2(uv.x * aspect, uv.y);

    vec3 finalColor = vec3(0.0);

    for (int i = 0; i < 30; i++) {
        if (i >= u_active_instances) break;

        vec2 center = vec2(u_instance_centers[i].x * aspect, u_instance_centers[i].y);
        float age = u_instance_ages[i];
        float id = u_instance_ids[i];

        // Ring expands outward over time
        float maxRadius = 0.3 * u_scaleBoost;
        float ringRadius = age * expandSpeed * maxRadius;
        float dist = distance(uvCorrected, center);

        // Draw ring
        float ring = smoothstep(ringWidth, 0.0, abs(dist - ringRadius));
        float fade = 1.0 - age;

        // Rainbow color based on angle + unique ID
        float angle = atan(uvCorrected.y - center.y, uvCorrected.x - center.x);
        float hue = angle / 6.2832 + id * 0.1 + TIME * 0.1;
        vec3 color = hue2rgb(hue);

        finalColor += color * ring * fade * brightness;
    }

    gl_FragColor = vec4(finalColor, 1.0);
}
```

**shader.json:**
```json
{
  "fadeTime": 4.0,
  "scaleBoost": 3.0
}
```

---

## Using Community ISF Shaders

There are hundreds of free ISF shaders available online that you can use as libraries:

- **ISF Editor** — Write and test shaders in your browser at [editor.isf.video](https://editor.isf.video)
- **ISF Gallery** — Browse community shaders at [isf.video](https://isf.video)

Note: Community shaders that are "generators" (they create visuals from scratch) work best. Shaders that require an input image or video are not currently supported.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Shader doesn't appear in dropdown | Check that `library.json` has `"type": "ISF Shader"` |
| Shader loads but shows black | Check for typos in your GLSL code. Try the ISF Editor to debug. |
| Sliders don't appear | Make sure your INPUTS are valid JSON (check for missing commas) |
| Triggers don't respond | Make sure you declared the `u_active_instances` and `u_instance_centers` uniforms |
| Shader loads with errors | Do not declare `TIME`, `RENDERSIZE`, or your INPUT names as uniforms — they are auto-injected |
| Sliders in wrong order | Use alphabetical NAME prefixes (e.g. `aaFirst`, `abSecond`, `zzLast`) |
