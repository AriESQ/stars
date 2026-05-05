# IQ-Analog-Picture-TV
matlab files that create and decode IQ files and display image.   
files can be ran in matlab or gnu octave which is free
first run tx-am-image.m  loads in a jpeg and prints pixel height and width in the command window, note these, they will be needed in the rx-am-image script.
the tx file saves a i/q wave file in the location of the jpeg image.
one can use gnuradio to tx the wave file, by using waveread 2ch,  and using float to complex function in gnuradio.
for rx script need to input the h and w of the image, before running the script.   the rx script works by loading an iq file from standard sdr rx software like sdrsharp, sdr++, and sdrconsole.      be sure when recording iq file, the center freq of the sdr rx software matches the tx freq of the sdr transmitter.    for tx, should be able to use red pitaya, hackrf, and usrp devices as tx hardware.   to use red pitaya, it needs certain sample rates, so change fs from 48khz to 50khz in tx and rx scripts.
some details of what the scripts do:  tx file reads in jpeg, converts to black and white, inserts chirp for preamble and chirps for image line sync then save i/q wave file.    left = i,  right = q.        then the rx script reads in i/q file from sdr software, detects preamble, then starts searching for line sync and starts creating picture line by line.   kinda like old school tv.   with a sdr twist.   bandwidth of signal is a function of fs.   so if user wants bw of 12khz, change fs to 12khz in tx and rx files.   by lowering fs, tx time will be longer.  
if user has no sdr hardware, user can still create wave file and read in wave file with matlab or gnu octave.    a neat project for ee class or sdr experiments. 

added gnu octave files,  these scripts set picture to 800x800,  if you want something different, change it.
gnu octave is free for windows, linux,  so no need to buy matlab

see thegmr140  youtube


