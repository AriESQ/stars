# OpenMapper
## A Videomapper based on three.js

Runs on any plattform using Chrome or Firefox.
See [openmapper.ch](https://openmapper.ch)


</br>


[![Alt text](https://gitlab.com/Jaun1011/openmapper/raw/master/doc/openmapper_video_thumb.png)](https://vimeo.com/340283326)

### Find more devs!
If you are good in Three.js, JavaScript, Typescript, Mathematics, contact info at magdesign for work.</br>



## Usage

Node.js must be installed on the system.

### Install
```sh
cd client

$ npm install
```

```sh
cd backend

$ npm install
```

### Start Local Instance
```sh
$ cd client
$ npm run start

```

```sh
$ cd backend
$ npm run start:rest
```
(the `start:rest` is needed to display all the movies selectable from the folder)

### Run Tests
```sh
$ npm run test
```


### Build
```sh
$ npm run build

```
```
Open address in browser: localhost:8080
```

********************************

# Next steps (high priority)

- [ ] Fix Cutter!!

- [ ] Add comments in code, so we understand what is going on!
- [x] Hide menu by default, [see here](https://github.com/DefinitelyTyped/DefinitelyTyped/issues/36879)
- [ ] Autoplay videos by default
- [ ] Outlines and cutter hidden by default
- [ ] Add save and load presets 1-9, always load preset 1 when starting first time
- [ ] Make each quad selectable with [Raycaster](https://threejs.org/docs/#api/en/core/Raycaster) function (Sprites are selectable, Meshes still need work)
- [ ] The selected quad will update the menu content to show the current video, speed etc.
- [ ] Create seperate function for cutter, will open 80% of screen, quads not visible (see video)
- [x] Add fullsize function, so selected quad can be made fullscreen of browsers current window size, use [this](https://discourse.threejs.org/t/functions-to-calculate-the-visible-width-height-at-a-given-z-depth-from-a-perspective-camera/269) as solution
- [x] Add keycodes to all menu entrys so we can control with keystrokes
- [ ] Add iframe source, [see here](https://adndevblog.typepad.com/cloud_and_mobile/2015/07/embedding-webpages-in-a-3d-threejs-scene.html) to add slideshows and webpages
- [ ] Rewind, fast forward (for videos)

- here is a very good paper describing the mathematical stuff: https://www.inf.ufrgs.br/~oliveira/pubs_files/PG01_Adaptive_subdivision.pdf

## Medium priority

- [ ] Remote access on mapper (websockets, remote control mapping from another device)
- [ ] Sync various instances of openmappers
- [ ] Render mapping to file using [this](https://github.com/spite/ccapture.js/#what-is-ccapturejs-and-why-would-i-need-it) or  [this](https://janakiev.com/til/videos-and-gifs-with-threejs/)
- [x] Layer Up/Down for selected quad (mover spprite is faulty and needs a fix!)

@Jan => can you please explain in a few words how the Websockets thing is ment to work!

## Low priority

- [ ] Auto Snatch Draghandles
- [ ] Add resolution slider (5 - 200 quads resolution)


## Nice to have

- [ ] Other surfaces triangles, spheres (highly needed together with warp!), hexagons
- [ ] Bezier function [check this](https://computergraphics.stackexchange.com/questions/3764/apply-distortion-to-b%C3%A9zier-surface?answertab=votes#tab-top) might be based on [this](https://pomax.github.io/bezierjs/) and needs again a shit load of mathematical braining....
- [ ] List in UI to show all connected slaves
- [ ] Grid warp, see [this paper](https://www.ronenbarzel.org/papers/warp.pdf)
- [ ] Adjust brightness, contrast, rgb of output texture with [filters](https://threejs.org/examples/?q=filt#webgl_materials_texture_filters)
- [ ] Softedge blending on each surface
- [ ] Audio reactive FX
- [ ] OSC and APi to remotely load other files
- [ ] integrated DMX player (this is easy, take the scripts from PocketVJ)

### Openend issues regarding this project
- [ ] dat.gui Hide menu bug: https://github.com/DefinitelyTyped/DefinitelyTyped/issues/36879
- [ ] NDI Support: https://github.com/Streampunk/grandiose/issues/3