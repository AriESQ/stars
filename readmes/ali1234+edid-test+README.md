Useful commands:

Install an edid:

sudo cp edid-xxxx.bin /lib/firmware/test.bin

Check current loaded edid:

edid-decode /sys/devices/platform/gpu/drm/card1/card1-HDMI-A-1/edid
