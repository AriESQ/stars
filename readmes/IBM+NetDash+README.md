# NetDash
Platform agnostic network monitoring dashboard

# Dependencies
Python 3.5 or later with Tcl/Tk

# Setup
Requires configuration file, see example in config.txt

# Usage
 netdash.py [-h] [-t T] [-c C] [-q] path

### positional arguments
path - path to configuration file

### optional arguments
-h, --help - show usage information
  
-t T, -time T - update cycle time (in seconds)
  
-c C, -count C - number of pings to send per host each cycle

-q, -quiet - supress informational messages
