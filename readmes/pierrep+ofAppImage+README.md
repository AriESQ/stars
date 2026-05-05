# ofAppImage

This project assists in the creation of AppImages for [openFrameworks](https://openframeworks.cc/) on 64-bit x86 Linux.

The summary of steps are:

- Compile your OF app in an Ubuntu 16.04 Virtual Machine
- On your host machine, run the provided shell script with your ‘app name’ and the provided directory as arguments
- Copy across the ‘app’ binary and ‘data’ directory from the VM, and paste it in the new AppImage directory structure
- Use the official ‘appimagetool’ to build the AppImage

The bulk of the work is setting up the VM. Once that’s done, just run a couple of terminal commands and voila! You have a shiny new AppImage that basically will work with any OF app and will work with any Linux distros (not just Ubuntu!) at least as old as Ubuntu 16.04, which was from 2016.

### Caveats
If you use 3rd party libraries, you will need to add them yourself. Currently this AppImage structure supports all OF functionality under Linux, including GStreamer…so that means audio, video, OpenCV etc.

If you run into any issues or want to add any more libraries, let me know. This is meant to be a generic AppImage structure specifically made for OF, so if I’ve missed some libraries, I’ll be happy to add them.

### A Note About GLIBC
The AppImages created from this guide should run on all Linux distros that have GLIBC of a version equal to or greater than 2.23, which should be most distros released from around 2016 onwards.

To see what GLIBC your version of Linux has (provided you have development tools installed), type this in a terminal:
```
ldd --version
```

## Prerequisites
All of the steps below up until *_Clone the AppImage directory using the provided script_*, will take place in a Virtual Machine running Ubuntu 16.04.

### VirtualBox running Ubuntu 16.04
First you need to install a Virtual Machine running Ubuntu 16.04.
As of writing the current version of Ubuntu available is 16.04.7
Follow the on-line guides to install Virtualbox - the version I used was 6.1. 

### Install GCC6
In order to run the latest openFrameworks (0.11.x) on Ubuntu 16.04, you'll need to install GCC 6:

```
sudo apt-get update && \
sudo apt-get install build-essential software-properties-common -y && \
sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y && \
sudo apt-get update && \
sudo apt-get install gcc-6 g++-6 -y && \
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6 && \
gcc -v
```

### Install openFrameworks
Download openFrameworks 0.11.2, or whatever is the current version.
Proceed to extract the downloaded OF drectory, then run the scripts in "openFrameworks"/scripts/ubuntu/

Make sure to edit the `install_dependencies.sh` script first. Open it up with your favourite editor and search for the text:
```
libgl1-mesa-dev${XTAG}
```
Remove the `${XTAG}` suffix, save the file, then run the scripts, e.g.

```
~/code/of_v0.11.2_linux64gcc6_release/scripts/linux/ubuntu$ sudo ./install_dependencies.sh
~/code/of_v0.11.2_linux64gcc6_release/scripts/linux/ubuntu$ sudo ./install_codecs.sh
```

Follow the script prompts and hit 'Y' for everything.
This should install all the required dependencies.

### Compile your application
Fetch your application code, typically from a version control system like git.
Compile it as an openFrameworks app, either using `Make` or whatever your preferred IDE is.


## Building the AppImage
The following steps take place on the host computer, apart from the copying of the compiled binary.

### Clone the AppImage directory using the provided script
Back on your host system (not on the VM) run the `rename-appimage.sh` bash script, and pass as a parameter the name of the app you compiled in the previous step, which will become the project name.
The second parameter the script takes is the default directory structure provided in this repository.
Run the script as follows:

```
$ ./rename-appimage.sh appname myApp-dir
```
where "appname" is your application name.

### Copy your compiled application
Copy your app compiled on the 16.04 VM into the now cloned AppImage directory created by the shell script, on your host machine. 
It will be called `appname-dir`, and you should copy the compiled OF binary as well as the `data` directory into the `./appname-dir/usr/bin/` directory.
Delete the existing `myApp` binary that's in that folder, as your application will now replace it.

### Download the appimagetool
Download the appimagetool, it is the application that actually creates the AppImage once your directory structure is ready:

https://github.com/AppImage/AppImageKit/releases

I used the appimagetool-x86_64.AppImage release.
Then make it executable:

```
chmod a+x appimagetool-x86_64.AppImage
```

### Build the AppImage
The final step is to build your AppImage with the appimagetool. Use the following command, which will depend on the exact name of the appimagetool, e.g.
```
./appimagetool-x86_64.AppImage ./appname-dir/
```

The final AppImage will be called something like `appname-x86_64.AppImage`.

Make it executable by running `chmod a+x appname-x86_64.AppImage` and you are good to go!
If you want further integration into the desktop, have a look at https://github.com/TheAssassin/AppImageLauncher/releases

### (optional) Creating an Icon

The best way to set an icon for your app is to do it internally. Include the following code in your main.cpp, and put an appropriate icon file in your `data/assets` folder (or wherever you prefer):

```
    ofApp *app = new ofApp();

    //Need to make setWindowIcon public in libs/openFrameworks/app/ofAppGLFWWindow.h to work
    ofAppGLFWWindow* win;
    win = dynamic_cast<ofAppGLFWWindow *> (ofGetWindowPtr());
    win->setWindowIcon("assets/icon_64x64.png");

    ofRunApp(app);
```
The other icon found inside the AppImage structure (the myApp.svg that gets renamed to _appname.svg_) is useful if you want to take advantage of Desktop integration tools for AppImage, such as the AppImageLauncher mentioned above. You can use the default OF icon provided, or make up your own using a vector graphic tool like Inkscape.

Note: currently in official releases the setWindowIcon() method above is private - this has been fixed in the latest master branch


### Troubleshooting
If you want to take a look at the directory structure and files of your appimage, you can extract it as follows:

```
$ appname-x86_64.AppImage --appimage-extract
```

If you want to certify your AppImage, download the linting tool at https://github.com/TheAssassin/appimagelint

Then you can run `./appimagelint-x86_64.AppImage ./appname-x86_64.AppImage` to receive a report of the integrity of your AppImage.

