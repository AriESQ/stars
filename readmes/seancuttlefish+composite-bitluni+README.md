# composite-bitluni

Original code taken from: https://github.com/bitluni/ESP32SpaceShooter

This is a stripped-down program for generating composite video on the ESP32 based on bitluni's "Space Shooter" game. It was the starting point for the vdu project, but is generally useful when working with bitluni's composite video code for the ESP32.

Basically, I took all of the code I didn't want out of bitluni's game to leave something that allows you to draw text, dots, lines, triangles and filled and unfilled rectangles. I also added some comments and moved a few things around to help with readabiliy. The process of doing this was very helpful in helping me to understand his code. All the good stuff is still bitluni's, of couse.

As with the bitluni original, the composite video output is on pin 25. Yhere is no audio in this version.

### Control
- graphics.init
- graphics.begin
- graphics.end

### Text
- graphics.setTextColor(int front, int back)
- graphics.setFont(Font &font)
- graphics.setCursor(int x, int y)
- graphics.print(const char *str)
- graphics.print(int number, int base = 10, int minCharacters = 1)

### Graphic
- graphics.dot(int x, int y, int color) // there are other dot related functions.
- graphics.line(int x1, int y1, int x2, int y2, unsigned int color)
- graphics.triangle(int x1, int y1, int x2, int y2, int x3, int y3, unsigned int color)
- graphics.rect(int x, int y, int w, int h, unsigned int color)
- graphics.fillRect(int x, int y, int w, int h, unsigned int color)

### Colour
- graphics.rgb
- graphics.rgba

## Notes

### SimplePALOutpit.h
- The composite-video-over-the-ESP32's-DAC stuff is all very clever and explained in bitluni's YouTube videos.

### RGB2YUV.h
- This is a big lookup table used in the conversion of RGB to the YUV colour model used in composite video.

### Graphics.cpp / Graphics.h
- There is a "backbuffer" where all the updates are placed while a frame is being constructed.
- The backbuffer is copied to "frame" when it is ready to be displayed.
- "Graphics.init" creates the buffer.
- "Graphics.begin" (optionally) clears the buffer.
- "Graphics.end" copies the buffer to the frame for SimplePALOutpit.h to render as composite video.
- The "Graphics.dot" functions are used when rasterising (converting to dots) a line, rectangle. rect etc.
- "Graphics.dotFast" has no frame boundary check. Is it that much faster?
- The "Graphics.line" function works out the dots that need to be shown when drawing a line between two points.
- I base all of my polygons (triangles, filled and unfilled squares) on Graphics.line. bitluni's code is a little different.
- Rather than develop any more graphical functions, I think fuure versions of this code should make use of a pre-existing graphics library.

### bitluni's Videos
- Pt1 https://www.youtube.com/watch?v=5t1_XNc3vNw
- Pt2 https://www.youtube.com/watch?v=Qpt14gJVpTk
- Pt3 https://www.youtube.com/watch?v=MOoKQnWF4OY
- Pt4 https://www.youtube.com/watch?v=-JXuwwXQh8c

