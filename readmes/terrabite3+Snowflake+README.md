# Snowflake

## Getting started

Connect the snowflake to your computer and turn it on. You should see a USB drive called CIRCUITPY appear. Inside are several `.py` files with the source code. You can open these files with any text editor. Whenever you save the file, the program will start running again from the beginning.

* `code.py` is the top-level file. It sets up the display, buttons, and accelerometer. It contains the main loop which reads input from the buttons and updates the display.
* `mode.py` is where the modes are created. Each mode is contained in a class, which holds the code for updating the display. At the bottom is `ModeSwitcher`, which has the list of all the modes.
* `display.py` is responsible for controlling the LED display. It provides several ways to access all the LEDs, by arm, by ring, and by index. The code that actually controls the LEDs is in the `xmas3` module, which is written in C and runs on the 2nd core of the microcontroller. This allows the LEDs to be flicker-free and dimmable.
* `button.py` is responsible for checking when the buttons are pressed.
* `accelerometer.py` sets up the accelerometer, but most of the interesting details are in the `adafruit_lis3dh` module.

## Adding a new mode

This section is a step-by-step tutorial for adding your first custom mode.

1. Connect the snowflake to your computer and turn it on.
2. Open `mode.py` in a text editor. Anything will do, but a code editor like Visual Studio Code will be helpful.
3. At the top, under the `import` statements, we will add our new mode. Write the following. (The lines that start with `#` are comments, you may copy them if you )

```python
# This mode will blink on for 1 second, off for 1 second
class BlinkMode:
    def __init__(self, display):
        self.__display = display
        # The delay between calls to draw() should be 1/100th second
        self.delay = 0.01
        # This counter will keep track of how many 1/100th seconds have passed.
        self.counter = 0

    def start(self):
        # This function is called when we start the mode. In this case we don't need to do anything here.
        pass

    def draw(self):
        # Add 1 to the counter. If it has reached 200, reset it to 0.
        self.counter += 1
        if self.counter >= 200:
            self.counter = 0
        # If the counter is less than 100, turn all the LEDs on to their maximum of 255. 
        # Otherwise turn them all off.
        if self.counter < 100:
            self.__display.set_all(255)
        else:
            self.__display.set_all(0)
```

4. Down in `ModeSwitcher`, you'll see a list of modes. Add the new mode to the list in a new category.

```python
[
    BlinkMode(display)
]
```

5. Save `mode.py`. You should see the program restart. Now press the left button until the correct mode group is selected. You should see it blink!


## What if it doesn't work? (Debugging)

TODO: Use putty


## What if I break it?

If it stops working and you don't know why, the first step is to try reloading the original Python files. Back up your changes by copying the Python files from the USB drive to your computer. Then copy the original Python files from this repository to the USB drive.

If it's still broken, you may need to reload the firmware. Turn the snowflake off, then hold the right button while turning it on. A USB drive will appear called RPI-RP2. Copy `firmware.uf2` to it. The USB drive will disappear, and the normal CIRCUITPY drive will appear.


## How can I share my modes?

TODO: PR

