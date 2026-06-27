# P4 KVM

This project uses an ESP32 P4 (Rev < 3) and a Toshiba TC358743 HDMI to CSI adapter as an Remote IP KVM

## WARNING

This is NOT production software! THis is a POC, use this at your own risk! There are many bugs, there is NOT security, none. There is no wifi in this firmware, there is only ethernet.

## Parts Needed (affiliate links)

- Any [esp32-p4 module with rpi camera compatible CSI interface + ethernet](https://amzn.to/4v9c3Nf)
- [Toshiba TC358743 HDMI to CSI adapter](https://amzn.to/44mJyAp)

## 3d Printed Enclosure

This ony works with the specific parts above:

[Makerworld](https://makerworld.com/en/models/2961981-esp32-p4-ip-kvm-enclosure)

## Building/Flashing Firmware

1. Use esp-idf, 6.0.1
2. run menuconfig (select chip revision < 3, choose options in p4kvm>)
3. idf.py build flash monitor (monitor is optional)
4. Open p4kvm.local in your browser

## Building Web App

1. cd web
2. npm install
3. npm run build
4. follow build/flash steps above

## FAQ

### How do I access this remotely?

You will need some sort of vpn, like tailscale, wireguard, etc., do not expose this to the public internet.

### How do I change the resolution/framerate?

This is not supported yet, but you can change the EDID in tc358743_edid_bin defined in tc358743_edid_1080p30.h if you want to experiment.

### Can I change the escape key from leaving captured input?

Afaik, it's not possible to change the escape key in a browser.

### Why are you missing X feature?

This is a POC, not a production project. Please fork it and customize it!

## Troubleshooting & known issues

- if the source goes to sleep, the p4kvm doesn't always recover, WIP
- some systems don't like the EDID, try changing the EDID
- try plugging in your target system before booting the p4 kvm
- try a different HDMI cable or USB cable
- look at the diagnsotics for the tc358743: SYS_STATUS, i.e. (TMDS=1 HDMI=1 SYNC=1 DDC5V=1), they should all be 1

## Video

Chip revisions on the ESP32 P4 are very critical, this project assumes you have a Rev 1.3 chip. Rev 3+ chips will be able to use H264 encoding, hopefully, but it's not included in this firmware.
**CSI path is fixed** to **RGB888** for now, YUV doesn't work well with the jpeg encoder

## Menuconfig (`P4KVM`)

- **`P4KVM_TC358743_RST_GPIO`**: reset line (active low); use `-1` if unwired (default GPIO 23).
- **`P4KVM_JPEG_QUALITY`**: 1-100. (This is also available through the UI)
- **Ethernet**: `P4KVM_ETH_ENABLE` and RMII/MDIO/PHY GPIO options when `SOC_EMAC_SUPPORTED` applies.
