# toeknife
Carves partial DEFLATE data

# Usage
usage: ToeKnife [-h] [--window WINDOW] [--skip SKIP] [--file FILE] [--data DATA] [--guesses GUESSES]
                [--dynamic DYNAMIC] [--table]

options:
  - -h, --help         show this help message and exit
  - --window WINDOW    How many bytes of sample decompressed data to present to you (default is 20)
  - --skip SKIP        How many bits to pop from buffer for alignment (default 0)
  - --file FILE        Filename of the file that contains the compressed fragment
  - --data DATA        ASCIIHex representation of the filedata right on the commandline
  - --guesses GUESSES  Guessfile for partial data refered to by length-distance pairs
  - --dynamic DYNAMIC  provide file with initial data fragment of dynamic block
  - --table            Dumps Huffman table to illustrate which characters are valid (for potential guesses)

# Justification
In section 1.1 of RFC-1951:  
*The data format defined by this specification does not attempt to:*  
*Allow random access to compressed data;*  

This doesn't mean that it's impossible, just that the specification isn't written to for this purpose. ToeKnife helps to assist with some random access.

# Sample Workflow
For a sample phrase of:  
*Some numbers are one, two, three, and four. four is the only of those that has four letters in it*  

If Compressed with Fixed Huffman codes the ASCIIHex would be:
*0bcecf4d55c82bcd4d4a2d2a56482c4a55c8cf4bd5512829cfd75128c9284a4dd55148cc4b5148cb2f2dd203930a99c50a2519a90af97939950af9690a2519f9c5a90a251989250a1989c5102539a9252520e332f314324b00*  

In our example, the code section of the ASCIIHex is the partial data we are working with:
0bcecf4d55c82bcd4d4a2d2a56482c4a55c8cf4bd5512829cfd75128c9284a4dd55148cc4b5148cb`2f2dd203930a99c50a2519a90af97939950af9690a2519f9c5a90a251989250a1989c5102539a9252520e332f314324b00`

*~/code/toeknife ❯ python toeknife.py --window 70 --data '2f2dd203930a99c50a2519a90af97939950af9690a2519f9c5a90a251989250a1989c5102539a9252520e332f314324b00' --guesses guesses.txt*
`b'\xe98gQbq\x03\x16q\x19\x01\x19\x01\x0f\r\t"q\x0fq\x0f\x19\x01\x0f\x17\x0f\x17\x19\x01\x17\x0f\x17\x19\x01q\x01\x19\x01q\x01q\x03\x16q\x19\x01lett????in it'`  
`Does this look right?`n  

`b'ers ???????????????????????? fo\xd2\xa2. four is the only of those that has '`  
`Does this look right?`n  

`b'ers ???????????????????????? fo\xa5r. four is the only of those that has '`  
`Does this look right?`n  

`b'ers ???????????????????????? four. four is the only of those that has '`  
`Does this look right?`y  
Recovered Data: b'ers ???????????????????????? four. four is the only of those that has four letters in it'  
Symbol Form:    ur.[0:5,6] is the only of those that has[1:6,35]lett[2:4,79]in it[EOB]

# Workflow Explanation
Due to unknown alignment in a variable-width DEFLATE bitstream, the tool kind of trial and errors it with your assistance (not making assumptions for you). It will keep looping to ask you if the 'auditioned' data looks right. It displays a sample amount of the data (by default 20 bytes). We overrode that sample amount to 70 bytes with `--window 70`. We then fed it the partial ASCIIHex data with `--data`. We could have also provided this as a binary with `--file`.  

Assuming we ran this without a guess.txt file, if you look at the final output 'Symbol Form,' this allows us to take some guesses at what the data might be. The first length-distance pair will be 5 characters 6 bytes back, we are guessing that those characters might be 'four '. We don't have a guess for the 6,35, but 'lett' followed by 4 more characters (79 bytes back), this could be the word 'letters ', so our guess could be 'ers '. The initial number before the colon in these tokens is just a numbered index, which is used in the guesses file, of which would look like this:  
`0: four`  
`2:ers `  

Now that we have those guesses, it will fill those values in for us with the `--guesses guesses.txt` argument.

# Sample Command for Huffman Fragment (Dynamic Mode DEFLATE)
`python toeknife.py --dynamic partialhuff.bin --window 70 --data 'ac7bffb0940e2b6b8f5213ae480fa4de04fe7ae601'`  

The full data with huffman table and full (non fragment) data is:  
`8dcbd10980400c04d156b600b10b0b0961258133caada0767fda811fef676096dbb6a311629d564eac7bffb0940e2b6b8f5213ae480fa4de04fe7ae601`  

The original phrase that was compressed:  
*Example sentance for forensic analysis, which is an example sentance for forensic analysis.*
