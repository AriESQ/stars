# Synth V1

[https://v1.autr.studio](https://v1.autr.studio)

web-based video synth prototype circa 2022:

* uses simple WebGL context and ISF renderer code
* blocks flow from left-to-right and top-to-bottom (columns are organisational, drag and drop)
* right-click to assign MIDI
* blocks are compiled into single shader in real-time (inspired by Hydra)
* entire patch exports as an ISF (ie. VDMX, TD, OF etc)
* also exports JSON MIDI config for VDMX (must be manually reassigned)

some notes:

* very early version (bugs etc!)
* mini toggle buttons are to reduce range of adjustments for feedback
* WebGL context pauses rendering if not within window frame
* all WebMIDI assignments are smoothed
* L = quicksave (browser), P = save ISF (file)
* autoWB tool is to produce oscillations

Dev:

```
npm i
npm run dev
```

Prod:

```
cd build.synth.v1
chmod -x serve.sh
./serve.sh
```

### Synth V2 

pending refactor in another repo:

* includes spinoff of ISF spec (with backwards compat)
* backend / frontend separation (babylonjs & babylonnative)
* native implementation for rpi and upcycled hardware