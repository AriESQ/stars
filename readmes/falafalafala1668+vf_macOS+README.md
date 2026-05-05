#  vf_macOS
Command-line macOS Virtual Machine on Apple Silicon

## Build

Run `xcodebuild` then `./build/Release/vf_macOS`

## Running

~~~
vf_macOS -f <folderPath> <options>

            -f <folderPath>          VM Folder Path(Must, Full Path)
            -g                       Show GUI
            -n <ipswPath>            New Install with ipsw Path
            -p <count>               CPU Core Count(Default 2)
            -m <size>                Memory Size(GB, min 4)
            -d <size>                Disk size(GB, Default 64)
            -D <img path>            Attach img path
~~~

## References
https://github.com/KhaosT/MacVM

https://github.com/evansm7/vftool