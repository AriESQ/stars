# parallelprocs

Run commands via GNU Parallel or something like it.

# Synopsis

````
$ cat test.py
#!/usr/bin/env python

from parallelprocs import run

try:
    run(['echo foo', 'echo bar', 'echo baz'], verbose=True)
except Exception as e:
    print(e)
$ ./test.py
Running job (# jobs = 3)
bar
baz
foo
````

# Description

The module exposes a single function `run` that takes the following arguments:

## Required Arguments:

commands [str]: commands

## Keyword Options

* parallel (str): path to "parallel", default "which('parallel')"
* num_procs (int): num of concurrent processes, default "0" to use all CPUs
* verbose (bool): print messages to sys.stderr, default "False"
* halt (int): number of failed jobs to trigger halt, default "0" for no halt

# Author

Ken Youens-Clark <kyclark@gmail.com>
