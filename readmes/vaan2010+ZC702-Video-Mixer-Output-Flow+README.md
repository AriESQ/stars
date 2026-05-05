# ZC702 Video Mixer Output Flow
+ This article mainly explains how to use the official demo to output Video Mixer via ADV7511 HDMI on ZC702

**Last update: 2024/05/18**

+ Vivado Version: 2021.1

+ Vivado 2020.1, 2020.2, and 2021.1 have known bugs related to image processing IPs such as VPSS, Video Mixer, and Video Multi-Scaler, which may cause issues during synthesis. You can refer to the following link for troubleshooting:

[Vivado HLS - 2021.1 - Why does synthesis stall when using Windows OS?](https://support.xilinx.com/s/article/Patch-AR-for-HLS-IP-patch?language=en_US)

### 0. After downloading the zip file from the above link, extract it to the C drive. Then, add an environment variable and restart Vivado to resolve the issue

<img src="Images/M1.png"/>

## Build ZC702 Block Design on Vivado

### 1. Refer to the ZC702 HDMI Block Design, and add Video Mixer and two GPIOs

+ ZYNQ7 Processing System

<img src="Images/M2.png"/>

<img src="Images/M3.png"/>

<img src="Images/M4.png"/>

+ Video Test Pattern Generator

<img src="Images/M5.png"/>

+ AXI4-Stream to Video Out

<img src="Images/M6.png"/>

+ Video Timing Controller

<img src="Images/M7.png"/>

<img src="Images/M8.png"/>

+ Clocking Wizard

<img src="Images/M9.png"/>

<img src="Images/M10.png"/>

+ AXI IIC

<img src="Images/M11.png"/>

+ AXI4-Stream Subset Converter

<img src="Images/M12.png"/>

+ GPIO-0

<img src="Images/M13.png"/>

+ GPIO-1

<img src="Images/M14.png"/>

+ Video Mixer

<img src="Images/M15.png"/>

+ AXI Interconnect

<img src="Images/M16.png"/>

+ Connect the above IPs – do not connect 'sof_state_out'

<img src="Images/M17.png"/>

<img src="Images/M18.png"/>

Run Connection Automation – Select 148 MHz for all Clock Sources

<img src="Images/M19.png"/>

<img src="Images/M20.png"/>

<img src="Images/M21.png"/>

<img src="Images/M22.png"/>

<img src="Images/M23.png"/>

### 2. Add the XDC content, which can be downloaded from this [link](https://support.xilinx.com/s/feed/0D52E00007IPcI2SAL?language=en_US)

Alternatively, you can find the file in 'XVES_0019\src\constr\ZC702.xdc'

Remember, the HDMI output port must match the port names specified in the XDC file

<img src="Images/M24.png"/>

Modify the XDC content

<img src="Images/M25.png"/>

<img src="Images/M26.png"/>

<img src="Images/M27.png"/>

### 3. Create HDL Wrapper & Generate Bitstream

<img src="Images/M28.png"/>

### 4. This step will export the XSA to Vitis for writing C code to control the FPGA

<img src="Images/M29.png"/>

## Build ZC702 Application on Vitis

### 5. Open Vitis and import the XSA to create the Platform

<img src="Images/M30.png"/>

+ After creating the Platform, proceed with the Build to generate the linking files

<img src="Images/M31.png"/>

### 6. Select BSP and create an Application using the official Video Mixer Example Code provided

<img src="Images/M32.png"/>

<img src="Images/M33.png"/>

### 7. Import the previously written code for ZC702 HDMI to write to the ADI HDMI Chip

<img src="Images/M34.png"/>

### 8. Open 'xv_mix_example.c' and add the following code snippets

<img src="Images/M35.png"/>

<img src="Images/M36.png"/>

+ main function

<img src="Images/M37.png"/>

<img src="Images/M38.png"/>

+ The build has an error because the GPIO names do not match Vivado. They need to be changed

<img src="Images/M39.png"/>

<img src="Images/M40.png"/>

<img src="Images/M41.png"/>

### 9. Right-click on the application and select "Run as" -> "1 Launch Hardware" to view the results

<img src="Images/M42.png"/>

+ ZC702 Hardware Configuration

<img src="Images/M43.png"/>

+ Result

<img src="Images/M44.png"/>

<img src="Images/M45.png"/>

<img src="Images/result.gif"/>

