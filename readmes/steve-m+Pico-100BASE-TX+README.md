# Pico-100BASE-TX - Bit-banged 100 MBit/s Ethernet

This library allows to stream out data with around 11 MByte/s from a RP2040 or RP2350 MCU using the PIO to bit-bang a 100 MBit/s Fast Ethernet connection.
It is somewhat similar to [Pico-10BASE-T](https://github.com/kingyoPiyo/Pico-10BASE-T), which implemented TX-only 10 MBit/s Ethernet.

**Warning: Do not connect to any POE capable equipment!**

Ideally use a pulse transformer with proper matching circuitry, or at least the 47 + 470 Ohms resistors as seen [here](https://github.com/kingyoPiyo/Pico-10BASE-T?tab=readme-ov-file#setup). In my experiments I directly connected the two GPIOs to an old ethernet cable and it worked with most devices I've tested - only do that at your **own risk**. You also could use some old Ethernet switch and connect it in between the Pico and your machine to be safe.
ASUS mainboards with LANGuard only work when using the resistors or a pulse transformer.

Demo digitizing some WBFM IF signal with the internal ADC and streaming it out via Fast Ethernet:

https://github.com/user-attachments/assets/e150bc89-122c-4669-ae62-b9b03f8b2769

## How does it work?

10BASE-T is rather trivial to implement using an SPI peripheral, as it only uses two voltage levels and Manchester encoding. 100BASE-TX transmission however is harder to implement, it uses [MLT-3](https://en.wikipedia.org/wiki/MLT-3_encoding) encoding, is scrambled, uses a [4B5B](https://en.wikipedia.org/wiki/4B5B) line code, and is transmitted at 125 MHz symbol rate.

### MLT-3

There are three levels this code sequentially cycles through, -1, 0 and +1. If there is a zero to be transmitted, the state remains identical to the last symbol. For a one, it moves to the next state. For a row of ones, the output would be -1, 0, +1, 0, -1, 0 and so on.

Using the side-set feature of the PIO, MLT-3 encoding is implemented on two GPIOs that output either 0b01, 0b00 or 0b10 for each MLT-3 symbol, respectively. As the twisted pair is connected between those two GPIOs, the three voltage levels are obtained.

### Scrambling

The scrambler is implemented using an [LFSR](https://en.wikipedia.org/wiki/Linear-feedback_shift_register) that is 11 bits wide and has taps at the 11th and 9th bit (x^11 + x^9 + 1). This results in a pseudorandom sequence that repeats after 2047 bits. We pre-compute a lookup-table that contains 30 bits of the sequence per entry, and uses 2047 entries (plus the maximum size of a frame for convenience). This takes around 10 KB of RAM in the MCU.

### 4B5B encoding

Each 4-bit nibble is encoded using the [4B5B](https://en.wikipedia.org/wiki/4B5B) line code resulting in 5 bits. Special 5-bit symbols J, K as well as T and R are reserved to signal the start and end of an Ethernet frame, furthermore there is an idle symbol consisting of all ones.
For efficiency purposes, we use a LUT with 256 entries, containing two 4B5B symbols per entry. This allows to encode each byte of the Ethernet frame with only one access into the table.

### Checksum calculation

The Ethernet FCS (Frame Check Sequence) is calculated by using the DMA CRC sniffer in CRC32 mode, the (optional) UDP checksum also uses the DMA sniffer in sum mode.

### Additional notes

With pre-inversion of the scrambling code (already containg the idle symbol), we can directly send the stream of idle symbols to the PIO by DMA. So we only have to use CPU cycles if we really want to transmit a frame.

[This page](https://2007.blog.dest-unreach.be/2009/06/11/ethernet-100base-tx/) also contains some useful information in addition to [IEEE 802.3](https://2007.blog.dest-unreach.be/wp-content/uploads/2017/12/802.3-2005-sec2.pdf).

## Building

Make sure you have the latest version of the [pico-sdk](https://github.com/raspberrypi/pico-sdk) installed together with an appropriate compiler. You should be able to build the [pico-examples](https://github.com/raspberrypi/pico-examples).

To build Pico-100BASE-TX for a Pico2:

    git clone https://github.com/steve-m/Pico-100BASE-TX.git
    mkdir Pico-100BASE-TX/build
    cd Pico-100BASE-TX/build
    export PICO_SDK_PATH=/<path-to>/pico-sdk
    cmake -DPICO_PLATFORM=rp2350 -DPICO_BOARD=pico2 ../
    make -j 8

After the build succeeds you can copy the resulting *.uf2 file of the application you want to run to the board.

## Example applications

The repository contains a library - libpico100basetx - which implements the main functionality. It reads the data from a ringbuffer, and streams it out via the 100BASE-TX UDP frames.
In addition to that, the apps folder contains a couple of example applications:

### counter

This application uses the PIO to generate a 16-bit counter value which is written to a DMA ringbuffer, which is then streamed out via UDP datagrams.

### internal_adc

The data from the internal ADC is streamed out.

### pcm1802_audio

This app streams the audio data from a PCM1802 audio ADC board. The used pinout is the same as on this [adapter PCB](https://github.com/Sev5000/Pico2_12bitADC_PCMAudio), and the audio samplerate is 75 kHz.


## Credits

Pico-100BASE-TX is developed by Steve Markgraf, and is loosely based on [hsdaoh-rp2350](https://github.com/steve-m/hsdaoh-rp2350).


