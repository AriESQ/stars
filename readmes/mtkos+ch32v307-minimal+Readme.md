## ch32v307-minimal

This repository is a companion to my ch32v203-minimal repository. The programs are the same, with minimal changes to make them work on the bigger board. The startup code has been changed
a little, to ensure that the vector table (if present) is always word-aligned. So -march=rv32imac_zicsr (with compressed instructions) can be used throughout. Everything has been tested on
Debian 12 (gcc 12.2) and Debian 13 (gcc 13.2). The picolibc example uses the random number generator (chapter 29 of the manual), which is not present on ch32v203.
