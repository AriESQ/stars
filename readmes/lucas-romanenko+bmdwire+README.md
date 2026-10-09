<p align="center"><img src=".github/banner.png" alt="bmdwire: Python libraries for Blackmagic Design broadcast devices. One package, four device families, one version." width="100%"></p>

Python libraries for Blackmagic Design broadcast devices: one package, one version, four device families.

[![CI](https://github.com/lucas-romanenko/bmdwire/actions/workflows/ci.yml/badge.svg)](https://github.com/lucas-romanenko/bmdwire/actions/workflows/ci.yml) [![PyPI](https://img.shields.io/pypi/v/bmdwire.svg?label=pypi)](https://pypi.org/project/bmdwire/) ![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)

```sh
pip install bmdwire
```

| Import | Purpose | License | Docs |
|---|---|---|---|
| **`atemwire`** | ATEM switchers: the native UDP protocol, a connection pool, macro bytecode, "Save Switcher State" profiles | LGPL-3.0-only | [atemwire/README.md](atemwire/README.md) |
| **`hyperdeckwire`** | HyperDeck recorders: transport control and clip listing over TCP 9993, clip upload over FTP, and the deck's configuration (network, FTP / Web Media Manager / Ethernet Protocol switches, certificate, users, time) over the API HyperDeck Setup drives | MIT | [hyperdeckwire/README.md](hyperdeckwire/README.md) |
| **`ultimattewire`** | Ultimatte 12 keyers: archive and restore over the native TCP protocol, Smart Remote 4 compatible zips | MIT | [ultimattewire/README.md](ultimattewire/README.md) |
| **`videohubwire`** | Videohub routers: state snapshot, crosspoint routing, labels over TCP 9990 | MIT | [videohubwire/README.md](videohubwire/README.md) |

All four are pure standard library except atemwire, whose small C extension ships prebuilt for Linux, macOS and Windows on CPython 3.10 to 3.14, so installing needs no compiler. Pin the version in a requirements file (`bmdwire==1.2.0`) so a later release cannot change your install under you.

## atemwire stands on pyatem

**atemwire is a fork of [pyatem](https://git.sr.ht/~martijnbraam/pyatem) by
Martijn Braam and the OpenAtem contributors.** Years of reverse engineering
the ATEM protocol came before any of this, and that work is what made the
rest possible. It branched at upstream commit `8f45831` (2026-03-14) and was
then developed for months against live switchers: transport reliability
fixes, a declarative wire-format layer, corrected and extended message
coverage, macro upload, and profile save and restore.

The licence is unchanged and not negotiable: **LGPL-3.0-only**, the same as
upstream. Improvements to atemwire stay open, as they should. The other three
libraries here were written from scratch and are MIT. The distribution's
licence expression is `LGPL-3.0-only AND MIT`, and each package directory
carries the text that governs it.

If you want the original rather than this fork, it is at
<https://git.sr.ht/~martijnbraam/pyatem> and it is still maintained.

## Why one package

The four libraries share an author, a shape and a purpose: they are the device layer of one broadcast control application, extracted and published so others can use them. Until 1.0.x each was its own PyPI project with its own version number. Nothing downstream ever wanted them apart, and four numbers to track for one release train was confusion with no benefit, so since 1.1.0 they are one distribution: one tag, one version, one line to pin. The import names did not change.

The four old PyPI projects (`atemwire`, `hyperdeckwire`, `ultimattewire`, `videohubwire`) were deleted on 2026-09-16; bmdwire is the only package. They were not replaced by shims, on purpose: a release of `atemwire` that depended on bmdwire would have broken `pip install -U atemwire`, because pip installs the dependency first and then removes the old package's files, which are the same paths bmdwire just wrote. **If an environment still has any of the four old packages from before, uninstall them before installing bmdwire** (`pip uninstall atemwire hyperdeckwire ultimattewire videohubwire`). Two distributions owning one module directory work until one of them is uninstalled. A fresh virtualenv, a pipx install or a container build never has this problem.

## Development

```sh
git clone https://github.com/lucas-romanenko/bmdwire.git
cd bmdwire
pip install -e ".[test]"      # builds atemwire's C extension in place, needs a compiler
python -m pytest
```

The editable install matters: a plain `pip install .` puts the extension in site-packages, and `python -m pytest` run from the checkout then imports the source tree without it and fails on `atemwire.mediaconvert`. The suite needs no hardware. CI runs it on Python 3.10, 3.12 and 3.14 for every push and pull request, and builds an sdist and a wheel to prove the metadata.

A release is a tag `v<version>` on `main` whose version equals `project.version` in `pyproject.toml`; pushing it builds the sdist and the wheels and publishes them to PyPI. `pip show bmdwire`, not a hand-typed number, is how to know what is installed.

Not affiliated with or endorsed by Blackmagic Design Pty Ltd. ATEM, HyperDeck, Ultimatte and Videohub are trademarks of Blackmagic Design.
