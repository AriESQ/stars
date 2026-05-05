# glinet-kismet-remote-cap

## Description

This project using a Gli-Net Puli as a mobile remote wifi capture device is to monitor and analyze the wireless traffic in different locations. The project was created to solve the problem in using purpose built everyday use hardware instead of developer boards built for lab use. The Puli is a portable 4G smart router that supports OpenWrt and has a large storage compatibility. It also has a rechargeable battery and an interchangeable module that can use CAT4 or CAT6 modules for different bands and throughput. The Puli can use the LTE or ethernet connection to backhaul the data to a kismet server installed on a cloud instance, through a VPN tunnel, which provides security and privacy for the captured data.

Some of the limitations of the device are that it has a relatively low Wi-Fi speed of 300 Mbps, which may not be enough for capturing high-bandwidth traffic. It also has a limited battery life of about 8 hours, which may require frequent recharging or external power sources. Additionally, the device may not support some of the latest Wi-Fi features such as IPv6 and WPA3, which may affect its compatibility and performance with some networks.

## Table of Contents

If your README is long, add a table of contents to make it easy for users to find what they need.

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Reguirements

### Hardware
- Gli-Net Puli (GL-XE300) with a EC25-G
- GPS Patch antenna with a UFA connector

### Software
- Kismet server
- kismet_cap_linux_wifi compiled for the openwrt version of the device
- GPSD
- Python3
- PIP
- https://github.com/hobobandy/python-kismet-metagpsd

## Installation

1. Rewire or add GPS patch antenna with a UFA connector.
2. Run AT command to enable GPS module on the Modem.
3. 
4. Compile the kismet_cap_linux_wifi OpenWRT package. Use OpenWRT compiler on a Linux device, use generic devices.
5. Install GPSD, Python3, PIP OpenWRT packages
6. Download https://github.com/hobobandy/python-kismet-metagpsd on your local machine and SCP the repo onto the router then install on device using pip
7. Install Kismet server on a remote machine, then obtain apikey for tcp connection from Puli to Kismet server.
8. Run these 3 commands starting with;
   - Start gpsd `gpsd /dev/ttyUSB2` and verify signal with `cgps`
   - Start kismet `kismet_cap_linux_wifi --tcp --connect 10.101.0.2:3501 --source=wlan0:name=remote0,metagps=remote0`
   - Start metagps `python3 metagpsd.py --connect 10.101.0.2:2501 --metagps remote0 --apikey=<admin role key>`
   
## Usage

Provide instructions and examples for use. Include screenshots as needed.

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

    ```md
    ![alt text](assets/images/screenshot.png)
    ```

## Credits

List your collaborators, if any, with links to their GitHub profiles.

If you used any third-party assets that require attribution, list the creators with links to their primary web presence in this section.

If you followed tutorials, include links to those here as well.

## License

The last section of a high-quality README file is the license. This lets other developers know what they can and cannot do with your project. If you need help choosing a license, refer to [https://choosealicense.com/](https://choosealicense.com/).

---

🏆 The previous sections are the bare minimum, and your project will ultimately determine the content of this document. You might also want to consider adding the following sections.

## Badges

![badmath](https://img.shields.io/github/languages/top/lernantino/badmath)

Badges aren't necessary, per se, but they demonstrate street cred. Badges let other developers know that you know what you're doing. Check out the badges hosted by [shields.io](https://shields.io/). You may not understand what they all represent now, but you will in time.

## Features

If your project has a lot of features, list them here.

## How to Contribute

If you created an application or package and would like other developers to contribute it, you can include guidelines for how to do so. The [Contributor Covenant](https://www.contributor-covenant.org/) is an industry standard, but you can always write your own if you'd prefer.

## Tests

Go the extra mile and write tests for your application. Then provide examples on how to run them here.


1. rewire gps antenna

2. enable gps using at commands

3. at command rod knows about

3. start gpsd `gpsd /dev/ttyUSB2` and verify signal with `cgps`

4. start kismet `kismet_cap_linux_wifi --tcp --connect 10.101.0.2:3501 --source=wlan0:name=remote0,metagps=remote0`

5. start metagps `python3 metagpsd.py --connect 10.101.0.2:2501 --metagps remote0 --apikey=<admin role key>`
