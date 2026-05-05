
# Macrosilicon MS2107 CVBS to USB converter research

Cheap CVBS-USB converter device contains **MS2107** chip and **AT24C16** EEPROM.

I want to fix some issues in behavior. I read EEPROM with **CH341A** EEPROM programmer and tried to understand internal structure.

Here's my research results:

## Useful resources

8051 command line disassembler, helpful for code analysis
https://github.com/anarcheuz/8051-disassembler.git

ms-tools: research and modifications for MS2106 MS2109 MS2130 chips
https://github.com/BertoldVdb/ms-tools.git

MS2107 datasheet
https://item.szlcsc.com/datasheet/MS2107/44259544.html

## EEPROM data structure

### Format structure

MS2107 EEPROM contains section:
1. [2 bytes] Signature 08 16
2. [2 bytes] Code size N
3. [from 0x04 to 0x30 bytes]  Header data. Configuration parameters and USB devices names
4. [N bytes] Code size 
5. [2 bytes] Header checksum
6. [2 bytes] Code checksum
7. ?? Extended configuration section or code

### Checksums

EEPROM contains 2 checksums, first for code, second for header, but firmware version field is excluded from checksum calculation.

Type of checksums is simple **uint16**, just sum of bytes:

```
header_checksum = sum(2:11) + sum(16:0x30)  # excluded last 4 bytes from first 16-byte line
code_checksum = sum(0x30:0x30+code_size)
```

### Details

| RAM address   | Byte address<br>Offset in EEPROM  | Len<br>bytes | Default value   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|---------------|-----------------------------------|--------------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0xC7D0        | 0x00 0x01                         | 2            | 0x08 0x16       | EEPROM image signature                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 0xC7D2        | 0x02 0x03                         | 2            | my case: 0x00E9 | **Program code length** (N), it started from byte 0x30 in EEPROM.<br>Code length can be 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 0xC7D4        | 0x04 0x05                         | 2            | 0xFFFF          | **USB VID** *(big endian, first byte is hi-byte, second lo-byte)*<br>When default value is specified, chip uses 0x534D                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 0xC7D6        | 0x05 0x06                         | 2            | 0xFFFF          | **USB PID** *(big endian, first byte is hi-byte, second lo-byte)*<br>When default value is specified, chip used 0x0021                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 0xC7D8        | 0x08                              | 1            | my case: 0x03   | **Common flags**<br>bit 0 - Patch_Common<br>bit 1 - USB_cmd<br>bit 2 - USB_int<br>bit 3 - Timer_Int<br>bit 4 - VSync_int<br>bit 5 - TVD_int<br>bit 6 - Reserved<br>bit 7 - Reserved                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 0xC7D9        | 0x09                              | 1            | my case: 0xFD   | **Function flag 1**<br>bit 0 - AV port enabled (1-enabled, 0-disabled)<br>bit 1 - SV port enabled (1-enabled, 0-disabled)<br>other bits: 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 0xC7DA        | 0x0A                              | 1            | my case: 0x01   | **Mute pattern (high 4 bits) and Function flag 2 (low 4 bits)**<br><br>   H 4bit             L 4bit<br>[mute partern] [functions 2 enabled]<br><br>**Mute patterns values**<br>0x0 - pure black<br>0x1 - pure blue<br>0x2 - pure green<br>0x3 - pure red<br>0x4 - pure white<br>0x5 - cross hatch<br>0x6 - H ramp<br>0x7 - V ramp<br>0x8 - color bar<br>0x9 - H gray scale<br>0xA - V gray scale<br>0xB - 2nd H gray scale<br>0xC - primary color <br>0xD - interlace black <br>0xE - B&W random<br>0xF - color random<br><br>**Functions 2 flag bits**<br>bit 0 (0x01) - audio enable<br>bit 1 (0x02) - stereo enabled<br>bit 3 (0x04) - save Brightness/Contrast/Saturation/Hue <br>            (4-byte signed int8 config block after checksums) |
| 0xC7DB        | 0x0B                              | 1            |                 | **Default port (high bit) and default TV mode (low 7 bits) selector**<br><br>   H 1bit           L 7bit<br>[default port] [default TV mode]<br><br>**Default port**<br>0 - AV<br>1 - SV  <br><br>**Default TV mode**<br>0x00 - NTSC 358<br>0x01 - NTSC 443 <br>0x02 - PAL<br>0x03 - PAL M<br>0x04 - PAL NC<br>0x05 - SECAM<br>0x06 - PAL 60<br>0x7F - NO SIGNAL                                                                                                                                                                                                                                                                                                                                                                                     |
| 0xC7DC-0xC7DF | 0x0C-0x0F                         | 4            |                 | Firmware version (not used in CRC calculation)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 0xC7E0        | 0x10                              | 1            | 0x0A            | USB Video device name length. 0xFF - no specified name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 0xC7E1-0xC7EF | 0x11-0x1F                         | 15           | "USB Video"     | 'USB Video' device name. Bytes after text contain 0xFF.<br>If no name specified, all field should contain 0xFF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 0xC7F0        | 0x20                              | 1            | 0x0A            | USB Audio device name length. 0xFF - no specified name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 0xC7F1-0xC7FF | 0x21-0x2F                         | 15           | "USB Audio"     | 'USB Audio' device name. Bytes after text contain 0xFF.<br>If no name specified, all field should contain 0xFF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 0xC800        | 0x30-(0x30+N)                     | N            |                 | Code section                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 0xC800+N      | (0x30+N)                          | 2            |                 | Code checksum                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 0xC800+N+2    | (0x30+N)+2                        | 2            |                 | Header checksum (excludes firmware version field)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 0xC800+N+4    | (0x30+N)+4                        | ?            |                 | **Extended configuration section** <br>It contains BCSH values if enabled in Functions 2 flag.<br>Some additional data or code may be included                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |


## Fix checksums after EEPROM modifications

I wrote simple python script for verify and recalculate checksums for *MS2107* EEPROM images, it placed in `eeprom_checksum_tool` directory.

**How to use script `test_fix_checksum.py`**

1. Create file `eeprom.bin` with binary data from EEPROM and place it into directory with `test_fix_checksum.py`
2. Open terminal or cmd, change directory to `{PROJECT_DIR}/eeprom_checksum_tool`
3. Run `python test_fix_checksum.py` without parameters
4. Script verifies checksums, recalculate them and create file `eeprom_modified.bin` file with correct recalculated checksums

## Code section analysis (research results)

Code section contains:
When EEPROM is loaded, it placed by RAM address 0xC7D0. So, code section started in EEPROM on address 0x30, will be placed in RAM to 0xC8000.
Hook size is 0x10 bytes. They can call or jump above 

1. Hooks table (0x30-N*0x10)
   Depending on which bits are set in Common Flags, these hooks are called or not. The hook size is 0x10, typically jmp or call to the addresses below.
   Hook table:

| Offset in EEPROM  | RAM address  | CommonFlags bit  | Description                                                             |
|-------------------|--------------|------------------|-------------------------------------------------------------------------|
|  0x30             | 0xC800       | 00000001b (0x01) |  Patch_common. This hook **is not** called from an ISR.                 |
|  0x40             | 0xC810       | 00000010b (0x02) |  USB_cmd. This hook is called from an ISR.                              |
|  0x50             | 0xC820       | 00000100b (0x04) |  USB_isr. ???                                                           |
|  0x60             | 0xC830       | 00001000b (0x08) |  Timer_int. Called by timer ISR                                         |
|  0x70             | 0xC840       | 00010000b (0x10) |  VSync_int. Called when a vertical sync signal is received.             |
|  0x80             | 0xC850       | 00100000b (0x20) |  TVD_int. Does not work for MS2107, but actually present                |

2. User code
   User code is located in hooks and in lower memory. Often, 16 bytes (0x10) isn't enough for the current hook, so it jumps lower into the EEPROM.


### Firmware behavior logic

After starting at address 0x0000, execution is transferred to the main function at address 0x5297. After waiting for memory initialization (a 0x00 byte is written to cell 0x7F and checked to be 0x00),
control resumes at address 0x52DE.

### Common Patch
The hook is located in memory at address 0xC800 (in EEPROM offset is 0x30).

Called from subroutine 0x6F9E.   
   
```c
void _6F9E(uint8_t val) {
  [0xC66B] = val
  _C800(); // call user code hook (from EEPROM)
}

void _6F47() {
  if ([0xC7D8] & 1) {  // If Patch_Common enabled in CommonFlags
    _6F9E();  // call
  }
}   
```   
   
Hook code text from the EEPROM of a real device:   

```c
_S1REL = SFR 0x9D

void _C800(uint8_t val) {

  if(val == 1) {
    //_C85A
	_A = [0xFC08];
	[0xFC08] = _A & 0xFD;
	[0xFC08] = [0xFC08] | 1;
	SFR[0x9D] |= 0x07;   // SFR 0x9D -> S1REL 
	if ([0x0043] == 1) {
	  [0xFC44] |= 0x10;
	}
	
	if ([0x0044] == 0) {
	  [0xF80B] &= 0xEF;
	  [0xF804] |= 0x10;
	  [0xF809] |= 0x08;
	  return;
	}
	
	[0xF847] |= 0x07;
	[0xF804] |= 0x30;
	[0xF809] |= 0x18;
	return;
  } else if(val ==2) {
    //_C8A7
	if ([0x0040] - 0x07 < 0) {
	  if ([0xFB4F] & (1<<4) != 0) {
	    if ([0x0020] & (1<<5) != 0) {
		  [0x0020] &= (0xFF ^ (1<<5)); // clear bit 5
		  return;
		}
	  }
	}
	  
	if ([0xFB4F] & (1<<4) != 0) {
	  return;
	}
	  
	if ([0x0020] & (1<<5) != 0) {
	  return;
	}

	[0x0020] |= (1<<5);
	return;
  } else if(val ==5) {
    //_C8A4
	_5659(); // call to main code
	[0xF808] &= 0x11;
	[0xF9A0] = 1;
	_6087();  // call to main code
	return;
  } else if(val ==7 || val ==13) {
    //_C874
	if ([0x0044] == 0) {
	  [0xF80B] &= 0xEF;
	  [0xF804] |= 0x10;
	  [0xF809] |= 0x08;
	  return;
	} else {
	  [0xF847] |= 0x07;
	  [0xF804] |= 0x30;
	  [0xF809] |= 0x18;
	  return;
	}
  } else if(val == 0xF5) {
    [0xFC0B] &= 0xEF;
    return;
  }
}
```

### USB_cmd

Routine memory address 0xC810

```c
void _C810() {
  _A = [0x000B];
  if (_A & (1<<5) != 0) {
    uint8_t R7 = [0x0010];
	if (R7 == 2) {
	  _A = [0xC7DA];
	  if (_A & (1<<0) == 0) {
	    [0x000F] = 0;
		[0x0010] = 4;
	  }
	}
  }
  
  if ([0x000B] & (1<<7) == 0) {
    _A = [0x0012] | [0x0011];
	if (_A) {
	  [0x0022] |= (1<<6);
	  PORT0 |= (1<<6);
	}
  }

  _44BA();
}
```
   

### VSync handler analyze

The ISR that handles the VSync interrupt is located at 0x5FA2. Its logic is simple: if the bit in CommonFlags is set, the user-defined hook at 0xC840 is called; if not, the default handler at 0x5EFF is called.

The default handler performs the following functions:

Checks RAM location 0x003A (1 byte). If it's not 0, it executes the operation, and at the end, 0 is written to that location. If it's 0, the routine exits.

Apparently, this is where the signal indicating that vertical synchronization has been detected is found.

I couldn't find any code that writes anything other than 0 there... perhaps the DMA peripherals do this. 

// Memory cells involved in processing if [0x003A] != 0:

//0x0043 (1 byte) - the value is read from there and the lower two bits are inverted. If the value is not 0 after inversion (the bits were initially set), then branch 1 is executed; if 0, then branch 2.

Pseudocode for handlers and ISRs:

```c
void _5EFF() {
  if ([0x003A] != 0) {
    _A = [0x0043] ^ 0x03;
	if (!_A) {
      [0xFE90] = [0xC67B];
      [0xFE91] = [0xC67D];
      [0xFE93] = [0xC67F];
      [0xFE92] = [0xC681];
	
	} else {
      _6AF5([0xC67B])
      _6AD3([0xC67D])
      _6B17([0xC681])
      _6B39([0xC67F])
	}
	
    [0x0020] |= 1;
    [0x0052] = 0
    [0x0053] = 0
    [0x003A] = 0
  }
}

void _6AF5(uint8_t val) {
  [0xC649] = val;
  _6FF1(val, 0xFB, 0x70); // [0xFB70] = val
  _A = [0xC649];
  [0xC612] = _A;  // actually this is 'val'
  [0xC616] = _A;
  [0xC61A] = _A;
  [0xC61E] = _A;
}

void _6AD3(uint8_t val) {
  [0xC649] = val;
  _6FF1(val, 0xFB, 0x71); // [0xFB71] = val
  _A = [0xC649];
  [0xC613] = _A; // actually this is 'val'
  [0xC617] = _A;
  [0xC61B] = _A;
  [0xC61F] = _A;
}

void _6B17(uint8_t val) {
  [0xC649] = val;
  _6FF1(val, 0xFB, 0x72); // [0xFB72] = val
  _A = [0xC649];
  [0xC614] = _A; // actually this is 'val'
  [0xC618] = _A;
  [0xC61C] = _A;
  [0xC620] = _A;
}

// This subroutine actually writes value v1 to memory [H=v2|L=v3]
void _6FF1(uint8_t v1, uint8_t v2, uint8_t v3) {
  [(uint16_t(v2) << 8) | v3] = v1;
}

// ISR VSYNC handler
void _IE1_0() {
  _SAVE(A B DPR RAM[0x0000-0x0007]); // save state
  _A = [0xC7D8]; // This is CommonFlags value from EEPROM
  if (_A & 0x10) {   // check VSync_int bit in Common flags
    _C840();  // call handler from user code (EEPROM)
  } else {
    [0xF006] = 0;
	[0x0037] = 1;
	_5EFF(); // call default handler
  }
  _RESTORE(RAM[0x0000-0x0007] DPR B A); // restore state
}
```

0xC67B (1 byte) - from this cell value is read in both branches.


## USB_int handler analysis

The ISR is located at address 0x632F. It saves the memory state, calls the subroutine at address 0x40E4, restores it, and exits.

In subroutine 0x40E4:

Data is read from the peripherals at addresses 0x0032 (S1BUF SFR 0x9B), 0x0031 (SFR 0x96), and 0x0033 (SFR 0x97) in RAM.

0x9B is UART, 0x96 and 0x97 are PWM settings.

The user USB_int handler (0xC820) is called if the corresponding bit is set in CommonFlags (0xC7D8). Processing continues.

**Unlike other handlers, the user USB_int handler does not replace the main processing, but rather complements it.**


## Timer_int handler analysis

The ISR is located at ROM address 0x5BC8.
If a user handler is installed and the corresponding bit in CommonFlags is set, it will be called (0xC830) and will override the main processing.

If a user handler is not specified, the following actions are performed (they will not be performed if the user has their own handler):

1. Increment the 16-bit counter in RAM [0x0051] (low byte), [0x0050] (high byte)

2. Increment the 16-bit counter in RAM 0x0053 (low), 0x0052 (high)

3. Increment the 16-bit counter in RAM 0x0055 (low), 0x0054 (high)

4. [0xF005] = 0;



## TVD_int handler analysis

The ISR is located at 0x62B1. Its sole function is to call the user hook at 0xC850 if bit 5 in CommonFlags is set.

There is no default handler.



## Memory

0x0013 - HID (8 bytes)

0x0050 - Timer counter (2 bytes)

0x0052 - Timer counter (2 bytes)

0x0054 - Timer counter (2 bytes)


126 - UART baud rate (low byte) - delay value between bits

127 - UART baud rate (high byte) - delay value between bits

GPIO bit 4 unlocks the EEPROM. 0 - unlocked, 1 - locked

The EEPROM is read and written via I2C



...TBD...

