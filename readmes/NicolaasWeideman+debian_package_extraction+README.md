# Debian Package Extraction
Search recursively for all debian packages and extract them to a specified destination.
It can also, optionally, delete all non-elf files from the extracted deb package.

## Dependencies
- [dpkg](http://man7.org/linux/man-pages/man1/dpkg.1.html)

## Example usage
- `python3 extract_debs.py /path/to/deb/mirror/ /absolute/path/to/extract/to`
- `python3 extract_debs.py --del_nonelfs=True /path/to/deb/mirror/ /absolute/path/to/extract/to`
