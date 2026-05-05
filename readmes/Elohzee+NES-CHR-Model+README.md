
# NES-CHR-Model
This library is an offshoot project from my all in one NES ROM hacking program. It allows you to load, write to, and save CHR data to *.chr  and *.nes ROM files.

## Usage

To load a CHR Model, you will need to create a CHRModel object. It will default to a new 4kb CHR. However, you can provide it with access to external files by passing a string into the constructor upon creation. The CHR data will be automatically loaded when the object is created. Index (0-3) refers to which of the NES' 4 available colors is intended to be displayed. You can use WritePixel(x, y, index); to write an individual pixel to the index array. When writing, keep in mind that NES CHR is always 128px wide, so that is the maximum x value. If you exceed this, it will simply wrap to the next row. You can save the file with SaveCHR(filename); which will output the index array to the file that is passed through (as string). You can load and edit both  *.chr  and *.nes ROM files.

## Example:
```C++
#include "CHRModel.h"

CHRModel blankCHR; //creates a blank 4kb CHR
CHRModel 8kbCHR = CHRModel(8192);
CHRModel lozCHR = CHRModel("Legend_Of_Zelda.chr"); //opens existing CHR

int main()
{
  lozCHR.WritePixel(133, 46, 2); //writes index of 2 to (133, 46)
  lozCHR.SaveCHR("Legend_Of_Zelda.chr"); //saves to Legend_Of_Zelda.chr;
  8kbCHR.WritePixel(60, 90, 3); //writes index of 3 to (60, 90)
  8kbCHR.SaveCHR("new.chr"); //creates a new file called "new.chr" and saves the CHR data there
  return 0;
}
```

## Special thanks
b0b_d0e, studsX
