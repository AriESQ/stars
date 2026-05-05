# DVA-Fidelity

Is a method mainly designed to automatically find frame/field timing issues in a video signal chain resulting in a digital video file.

It consists of 3 parts:

  * A specially crafted test-video
  * A corresponding evaluation tool
  * Analysis results as plain text file

Conventional test-videos are only designed for checking image quality, but cannot be used to analyze any time-based behavior that requires monitoring data over a certain time period. This is, for example, necessary to examine frame/field timing handling. Our signal analysis must not be mistaken with analyzing an analogue video signal on a voltage level (e.g. using an oscilloscope), as DVA Fidelity only verifies whole images - not lines, signal voltages or sync-tips, etc.

What we call "frame/field timing issues", are incidents where a whole frame and/or field at a certain time position in an output video does not contain the expected field/frame information from the source video at the right time index. Typical examples would be "dropped frame/field", "duplicated frame/field", etc.

When testing for frame/field timing issues, it is necessary to know that timing corrections are not always caused by faulty devices. In some cases they are normal: Whenever video equipment is connected to each other, each is running with its own timer. In case there is no ability for them to be synchronized by clocking mechanisms, it is clear that sooner or later those timers will drift apart, requiring runtime corrections to be made to the video signal. However, even though these timing corrections are necessary, each equipment handles these corrections differently.

So "DVA Fidelity" is a way of detecting and visualizing any intervention in the original video signal, and therefore provides a way of comparing timing-handling methods of different equipment to each other. 
