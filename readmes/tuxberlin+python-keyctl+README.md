[//]: # (-*- coding: utf-8 -*-)

[![PyPI Package version](https://img.shields.io/pypi/v/keyctl.svg)](https://pypi.python.org/pypi/keyctl)
[![PyPI Python version](https://img.shields.io/pypi/pyversions/keyctl.svg)](https://pypi.python.org/pypi/keyctl)
[![License](https://img.shields.io/github/license/tuxberlin/python-keyctl.svg)](https://raw.githubusercontent.com/tuxberlin/python-keyctl/master/LICENSE)


<h1>python-keyctl</h1>

Basic management of keys in the Linux kernel keyring in Python. Also comes with a small gui.

* [Description](#description)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
  * [Module](#module)
  * [GUI](#gui)
* [Development](#development)
  * [Warning](#warning)
* [Similar projects](#similar-projects)
* [License](#license)



# Description

This is a small library to make use of some functions of the kernel keyring in Python.
You can read, add and delete keys.

It simply uses the keyctl command (invoking it via subprocess), so this util must be installed.

Available functions:

 * **list** *(list all keys in keyring)*
 * **describe** *(retrieve key name/description)*
 * **read/pipe/print** *(retrieve key content)*
 * **update** *(modify key content)*
 * **add** *(add key)*
 * **revoke/unlink** *(delete key)*
 * **search/request** *(search for a key by name)*
 * **clear** *(remove all keys from keyring)*

There are many more functions with keys in the kernel keyring (e.g. permissions)
that is needed for proper keymanagement. But for my usecase I just needed the
given simple functionality.

:warning: You might need to link your keyrings (e.g. for the testcases using the default keyring)
to have proper permissions.
E.g.:
```sh
$ keyctl link @u @s
```


# Requirements

Python 3.9
```sh
$ sudo apt install python3.9
$ python --version
Python 3.9.18
```

pip
```sh
$ sudo apt install python3-pip
$ pip --version
pip 23.3.2 from .... (python 3.9)
```

The 'keyctl' command
```sh
$ sudo apt install keyutils
$ dpkg -s keyutils | grep Version
Version: 1.6.1
```

If you want to use the GUI, you also need PySide6
```
$ pip install pyside6
$ python3 -c "import PySide6; print(PySide6.__version__)"
6.6.1
```



# Installation

```
$ pip install keyctl
```

Ready to use.



# Usage

## Module
Get all keys:
```python
from keyctl import Key
keylist = Key.list()
for mykey in keylist:
    print(mykey.id)
```

Read existing key:
```python
from keyctl import Key
mykey = Key(123)
print(mykey.name)
print(mykey.data)
print(mykey.data_hex)
```

Find key by name:
```python
from keyctl import Key
mykey = Key.search('test key')
print(mykey.id)
```

Add key:
```python
from keyctl import Key
mykey = Key.add('test key', 'test content')
print(mykey.id)
```

Delete key:
```python
from keyctl import Key
mykey = Key(123)
mykey.delete()
```

Update key:
```python
from keyctl import Key
mykey = Key(123)
mykey.update('new content')
```


## GUI
To open the GUI, run the installed command.
```
$ keyctlgui
```

![GUI Screenshot](https://github.com/tuxberlin/python-keyctl/wiki/images/screenshot.jpg)



# Development

## Warning

If you run the integrated tests, your user keyring will be cleared.
Don't do this when you have active keys e.g. for encryption.



# Similar projects

Similar projects you might want to check out:

 * https://github.com/sassoftware/python-keyutils (more complete, available in debian repo)
 * https://github.com/jdukes/pykeyctl (more complete, direct library wrapper)



# License

GPL-3.0  
see [LICENSE](https://raw.githubusercontent.com/tuxberlin/python-keyctl/master/LICENSE) file
