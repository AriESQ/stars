# DXV Codec

The DXV codec uses GPU-enabled [S3 Texture Compression](https://en.wikipedia.org/wiki/S3_Texture_Compression) similar to the [HAP codec](https://github.com/Vidvox/hap). I also has optional CPU-compression using [LZF](https://en.wikibooks.org/wiki/Data_Compression/Dictionary_compression#LZF), which is very similar in performance to [Snappy](https://github.com/google/snappy) used by HAP. Based on these technical specifications the codecs should be almost identical in performance.

### Background articles:
https://cdm.link/2009/03/exclusive-inside-resolumes-new-gpu-powered-live-visual-ready-dxv-codec/  
https://resolume.com/software/codec  

## Specification
The file format specification is not made available, but it has been reverse-engineered by developers of the ffmpeg libraries. The following specification is based on the code available here: https://github.com/FFmpeg/FFmpeg/blob/master/libavcodec/dxv.c

### File format
The file format is QuickTime MOV. This container format has multiplexed video and audio streams comprised of interleaved packets. In order to identify the file as DXV the video stream is marked by a FourCC identifier (also called RIFF or OSType). Following identifiers have been registered:
| FourCC | Version |
|--------|---------|
| DXDI   | DXV 1   |
| DXD3   | DXV 3   |


### DXV 3 packet header
| Byte offset | Data type | Description       |
|-------------|-----------|-------------------|
| 0           | 32-bit    | Tag *             |
| 4           | 8-bit     | Version major + 1 |
| 5           | 8-bit     | Version minor     |
| 6           | 8-bit     | Raw flag          |
| 7           | 8-bit     | Unknown           |
| 8           | 32-bit    | Size              |

#### Tag
This is a FourCC-style tag identifying the type of texture compression used. Here are some possible values:
| FourCC |
|--------|
| DXT1   |
| DXT5   |
| YCG6   |
| YG10   |

### DXV 1 packet header
Previous versions (DXV1) used a smaller 4-byte header.
| Bit offset  | Bit length | Description |
|-------------|------------|-------------|
| 0           | 24         | Size        |
| 24          | 4          | Flags *     |
| 28          | 4          | Version + 1 |

#### Flags
Bits set  
1 - DXT1  
2 - DXT5  
3 - RAW (no LZF)  

### Data
The data following the header has the size described by the size-field in the header. In DXV 1 the data may be compressed by LZF-compression (indicated by the missing raw-flag). But in the later DXV 3 there seems to be no LZF-compression available - probably due to the poor performance with high-resolution content.
