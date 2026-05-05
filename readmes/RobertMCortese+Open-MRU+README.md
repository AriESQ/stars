# Open-MRU
An open source Memory Recording Unit to record a firewire stream based on the Raspberry Pi 5.

**Synopsis**
Firewire cameras are still popular whenever videographers are looking for a retro asthetic.  Unfortunately due to their age their mechanical components (Tape drives) are starting to fail.  At one time Sony made a MRU unit, but hasn't produced it since 2008.

This project creates something of similar, but with the expanded functionality of a Raspberry Pi.  The script monitors the firewire bus to see when the camcorder is in a "Record" state, then launches DVGrab.

sudo apt install dvgrab libraw1394-dev libavc1394-dev python3-dev python3-rpi.gpio
sudo python3 camcorder_monitor.py &

More to come.
