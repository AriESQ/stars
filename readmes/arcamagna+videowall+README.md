# videowall
**Mimics a video wall by creating an overlay filter for ffmpeg. Works with both videos and images.**

### Usage  
```  
videowall [options] [files..]
```
### Options
	-n <number>
	   Number of rows (max 16). Default is 4, or 3 in portrait mode.  
	
	-m <number>
	   Maximum number of files. This determines the tile sequence before repeating.  
	
	-M <letter>
	   Display mode for tiles. Landscape mode is used by default.
	   L  Use landscape files only.
	   p  Portrait mode.
	   P  Use portrait files only.
	
	-s <number>
	   Skip number of valid files e.g. -s4 use 5th valid file onwards.

	-c
	   File check (slower start up).
	
	-F <number>
	   Target frame rate. Default 30 fps.  
	
	-r
	   Find files recursively.  
	
	-f <string>
	   Filter filetype(s) e.g. "mp4 jpg".  
	
	-t <string>
	   Title type (name or tag) and position (centre or left) e.g. "tag centre". Default is no titles.
	
	-d <number>
	   Duration in seconds.
	
	-S
	   Shuffle file order.
	
	-g <string>
	   Grid or bezel colour and thickness e.g. "black 3" or "#000000 3". Default is no grid.  

	-a <path|number>
	   File name or tile number for audio source. Default is no audio.
	
	-o <path>
	   Specify a path and file name to record output.  

	-l
	   Use with output file to specify lossless H.264 encoding.

	-p
	   Use with output file to specify Apple ProRes encoding.

	-D
	   demo	

### Files
Directory name or list of videos/images. If omitted current directory is used.

### Operation
If there aren't enough files available or the number of files is limited with -m then they will be repeated to fill the given area.
Performance can be very slow for larger values of n especially when mode is L or P or tag is used for title.
Lossless or ProRes encoding can produce very large files. These have very little or no compression and are best used with a set duration.
Encoding parameters can be modified in the config file if needed.

Press q to quit

### Examples
```
videowall
```
Produces a 4x4 grid of videos and/or images from the current directory. Sequence will be repeated if there aren't 16 unique valid files.
```
videowall -Mp -Sn2 -g"#054da5 4" -t "tag centre"
```
2x4 random grid of videos each having a 4 px blue frame and title tag bottom centre if one exists.
```
videowall -n6 -f "mp4 mkv" -rs 50 -o "/tmp/6x6 video wall.mp4" ~
```
6x6 grid by recursively searching for mp4 and mkv files in user directory. The first 50 files will be skipped. Files will not be checked for valid
video streams. Output will be recorded to "/tmp/6x6 video wall.mp4" instead of displaying on screen.
