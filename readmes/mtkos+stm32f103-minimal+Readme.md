## stm32f103-minimal

My ch32v003-minimal repository shows how to program the risc-v ch32v003 microcontroller without using proprietary software. The present repository does the same for the ARM-based STM32F103.
The differences are explained in the Readme files of the programs.

The following documentation has been used, in addtion to the architecture-independent resources used in the ch32v003-minimal repository:

[Cortex-M3] Cortex-M3 Devices Generic User Guide. Can be obtained from <https://developer.arm.com/documentation/dui0552/latest/>.

[ARMv7-M] The Arm v7-M Architecture Reference Manual. Can be obtained from <https://developer.arm.com/documentation/ddi0403/latest>. 

[RM0008] The STM32F103 reference manual. Can be obtained from <https://www.st.com/resource/en/reference_manual/rm0008-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf>.

The first two of these contain information about core peripherals like the NVIC interrupt controller and SysTick.
