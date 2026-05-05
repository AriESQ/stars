## FREE Embedded Hacking Course [HERE](https://github.com/mytechnotalent/Embedded-Hacking)
### VIDEO PROMO [HERE](https://www.youtube.com/watch?v=aD7X9sXirF8)

<br>

# RP2350 UART Driver
An RP2350 UART driver written entirely in ARM Assembler.

<br>

# Install ARM Toolchain (Windows / RP2350 Cortex-M33)
Official Raspberry Pi guidance for RP2350 ARM recommends the Arm GNU Toolchain from developer.arm.com.

## Official References
- Raspberry Pi Pico SDK quick start: [HERE](https://github.com/raspberrypi/pico-sdk#quick-start-your-own-project)
- Tool downloads (official): [HERE](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)

## Install (PowerShell)
```powershell
$url = "https://developer.arm.com/-/media/Files/downloads/gnu/15.2.rel1/binrel/arm-gnu-toolchain-15.2.rel1-mingw-w64-x86_64-arm-none-eabi.zip"
$zipPath = "$env:TEMP\arm-toolchain-15-x64-win.zip"
$extractPath = "$env:TEMP\arm-extract"
$dest = "$HOME\arm-toolchain-15"

Invoke-WebRequest -Uri $url -OutFile $zipPath
Expand-Archive -LiteralPath $zipPath -DestinationPath $extractPath -Force
Move-Item "$extractPath\arm-gnu-toolchain-*" $dest -Force
Get-ChildItem -Path $dest | Select-Object Name
```

## Add Toolchain To User PATH (PowerShell)
```powershell
$toolBin = "$HOME\arm-toolchain-15\bin"
$currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentUserPath -notlike "*$toolBin*") {
  [Environment]::SetEnvironmentVariable("Path", "$currentUserPath;$toolBin", "User")
}
```

Close and reopen your terminal after updating PATH.

## Verify Toolchain
```powershell
arm-none-eabi-as --version
arm-none-eabi-ld --version
arm-none-eabi-objcopy --version
```

## Build This Project
```powershell
.\build.bat
```

## UART Terminal Setup (PuTTY)
- Speed: 115200
- Data bits: 8
- Stop bits: 1
- Parity: None
- Flow control: None

## UART Wiring (Pico 2 Target)
- GP0 = UART0 TX (target output)
- GP1 = UART0 RX (target input)
- GND must be common between target and USB-UART adapter/debug probe
- Cross wiring is required: adapter TX -> GP1, adapter RX -> GP0

<br>

# Hardware
## Raspberry Pi Pico 2 w/ Header [BUY](https://www.pishop.us/product/raspberry-pi-pico-2-with-header)
## USB A-Male to USB Micro-B Cable [BUY](https://www.pishop.us/product/usb-a-male-to-usb-micro-b-cable-6-inches)
## Raspberry Pi Pico Debug Probe [BUY](https://www.pishop.us/product/raspberry-pi-debug-probe)
## Complete Component Kit for Raspberry Pi [BUY](https://www.pishop.us/product/complete-component-kit-for-raspberry-pi)
## 10pc 25v 1000uF Capacitor [BUY](https://www.amazon.com/Cionyce-Capacitor-Electrolytic-CapacitorsMicrowave/dp/B0B63CCQ2N?th=1)
### 10% PiShop DISCOUNT CODE - KVPE_HS320548_10PC

<br>

# Build
```
.\build.bat
```

<br>

# Clean
```
.\clean.bat
```

<br>

# Tutorial

## Part I — Foundations (Chapters 1–6)

### [Chapter 1: What Is a Computer?](TUTORIAL/CHAPTER-01.md)
- [Introduction](TUTORIAL/CHAPTER-01.md#introduction)
- [The Fetch-Decode-Execute Cycle](TUTORIAL/CHAPTER-01.md#the-fetch-decode-execute-cycle)
- [The Three Core Components](TUTORIAL/CHAPTER-01.md#the-three-core-components)
- [Microcontroller vs Desktop Computer](TUTORIAL/CHAPTER-01.md#microcontroller-vs-desktop-computer)
- [What Is RP2350?](TUTORIAL/CHAPTER-01.md#what-is-rp2350)
- [What Is ARM Cortex-M33?](TUTORIAL/CHAPTER-01.md#what-is-arm-cortex-m33)
- [What Is Assembly Language?](TUTORIAL/CHAPTER-01.md#what-is-assembly-language)
- [Why Learn Assembly?](TUTORIAL/CHAPTER-01.md#why-learn-assembly)
- [What We Will Build](TUTORIAL/CHAPTER-01.md#what-we-will-build)
- [Summary](TUTORIAL/CHAPTER-01.md#summary)

### [Chapter 2: Number Systems — Binary, Hexadecimal, and Decimal](TUTORIAL/CHAPTER-02.md)
- [Introduction](TUTORIAL/CHAPTER-02.md#introduction)
- [Decimal — Base 10](TUTORIAL/CHAPTER-02.md#decimal--base-10)
- [Binary — Base 2](TUTORIAL/CHAPTER-02.md#binary--base-2)
- [Hexadecimal — Base 16](TUTORIAL/CHAPTER-02.md#hexadecimal--base-16)
- [The 0x Prefix](TUTORIAL/CHAPTER-02.md#the-0x-prefix)
- [Bit Numbering](TUTORIAL/CHAPTER-02.md#bit-numbering)
- [Common Bit Patterns in Our Firmware](TUTORIAL/CHAPTER-02.md#common-bit-patterns-in-our-firmware)
- [Two's Complement — Signed Numbers](TUTORIAL/CHAPTER-02.md#twos-complement--signed-numbers)
- [Data Sizes on ARM Cortex-M33](TUTORIAL/CHAPTER-02.md#data-sizes-on-arm-cortex-m33)
- [Summary](TUTORIAL/CHAPTER-02.md#summary)

### [Chapter 3: Memory — Addresses, Bytes, Words, and Endianness](TUTORIAL/CHAPTER-03.md)
- [Introduction](TUTORIAL/CHAPTER-03.md#introduction)
- [The Address Space](TUTORIAL/CHAPTER-03.md#the-address-space)
- [Bytes, Halfwords, and Words](TUTORIAL/CHAPTER-03.md#bytes-halfwords-and-words)
- [Alignment](TUTORIAL/CHAPTER-03.md#alignment)
- [Little-Endian Byte Order](TUTORIAL/CHAPTER-03.md#little-endian-byte-order)
- [Memory-Mapped Registers](TUTORIAL/CHAPTER-03.md#memory-mapped-registers)
- [The Stack](TUTORIAL/CHAPTER-03.md#the-stack)
- [Flash Memory (XIP)](TUTORIAL/CHAPTER-03.md#flash-memory-xip)
- [SRAM](TUTORIAL/CHAPTER-03.md#sram)
- [Reading the Address Map](TUTORIAL/CHAPTER-03.md#reading-the-address-map)
- [Summary](TUTORIAL/CHAPTER-03.md#summary)

### [Chapter 4: What Is a Register?](TUTORIAL/CHAPTER-04.md)
- [Introduction](TUTORIAL/CHAPTER-04.md#introduction)
- [The ARM Cortex-M33 Register File](TUTORIAL/CHAPTER-04.md#the-arm-cortex-m33-register-file)
- [Registers r0-r3: Arguments and Scratch](TUTORIAL/CHAPTER-04.md#registers-r0-r3-arguments-and-scratch)
- [Registers r4-r11: Callee-Saved](TUTORIAL/CHAPTER-04.md#registers-r4-r11-callee-saved)
- [Register r12 (IP): Intra-Procedure Scratch](TUTORIAL/CHAPTER-04.md#register-r12-ip-intra-procedure-scratch)
- [Register r13 (SP): Stack Pointer](TUTORIAL/CHAPTER-04.md#register-r13-sp-stack-pointer)
- [Register r14 (LR): Link Register](TUTORIAL/CHAPTER-04.md#register-r14-lr-link-register)
- [Register r15 (PC): Program Counter](TUTORIAL/CHAPTER-04.md#register-r15-pc-program-counter)
- [Special Registers](TUTORIAL/CHAPTER-04.md#special-registers)
- [The Program Status Register (xPSR)](TUTORIAL/CHAPTER-04.md#the-program-status-register-xpsr)
- [Register Usage in Our Firmware](TUTORIAL/CHAPTER-04.md#register-usage-in-our-firmware)
- [Summary](TUTORIAL/CHAPTER-04.md#summary)

### [Chapter 5: Load-Store Architecture — How ARM Accesses Memory](TUTORIAL/CHAPTER-05.md)
- [Introduction](TUTORIAL/CHAPTER-05.md#introduction)
- [Why Load-Store?](TUTORIAL/CHAPTER-05.md#why-load-store)
- [The Load Instruction: ldr](TUTORIAL/CHAPTER-05.md#the-load-instruction-ldr)
- [The Store Instruction: str](TUTORIAL/CHAPTER-05.md#the-store-instruction-str)
- [The Load-Modify-Store Pattern](TUTORIAL/CHAPTER-05.md#the-load-modify-store-pattern)
- [Byte and Halfword Access](TUTORIAL/CHAPTER-05.md#byte-and-halfword-access)
- [Push and Pop](TUTORIAL/CHAPTER-05.md#push-and-pop)
- [Memory Access in Our Firmware](TUTORIAL/CHAPTER-05.md#memory-access-in-our-firmware)
- [Summary](TUTORIAL/CHAPTER-05.md#summary)

### [Chapter 6: The Fetch-Decode-Execute Cycle in Detail](TUTORIAL/CHAPTER-06.md)
- [Introduction](TUTORIAL/CHAPTER-06.md#introduction)
- [The Three Stages](TUTORIAL/CHAPTER-06.md#the-three-stages)
- [The Pipeline](TUTORIAL/CHAPTER-06.md#the-pipeline)
- [A Concrete Example](TUTORIAL/CHAPTER-06.md#a-concrete-example)
- [How Branch Instructions Affect the Pipeline](TUTORIAL/CHAPTER-06.md#how-branch-instructions-affect-the-pipeline)
- [The Cortex-M33 Execution Model](TUTORIAL/CHAPTER-06.md#the-cortex-m33-execution-model)
- [Clock Speed](TUTORIAL/CHAPTER-06.md#clock-speed)
- [Summary](TUTORIAL/CHAPTER-06.md#summary)

## Part II — The ARM Instruction Set (Chapters 7–12)

### [Chapter 7: ARM Cortex-M33 ISA Overview](TUTORIAL/CHAPTER-07.md)
- [Introduction](TUTORIAL/CHAPTER-07.md#introduction)
- [The ARM Design Philosophy](TUTORIAL/CHAPTER-07.md#the-arm-design-philosophy)
- [Thumb-2 Instruction Encoding](TUTORIAL/CHAPTER-07.md#thumb-2-instruction-encoding)
- [Instruction Categories](TUTORIAL/CHAPTER-07.md#instruction-categories)
- [Instruction Encoding Formats](TUTORIAL/CHAPTER-07.md#instruction-encoding-formats)
- [Instructions Used in Our Firmware](TUTORIAL/CHAPTER-07.md#instructions-used-in-our-firmware)
- [Summary](TUTORIAL/CHAPTER-07.md#summary)

### [Chapter 8: ARM Immediate and Move Instructions](TUTORIAL/CHAPTER-08.md)
- [Introduction](TUTORIAL/CHAPTER-08.md#introduction)
- [The mov Instruction](TUTORIAL/CHAPTER-08.md#the-mov-instruction)
- [The ldr Pseudo-Instruction](TUTORIAL/CHAPTER-08.md#the-ldr-pseudo-instruction)
- [The ldr Immediate Instruction](TUTORIAL/CHAPTER-08.md#the-ldr-immediate-instruction)
- [Immediate Encoding in Thumb-2](TUTORIAL/CHAPTER-08.md#immediate-encoding-in-thumb-2)
- [Constants in Our Firmware](TUTORIAL/CHAPTER-08.md#constants-in-our-firmware)
- [The add and sub Immediates](TUTORIAL/CHAPTER-08.md#the-add-and-sub-immediates)
- [Summary](TUTORIAL/CHAPTER-08.md#summary)

### [Chapter 9: ARM Arithmetic and Logic Instructions](TUTORIAL/CHAPTER-09.md)
- [Introduction](TUTORIAL/CHAPTER-09.md#introduction)
- [Arithmetic Instructions](TUTORIAL/CHAPTER-09.md#arithmetic-instructions)
- [Logic Instructions](TUTORIAL/CHAPTER-09.md#logic-instructions)
- [Shift Instructions](TUTORIAL/CHAPTER-09.md#shift-instructions)
- [The Suffix 's' — Flag Updates](TUTORIAL/CHAPTER-09.md#the-suffix-s--flag-updates)
- [The Read-Modify-Write Pattern](TUTORIAL/CHAPTER-09.md#the-read-modify-write-pattern)
- [Summary](TUTORIAL/CHAPTER-09.md#summary)

### [Chapter 10: ARM Memory Access Instructions — Load and Store Deep Dive](TUTORIAL/CHAPTER-10.md)
- [Introduction](TUTORIAL/CHAPTER-10.md#introduction)
- [ldr — Load Register](TUTORIAL/CHAPTER-10.md#ldr--load-register)
- [str — Store Register](TUTORIAL/CHAPTER-10.md#str--store-register)
- [push and pop — Stack Operations](TUTORIAL/CHAPTER-10.md#push-and-pop--stack-operations)
- [Addressing Modes](TUTORIAL/CHAPTER-10.md#addressing-modes)
- [Memory Access Sizes](TUTORIAL/CHAPTER-10.md#memory-access-sizes)
- [Memory Access in Hardware Configuration](TUTORIAL/CHAPTER-10.md#memory-access-in-hardware-configuration)
- [The Polling Loop Pattern](TUTORIAL/CHAPTER-10.md#the-polling-loop-pattern)
- [Summary](TUTORIAL/CHAPTER-10.md#summary)

### [Chapter 11: ARM Branch Instructions](TUTORIAL/CHAPTER-11.md)
- [Introduction](TUTORIAL/CHAPTER-11.md#introduction)
- [Unconditional Branch: b](TUTORIAL/CHAPTER-11.md#unconditional-branch-b)
- [Branch with Link: bl](TUTORIAL/CHAPTER-11.md#branch-with-link-bl)
- [Branch Exchange: bx](TUTORIAL/CHAPTER-11.md#branch-exchange-bx)
- [Condition Flags](TUTORIAL/CHAPTER-11.md#condition-flags)
- [Conditional Branches](TUTORIAL/CHAPTER-11.md#conditional-branches)
- [Branches Used in Our Firmware](TUTORIAL/CHAPTER-11.md#branches-used-in-our-firmware)
- [Polling Loops](TUTORIAL/CHAPTER-11.md#polling-loops)
- [Branch Range](TUTORIAL/CHAPTER-11.md#branch-range)
- [Summary](TUTORIAL/CHAPTER-11.md#summary)

### [Chapter 12: ARM Jumps, Calls, and Returns](TUTORIAL/CHAPTER-12.md)
- [Introduction](TUTORIAL/CHAPTER-12.md#introduction)
- [The bl Instruction — Function Call](TUTORIAL/CHAPTER-12.md#the-bl-instruction--function-call)
- [The bx lr Instruction — Function Return](TUTORIAL/CHAPTER-12.md#the-bx-lr-instruction--function-return)
- [The Complete Call/Return Sequence](TUTORIAL/CHAPTER-12.md#the-complete-callreturn-sequence)
- [The Problem: Nested Calls](TUTORIAL/CHAPTER-12.md#the-problem-nested-calls)
- [The Solution: push/pop](TUTORIAL/CHAPTER-12.md#the-solution-pushpop)
- [Leaf Functions vs Non-Leaf Functions](TUTORIAL/CHAPTER-12.md#leaf-functions-vs-non-leaf-functions)
- [The Call Graph](TUTORIAL/CHAPTER-12.md#the-call-graph)
- [The Thumb Bit](TUTORIAL/CHAPTER-12.md#the-thumb-bit)
- [Summary](TUTORIAL/CHAPTER-12.md#summary)

## Part III — Assembly Programming (Chapters 13–17)

### [Chapter 13: Pseudo-Instructions — What the Assembler Does For You](TUTORIAL/CHAPTER-13.md)
- [Introduction](TUTORIAL/CHAPTER-13.md#introduction)
- [ldr r0, =value — Load Constant](TUTORIAL/CHAPTER-13.md#ldr-r0-value--load-constant)
- [.equ — Define a Constant Symbol](TUTORIAL/CHAPTER-13.md#equ--define-a-constant-symbol)
- [.include — Include Another File](TUTORIAL/CHAPTER-13.md#include--include-another-file)
- [.global — Export a Symbol](TUTORIAL/CHAPTER-13.md#global--export-a-symbol)
- [.type — Declare Symbol Type](TUTORIAL/CHAPTER-13.md#type--declare-symbol-type)
- [.size — Declare Symbol Size](TUTORIAL/CHAPTER-13.md#size--declare-symbol-size)
- [.word — Emit a 32-bit Constant](TUTORIAL/CHAPTER-13.md#word--emit-a-32-bit-constant)
- [.byte / .hword — Emit Smaller Constants](TUTORIAL/CHAPTER-13.md#byte--hword--emit-smaller-constants)
- [Pseudo-Instructions vs Directives](TUTORIAL/CHAPTER-13.md#pseudo-instructions-vs-directives)
- [Summary](TUTORIAL/CHAPTER-13.md#summary)

### [Chapter 14: Assembler Directives — Controlling the Assembly Process](TUTORIAL/CHAPTER-14.md)
- [Introduction](TUTORIAL/CHAPTER-14.md#introduction)
- [.syntax unified](TUTORIAL/CHAPTER-14.md#syntax-unified)
- [.cpu cortex-m33](TUTORIAL/CHAPTER-14.md#cpu-cortex-m33)
- [.thumb](TUTORIAL/CHAPTER-14.md#thumb)
- [.section — Define Output Section](TUTORIAL/CHAPTER-14.md#section--define-output-section)
- [.align — Alignment](TUTORIAL/CHAPTER-14.md#align--alignment)
- [.equ — Define a Constant](TUTORIAL/CHAPTER-14.md#equ--define-a-constant)
- [.global — Export Symbol](TUTORIAL/CHAPTER-14.md#global--export-symbol)
- [.type — Symbol Type](TUTORIAL/CHAPTER-14.md#type--symbol-type)
- [.size — Symbol Size](TUTORIAL/CHAPTER-14.md#size--symbol-size)
- [.word — Emit 32-bit Value](TUTORIAL/CHAPTER-14.md#word--emit-32-bit-value)
- [.byte / .hword — Emit Smaller Values](TUTORIAL/CHAPTER-14.md#byte--hword--emit-smaller-values)
- [.include — File Inclusion](TUTORIAL/CHAPTER-14.md#include--file-inclusion)
- [KEEP in Linker Context](TUTORIAL/CHAPTER-14.md#keep-in-linker-context)
- [Summary of All Directives Used](TUTORIAL/CHAPTER-14.md#summary-of-all-directives-used)
- [Summary](TUTORIAL/CHAPTER-14.md#summary)

### [Chapter 15: The Calling Convention and Stack Frames](TUTORIAL/CHAPTER-15.md)
- [Introduction](TUTORIAL/CHAPTER-15.md#introduction)
- [The ARM AAPCS Calling Convention](TUTORIAL/CHAPTER-15.md#the-arm-aapcs-calling-convention)
- [Caller-Saved Registers: r0-r3, r12](TUTORIAL/CHAPTER-15.md#caller-saved-registers-r0-r3-r12)
- [Callee-Saved Registers: r4-r11](TUTORIAL/CHAPTER-15.md#callee-saved-registers-r4-r11)
- [The Stack Frame](TUTORIAL/CHAPTER-15.md#the-stack-frame)
- [Function Prologue and Epilogue](TUTORIAL/CHAPTER-15.md#function-prologue-and-epilogue)
- [Leaf vs Non-Leaf Functions](TUTORIAL/CHAPTER-15.md#leaf-vs-non-leaf-functions)
- [Our Firmware's Functions](TUTORIAL/CHAPTER-15.md#our-firmwares-functions)
- [Summary](TUTORIAL/CHAPTER-15.md#summary)

### [Chapter 16: Bitwise Operations for Hardware Programming](TUTORIAL/CHAPTER-16.md)
- [Introduction](TUTORIAL/CHAPTER-16.md#introduction)
- [The Bit Manipulation Toolkit](TUTORIAL/CHAPTER-16.md#the-bit-manipulation-toolkit)
- [Setting a Bit: orr](TUTORIAL/CHAPTER-16.md#setting-a-bit-orr)
- [Clearing a Bit: bic](TUTORIAL/CHAPTER-16.md#clearing-a-bit-bic)
- [Testing a Bit: tst](TUTORIAL/CHAPTER-16.md#testing-a-bit-tst)
- [Isolating Bits: ands](TUTORIAL/CHAPTER-16.md#isolating-bits-ands)
- [Masking Multiple Bits](TUTORIAL/CHAPTER-16.md#masking-multiple-bits)
- [The Read-Modify-Write Pattern](TUTORIAL/CHAPTER-16.md#the-read-modify-write-pattern)
- [Shift for Bit Position](TUTORIAL/CHAPTER-16.md#shift-for-bit-position)
- [Shifting Values into Position](TUTORIAL/CHAPTER-16.md#shifting-values-into-position)
- [Clearing a Bit Field](TUTORIAL/CHAPTER-16.md#clearing-a-bit-field)
- [Summary](TUTORIAL/CHAPTER-16.md#summary)

### [Chapter 17: Memory-Mapped I/O — Controlling Hardware Through Addresses](TUTORIAL/CHAPTER-17.md)
- [Introduction](TUTORIAL/CHAPTER-17.md#introduction)
- [How Memory-Mapped I/O Works](TUTORIAL/CHAPTER-17.md#how-memory-mapped-io-works)
- [Reading vs Writing Peripheral Registers](TUTORIAL/CHAPTER-17.md#reading-vs-writing-peripheral-registers)
- [The RP2350 Peripheral Address Map](TUTORIAL/CHAPTER-17.md#the-rp2350-peripheral-address-map)
- [UART0 Register Map](TUTORIAL/CHAPTER-17.md#uart0-register-map)
- [Volatile Behavior](TUTORIAL/CHAPTER-17.md#volatile-behavior)
- [Atomic Aliases](TUTORIAL/CHAPTER-17.md#atomic-aliases)
- [Why Not Use Special I/O Instructions?](TUTORIAL/CHAPTER-17.md#why-not-use-special-io-instructions)
- [Barriers: dsb and isb](TUTORIAL/CHAPTER-17.md#barriers-dsb-and-isb)
- [Summary](TUTORIAL/CHAPTER-17.md#summary)

## Part IV — RP2350 Hardware (Chapter 18)

### [Chapter 18: The RP2350 Microcontroller — Architecture and Hardware](TUTORIAL/CHAPTER-18.md)
- [Introduction](TUTORIAL/CHAPTER-18.md#introduction)
- [RP2350 Block Diagram](TUTORIAL/CHAPTER-18.md#rp2350-block-diagram)
- [The ARM Cortex-M33 Core](TUTORIAL/CHAPTER-18.md#the-arm-cortex-m33-core)
- [Memory Map](TUTORIAL/CHAPTER-18.md#memory-map)
- [The Bus Fabric](TUTORIAL/CHAPTER-18.md#the-bus-fabric)
- [The Reset Controller](TUTORIAL/CHAPTER-18.md#the-reset-controller)
- [The Clock System](TUTORIAL/CHAPTER-18.md#the-clock-system)
- [The XOSC (Crystal Oscillator)](TUTORIAL/CHAPTER-18.md#the-xosc-crystal-oscillator)
- [UART0 Peripheral](TUTORIAL/CHAPTER-18.md#uart0-peripheral)
- [GPIO and Pin Multiplexing](TUTORIAL/CHAPTER-18.md#gpio-and-pin-multiplexing)
- [The Coprocessor Interface](TUTORIAL/CHAPTER-18.md#the-coprocessor-interface)
- [The Boot Process](TUTORIAL/CHAPTER-18.md#the-boot-process)
- [The Vector Table](TUTORIAL/CHAPTER-18.md#the-vector-table)
- [Summary](TUTORIAL/CHAPTER-18.md#summary)

## Part V — Build System (Chapters 19–20)

### [Chapter 19: The Linker Script — Placing Code in Memory](TUTORIAL/CHAPTER-19.md)
- [Introduction](TUTORIAL/CHAPTER-19.md#introduction)
- [Our Linker Script: linker.ld](TUTORIAL/CHAPTER-19.md#our-linker-script-linkerld)
- [Line-by-Line Explanation](TUTORIAL/CHAPTER-19.md#line-by-line-explanation)
- [The Memory Layout](TUTORIAL/CHAPTER-19.md#the-memory-layout)
- [Summary](TUTORIAL/CHAPTER-19.md#summary)

### [Chapter 20: The Build Pipeline — From Assembly to UF2](TUTORIAL/CHAPTER-20.md)
- [Introduction](TUTORIAL/CHAPTER-20.md#introduction)
- [Our Build Script: build.bat](TUTORIAL/CHAPTER-20.md#our-build-script-buildbat)
- [Stage 1: Assembly](TUTORIAL/CHAPTER-20.md#stage-1-assembly)
- [Stage 2: Linking](TUTORIAL/CHAPTER-20.md#stage-2-linking)
- [Stage 3: Binary Extraction](TUTORIAL/CHAPTER-20.md#stage-3-binary-extraction)
- [Stage 4: UF2 Conversion](TUTORIAL/CHAPTER-20.md#stage-4-uf2-conversion)
- [The Complete Flow](TUTORIAL/CHAPTER-20.md#the-complete-flow)
- [Cleaning](TUTORIAL/CHAPTER-20.md#cleaning)
- [The Family ID: 0xe48bff59](TUTORIAL/CHAPTER-20.md#the-family-id-0xe48bff59)
- [Summary](TUTORIAL/CHAPTER-20.md#summary)

## Part VI — Source Code Walkthroughs (Chapters 21–29)

### [Chapter 21: image_def.s — The PICOBIN Block Byte by Byte](TUTORIAL/CHAPTER-21.md)
- [Introduction](TUTORIAL/CHAPTER-21.md#introduction)
- [Full Source: image_def.s](TUTORIAL/CHAPTER-21.md#full-source-image_defs)
- [Line-by-Line Walkthrough](TUTORIAL/CHAPTER-21.md#line-by-line-walkthrough)
- [The Complete Block in Memory](TUTORIAL/CHAPTER-21.md#the-complete-block-in-memory)
- [Why Secure Mode?](TUTORIAL/CHAPTER-21.md#why-secure-mode)
- [Summary](TUTORIAL/CHAPTER-21.md#summary)

### [Chapter 22: constants.s — Every .equ Definition Explained](TUTORIAL/CHAPTER-22.md)
- [Introduction](TUTORIAL/CHAPTER-22.md#introduction)
- [Full Source: constants.s](TUTORIAL/CHAPTER-22.md#full-source-constantss)
- [Line-by-Line Walkthrough](TUTORIAL/CHAPTER-22.md#line-by-line-walkthrough)
- [How .equ Works](TUTORIAL/CHAPTER-22.md#how-equ-works)
- [The .include Mechanism](TUTORIAL/CHAPTER-22.md#the-include-mechanism)
- [Summary](TUTORIAL/CHAPTER-22.md#summary)

### [Chapter 23: stack.s and vector_table.s — Stack Initialization and the Vector Table](TUTORIAL/CHAPTER-23.md)
- [Introduction](TUTORIAL/CHAPTER-23.md#introduction)
- [Part 1: vector_table.s](TUTORIAL/CHAPTER-23.md#part-1-vector_tables)
- [Part 2: stack.s](TUTORIAL/CHAPTER-23.md#part-2-stacks)
- [Summary](TUTORIAL/CHAPTER-23.md#summary)

### [Chapter 24: reset_handler.s — The Boot Sequence Line by Line](TUTORIAL/CHAPTER-24.md)
- [Introduction](TUTORIAL/CHAPTER-24.md#introduction)
- [Full Source: reset_handler.s](TUTORIAL/CHAPTER-24.md#full-source-reset_handlers)
- [Line-by-Line Walkthrough](TUTORIAL/CHAPTER-24.md#line-by-line-walkthrough)
- [The Boot Sequence Diagram](TUTORIAL/CHAPTER-24.md#the-boot-sequence-diagram)
- [Why Order Matters](TUTORIAL/CHAPTER-24.md#why-order-matters)
- [Summary](TUTORIAL/CHAPTER-24.md#summary)

### [Chapter 25: xosc.s — Crystal Oscillator Initialization](TUTORIAL/CHAPTER-25.md)
- [Introduction](TUTORIAL/CHAPTER-25.md#introduction)
- [Full Source: xosc.s](TUTORIAL/CHAPTER-25.md#full-source-xoscs)
- [Function 1: Init_XOSC](TUTORIAL/CHAPTER-25.md#function-1-init_xosc)
- [Function 2: Enable_XOSC_Peri_Clock](TUTORIAL/CHAPTER-25.md#function-2-enable_xosc_peri_clock)
- [Clock Path Diagram](TUTORIAL/CHAPTER-25.md#clock-path-diagram)
- [Why XOSC Matters for UART](TUTORIAL/CHAPTER-25.md#why-xosc-matters-for-uart)
- [Summary](TUTORIAL/CHAPTER-25.md#summary)

### [Chapter 26: reset.s — Releasing IO_BANK0 from Reset](TUTORIAL/CHAPTER-26.md)
- [Introduction](TUTORIAL/CHAPTER-26.md#introduction)
- [Full Source: reset.s](TUTORIAL/CHAPTER-26.md#full-source-resets)
- [Line-by-Line Walkthrough](TUTORIAL/CHAPTER-26.md#line-by-line-walkthrough)
- [The RP2350 Reset Controller](TUTORIAL/CHAPTER-26.md#the-rp2350-reset-controller)
- [Why Not Release Everything at Once?](TUTORIAL/CHAPTER-26.md#why-not-release-everything-at-once)
- [The Atomic Clear Alternative](TUTORIAL/CHAPTER-26.md#the-atomic-clear-alternative)
- [Summary](TUTORIAL/CHAPTER-26.md#summary)

### [Chapter 27: uart.s Part 1 — UART_Release_Reset and UART_Init](TUTORIAL/CHAPTER-27.md)
- [Introduction](TUTORIAL/CHAPTER-27.md#introduction)
- [Function 1: UART_Release_Reset](TUTORIAL/CHAPTER-27.md#function-1-uart_release_reset)
- [Function 2: UART_Init](TUTORIAL/CHAPTER-27.md#function-2-uart_init)
- [UART Register Map Summary](TUTORIAL/CHAPTER-27.md#uart-register-map-summary)
- [Summary](TUTORIAL/CHAPTER-27.md#summary)

### [Chapter 28: uart.s Part 2 — UART0_Out and UART0_In](TUTORIAL/CHAPTER-28.md)
- [Introduction](TUTORIAL/CHAPTER-28.md#introduction)
- [Function 1: UART0_Out (Transmit)](TUTORIAL/CHAPTER-28.md#function-1-uart0_out-transmit)
- [Function 2: UART0_In (Receive)](TUTORIAL/CHAPTER-28.md#function-2-uart0_in-receive)
- [Register Usage Comparison](TUTORIAL/CHAPTER-28.md#register-usage-comparison)
- [The Polling Pattern](TUTORIAL/CHAPTER-28.md#the-polling-pattern)
- [Data Flow Through the UART](TUTORIAL/CHAPTER-28.md#data-flow-through-the-uart)
- [Summary](TUTORIAL/CHAPTER-28.md#summary)

### [Chapter 29: main.s — The Echo Loop](TUTORIAL/CHAPTER-29.md)
- [Introduction](TUTORIAL/CHAPTER-29.md#introduction)
- [Full Source: main.s](TUTORIAL/CHAPTER-29.md#full-source-mains)
- [Line-by-Line Walkthrough](TUTORIAL/CHAPTER-29.md#line-by-line-walkthrough)
- [The Complete Execution Flow](TUTORIAL/CHAPTER-29.md#the-complete-execution-flow)
- [What Makes This a Complete Firmware](TUTORIAL/CHAPTER-29.md#what-makes-this-a-complete-firmware)
- [Summary](TUTORIAL/CHAPTER-29.md#summary)

## Part VII — Full Integration (Chapter 30)

### [Chapter 30: Full Integration — From Power-On to Echo](TUTORIAL/CHAPTER-30.md)
- [Introduction](TUTORIAL/CHAPTER-30.md#introduction)
- [The Files](TUTORIAL/CHAPTER-30.md#the-files)
- [Phase 1: Build](TUTORIAL/CHAPTER-30.md#phase-1-build)
- [Phase 2: Flash](TUTORIAL/CHAPTER-30.md#phase-2-flash)
- [Phase 3: Boot ROM](TUTORIAL/CHAPTER-30.md#phase-3-boot-rom)
- [Phase 4: Hardware Reset Sequence](TUTORIAL/CHAPTER-30.md#phase-4-hardware-reset-sequence)
- [Phase 5: Reset_Handler](TUTORIAL/CHAPTER-30.md#phase-5-reset_handler)
- [Phase 6: The Echo Loop (main.s)](TUTORIAL/CHAPTER-30.md#phase-6-the-echo-loop-mains)
- [The Complete Address Map](TUTORIAL/CHAPTER-30.md#the-complete-address-map)
- [What We Built](TUTORIAL/CHAPTER-30.md#what-we-built)

<br>

# main.s Code
```
/**
 * FILE: main.s
 *
 * DESCRIPTION:
 * RP2350 Bare-Metal UART Main Application.
 * 
 * BRIEF:
 * Main application entry point for RP2350 UART driver. Contains the
 * main loop that echoes UART input to output.
 *
 * AUTHOR: Kevin Thomas
 * CREATION DATE: November 2, 2025
 * UPDATE DATE: November 27, 2025
 */

.syntax unified                                  // use unified assembly syntax
.cpu cortex-m33                                  // target Cortex-M33 core
.thumb                                           // use Thumb instruction set

.include "constants.s"

/**
 * Initialize the .text section. 
 * The .text section contains executable code.
 */
.section .text                                   // code section
.align 2                                         // align to 4-byte boundary

/**
 * @brief   Main application entry point.
 *
 * @details Implements the infinite blink loop.
 *
 * @param   None
 * @retval  None
 */
.global main                                     // export main
.type main, %function                            // mark as function
main:
.Push_Registers:
  push  {r4-r12, lr}                             // push registers r4-r12, lr to the stack
.Loop:
  bl    UART0_In                                 // call UART0_In
  bl    UART0_Out                                // call UART0_Out
  b     .Loop                                    // loop forever
.Pop_Registers:
  pop   {r4-r12, lr}                             // pop registers r4-r12, lr from the stack
  bx    lr                                       // return to caller

/**
 * Test data and constants.
 * The .rodata section is used for constants and static data.
 */
.section .rodata                                 // read-only data section

/**
 * Initialized global data.
 * The .data section is used for initialized global or static variables.
 */
.section .data                                   // data section

/**
 * Uninitialized global data.
 * The .bss section is used for uninitialized global or static variables.
 */
.section .bss                                    // BSS section
```

<br>

# License
[Apache License 2.0](https://github.com/mytechnotalent/RP2350_UART_Driver/blob/main/LICENSE)
