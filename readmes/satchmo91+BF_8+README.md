The BF_8 is an 8-track MIDI controller. It has 8 faders and 8 corresponding toggle switches as well as a 4-digit 7-segment display and a program button. The BF_8 interfactes via USB Type C connector where it also reveives its 5V power.

Normal Operation:
Faders - Moving any of the faders sends out a MIDI packet containing the CC Message assigned to that fader and the current value which is between 0 and 127. The value sent is represented on the display. The MIDI packet is only send when a value changes.
Switches - Toggling the switch up sends out a MIDI packet with the CC message assigned to that switch with a value of 127. Toggling the switch down does the same, but sends a value of 0 instead. The packet is only sent once per toggle.

Fader CC Program Mode (CCF):
Pressing the program button once enters Fader CC Program mode and the display will read "CCF." While this mode is active, moving any of the faders does not send out a MIDI packet, but instead is used to change that fader's CC Message. Move the fader you want to program to the desired CC value. After a moment of inactivity, that fader will then be programmed to send out that CC value. Repeat this process for the other faders as only one can be programmed at a time. *NOTE* If you pressed the button, but do not want to re-program a fader, continuing to press the button before the value is programmed will cycle around to Normal Operation mode and nothing will be programmed. The program delay is 4 seconds.

Switch CC Program Mode (CCb):
Pressing the program button twice enters Switch CC Program Mode and display will read "CCb." While this mode is active, you can program the switches the same way you programmed the the faders above, the only difference being that you use the fader beneath the switch to change its value.

Channel Program Mode (CH):
Pressing the program button thrice enters Channel Program Mode. In this mode, moving any of the faders can be used to change the unit's channel. Note that the channel is set for the entire unit. It is not possible to send MIDI messages on different channels without reprogramming the unit.



FAQ
- Why does the damn thing keep jittering between two values?
    The ADC on the Pro Micro is having a hard time differentiating between two values and as a result will jitter back and forth. To mitigate this, I've added smoothing capacitors to the faders and am using a running average to smooth the data. Still it's not entirely eliminated so the unit also "locks in" a value after being still for 400ms. If you can gently nudge the fader to hold a position for that short period, the value will remain steady until a fader is moved again. It's annoying and I'm hoping to make the unit more robust in future versions.

- Explain the name.
    That's not a question, but okay. It was originally going to be called the FADER_8, but Notes and Volts on YouTube already had a device called FADR-4, so I had to change the name. Originally the unit was designed with momentary buttons instead of switches thus, Buttons Faders 8 => BF_8. I didn't want to use FB because I didn't want it to be associated or confused with Facebook for some reason. During development I figured that most people would use those buttons to control "mute" or "solo" functions in their DAW and since the button was sending 127 when pressed and 0 when released, the DAW would mute then unmute with each press. There are software solutions to that problem, but I figured that it would actually be more handy if the button would latch in the high or low position, so I changed it to switches.

- Why not "BS_8" then?
    Why do you think?

- Does the BF_8 love me unconditionally?
    No.

Credits:
Designed by Erik D. Herrmann II

Special thanks to Notes and Volts for his videos where he made a very similar product. It was very inspirational and I highly recommend checking out his channel. Also, thanks to my dad, Erik Herrmann Sr. for help and feedback during testing and building the first unit. Love ya, pops.
