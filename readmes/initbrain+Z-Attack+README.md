Z-Attack
========
Z-Wave Packet Interception and Injection Tool
[GNU GPL v3 license](http://www.gnu.org/licenses/gpl-3.0.txt)

*   **Hardware**

    This program use the custom [RFCat firmware](https://bitbucket.org/atlas0fd00m/rfcat) written by [At1as](https://twitter.com/at1as) and is compatible with:

    * The [Texas Instrument development KIT](http://www.ti.com/tool/cc1110-cc1111dk) (with UART bridge)
    * The [RfCat](http://int3.cc/products/rfcat) USB Radio Dongle
    * The [YARD Stick One](https://greatscottgadgets.com/yardstickone/) USB Radio Dongle

    For any help use "-h".


*   **Installation**

    If you want to use this tool which is based on RFCat you need to install rflib  
    <https://bitbucket.org/atlas0fd00m/rfcat/downloads>
    
    Using Z-Attack requires that you either use the python script in root mode (sudo works well),  
    or configure udev to allow non-root users full access to your dongle.  
    Additional details are on the RFCat project page:  
    <https://bitbucket.org/atlas0fd00m/rfcat>

    Debian install dependencies:

        pip install pydot
        apt-get install python-tk python-imaging-tk python-usb graphviz

    On Ubuntu, if you are experiencing this error:

        Couldn't import dot_parser, loading of dot files will not be possible

    Just install the *python-pydot* package from the Ubuntu Software repository

        sudo apt-get install python-pydot python-tk python-imaging-tk python-usb graphviz


*   **Changelog**

    Version 0.1:

        First release

    Version 0.1.1:

        Code cleaned, PEP8 (partially)
        Information added to the readme file
        Information added to the graph generator
        CSV logging disabled by default
        GUI improvement:
            Logo cropped, compressed and moved to the About window
            The HomeID listbox now fit the window and have a scrollbar
            Order of the text (reception) reversed and auto scrolling if the user don't use the scrollbar
            Send frame (advanced mode) window reorganization, brodcast src/dst and scrollbars added
