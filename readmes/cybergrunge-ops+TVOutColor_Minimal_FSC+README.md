# TVOutColor_Minimal_FSC

stripped down to the core in hopes of later repurposing as a framebuffer 

file size has been cut down to <3kb, more work needs to be done.

<s>only tested on Uno board + Arduino version 1.0.6 so far</s> 
i have tested and it works with newer Arduino IDE for Uno as well.


# Outline of Re-Engineering

the original project file can be found here: https://github.com/cybergrunge-ops/TVoutColor_20131004/

The main project file is dependent on some headers and code that is specific to the different classes that are used. there are several headers which just define various things without running any code such as defINT and defTIMER and defCOLOR etc. the header files can pretty much all be consolidated into one for portability, and to make these values easier to find in one place for tweaking.

## CSYS

The first class is `CSYS`, which has a convenient name because it basically is a class with functions for initializing the system. `defSYS.h` tells us that the `CSYS` class is pretty simple, it just has three public functions that are self-explanatory: `Ini()`, which initializes port, timer and interrupts; `delay132()`, which is used in place of arduino's `delay()` and `delayMicroseconds()` due to the customized timer setup; and then `IniUART()`, which is also self-explanatory - it simply configures the ATMega328 chip so that serial functions normally despite the chip not being clocked at 16Mhz. CSYS is not too difficult to understand and deconstruct. In my work on the project I just put all of the CSYS::Ini() functions directly into the `void setup()` of my project and freed `delay132()` from its class imprisonment which (i think) has not resulted in anything terrible, but then again i havent yet tried animating things. finally, Since I am not using serial i just get rid of `IniUART()`. 

## CCSL

next there is `CCSL` which is not as obviously named, i cant figure out what the name means. but from what i can gather it is mainly used for functions having to do with sprites and text display. annoyingly, it does have some other stuff that probably should be in the `CSYS` or `CINT` classes instead. Its public functions are: aptly named `clear_screen()`, `set_cursor()`, `put_char()`, `set_line_color()` and then (differently-capitalized and without underscore...) `SetVram()`. this last one is used by the character generator, but as shown in the un-implemented code for space invader style sprites, can also let you make your own sprites, which can then be placed on the screen using `put_char()`. im not sure if this is going to really be useful to me since i want to make a framebuffer, but maybe someday i will use it. for the most part i just get rid of `CCSL`.

## CCRT

then there is CCRT which is pretty much abandoned. It doesn't do anything.

## CINT

finally there is `CINT`, which is also conveniently named as it is the class for the Interrupt stuff, and is where all the work for generating video is done. despite interrupts being horrifyingly complicated and stressful when you are just starting out, this code is really simple and elegant and makes me come close to not despising object-oriented programming. `defINT.h` has a bunch of useful defines and then constructor for CINT. the class contains all the functions used to actually generate video (`INT_SP_Txt`, `INT_SP_FSC` etc) including `JobAsy()`, `ExecFunc()`, and `FitDelay()`, all which just help with the flow of timing to keep the signal stable, and which use private variables of `CINT` to adjust themselves automatically and (usually) work great. The `Ini()` function for `CINT` just sets everything to zero or off which needs to be off while setup is being done. `CINT` also though has `Check132ms()`, which is called by `delay132()` which you will remember is a function of `CSYS`. this makes things confusing to have a class' function inside of a different class' function...... but we can find a way to make that more intuitive.

## Teardown

So, my primary goal is to make a version of the program which can do very basic things under 5kb leaving plenty of room for other stuff. first i get rid of the unused "invader" sprites, then also get rid of the character generator. then, consolidate the classes into just `CINT` and `CSYS`. then, get rid of unused display modes among `INT_SP_Txt`, `INT_SP_Txt_ODD`, `INT_SP_Txt_B`, etc etc. for my purposes i just want to have `INT_SP_FSC` to mess around with. In the original project folder the majority of space is taken up by these as well as `ICF1`. this code, to me, is kind of hard to understand both because it uses function pointers, and because i guess i dont really understand the motivation for using the weird function pointer array in the first place. Regardless, that pointer array takes up an enormous amount of memory so we can just get rid of it and then put the desired function (in my case, `objINT.Int_FSC`) into the Interrupt Service Routine below. This cuts the code down to 4kb or so. going back into the main project file and the headers, we can get rid of all the initializers and values that are no longer needed.

For this repo, what we get is a version of TVoutColor which is just over 2kb and simply operates the FSC mode to generate a solid color on the screen. Although not implemented here, if you mess around with the `define`s you can adjust the resolution to generate an actual full screen of solid color, rather than TVoutColor's original box of solid color that doesn't actually fill the screen.


