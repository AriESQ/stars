################# DoubleVison Install Notes #################

1. Download and install filter plugins Recursion, Move, and Source Clone from obsproject.com. These are all
developed by user Exeldro and are available as free downloads. 


https://obsproject.com/forum/resources/recursion-effect.1008/
https://obsproject.com/forum/resources/move.913/
https://obsproject.com/forum/resources/source-clone.1632/


2. Once all plugins are installed, open OBS and select import under the Scene Collection tab in the tool bar.

3. Select the OBS DoubleVison.json file to load all scene data. This includes filters and filter settings for
each source.

4. Select your video capture device in the Video Capture Device properties

5. Open filter settings by right-clicking the Video Capture Device and selecting Filters. Open each of the Hue 
and Offset filter settings and scroll to the bottom. Click Start.

################# DoubleVision Patch Notes #################

This patch uses two combinations of Chroma Key + Recursion filter plugins to create a complex visual echo
pattern that is then modulated with a colorizer and automated offset values. The main patch is then
duplicated with the Source Clone plugin and flipped on the horizontal field. This is overlaid on top of the
first source and blended to create the final image.

Filters in OBS are processed sequentially from the top of the list down. See notes below:

	Chroma Key (keys out parts of the original image)
	↓
	Recursion (scale is set larger than the original image so that the recursions grow larger over top
	↓	   the image instead of tunneling into the image if the scale was set smaller. X and Y offset
	↓	   is then adjusted to keep the recursions closer to the center of the image. Delay is set
	↓	   to 500ms)
	↓
	Color Correction (adds some saturation before the next chroma key)
	↓
	Chroma Key 2 (keys out parts of the processed image thus far, including recursions that were
	↓	      processed above)
	↓
	Color Correction 2 (adds more saturation, the Hue parameter will be automated later to create a
	↓		    colorizer, which is affecting each of the recursions from above)
	↓
	Recursion 2 (the colorized recursions from above now enter a second recursion instance which is
	↓	     similar to the first but with a slightly longer delay at 800ms. This recursion 
	↓	     instance preserves the colors of each recursion from above. Instead of colorizing
	↓	     the entire image with the previous step, this recursion 'freezes' each iteration
	↓	     when it occurs and creates the rainbow effect. 
	↓
	Color Correction 3 (further adjustments to the processed image)
	↓
	Sharpen (sharpen adjustment to create sharper lines on the recursions and keeps the final
	↓	 image from getting muddy or washed out)
	↓
	Hue A + B (a pair of Move Value filters which automate the value of the Hue parameter of the 
	↓	   Color Correction 2 filter above. The value limit of the Hue parameter is +/-180 but the
	↓	   values can exceed be set beyond that limit in the Min/Max settings in Move Value. The A
	↓	   filter is set to start the B filter when completed. The B filter is set to start the A
	↓	   filter when completed. This creates an infinite, randomized, and dynamic colorizer.
	↓
	Offset X A + B (same process as above, but this Move automates the X Offset value of the Recursion 2
	↓		filter. Creates randomized movement on the X axis, swaying the rainbow echoes back
	↓		and forth.)
	↓
	Offset Y A + B (same process as above, but this Move automates the Y Offset value of the Recursion 2
	↓		filter. Creates randomized movement on the Y axis, bouncing the rainbow echoes up
	↓		and down. Combined with the Offset X Move above, this creates a subtle sense of
	↓		movement within the image and allows the recursions to spread out dynamically within
	↓		the scene.)
	↓
	Sharpen (sharpen adjustment to create sharper lines on the recursions and keeps the final
		 image from getting muddy or washed out)

The Source Clone filter is then used to duplicate this source so that we can use the Transform and Blend
settings to mirror the image on the horizontal field. 

################# Troubleshooting #################

1. Image is dark, completely blank, or static (not moving)

	-Check your video source. Try deactivating and reactivating video source in source properties

2. Recursions seem stuck or are not fading

	-This can happen sometimes if OBS is closed without deactivating the video device first. It will fade
	 over time but the Chroma Key filters can be deactived and reactived to clear the bad recursions

3. The automated filters are not working

	-Open filter settings for the Hue, and Offset X/Y filters and scroll to the bottom. Click Start

4. Recursions are flashing or blinking

	-This can happen if the delay time is changed to a greater value while the patch is running. IT will
	 fade in time

####################################################

All credit to Exeldro for creating and developing these filter plugins

https://obsproject.com/forum/resources/authors/exeldro.128836/
