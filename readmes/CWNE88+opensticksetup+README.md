# opensticksetup
Instructions to set up Debian OpenStick

# Install required programs
sudo apt install git python3-venv adb fastboot


# Get edl
git clone --recurse-submodules https://github.com/bkerler/edl.git
cd edl
python3 -m venv venv
venv/bin/pip install .


# Let edl use the stick without sudo, and keep this system's ModemManager from grabbing it:

echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="05c6", \
ATTRS{idProduct}=="9008", TAG+="uaccess", ENV{ID_MM_DEVICE_IGNORE}="1"' | \
sudo tee /etc/udev/rules.d/99-qcom-edl.rules

sudo udevadm control --reload


# Grab an IP address from it
sudo dhclient enx025051533438

# Open web page to turn on adb
https://192.168.100.1/usbdebug.html

# Check if you can see it as an adb device
adb devices

# Reboot it into edl
adb reboot edl

# Check it came up in edl
lsusb | grep 05c6:9008

# Get backup of existing image. Run these from edl folder and give this particular usb stick a name (their radios all have different calibration) 

E=venv/bin/edl
B=~/stick-backups/stick2
mkdir -p $B
$E printgpt > $B/gpt.txt
$E rf $B/full-emmc.bin
$E rl $B/partitions --genxml
$E reset

# Make a checksum of it
cd $B
sha256sum full-emmc.bin partitions/* > SHA256SUMS

# Check board type
strings ~/stick-backups/stick2/partitions/system.bin | grep ro.product.model
# or
adb shell getprop ro.product.model

####NOT THIS
# Put back in EDL mode
#adb reboot edl

# get openstick debian image
# https://github.com/kinsamanka/OpenStick-Builder/releases

cd
mkdir openstick
cd openstick
wget https://github.com/kinsamanka/OpenStick-Builder/releases/download/v0.2/openstick-debian.zip
unzip openstick-debian.zip

# Put it into fastboot mode
adb reboot bootloader

# Check it's ready to go
fastboot devices


# Install the openstick images onto the stick. Run this from the dir you unzipped

# First the bootloader files
fastboot flash partition gpt_both0.bin
fastboot flash aboot aboot.mbn
fastboot flash hyp hyp.mbn
fastboot flash rpm rpm.mbn
fastboot flash sbl1 sbl1.mbn
fastboot flash tz tz.mbn
fastboot flash cdt sbc_1.0_8016.bin

# Next the Linux files (Will take a LONG time!)
fastboot flash boot boot.bin
fastboot flash rootfs rootfs.bin

# Next put the original IMEI and calibration data back on
B=~/stick-backups/stick2/partitions
fastboot flash sec $B/sec.bin
fastboot flash fsc $B/fsc.bin
fastboot flash fsg $B/fsg.bin
fastboot flash modemst1 $B/modemst1.bin
fastboot flash modemst2 $B/modemst2.bin
fastboot flash modem $B/modem.bin
fastboot flash persist $B/persist.bin

# Reboot into OpenStick
fastboot reboot

ssh user@192.168.5.1
password=1

# Expand file system
df -h
lsblk
sudo resize2fs /dev/mmcblk0p15
df -h


# Modem part

# Show modem status
mmcli -m 0


# Show the connections NetworkManager looks after
nmcli connection show

NAME     UUID                                  TYPE      DEVICE    
usb      6d73d069-b482-41ec-bbc2-f769089700cb  ethernet  usb0      
hotspot  4e35e5da-f566-46e1-9d90-8bdc0adde58f  wifi      wlan0     
lte      1a84c1e6-6688-4be5-b05a-4ceee414f8ed  gsm       wwan0qmi0 
lo       d93764d8-b4a9-4351-b525-ba163d8232c4  loopback  lo


# Modify the "lte" connection to point to telstra.internet and IPv4/IPv6 and reset it
sudo nmcli connection modify lte gsm.apn telstra.internet ipv4.method auto ipv6.method auto
sudo nmcli connection down lte; sudo nmcli connection up lte

# Check it with this
nmcli -g gsm.apn,ipv4.method,ipv6.method connection show lte


# Force it to only try 4g, since 3g has been switched off
sudo mmcli -m 0 --set-allowed-modes='4g'

# Check it with this
mmcli -m 0 | grep -A5 Modes



# Make it keep trying if it struggles rather than give up
sudo nmcli connection modify lte connection.autoconnect-retries 0


# Check it with this
nmcli -g connection.autoconnect-retries connection show lte




