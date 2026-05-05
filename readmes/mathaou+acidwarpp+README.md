# Acidwarpp

#### What is Acidwarp?

https://github.com/mathaou/acidwarpp/assets/16282787/d0bc06b8-a8eb-4893-993e-37198a2ad68e

---

"Acidwarp is an eye candy program which displays various patterns and animates them by changing the palette."

This is a C++ SDL2 port of Acidwarp with ImGui for a user interface. Acidwarp was originally written for MS-DOS by Noah Spurrier, then was ported by Steven Willis and Boris Gjenero. Then finally myself.

This README and this codebase are both based on [Boris' port](https://github.com/dreamlayers/acidwarp).

#### Using the program

---

Use the following keys to control the program:

| Key | Action |
| --- | ---    |
| Up | Rotate palette faster |
| Down | Rotate palette slower |
| l | (L)ock: stay on current pattern, but keep changing palette |
| k | switch to the next pallette |
| p | (P)ause: totally stops pallette rotation and pattern changing. |
| q | (Q)uit: causes Acidwarp to exit |
| n | (N)ext pattern |
| g | Toggle (G)UI |

CTRL+C to quit also works.

---

TODO:

1. Fullscreen toggle is busted so just fullscreen for now
2. List clicking pattern is weird in GUI; you need to double click for it to work.

---

#### Building the Program

If you have CMake installed you should be good to go. I developed in Visual Studio 2022 and had no problems compiling and developing.

---

#### Original README

Originial authors website:

The original author's site about Acidwarp: http://www.noah.org/acidwarp/

For historical reasons, here's the original README:

```
Acidwarp for Linux 1.0 by Steven Wills <willssl@jmu.edu>

What is this?

This is a linux port of the popular dos program Acidwarp.  Acidwarp is a
program that makes neat looking pictures and rotates the palette. Its only
use is for entertainment, but it is neat. I stumbled upon source code for
Acidwarp on the net one day, and decided that it was high time someone
ported it to linux. So, here it is. (for more info about Acidwarp, see 
the README for the dos version, included below)

I used gcc 2.7.2, svgalib 1.2.10 and libc 5.2.18.  I added an option to
use higher resolution and control the rate of palette rotation. I did not
impliment the option to select which palette is used.  This port was done 
on intel hardware, but I suspect that it will work on others. This is 
the second public release of the linux version, and it has been fairly
well tested. Still, please let me know if you discover any bugs, or if you
just want to offer feedback. Thanks. 

In this version I have added a few more features. These are mostly
keyboard commands. They are:

  Up: causes the pallette to rotate faster.
Down: causes the pallette to rotate slower.
   l: (L)ock on the current pattern.
   k: switch to the next pallette.
   p: (P)ause. Totally stops pallette rotation and pattern changing.
   q: (Q)uit. Causes Acidwarp to exit.
   n: (N)ext pattern.

Acidwarp is distributed under the GPL.

/* The README for the dos version follows */

Acid Warp V4.2 By Noah Spurrier

This is Acid Warp for DOS. It's an eye-candy program. Run it and watch the
pretty colors. Each picture is the graphic representation of a mathematical
function. All math is done with integer approximations so Acid Warp should
be pretty fast even on machines without a math chip. It might take as long
as 30 to 40 seconds to generate each picture on a slow machine.

I added a few new picture functions (now there are over 40) and I improved
the color palettes so that they seem more hypnotic. Don't forget to try
Acid Warp with the "p8" option. This forces all the pictures to be very
trippy. The default is to mix mellow and trippy pictures. Also don't forget
the "w" option which displays a document that describes how to turn your
monitor into a wall projector for Acid Warp.

Sorry this version took so long. I didn't expect people to like Acid Warp
so much. I had a lot of help from Mark Bilk in fixing this code up. He pretty
much redid all the interrupt routines so they should be more stable now and
he figured out how to get rid of the screen flicker that annoyed about 1/3
of the VGA cards that we tried it on. This was the biggest complaint about
the old version. It should be fixed now. Hooray!

Sorry, but the make file is in a bit of a mess. The VC++70.MAK file
should work for older versions of Visual C++, but I have not had the chance
to test it. This source was written for Turbo C, then for Microsoft C++ 7.0.
I have not bothered to convert it to VC++ 2.2.
All the source files should be in a readable condition.

This is free software, but if you happen to have any weird information to
send me as a token of your appreciation then mail it to "noah@noah.org".
I'd really like a copy of Amanda Fielding's film on Trepanning called
"Heartbeat in the Brain". 
```
