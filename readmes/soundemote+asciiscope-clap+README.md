# asciiscope-clap

https://mit-license.org/
```rust
// project version 0.1.0
// Soundemote signal visuals inside CLAP/JUCE hosts
// plugin window now, live synth visuals next

plugin identity : Asciiscope CLAP
foundation      : baconpaul sidequest-startingpoint
format path     : CLAP first, VST3/AUv2 wrappers from clap-wrapper
visual goal     : dark colorful console-style signal art
render goal     : CPU-built sample-coherent glyph traces, GPU effects later
next step       : richer snapshot-fed ASCII scenes inside the JUCE editor
```
![example.gif](https://github.com/soundemote/asciiscope/blob/main/example.gif)

## what is this?

Asciiscope CLAP is the plugin-side path for Asciiscope.

The terminal app stays independent and terminal-first. This repo adapts the
same signal-visual idea into a plugin editor that can eventually react to synths,
tracks, buses, and host automation.

```text
asciiscope       -> terminal-native visual instrument
asciiscope-clap  -> plugin editor / host input path
soemdsp          -> future shared DSP and signal concepts
```

## current status

This repo is still intentionally close to the startingpoint architecture.

```markdown
done  : visible product/plugin identity rename to Asciiscope CLAP
done  : tiny JUCE visual component with demo/VU-derived motion
done  : audio-to-editor visual snapshot boundary
done  : snapshot timing metadata for sample-aware visual rendering
done  : rolling UI-side waveform history for block snapshots
done  : simple Scope Mode and Palette plugin parameters
done  : Trace Gain parameter for pushing quiet input into visible motion
done  : stereo snapshot history for width-reactive visual motion
done  : snapshot block/frame/age readouts for host testing
done  : stereo correlation in the audio snapshot readout
done  : width-reactive sparkle from stereo correlation
done  : transient/crest flash from audio snapshot peaks
done  : transient-reactive scope frame glow
done  : subtle terminal scanline texture over the JUCE scope view
done  : translucent readout shelves for denser scope scenes
done  : smoothed visual metrics for steadier host readouts
done  : live/stale snapshot feed indicator
done  : stale snapshot visual decay for calmer transport-stop behavior
done  : compact L/R meters inside the scope frame
done  : peak-hold ticks on the L/R meters
done  : compact stereo correlation meter inside the scope frame
done  : smoothed L/R levels for steadier meters and motion
done  : sin/cos circle diagnostic button with frequency control
done  : neutral visual frame built from glyph cells, trace glyphs, and readouts
done  : JUCE Graphics renderer for the visual frame
done  : distinct Wave, Mirror, and Spectral frame-building paths
done  : phosphor-style glyph memory for smoother JUCE frame trails
done  : moving sin/cos circle diagnostic with persistent ASCII trail
done  : point-to-point interpolation for contiguous circle trails
done  : Trace Interpolation modes for Off, Linear, and Catmull trail smoothing
done  : Trace Interpolation also smooths rolling audio history sampling
done  : Trace Sync parameter for rising-zero-crossing waveform stabilization
done  : trace interpolation applied to Wave, Mirror, and Spectral overlays
done  : bright live trace glyph overlay for Wave, Mirror, and Spectral modes
done  : short phosphor memory for live trace glyph overlays
done  : stereo phase spark layer from actual audio snapshot samples
done  : silence-aware phase sparks for calmer host input testing
done  : quiet/signal state in the snapshot feed readout
done  : renderer readout confirms current JUCE glyph path
kept  : existing engine/editor/classes/namespace shape
next  : plugin-host visual testing and denser trace experiments
later : optional GPU effects after the CPU glyph/trace renderer
later : Asciiscope scene/render adapter
```

## build

```powershell
cmake -S . -B build
cmake --build build --config Release
```

The project currently builds CLAP, VST3, AUv2 wrapper targets, and a standalone
target through the existing startingpoint/clap-wrapper setup.

Current Windows build artifacts:

```text
build\asciiscope-clap_assets\CLAP\Release\Asciiscope CLAP.clap
build\asciiscope-clap_assets\VST3\Release\Asciiscope CLAP.vst3
build\asciiscope-clap_assets\Standalone-asciiscope-clap_standalone\Release\Asciiscope CLAP.exe
```

The standalone is the fastest editor smoke test. The CLAP build is the main host
target for live synth/signal testing.

## architecture notes

Preserved for now:

```markdown
baconpaul::sidequest_ns namespace
clapimpl::SideQuest<multiOut>
ui::PluginEditor
ui::MainPanel
60 Hz editor IdleTimer
existing scalar audio/UI queue
current audio port shape
```

Near-term insertion point:

```text
Engine::process()
    -> lightweight visual snapshot, published with non-blocking try_lock
    -> PluginEditor::idle()
    -> AsciiscopeVisualComponent::repaint()
    -> AsciiscopeVisualComponent::paint(juce::Graphics&)
```

Current extraction seams:

```markdown
signal enters        : Engine::process() captures output blocks
state updates        : PluginEditor::idle() drains the latest snapshot
drawing happens      : AsciiscopeVisualComponent::paint()
reusable core        : snapshot shape, rolling history, visual frame, visual mode math
plugin/editor shell  : patch params, MainPanel ownership, JUCE repaint loop
```

Do not make the terminal app become a plugin project. The plugin should adapt to
Asciiscope concepts.

`IVisualSurface` is still deferred. The current priority is learning what the
JUCE editor needs from snapshot-fed drawing before shaping a shared surface API.

The base renderer should stay CPU-first and sample-aware. That is the cleanest
path for tight audio/visual cohesion: waveform traces, interpolation, trail
memory, and glyph placement can be generated from the same signal timeline that
feeds the sound, with temporal density limited by the source data and visual
budget rather than by a GPU frame clock.

GPU work is still useful later, but as an effects/output layer after the CPU
visual state exists: glow, bloom, phosphor diffusion, feedback, capture surfaces,
or Syphon/Spout-style output experiments. The plugin should remain usable with
the default JUCE software renderer, and the console identity should stay
glyph-first either way.

## future

```rust
AsciiscopeVisualComponent
// small JUCE component with the dark console look

AsciiscopeVisualFrame
// glyph cells, trace glyphs, and readouts generated before drawing

JuceVisualFrameRenderer
// current default CPU draw path using juce::Graphics and monospaced glyphs

GpuVisualEffectsLayer
// optional later layer for glow, bloom, feedback, and capture/output experiments

DemoVisualInput
// non-audio first visual feed for proving editor rendering

AudioVisualSnapshot
// lock-safe handoff from audio thread to editor thread, now present in minimal form

RollingWaveformHistory
// UI-side fixed buffer that turns small audio blocks into a visible trace

SignalFrameAdapter
// maps plugin data toward Asciiscope SignalFrame concepts

LiveScopeMode
// oscilloscope / spectral / particle modes driven by real synth signals
```
