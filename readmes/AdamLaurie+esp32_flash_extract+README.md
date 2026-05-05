# esp32_flash_extract

This quick and dirty code extracts the contents of a binary file created by reading out the flash from block 0 via the bootloader.

It will create a sequence of files with the segment name and loading address ready for manual loading into your favourite reversing tool.

I created this as the esptool.py image_info command ignores the secondary bootloader and user code and also provide incorrect file offsets for manual extraction.

Tested only on ESP8622. YMMV.
