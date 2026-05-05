<div align="center">

<h1> dHashPy </h1>

<h3>Row-wise gradient dHash algorithm in python.</h3>
  
dHash algorithm was originally described at <a href="https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html" target="_blank">Kind of Like That - The Hacker Factor Blog</a> 

</div>

<p align="center">
<a href="https://github.com/akamhy/dhashpy/actions?query=workflow%3AUbuntu"><img alt="Build Status" src="https://github.com/akamhy/dhashpy/workflows/Ubuntu/badge.svg"></a>
<a href="https://github.com/akamhy/dhashpy/actions?query=workflow%3AWindows"><img alt="Build Status" src="https://github.com/akamhy/dhashpy/workflows/Windows/badge.svg"></a>
<a href="https://codecov.io/gh/akamhy/dhashpy"><img alt="codecov" src="https://codecov.io/gh/akamhy/dhashpy/branch/main/graph/badge.svg?token=HVwlPMnsPA"></a>
<a href="https://dhashpy.readthedocs.io/en/latest/"><img alt="docs" src="https://readthedocs.org/projects/dhashpy/badge/?version=latest&style=flat"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>


### Installation

  - Using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```bash
pip install dhashpy -U
```

  - Install directly from GitHub:

```bash
pip install git+https://github.com/akamhy/dhashpy.git
```

### Usage
```python
>>> from dhashpy import DHash
>>> file = "/home/akamhy/Pictures/map_of_maths.png"
>>> dhash_file = DHash(file)
>>> dhash_file
DHash(hash=0b0110010000000011101010111100110111001101100011111000111100001110, hash_hex=0x6403abcdcd8f8f0e, path=/home/akamhy/Pictures/map_of_maths.png)
>>>
>>> dhash_file.hash # A 64-bit hash, notice the prefix "0b" indicating it's binary. Total string length = 64 + 2 = 66
'0b0110010000000011101010111100110111001101100011111000111100001110'
>>>
>>> len(dhash_file)
66
>>> dhash_file.bits_in_hash
64
>>>
>>> dhash_file.hash_hex
'0x6403abcdcd8f8f0e'
>>>
>>> dhash_file - "0x6403abcdcd8f8f0e"
0
>>>
>>> dhash_file == "0x6403abcdcd8f8f0e"
True
>>>
>>> dhash_file - "0b0110010000000011101010111100110111001101100011111000111100001110"
0
>>>          
>>> dhash_file
dhash_file
>>> dir(dhash_file)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__weakref__', 'bin2hex', 'bits_in_hash', 'calc_hash', 'hamming_distance', 'hash', 'hash_hex', 'height', 'hex2bin', 'image', 'path', 'width']
>>> dhash_file.height
8
>>> dhash_file.width
9
>>> dhash_file.image
<PIL.Image.Image image mode=L size=9x8 at 0x7F9D324C0580>
>>>
```

> Docs :  <https://dhashpy.readthedocs.io/en/latest/>


### License
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/akamhy/dhashpy/blob/main/LICENSE)


Released under the MIT License. See
[license](https://github.com/akamhy/dhashpy/blob/master/LICENSE) for details.
