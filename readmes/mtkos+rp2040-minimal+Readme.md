## rp2040-minimal

My stm32f103-minimal repository shows how to program the STM32F103 microcontroller using little more than the GNU C compiler and binutils. The present repository does the same for the 
rp2040 microcontroller by Raspberry Pi. The reason for wanting to do this is that the usual way of programming rp2040, using the SDK, hides the inner workings of the chip. This is usually
desirable, but not if you want to understand the chip at the bare-metal level. The only program taken from the sdk is pioasm, which is so specific for this MCU that I did not find it worthwhile
to write my own.

The following documentation has been used, in addtion to the resources used in the stm32f103-minimal repository:

[RP2040] RP2040 Datasheet. Can be obtained from <https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf/>.

Because both boards use a ARM Cortex-M CPU (M3 and M0+ respectively), there are a lot of similarities. But the following differences should be noted:

1. The rp2040 has no on-board flash. Instead external flash chips are used. Some configuration is needed before the processor can fetch data and instructions from the chip. Details can be found
in section 2.6.3 of the datasheet. This configuration is done by the 'secondary bootlader', which is loaded into the first 256 bytes of flash. A very simple secondary bootloader (not using quad SPI)
can be found in the 'boot2' map.

2. The peripherals work a little bit differently. How to use them is explained in the Readme's of the various programs.

3. The rp2040 has an interesting peripheral, called the PIO, which is specific to this MCU. It is documented in chapter 3 of the data sheet. An example program can be found in the
'ws2812d' map.

4. The rp2040 is a dual core processor. The blink-multicore program shows how to use the second core.

In the include files, which define the registers and bit fields, the same names have been used as in the rp2040 SDK, which, in turn, have a simple relationship to the names used in [rp2040].
Hence, the programs should be easy to understand if you have this datasheet at hand.

The board I used is YD-2040. Compared to the Raspberry Pi Pico it has a few extra's. A reset button, which is handy if you upload UF2 files for programming, a user button (connected to
GPIO24) and a ws2812 three-color LED, connected to GPIO23. If you want to use the latter, you will have to close the R68 soldering bridge.
