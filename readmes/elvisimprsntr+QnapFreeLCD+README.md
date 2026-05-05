QnapFreeLCD
===========
Original author Dirk Brenken (dibdot@gmail.com)


WARNING
========
This is a beta version, at the time of writing it was only tested on a TS-453A.
https://www.techpowerup.com/review/qnap-ts-453a/

This script is only for QNAP-devices running TrueNAS CORE (stock QNAP firmware is not supported!).

SCOPE
======
This script does (should do ;-) the following:
- read input for LCD status messages from a separate helper script (see sample function library)
- display status messages on LCD panel
- auto-cycling through status messages
- non-blocking manual navigation via LCD front panel buttons between messages
- fully configurable input-, message-,display- cycles & timeouts

REQUIREMENTS
=============
- QNAP device with LCD display & TrueNAS CORE

GET STARTED
============
- Make this script executable (chmod a+x).
- Adjust path & timeout parameters to your needs (see comments for all configurable options below)
- Rename & adjust distributed sample function library script to your needs
- Start this script ...

CHANGELOG
==========
version 0.1: initial test release for TrueNAS CORE

TODO
=====
- Add HD temps
- Add multiple zfs pools

