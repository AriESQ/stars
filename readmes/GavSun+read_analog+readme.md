# Reading the Analog channels available on RP2350A.

The major objectives of this project are :
1. To understand how to read multiple analog channels using round-robbin sampling.
2. To understand how to access ADC FIFO for collecting sampled values.
3. To understand how to use ADC_FIFO_IRQ for timely reading the samples in the FIFO. 

## Description: 

This project uses the RP2350 (RPi PICO 2) & it's ADC peripheral to read all the available analog channels.
RP2350A support 5 analog channels. Out of these 5 analog channels:
- 3 channels (Ch0, Ch1, Ch2) are available on the PICO 2 pinouts, 
- 1 Analog channel is connected to Vsys power supply line internally on the PICO 2 board,
- and the last fifth channel is connected to on-chip temperature sensor.
All these 5 channels are read using round robbin sampling. For each channel multiple 
samples are collected, then averaged before communicating the final values over the UART.

### Relevant code & header files are:
1. main.c 

### Hardware : 
RPi PICO2 board.

**Note** : The analog signals are simulated by connecting a 10K potentiometer (or a multi turn 
presset) between 3.3V and AGND. The mid point of potentiometer is connected to 
GPIO26, 27, 28 pins on the PICO 2 board.
The onboard VSYS is already connected to GPIO29 (i.e.ADC CH3).
Onchip temperature sensor is connected to ADC CH4

### Tools
VSCode with Rapberry Pi Pico Project extension
