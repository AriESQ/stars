# Docker Fun (well, PodMan, actually)
- a docker example using debian and raspberry pi sdk
- to create a development environment

## build.sh - build the Docker image
- cleans up (prunes) old containers and images
- builds to rpi-pico-sdk-image
- runs the RPi-Pico-SDK container
    - it initilizes the container
- does a `commit` which creates an image based on the last run
    - the new (final) image is called `rpi-pico-sdk-container`

## run.sh - run the docker image with ./projects mountpoint
- runs the rpi-pico-sdk-container
- mounts the local 'projects' folder as a volume
- you can build projects from the CLI
- or you can attach via VSCODE
- But, since you have the CLI there's no advantage to that
- Regardless, you can use your favorite IDE and edit the files in the ./projects folder and the results will be immediately be available in the container
- you can drag-n-drop .uf2 files from the ./projects folder to the RPI-RP2 device with no problems

## Files
- ./projects - your 'c' projects
- ./rpi-pico-sdk-image - files for building the Docker image
    - local scripts
        - build.sh - builds the image and container
        - Dockerfile - the Dockerfile for the image
        - install.sh - this is the `CMD` file that builds the PICO SDK in the image
        - pico_setup.sh - a doctored version of the "standard" RPI PICO SDK install script
    - delivered to rpi-pico-sdk:/home
        - bashrc - the .bashrc file for the finished image
    - delivered to rpi-pico-sdk:/usr/local/bin
        - env.sh - sets the PICO_SDK environment vars
        - hello.sh - a test program, prints "Hello World!"
        - login.sh - a script to cd /home and source .bashrc
        - makepico.sh a slightly hacked up version of Tony Smith's script to create a skeletal project folder complete with CMAKE scripts

## makepico.sh - Tony Smith's project template
 - `makepico.sh foldername`
 - run this inside the Docker container
 - generates a folder and initial files
 - main.c, main.h - template source files
 - CMakeLists.txt - a CMake script that points to PICO_SDK for all the goodies
 - pico_sdk_import.cmake - points to the "pico-extras"
 - make.sh - run once to create the 'build' folder and generate the .uf2 file
    - from then on just 'cd build' and 'make' to rebuild
    - no need to `cmake` again
    
## BUILDING FOR RPI - ERROR
- A strange error when running `./make.sh`
- /tmp/ccO4SZ7y.s:97: Error: selected processor does not support requested special purpose register -- `msr PRIMASK,r4'
    - Ignore it and re-run the `./make.sh` script
    - it will magically work again

## NOTES - using PodMan and creating Docker images

### Setup MacOS
- brew install wget
- brew install podman
- brew install --cask podman-desktop
- helper service:
    - The system helper service is not installed; the default Docker API socket address can't be used by podman. If you would like to install it run the following commands:
    - sudo /opt/homebrew/Cellar/podman/4.7.1/bin/podman-mac-helper install
    - You can still connect Docker API clients by setting DOCKER_HOST using the following command in your terminal session:
    - export DOCKER_HOST='unix:///Users/greg/.local/share/containers/podman/machine/qemu/podman.sock'
    - https://podman-desktop.io/docs/migrating-from-docker/using-podman-mac-helper

### Brew concepts
- formulae - download and compile source code and install cli tools
    - look in /opt/homebrew/Cellar
    - with symlinks to /usr/local/bin
- casks - download .app and .pkg files for installing GUI tools
    - delivered to /Applications
- bottles - precompiled binaries

### Get Debian
- podman machine init
    - downloads a 568MB Fedora image as your VM
- podman machine start
    - starts your podman server for listing repos etc
- podman machine set --rootful
    - do we need this?
- podman pull debian
    - download the latest debian from docker hub
- podman images
    - lists images

### Podman concepts
- IMAGE COMMANDS
    - podman images
        - list all remote and local images
    - podman run IMAGE [CMD] 
        - run the image with an optional command
    - podman run --name NAME -d -p EXTERNAL-PORT:INTERNAL-PORT IMAGE [CMD]
        - run image
        - assign a name
        - detached
        - map the internal port to the external port
    - podman build -t TAG DIRNAME
        - build the image wiht a tag name
        - DIRNAME where the Dockerfile exists
    - podman rmi IMAGE:TAG
        - remove an image
    - podman image prune
        - remove old versions
- CONTAINER COMMANDS
    - podman ps
        - list containers
    - podman ps -a 
        - list containers (even the stopped/exited ones)
    - podman run -it IMAGE --name NAME /bin/bash
        - runs the image
        - -i interactive 
        - -t pseudo-terminal
        - /bin/bash the program to run
    - podman start ID/NAME
        - restart the container
    - podman stop ID/NAME
        - stop the container
    - podman logs ID/NAME
        - print the logs from a container
    - podman rm ID/NAME
    - podman container prune
    - podman commit CONTAINER-NAME image-name
	-   to make a copy of a container into an image
    - podman save
    - podman cp /path/on/host [CONTAINER_ID]:/path/in/container

### Get RPI Pico SDK script
- wget https://raw.githubusercontent.com/raspberrypi/pico-setup/master/pico_setup.sh

### Run the container and create an image
- podman build -t rpi-pico-sdk-image .
    - create the image
- podman run rpi-pico-sdk-image

## Configure VSCode for RPI Pico and the SDK/Playground

Here are the steps:

Open the Command Palette (Ctrl+Shift+P) and type "C/C++: Edit Configurations (JSON)" and press Enter. This will open the c_cpp_properties.json file.

In the c_cpp_properties.json file, you will see a "configurations" section. In this section, there is an "includePath" setting. This is where you specify the paths to your include files.

Add the paths to your include files to the "includePath" setting. Paths are relative to the workspace root directory and should be separated by commas.

## To create a new project 

- inside the VM (podman container)
- `makepico.sh`

## VSCode
- Locally - install VSCode and the "Dev Containers" Extension
- You'll need to configure for PODMAN
    - https://code.visualstudio.com/remote/advancedcontainers/docker-options#_podman
- SHIFT-CMD-P -> "Dev Containers: Attach to Running Container"
    - It will install the server component for you

## Permission issues
- If you get problems with "Error statfs no such file or directory"
    - be sure to specify `-v /Volumes/GregsGit`
    - podman machine init podman-machine-default -v /Volumes/GregsGit

## TODO
- in Dockerfile - install PicoTool
- create Podman & Docker versions
- DONE:
    - set up home as identical to host

# pico-docker
