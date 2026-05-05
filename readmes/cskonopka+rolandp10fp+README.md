<p align="center">
  <img width="35%" height="35%" src="https://github.com/cskonopka/rolandp10fp/blob/master/img/rolandp10fp-logo.png?raw=true"/>
</p> 

<p align="center"><em>File preperation script for the Roland's P-10 Image Converter Lite</em></p>

current formats
========
- input: .mp4/.mov/.avi (* this will be expanded in the future)
- output: .mpg

requirements
========
- Python (https://www.python.org/)
- ffmpeg (http://ffmpeg.org/)
- Roland P-10 Image Converter Lite (http://proav.roland.com/products/p-10/downloads/)

how to use
========
1. First, place the files you wish to convert in the folder labeled "raw-videos"
2. Open the terminal and change the directory to this folder (rolandp10fp)
3. Run the script by typing "python rolandp10fp.py". Automatically a new folder named "converted" will be created and filled with videos with the extension ".mpg".
4. You're done! All the files in the folder named "converted" are now properly encoded and can be converted correctly using the "Roland P-10 Image Converter Lite" application for the Roland P-10 video sampler
