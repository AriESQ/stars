# MAGFest Alt Control Jam Launcher

Being developped in openFrameworks 0.9.8 using Visual Studio 2015

Instructions for building the controller are on the jam page.

2026 jam info & games: https://itch.io/jam/flip-out
2026 Controller code: https://code.emma.coop/andy/hardware_jam_2026_arduino

Launcher software by Andy Wallace
additional code by josephalopod (josephalopod.itch.io)

Logo by Matt Lepage

WE DO NOT OWN THESE GAMES. YOU MUST GET PERMISSION FROM THE JAMMERS TO SHOW THEIR WORK!

You can use this repo as a reference to make your own game launcher.

The whole thing is Windows only. Sorry.

This whole launcher is a direct descendent of the Dream Boxxx launcher I wrote years ago. Info about that here: https://arcadecommons.org/games/dreamboxxx/
That's why tons of stuff in this project is called "dreamlauncher"


# Install 

Open up files_to_install and instal them. You might not need them but then again you might! What's the harm?

This setup requires [AutoHotkey 1](https://www.autohotkey.com/) (not AutoHotkey 2, which is the first download on their site). I have included an installer for AutoHotkey 1.1.37 which I have confirmed works.

I also included an installer for [Notepad++](https://notepad-plus-plus.org/). You need some type of simple text editor and god help you if you're using Notepad.

# Teensy code

The arduino code for the teensy in the console lives in hardware_jam_2026_console

# Games

The games you want to launch should live in data/games/

Drop the exe + any data it needs in there.

You can also check out games_folder_example.jpg to see what it looked like for MAG 25.

Open each game once before you start the launcher. Otherwise windows security nonsense will pop up.

It is fine to to remove / add / change files here. Just make sure to update games.xml and to run the game once manually.

Screenshots and title images live in data/images


# Setting up the launcher

Take a look at games.xml and settings.xml in the data folder. This is where you can set everything.

Games.xml has all of the info for the games. Just delete entries you are not using. If you're adding things, make sure you get the path to the exe and images right.

Settings.xml has tons of options for customization. Feel free to mess with it. It has the MAGFest 2025 settings right now.

The launcher is dream_launcher.exe. This is because the software was originally written for the DreamBoxXx


# AutoHotkey

The reset works via AutoHotkey. AutoHotkey is an automation tool for windows.

Open the auto_launch.ahk script in a text editor (double clicking it will just run the script) and set the path to the launcher. This will be specific to where you put it on your computer.

By default it uses `K` as the reset key. You can change this if you want, but make sure that key is not used anywhere else.

`Win-Z` will kill the script.

Please note that if the script is running, pressing the reset key will close every window you have open and launch the launcher. So be aware if it is running and save your work haha.

The best thing to do is to have the AutoHotkey script launch on startup.

If you want some help setting up a windows computer to launch a game automatically and not get bogged down in updates and other aggravating things that windows tends to do, I have a guide: https://www.tumblr.com/andymakesgames/775682484969029632/setting-up-a-windows-11-computer-as-a-permanent?source=share


# Desktop

The desktop is visible for a moment when the launcher closes and the game launches.

I recommend hiding all desktop icons and setting the desktop background to be a loading screen or the provided logo image.


# Some common key values

for the settings file

UP : 357
DOWN : 359
LEFT : 356
RIGHT : 358
BACKSPACE : 8
RETURN : 13
SPACE : 32


# Jam Credits

Here are the folks who brought you Lever Up:
* Matt Lepage
* Socks Magocs
* Scott M
* Andy Wallace
* Ryan Wagahoff