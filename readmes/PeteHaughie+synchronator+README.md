# Synchronator

From the official website:

> The SYNCHRONATOR AV device transforms your audio into a composite video signal, compatible with all video equipment supporting composite video input.

> With 3 audio inputs and 1 video out, the SYNCHRONATOR device enables you to visualize your sounds on each of the primary color channels of the video signal.

> It adds video sync pulses and color coding signals to your audio, effectively disguising the input as a composite video signal.

> The device is powered with a 6V adapter and features a color/b&w switch as its only on-board controller. Other manipulations are done solely with the audio input.

The Synchronator was created by B Van Koolwijk and G J Prins in 2009 and has not had a release since 2013.

This version was built purely by the strength of description and uses FFT to split an audio signal into its low, middle, and high frequencies rather than discrete inputs for the RGB inputs and, if built for the Pi Zero 2, outputs on HDMI.