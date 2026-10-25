# Colorlight-i9-tools
A collection of tools and notes made while messing with the Colorlight i9 and the external "breakout" board from Muse Labs

(c) 2024 by kittennbfive - licence for each part specified inside corresponding README and/or files
  
EVERYTHING IS PROVIDED WITHOUT ANY WARRANTY!  

## Pinviewer
Inside folder `Pinviewer/` there is an interactive tool (HTML+Javascript) to show the pinout of the external board from Muse Labs.

## OpenOCD-file
Inside folder `prog_openocd/` there is a "command"(?)-file to program a bitstream into the FPGA using OpenOCD. It is based on the stuff from the official(?) repo but updated because of "deprecated"-warnings from OpenOCD. You can use it if you do not want to (or can't) use the scripts that are in the other repo.  
Please note that programming is horribly slow, changing the `adapter speed` does not help. As far as i know the connection for the microcontroller on the external board is *USB1.1* only, that's probably at least part of the problem. If you use the FOSS Yosys-toolchain you can add `--compress` to the arguments of `nextpnr-ecp5`, especially for small designs this *really* reduces flashing time.
