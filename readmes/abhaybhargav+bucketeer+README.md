# Bucketeer
Bucketeer is a small script that builds off the useful Sublist3r tool. 
The Tool tries to identify S3 Buckets and other useful subdomain information, that is used to perform subdomain takeover attacks.

## Install Instructions
- Clone this repo
- Clone repo with Sublist3r: [here](https://github.com/abhaybhargav/Sublist3r)
- Install with command: `python setup.py install`
- Ready to run bucketeer

```
python bucketeer.py -h
usage: bucketeer.py [-h] [-d DOMAIN] [--brute-only] [-o OUTPUT]

Bucketeer is a small script that builds off the useful Sublist3r tool. The
Tool tries to identify S3 Buckets and other useful subdomain information, that
is used to perform subdomain takeover attacks.

optional arguments:
  -h, --help    show this help message and exit
  -d DOMAIN     Domain for which subdomains and cloud services is to be
                enumerated
  --brute-only  Bruteforce Subdomain and don not enumerate through Search
                Engines
  -o OUTPUT     This will be a YAML file, which will have the
                `domain_name`.yaml by default
```             
