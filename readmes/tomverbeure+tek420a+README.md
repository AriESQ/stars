

**This is my scrapbook related to my Tektronix TDS 420A oscilloscope: drafts, some code, experiments. Don't expect things in the repo to be well organized or usable in any way. Eventually, some of the info here may end up in some blog post.**




# GPIB

## PyVisa

pip3 install gpib_ctypes


* Tek 420A Programmers Manual: http://w140.com/tekwiki/images/c/cd/070-8709-07.pdf

Fetching waveform:
    * See page 2-32 of programmers manual
    * `ACQ?`: Get acquistion parameters

```
RUNST;0;SAM;10;16;1
```

    * `ACQ:STATE RUN` : start acquisition
    * `ACQ:STATE STOP` : stop acquisition
    * `DATA:SOURCE CH1` : select data channel to fetch
    * `DATA:SOURCE CH1,CH2,CH3,CH4` : fetch multiple channels at once
    * `WFMPRE?` : waveform preamble information of all data:source channels
    * `CURV?` : waveform data
    * `WAVF?`: waveform preamble and waveform data together


Single acquistion:

    * `ACQ:STOPA SEQ`
    * `ACQ:REPE 1`
    * `ACQ:STATE ON`

Continuous acquistion:

    * `ACQ:STOPA RUNST`
    * `ACQ:STATE ON`



## USB permissions

(doesn't work...)

```
sudo vi /etc/udev/rules.d/72-linux_gpib_ni_usb.rules

SUBSYSTEMS=="usb", ACTION=="add", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="3923", ATTR{idProduct}=="709b", MODE="666", GROUP="tom", SYMLINK+="usb_gpib"
SUBSYSTEMS=="usb", ACTION=="add", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="3923", ATTR{idProduct}=="709b", RUN+="/usr/local/sbin/gpib_config"
KERNEL=="gpib[0-9]*", ACTION=="add", MODE="666", GROUP="tom"
```

```
sudo udevadm control -R
sudo udevadm monitor -e
udevadm info /dev/gpib0
```

In udev rule:
```
TAG+="test_gpib0"
```
This tag will show up in udevadm monitor


# TDS 420A firmware etc

* Use tektools: https://github.com/ragges/tektools
* https://groups.io/g/TekScopes/topic/69345603?p=Created,,,20,2,0,0::recentpostdate%2Fsticky,,,20,2,0,69345603

    Very good discussion bout tektools

* didn't compile out of the box with "cc". Changed to clang and it compiled.
* Put scope in firmware update mode by toggling 2 switches


* Dump boot ROM firmware: 0x0000_0000

```
tektool --debug --read bootrom.bin --length 524288
```

This fails with:
```
read_memory: invalid response: S
``

* Dump main firmware: 0x0400_0000

```
./tektool --read main_fw.bin --length 4192304 --base 0x01000000
```

* Dump settings: 0x0500_0000

```
./tektool --read settings.bin --length 262144 --base 0x05000000
```

Only 16 relevant bytes...

* Dump bootrom2.bin: 0x0800_0000

```
tektool --debug --read bootrom.bin --length 524288 --base 0x08000000
```

Differs from bootrom.bin at address 0x0000_0000


* Dump data_0x09000000.bin: 0x0900_0000

```
tektool --debug --read data_0x09000000.bin --length 524288 --base 0x09000000
```

Data seems to be repeating every 512 bytes. (But does it really?)

* Dump data_0x0d000000.bin: 0x0d000000

tektool --debug --read data_0x0d000000.bin --length 262144 --base 0x0d000000

* Program settings:


Program byte 5 to 0x00 -> read back 0x40
```
./tektool --write settings_short_05_00.bin --length 16 --base 0x05000000
./tektool --read dump.bin --length 16  --base 0x05000000; hexdump -C dump.bin
```

After reboot, value 5 is back to 0x00

Byte  6 -> 1: read back 0x40 for byte 5. No effect. Back to 0x00 after reboot. 
Byte  7 -> 1: read back 0x40 for byte 5. no effect. Back to 0x00 after reboot.
Byte  8 -> 1: read back 0x50 for byte 5, read back 0x0c (instead of 0x00 for byte 9). Back to 0x00 after reboot.
Byte  9 -> 1: doesn't stick. Stays 0x00. Byte 5 reads back 0x40.
Byte 10 -> 1: byte 10 stays 0xff. Byte 11 becomes 0x00. Back to original after reboot.
Byte 11     : no effect
Byte 12 -> 1: immediately stick. Back 0x0f after reboot.
Byte 13 -> 0,1: no effect.
Byte 14 -> 0,1: no effect.
Byte 15 -> 0,1: no effect.

68000 disassembler.

The resulting bootrom.bin file is 524288 in size. 

Used portion of the boot ROM seems to be from 0x0_0000 to ~0x0_6490?



./visa_cmd.py "PASSWORD PITBULL"
./visa_cmd.py "WORDCONSTANT:ATPUT 327687,1"
./visa_cmd.py "WORDCONSTANT:ATPUT 327689,1"
./visa_cmd.py "WORDCONSTANT:ATPUT 327686,1"


Hardcopy RS232 connector:

PCB 1  - DB9 1 - DCD
PCB 2  - DB9 6 - DSR
PCB 3  - DB9 2 - RXD
PCB 4  - DB9 7 - RTS
PCB 5  - DB9 3 - TXD
PCB 6  - DB9 8 - CTS
PCB 7  - DB9 4 - DTR
PCB 8  - DB9 9 - RI
PCB 9  - DB9 5 - GND
PCB 10 - DB9 case

Console RS232 connector:

https://forum.tek.com/viewtopic.php?t=138100#p279266

NC  Page 5  - PCB 1  - DB9 1 - DCD
    Page 10 - PCB 2  - DB9 6 - DSR
NC  Page 4  - PCB 3  - DB9 2 - RXD
    Page 9  - PCB 4  - DB9 7 - RTS
    Page 3  - PCB 5  - DB9 3 - TXD
TX  Page 8  - PCB 6  - DB9 8 - CTS
    Page 2  - PCB 7  - DB9 4 - DTR
#   Page 7  - PCB 8  - DB9 9 - RI 
#   Page 1  - PCB 9  - DB9 5 - GND
NC  Page 6  - PCB 10 - NC


NC    Page 5  - PCB 1  - NC
GND!  Page 10 - PCB 2  - DB9 5 - GND
NC    Page 4  - PCB 3  - DB9 9 - RI
      Page 9  - PCB 4  - DB9 4 - DTR
      Page 3  - PCB 5  - DB9 8 - CTS
TX!   Page 8  - PCB 6  - DB9 3 - TXD
      Page 2  - PCB 7  - DB9 7 - RTS
      Page 7  - PCB 8  - DB9 2 - RXD
      Page 1  - PCB 9  - DB9 6 - DSR
NC    Page 6  - PCB 10 - DB9 1 - DCD





Console Powerup log
```
           	Bootrom Header Checksum passed.
	Bootrom Total Checksum passed.
	BootRom Check Sum passed.
	Bus Error Timeout test passed.
	Bus Error Write to Bootrom passed.
	GPIB Test passed.
Kernel Diagnostics Complete.

Calling SDM (monitor) Routine.

SDM (monitor) not enabled.
	Enabling Bus Control register. Value = 0x2
	Flashrom Programming Voltage is OFF.
	Flashrom DSACK and JumpCode test passed.
	Flashrom Checksums passed.
Bootrom Diagnostics Complete.

Transferring control to the Flashrom.
sysDramControllerInit
sysDramByteStrobeTest
sysDramTest
bcopy(<Idata>)
bzero(<bss>)
intVecBaseSet(getVbr())
sysDevDramTest
0x0 bytes of development dram found
validateDataSpace
Outer Kernel DSACK Test
Pending Interrupt Test
Walk IPL to Zero Test
Timer Int Test
usrInit()
cacheEnables()
bzero(&edata,&end - &edata)
intVecBaseSet()
excVecInit()
bzero(&end,sysMemTop() - &end )
sysHwInit()
ioGlobalStdSet({STD_IN,STD_OUT,STD_ERR})
xcInit()
logInit()
sigInit()
dbgInit()
pipeDrv()
stdioInit()
dosFsInit()
ramDrv()
floatInit()
mathSoftInit()
spyStop()
timexInit()
selectInit()
symTblCreate(standAlone)
symTblCreate(stat)
sysStarSut(a
            rtni Pcopower-On Diag Sequence
hwAccountant probe routines
  Probe for unexpected pending ints
  Real time clk present
  Dsp Instr mem size
  Dsp D2 mem size
  Dsp D1 mem size
  Dsy Vect0 mem size
  Dsy Vect1 mem size
  Dsy Wfm0 mem size
  Dsy Wfm1 mem size
  Dsy Text0 mem size
  Dsy Text1 mem size
  Acq number of digitizers
  Acq mem size
>   Cpu timer interval uSec
  Cpu Dram size
  NvRam mem size
  Opt Math Package presence
  Opt RS232/ Cent presence
  Acq 8051 presence
  Acq ADG209C presence
  Opt 1M presence
  Acq record length size
  Opt TvTrig presence
  Dsy color presence
  Opt floppy drive presence
dsyWaitClock ................... pass
clockCalVerify ................. pass
cpuDiagBatTest ................. pass
cpuDiagAllInts ................. pass
cpuEEromLibDiag ................ pass
calLibDefaultCk ................ pass
dspForcedBus ................... pass
dsp68kD2MemTest ................ pass
optRS232DuartIO ................ pass
dsp68kMemTest .................. pass
dspRunVerify ................... pass
dspBusRequestTest .............. pass
dspImplicitBusAccess ........... pass
dspTristarMemTest .............. pass
dspDsyToDspInts ................ pass
dspAcqToDspInts ................ pass
nvLibrariansDiag ............... pass
dsyDiagResetReg ................ UNTESTED
atBusTest ...................... pass
dsyDiagResetReg ................ UNTESTED
dsyDiagVscReg .................. pass
dsyDiagPPRegMem ................ pass
dsyDiagRasRegMem ............... pass
dsyDiagRegSelect ............... pass
dsyDiagRamdacRegMem ............ pass
dsyDiagAllMem .................. pass
dsySeqYTModeV0Intens ........... pass
dsyDiagSeqXYModeV1 ............. pass
dsyRastModeV0Walk .............. pass
dsyRastModeV1Attrib ............ pass
dsyWaitClock ................... pass
attn8051testResult ............. pass
attnDACReadback ................ pass
dsyWaitClock ................... pass
acq8051testResult .............. pass
adgRegDiag ..................... pass
dsyWaitClock ................... pass
adgMemTestDiag ................. pass
trigComparatorTest ............. pass
trigDBERunsAfter ............... pass
tbiRampTest .................... pass
acqRampDiagAll ................. pass
dsyWaitClock ................... pass
fpDiagConf ..................... pass
et not started, either there was trouble or the devnet is missing
floppyDriverStartup()
can't open input 'fd0:/startup.bat'
  errno = 0x13 (S_errno_ENODEV)

/Thu May 9 11:26:15 PDT 1996/k2_vu/paulkr

Smalltalk/V Sun Version 1.12
Copyright (C) 1990 Object Technology International Inc.
0x2ff4684 (V main): 
brTriesMax:         1 busRequestCount: 1 busRequestGranted: 0
```

help:
```
-> help

help                       Print this list
dbgHelp                    Print debugger help info
nfsHelp                    Print nfs help info
netHelp                    Print network help info
spyHelp                    Print task histogrammer help info
timexHelp                  Print execution timer help info
h         [n]              Print (or set) shell history
i         [task]           Summary of tasks' TCBs
ti        task             Complete info on TCB for task
sp        adr,args...      Spawn a task, pri=100, opt=0, stk=20000
taskSpawn name,pri,opt,stk,adr,args... Spawn a task
td        task             Delete a task
ts        task             Suspend a task
tr        task             Resume a task
d         [adr[,nwords]]   Display memory
m         adr              Modify memory
mRegs     [task]           Modify a task's registers interactively
d0-d7,a0-a7,sr,pc  [task]  Display a register of a task
version                    Print VxWorks version info, and boot line

Type <CR> to continue, Q<CR> to stop: 

iam       "user"[,"passwd"]  Set user name and passwd
whoami                     Print user name
devs                       List devices
cd        "path"           Set current working path
pwd                        Print working path
ls        ["path"[,long]]  List contents of directory
ll        ["path"]         List contents of directory - long format
rename    "old","new"      Change name of file
copy      ["in"][,"out"]   Copy in file to out file (0 = std in/out)
ld        [syms[,noAbort][,"name"]] Load stdin, or file, into memory
                             (syms = add symbols to table:
                              -1 = none, 0 = globals, 1 = all)
lkup      ["substr"]       List symbols in system symbol table
lkAddr    address          List symbol table entries near address
checkStack  [task]         List task stack sizes and usage
printErrno  value          Print the name of a status value
period    secs,adr,args... Spawn task to call function periodically
repeat    n,adr,args...    Spawn task to call function n times (0=forever)
diskFormat  "device"       Format disk
diskInit  "device"         Initialize file system on disk

Type <CR> to continue, Q<CR> to stop: 

squeeze   "device"         Squeeze free space on RT-11 device

NOTE: arguments specifying 'task' can be either task id or "name"

value = 1 = 0x1
```


```
-> libManagerWordAt(0x50000)
value = 0 = 0x0
-> libManagerWordAt(0x50001)
value = 0 = 0x0
-> libManagerWordAt(0x50002)
value = 0 = 0x0
-> libManagerWordAt(0x50003)
value = 0 = 0x0
-> libManagerWordAt(0x50004)
value = 0 = 0x0
-> libManagerWordAt(0x50005)
value = 0 = 0x0
-> libManagerWordAt(0x50006)
value = 0 = 0x0
-> libManagerWordAt(0x50007)
value = 0 = 0x0
-> libManagerWordAt(0x50008)
value = 0 = 0x0
-> libManagerWordAt(0x50009)
value = 0 = 0x0
-> libManagerWordAt(0x5000a)
value = 0 = 0x0
-> libManagerWordAt(0x5000b)
value = 0 = 0x0
-> libManagerWordAt(0x5000c)
value = 0 = 0x0
-> libManagerWordAt(0x5000d)
value = 0 = 0x0
-> libManagerWordAt(0x5000e)
value = 0 = 0x0
-> libManagerWordAt(0x5000f)
value = 0 = 0x0
```

```
-> d 0x000000
05000080:  070c ff4e 0309 0001  0700 ffff 1cc3 ffff   *...5............*
05000090:  070c ff08 0309 0002  0700 ffff 1cc3 ffff   *................*
050000a0:  070c ff4e 0309 0002  0700 ffff 1cc3 ffff   *...5............*
050000b0:  070c ff08 0309 0002  0700 ffff 1cc3 ffff   *................*
050000c0:  070c ff4e 0309 0002  0700 ffff 1cc3 ffff   *...5............*
050000d0:  070c ff08 0309 0002  0700 ffff 1cc3 ffff   *................*
050000e0:  070c ff4e 0309 0002  0700 ffff 1cc3 ffff   *...5............*
050000f0:  070c ff08 0309 0001  0700 ffff 1cc3 ffff   *................*

-> d 0x1000000
01000000:  4e71 4ef9 0100 2850  0100 011e 0122 1b54   *NqN...(P.....".T*
01000010:  02e0 1000 02e3 33b0  280d 0100 002c 0100   *......3.(....,..*
01000020:  1d54 ffff ffff ffff  ffff 764f 434f 5059   *.T........vOCOPY*
01000030:  5249 4748 5420 5445  4b54 524f 4e49 5820   *RIGHT TEKTRONIX *
01000040:  494e 432c 2031 3938  392d 3139 3936 0000   *INC, 1989-1996..*
01000050:  4343 4f4f 5050 5959  5252 4949 4747 4848   *CCOOPPYYRRIIGGHH*
01000060:  5454 2020 5454 4545  4b4b 5454 5252 4f4f   *TT  TTEEKKTTRROO*
01000070:  4e4e 4949 5858 2020  4949 4e4e 4343 2c2c   *NNIIXX  IINNCC,,*

-> d 0x2000000
02000000:  0101 0101 0202 0202  0120 a924 0120 a924   *......... .$. .$*
02000010:  0120 a924 0120 a924  0120 a924 0120 a924   *. .$. .$. .$. .$*
02000020:  0120 a924 0120 a924  0120 a924 0120 a924   *. .$. .$. .$. .$*
02000030:  0120 a924 0120 a924  0120 a924 0120 a94c   *. .$. .$. .$. .L*
02000040:  0120 a94c 0120 a94c  0120 a94c 0120 a94c   *. .L. .L. .L. .L*
02000050:  0120 a94c 0120 a94c  0120 a94c 0120 a94c   *. .L. .L. .L. .L*
02000060:  0120 a94c 02ff cf94  0120 a94c 02ff db04   *. .L..... .L....*
02000070:  02ff f5bc 0120 a94c  0120 a94c 0120 a94c   *..... .L. .L. .L*

-> d 0x3000000
03000000:  
Bus Error

-> d 0x4000000
04000000:  2c00 2c00 2c00 2c00  2c00 2c00 2c00 2c00   *,.,.,.,.,.,.,.,.*
04000010:  2c00 2c00 2c00 2c00  2c00 2c00 2c00 2c00   *,.,.,.,.,.,.,.,.*
04000020:  2c00 2c00 2c00 2c00  2c00 2c00 2c00 2c00   *,.,.,.,.,.,.,.,.*
04000030:  2c00 2c00 2c00 2c00  2c00 2c00 2c00 2c00   *,.,.,.,.,.,.,.,.*
04000040:  2c00 2c00 2c00 2c00  2c00 2c00 2c00 2c00   *,.,.,.,.,.,.,.,.*
04000050:  2c00 2c00 2c00 2c00  2c00 2c00 2c00 2c00   *,.,.,.,.,.,.,.,.*
04000060:  2c00 2c00 2c00 2c00  2c00 2c00 2c00 2c00   *,.,.,.,.,.,.,.,.*
04000070:  2c00 2c00 2c00 2c00  2c00 2c00 2c00 2c00   *,.,.,.,.,.,.,.,.*

-> d 0x5000000
05000000:  070c ff4e 0309 0002  0700 ffff 1cc3 ffff   *...5............*
05000010:  070c ff08 0309 0001  0700 ffff 1cc3 ffff   *................*
05000020:  070c ff4e 0309 0001  0700 ffff 1cc3 ffff   *...5............*
05000030:  070c ff08 0309 0001  0700 ffff 1cc3 ffff   *................*
05000040:  070c ff4e 0309 0002  0700 ffff 1cc3 ffff   *...5............*
05000050:  070c ff08 0309 0002  0700 ffff 1cc3 ffff   *................*
05000060:  070c ff4e 0309 0001  0700 ffff 1cc3 ffff   *...5............*
05000070:  070c ff08 0309 0002  0700 ffff 1cc3 ffff   *................*

-> d 0x8000000
08000000:  0002 7ffe 0000 22d0  0000 07f0 0000 07f0   *......".........*
08000010:  0000 07f0 0000 07f0  0000 07f0 0000 07f0   *................*
08000020:  0000 07f0 0000 07f0  0000 07f0 0000 07f0   *................*
08000030:  0000 07f0 0000 07f0  0000 07f0 0000 0850   *...............P*
08000040:  0000 0850 0000 0850  0000 0850 0000 0850   *...P...P...P...P*
08000050:  0000 0850 0000 0850  0000 0850 0000 0850   *...P...P...P...P*
08000060:  0000 0850 0000 0850  0000 0850 0000 0850   *...P...P...P...P*
08000070:  0000 0850 0000 0850  0000 0850 0000 08ac   *...P...P...P....*

-> d 0x9000000
09000000:  4879 02e1 4879 02e1  4879 02e1 4879 02e1   *(�RJ(�RJ(�RJ(�RJ*
09000010:  4879 02e1 4879 02e1  4879 02e1 4879 02e1   *(�RJ(�RJ(�RJ(�RJ*
09000020:  4879 02e1 4879 02e1  4879 02e1 4879 02e1   *(�RJ(�RJ(�RJ(�RJ*
09000030:  4879 02e1 4879 02e1  4879 02e1 4879 02e1   *(�RJ(�RJ(�RJ(�RJ*
09000040:  4879 02e1 4879 02e1  4879 02e1 4879 02e1   *(�RJ(�RJ(�RJ(�RJ*
09000050:  4879 02e1 4879 02e1  4879 02e1 4879 02e1   *(�RJ(�RJ(�RJ(�RJ*
09000060:  4879 02e1 4879 02e1  4879 02e1 4879 02e1   *(�RJ(�RJ(�RJ(�RJ*
09000070:  4879 02e1 4879 02e1  4879 02e1 4879 02e1   *(�RJ(�RJ(�RJ(�RJ*

-> d 0xd000000
0d000000:  4848 4848 4848 4848  4848 4848 4848 4848   *((((((((((((((((*
0d000010:  4848 4848 4848 4848  4848 4848 4848 4848   *((((((((((((((((*
0d000020:  4848 4848 4848 4848  4848 4848 4848 4848   *((((((((((((((((*
0d000030:  4848 4848 4848 4848  4848 4848 4848 4848   *((((((((((((((((*
0d000040:  4848 4848 4848 4848  4848 4848 4848 4848   *((((((((((((((((*
0d000050:  4848 4848 4848 4848  4848 4848 4848 4848   *((((((((((((((((*
0d000060:  4848 4848 4848 4848  4848 4848 4848 4848   *((((((((((((((((*
0d000070:  4848 4848 4848 4848  4848 4848 4848 4848   *((((((((((((((((*
```

```
-> checkStack
  NAME        ENTRY        TID     SIZE   CUR  HIGH  MARGIN
------------ ------------ -------- ----- ----- ----- ------
tExcTask     _excTask     2ffc1d0   2988   160   656   2332 
tLogTask     _logTask     2ffac88   4988   164   724   4264 
tShell       _shell       2ff8f54   9532   852  3608   5924 
gpibIHTask   _gpibIHTask  2fed2a0   1528   136   204   1324 
fifoTask     _fifoTask    2fed9d4   1020    76   200    820 
causeEnable  _causeEnable 2fffcdc   1020   144   220    800 
rtcTicker    _dateTimeQue 2feed08   4092    72   140   3952 
priority_nod _priority_no 2ff0758   4088    68   696   3392 
grun Reboote _rebootGrun  2fe8d0c    992    72   156    836 
GPIB monitor _GpibMonitor 2fec970   1492    92   176   1316 
GPIB reboot  0x115c804    2fec060   1496    68   152   1344 
trigStatus   _trigStatusQ 2ffecd8   1496    60   424   1072 
GPIB parser  _Grun        2feb750   9996   888  1016   8980 
serialPrintQ _spTask      2fef424    992   228   336    656 
V main       _main        2ff4684   9532   144  1192   8340 
evalProcess  _eval_loop   2ff1e14   4996    64   272   4724 
centronicsTa _centronicsT 2fff40c   1016    80   164    852 
libSaver     _realLibSave 2ff4e48    528    84   152    376 
sysIdle      _sysIdle     2ffd790   1992    52   152   1840 
INTERRUPT                           1000     0   228    772 
value = 36 = 0x24 = '$'
```

```
reboot
ringBell
libNVFactoryValuesLoaded
```

```
libManagerByteAtPut 0x50007, 1          -> Option 5 - Video Trigger
libManagerByteAtPut 0x50009, 1          -> Option 2F - FFT
```


After programming all of this, still no 1M option:
```
-> libManagerWordAt 0x50000
value = 1 = 0x1
-> libManagerWordAt 0x50001
value = 0 = 0x0
-> libManagerWordAt 0x50002
value = 1 = 0x1
-> libManagerWordAt 0x50003
value = 1 = 0x1
-> libManagerWordAt 0x50004
value = 1 = 0x1
-> libManagerWordAt 0x50005
value = 1 = 0x1
-> libManagerWordAt 0x50006
value = 1 = 0x1
-> libManagerWordAt 0x50007
value = 1 = 0x1
-> libManagerWordAt 0x50008
value = 1 = 0x1
-> libManagerWordAt 0x50009
value = 1 = 0x1
-> libManagerWordAt 0x5000a
value = 0 = 0x0
-> libManagerWordAt 0x5000b
value = 1 = 0x1
-> libManagerWordAt 0x5000c
value = 1 = 0x1
-> libManagerWordAt 0x5000d
value = 1 = 0x1
-> libManagerWordAt 0x5000e
value = 1 = 0x1
-> libManagerWordAt 0x5000f
value = 1 = 0x1
```

With all libManager words (except 0x5000a) set to 1:

```
d 0x5000000
05000000:  070c ffa0 1209 0002  0700 ffff 1cc2 ffff   *................*
05000010:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000020:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000030:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000040:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000050:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000060:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000070:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
```

```
0x50000 -> 0
d 0x5000000
05000000:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000010:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000020:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000030:  070c ffe0 0209 0001  0700 ffff 1cc2 ffff   *................*
05000040:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000050:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000060:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000070:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
```

```
-> libManagerWordAt 0x50001
value = 0 = 0x0
-> d 0x5000000
05000000:  070c ffe0 1209 0002  0700 ffff 1cc2 ffff   *................*
05000010:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000020:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000030:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000040:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000050:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000060:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000070:  070c ffe0 0209 0001  0700 ffff 1cc2 ffff   *................*
```

```
-> libManagerWordAtPut 0x50003, 0
value = 65535 = 0xffff
-> d 0x5000000
05000000:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000010:  070c ffe0 0209 0001  0700 ffff 1cc2 ffff   *................*
05000020:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000030:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000040:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000050:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000060:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
05000070:  070c ffe0 0209 0002  0700 ffff 1cc2 ffff   *................*
```

Install Ghidra: 

sudo apt install openjdk-11-jdk

List all symbols with their address
```
lkUp "hw" 
```

hwProbe1MOption -> 

hwAccountantQuery: 

0x20f: size of acquisition RAM (131071)
0x216: ProbeD2MemSize
0x255: InstrumentNameStringPtr
0x271: hwProbeSpecialDiagModeActive
0x2a0: hwProbeSpecialDiagLoopCount
0x2a1: hwProbeSpecialDaigSeqId
0x2b8: 30000 points -> value when 1M option is not possible
0x2bf: TDS420A
0x317: MathPak  -> 0x50009
0x537: flashRomDateStringPtr
0x54c: TDS410A
0x560: TDS430A
0x700: hwProbeTvTrigPresent -> Check 0x50007

hwATableAddr: 0x02e57d78

-> d 0x02e57d78, 128
02e57d70:                       0117 7abe 0000 0000   *        ..z.....*

Links to 0x01177abe -> _hwADefaultTables: int[2] = { 0x13, 0x0c }

hwAActualValues:  table at 0x02e57d80

02e57d80:  0000 0001 0001 ffff  0003 ffff 0003 ffff   *................*
02e57d90:  0000 0fff 0000 0fff  0001 ffff 0000 0000   *................*
02e57da0:  0000 ffff 0000 0000  0000 0004 0000 0004   *................*
02e57db0:  0001 ffff 0000 411a  00a8 0000 02e0 0000   *......A.........*
02e57dc0:  001f ffff 00a0 0000  0007 ffff 0000 0001   *................*
02e57dd0:  0000 0001 0000 0001  0000 0001 0000 0000   *................*
02e57de0:  0000 7530 0000 0001  0000 0001 0000 0000   *..u0............*
02e57df0:  0000 0000 0000 0000  0000 0001 0000 0000   *................*

hwAExpectedValues: table at 0x02e57e00

02e57e00:  0000 0001 0001 ffff  0003 ffff 0003 ffff   *................*
02e57e10:  0000 0fff 0000 0fff  0001 ffff 0000 0000   *................*
02e57e20:  0000 ffff 0000 0000  0000 0004 0000 0004   *................*
02e57e30:  0001 ffff 0000 411a  00a8 0000 02e0 0000   *......A.........*
02e57e40:  001f ffff 00a0 0000  0007 ffff 0000 0001   *................*
02e57e50:  0000 0000 0000 0001  0000 0001 0000 0000   *................*
02e57e60:  0000 7530 0000 0000  0000 0000 0000 0000   *..u0............*
02e57e70:  0000 0000 0000 0000  0000 0000 0000 0007   *................*
02e57e80:  baad c0de baad c0de  011a 9cfe 011a 9cfe   *................*


Address 0x2e57de0: 0x7530 -> 30000
Address 0x2e57e60: 0x7530 -> 30000
Address 0x1179763: 0x1d4d0 -> 120000

Flow:
_hwProbeInstalledAcqRecordLength:
{
    call hwProbe1MOption()
    when return 0 -> return hwAccountantGetValue(3, 0x2b8) -> 30000
    else{
        Get actual memory installed -> hwAccountantQuery(0x20f) -> 131071
        Decrease actual memory installed by 1 until it's 1 smaller than 120000
    }

    return AcqRecordLength
}

hwProbe1MOption()
{
    hwAccountantQuery(0x216)    -> val1 = 262143 (0x3ffff)
    hwAccountantQuery(0x20f)    -> val2 = 131071 (0x1ffff)

    if ((val1 > 0xffffe) && (val2 > 0x1fffe)){
        return true;
    }

    return false;
}

Need to change return value of 0x2b8

(hwProbe1MPresent is not used anymore.)

_sysRam_Adrs: DRAM address starts at 0x02e0_0000.
_sysDramTest: checks from 0x02e0_0000 -> 0x02ff_ffff -> 128MB of RAM

_sysInitDataSpace:
    - copies flash data
        - copies data from 0x0122_1b54 to 0x02e0_1000 (size: 0x3_23b0)
            -> 0x2e0_1000 to 0x02e3_33b0
    - clears 0x02e3_33b0 -> 0x02f2_9634
            This includes that hw_AActualValues etc.

_hwAccountantInitialize()
    _hwAccountantStoreFoundValues(): sets values in _hwAExpectedValues and _hwAActualValue
    _hwAccountantActVsExp()


0xa00000 : NvRamStartAddr
