## Introduction

#### Why? 

Physical media distribution is rapidly becoming a dying art. Whether that's authoring CDs, DVDs, Cassette Tapes or VHS, the means of physical production for artists has an increasing bar of entry to it. This can be especially the case for new and younger artists who did not experience these mediums first-hand.

#### How?

By creating a format that is accessible to anyone with a computer. Whether it's a raspberry pi, a windows gaming laptop, a free wheeling linux machine or a mac. 

A format that is easily distributed via SD card, USB stick, or online.

#### What?

**Artist HTML**! 

Artists can create local-first web-pages as a home for their music, their visual artwork, whether that's images or video.

Artists can hand-craft these sites, or use one of the generators available: 

* **Your generator site here!**  Send a PR with code, or a link to add to this file!

--------
## Defining a standard

## Constraints

### Local-First

* Sites must execute without being online. The payload they come with should be sufficient to browse them.
* HTML + CSS + Javascript.
* Large frameworks and embedding huge JS run-times == a no-no
* Avoid embedding WASM for the same reason. 
* Don't assume the display. Build responsive, and cater for really constrained width/vertical for mobile, through to huge ass displays, with small screened raspberry-pi setups in between.
### File layout

An example media payload could be structured like so:

```
index.html
css\yourcss.css
pages\otherhtml.html
video\avideofile.mp4
audio\anaudiofile.mp3
```

All URLs should be relative to the root directory.

The only hard requirement here, is the index.html. Any players should assume this.
### Distribution media

* Standard sized SD Cards.
* Zip files.
* Hosted online
	* If so, a zip file for download to storage media should be supplied as a `ProjectName.zip` in the root of the website, and linked from index.html. This is to allow collectors to easily download as zip files, to then be extracted to SD Cards or loaded into dedicated playback hardware.

-----
## Examples

### Music
* [Audio Player](Examples/audio-album/index.html)

### Drawing/Painting
* Link your work here!

### Photography
* Link your work here!

### Video
* Link your work here!

----

Artist HTML is a passing thought from [Dave Wood](https://lightbeamapps.com) , Dave loves making apps and software that plays with real-time video, usually for mobile devices.

If you think this idea has legs, then drop me a line at [artisthtml@lightbeamapps.com](mailto:artisthtml@lightbeamapps.com). Artists are actively encouraged to raise PRs with their work to link here.

