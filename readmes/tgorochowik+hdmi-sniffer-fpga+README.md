# HDMI-Sniffer Quickstart

## Vivado project:

```vivado -mode batch -source fpga_project.tcl```

## Compile linux utils
Utils call various ioctls to the video-sniffer driver.
The most important might be `mode_tmds`, as by default, the sniffer streams data decoded to RGB.
The default mode can be changed in the linux driver.

When the system is up, to check if everything worked, get_res util can be used.
For RGB mode it should print the actual image resolution, for TMDS mode it should output 1970x3300.

The data can be acquired using dd utility, e.g.:

```dd if=/dev/video0 of=dump count=1 bs=`echo 1970*3300*10 | bc` ```

The dump can be analyzed and decoded using `tmds2rgb` util.
This util does not support InfoFrames at the moment.

## See also

* https://github.com/tgorochowik/linux-vsniffer/tree/video-sniffer-zybo

* https://github.com/tgorochowik/tmds2rgb
