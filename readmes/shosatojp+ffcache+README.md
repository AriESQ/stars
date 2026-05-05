# ffcache

![C/C++ CI](https://github.com/shosatojp/ffcache/workflows/C/C++%20CI/badge.svg)

Firefox cache extractor.

## Usage

### Get list of cache

```sh
FFCACHE_DIR=~/.cache/mozilla/firefox/hoge.default/cache2 ffcache --list
```

### Save cached file

```sh
FFCACHE_DIR=~/.cache/mozilla/firefox/hoge.default/cache2 ffcache --key https://example.com/image.png --out myimage.png
```

### Options

```sh
[usage]
ffcache [OPTIONS]
--list  -l      list all keys
--cache -c      cache2 directory
--key   -k      key
--out   -o      output path
```

### Python Binding

```sh
pip install ffcache
```

```py
from ffcache import FirefoxCache, FirefoxCacheEntry
from ffcache.helper import save
import urllib.parse
import os
import brotli
import gzip
import zlib
import sys

cache_dir = os.environ['FFCACHE_DIR']
out_dir = 'tmp'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

cache = FirefoxCache(cache_dir)

for entry in cache.records:
    url = entry.key
    print(url)

    filename = urllib.parse.quote(url, safe='')[:255]
    out_path = os.path.join(out_dir, filename)

    try:
        save(entry, out_path)
    except:
        pass
```

## install

download artifacts from [here](https://github.com/shosatojp/ffcache/actions) or manually build.

## build

### build on host

```sh
sudo apt-get install -y g++ python3.8-dev make python3-pip
pip3 install pybind11
make
```

### build with docker

```sh
sudo docker-compose up --build
```

* specify python version in `docker-compose.yml` (default python3.8)
