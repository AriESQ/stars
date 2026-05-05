# transport-stream-parser - MPEG2 TS parser for extracting video and audio streams

This simple Python module provides fucntions for parsing `MPEG2 TS` into TS packets and extracting video and audio streams by their PIDs. It also allows to view the transport stream packet by packet in a summarized form.

## Usage

Just import the package and use `parse_TS()` function to parse the TS packets from a file.

``` Python
import ts_parser as tsp

TS_packets = tsp.parse_TS('data/sample.ts')
```

Then, the audio and video streams can be directly extracted using `extract_stream()`

``` Python
tsp.extract_stream(TS_packets, 257, 'data/PID257.mp2') # audio
tsp.extract_stream(TS_packets, 256, 'data/PID256.264') # video
```

The module also offers a function for assembling  `PES` packets of specific `PID`.

``` Python
PES_packets = tsp.reassemble_PES(TS_packets, 257)
```

## Disclaimer

This is a simple module. It does not parse all the packet fields (at least yet), especially those not requiered to extract audio or video from the transport stream.


