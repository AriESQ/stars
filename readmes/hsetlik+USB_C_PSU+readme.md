# USB-C and li-ion power supply

I designed this little power supply board for my ongoing polyphonic synth project. Like most analog synths it needs a +/-12V supply, as well as a 3.3V supply to run a microcontroller and some other digital bits and pieces. It doesn't consume a crazy amount of power, so I thought a built-in battery and the ability to power the synth over USB-C would be nice features. As power supplies go it's a bit complicated, but the circuit is made up of six basic blocks which are each simple enough on their own so I'll go through each one below.

The KiCad files are for both the schematic and the PCB are in this repo along with a PDF of the schematic. There's an interactive BOM file inside the "bom" directory as well.

## Block 1: USB-C connector and PD negotiation

Throughout the revisions of this board I learned the hard way that power over USB-C isn't as simple as routing the VBUS pin to a power input. Devices that recieve power via USB-C PD (power delivery) must "negotiate" with the power source via the connector's two CC pins to request the needed voltage and current. A simple solution here is to connect CC1 and CC2 to ground each through their own 5.1k resistor. This, however limits the device to 500mA at 5V. In order to negotiate our target max power of 3A at 5 volts, we can use a dedicated IC like the [CYPD3177](https://www.infineon.com/dgdl/Infineon-EZ-PD_BCR_Datasheet_USB_Type-C_Port_Controller_for_Power_Sinks-DataSheet-v03_00-EN.pdf?fileId=8ac78c8c7d0d8da4017d0ee7ce9d70ad), which connects to our CC pins and negotiates for voltage and current values which are set by some resistor dividers. [This video](https://www.youtube.com/watch?v=W13HNsoHj7A&t=1458s) by Phil's Lab on YouTube is a great explanation of this IC and how to work with power over USB-C in general. The IC operates a MOSFET load switch (Q102 on the schematic) to connect the input 5V line to our VDD net when negotiation is successful. The USB data lines are also broken out from the connector to a header on the left of the board. They're routed at 90Ohm impedance and delay matched, though full disclosure I haven't tested USB data transmission through this board yet.

## Block 2: Battery charger- MCP73834T

The battery is connected to a two pin header at the board's left and charging is handled by the [MCP73834T](https://www.mouser.com/datasheet/2/268/MCHPS02791_1-2520625.pdf?srsltid=AfmBOorI071ICvB1H1zKlI4OQ19W84Uk-KKZgpKTywMe8cmfgQa4ltDp) charge management controller IC. The IC is powered by VDD and has two status LEDs (D101 and D102) to indicate the device's power and charging state. R106 sets the charging current, I've chosen 3.3k for a charging current of about 300mA.

## Block 3: Load switch/power switch

We want to be able to power the output SMPS converters from USB when we can and from the battery otherwise. Switching between them is handled by a p-channel MOSFET (Q101) and two schottky diodes (D104 & D105). The mechanical power switch (SW101) connects the output of those schottky diodes to the VCC net, which is the input for both the 3.3V and +12V converters. This switching configuration allows us to switch the load on and off without disrupting battery charging.

## Block 4: 3.3V rail- TPS63070

The input voltage on VCC can range anywhere from 5V with USB plugged in to 2V when running on battery. To keep the output voltage at 3.3V in an efficient way, I opted for the [TPS63070](https://www.ti.com/lit/ds/slvsc58b/slvsc58b.pdf?ts=1724595749000&ref_url=https%253A%252F%252Fwww.google.com%252F) Buck-Boost converter IC. This should give us similar efficiency and current limits in both buck and boost mode. The circuit I used is similar to the datasheet with the addition of the trimmer RV102 and the output status LED D108, as well as some extra output capacitance. I haven't pushed it yet, but this should be able to provide up to 2A of continuous current to the 3.3V line.

## Block 5: +12V rail- CS5173

The +12V rail is provided by a [CS5173](https://docs.rs-online.com/b3ee/0900766b8157398f.pdf) boost converter IC, which gets powered from VCC like the 3.3V converter. The circuit is again pretty similar to the datasheet with the addition of a trimmer RV101 to adjust the output voltage. With this configuration, the +12V line should be able to handle 1.5A.

## Block 6: -12V rail- NCV33163

Having tried several methods of creating a stable -12V rail from a single supply, I settled on the [NCV33163](https://www.onsemi.com/pdf/datasheet/ncv33163-d.pdf) switching regulator set up in inverting mode. The basic voltage-inverting configuration is shown and described on p12 of the datasheet. The IC itself is fairly large and the 180uH inductor it needs takes up significant space on the board, though the nominal 1A current limit (assuming a high enough current limit on the +12V input) will be plenty to power the synth's -12V line. Like the other rails, the output is adjustable via the trimmer RV103.
