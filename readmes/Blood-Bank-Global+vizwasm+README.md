This is how I typically generate a config for the sdlrig:

```
cargo build --target=wasm32-wasip1 --bin=tech && \
 cp  target/wasm32-wasip1/debug/tech.wasm ~/Desktop/veo/calc.wasm && \
 ls -l ~/Desktop/veo/calc.wasm
```

the main `calculate` function along with all the important strings for configuration and video definitions are in the tech.rs (sorry it's a bunch of assets not included in the repo, but you'll get the idea). The vizconfig.rs file uses all of that to generater the asset list for use by the controlling sdlrig application as well as sets up some basic UI / Keyboard HMI, the data model for the filters, recording, copy/paste, loops, etc.
