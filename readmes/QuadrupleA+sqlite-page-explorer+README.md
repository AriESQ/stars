# SQLite Page Explorer

A small GUI application built in [redbean](https://redbean.dev/) that lets you explore your [SQLite](https://sqlite.com/) databases "page by page" the way SQLite sees them.

![Top-level view](https://github.com/QuadrupleA/sqlite-page-explorer/blob/github_media/github_media/top_view.png)

---

## Why?

SQLite (and most databases) store data in disk-block-sized pages, usually 4KB, which helps make reads and writes as fast as possible.

Normally developers interact with databases on the "schema level" - tables, rows, and SQL. But taking a peek at the "page level" can give you some interesting insights:

* What your indexes actually look like on disk (they're basically separate little tables).
* How to store things more compactly (and thus make your queries and applications faster).
* Spot problems and inefficiencies you might not see on the schema level.
* Gain an intuition for B-Trees, one of computing's most important data structures, the foundation of most filesystems and databases.

## Run it anywhere

Thanks to the magic of redbean, [cosmopolitan](https://github.com/jart/cosmopolitan) and [αcτµαlly pδrταblε εxεcµταblε](https://justine.lol/ape.html), it's just a single 6.5 MB executable that runs natively on Windows, Linux, MacOS, various BSDs, on both ARM64 and x64. 

It's also a zip file that contains the Lua code that runs the app, parses the database binary format, etc.

## How to install

* Download `sqlite-page-explorer.com` from the [releases](https://github.com/QuadrupleA/sqlite-page-explorer/releases/). 
* On Unix-likes, `chmod +x`. 
* Drag a database file to it, or run it on the console: `sqlite-page-explorer.com mySqliteDatabase.db`. The app should open in a browser tab.
* When you're done, hit Ctrl-C twice in the console.

You might get virus warnings - αcτµαlly pδrταblε εxεcµταblεs seem to freak out browsers, operating system virus detection, etc. and generate false positives. I trust [jart](https://github.com/jart/) is not propagating malware here, and some notable projects like [llamafile](https://github.com/Mozilla-Ocho/llamafile) are using these same polyglot binary techniques, but take your usual precautions with anything you download off the internet. 

Also if you throw a large database at it (500 MB or more) it will likely be slow to load the top-level view, which reads every page.

## How to build

To build, you just need to `zip` the contents of `files/` into the stock `redbean-3.0.0-cosmos.com` which I downloaded from https://cosmo.zip/pub/cosmos/bin/ (click "redbean" on the list). You might need `zip` from there too if your system doesn't have it.

Or just run the `zipitup.py` python (3.6+) script that's included.

If you want to hack on it, you can run `redbean-3.0.0-cosmos.com -D files` to serve the app from the `files` subdirectory, so you don't have to rebuild the zip on every change.

## Not a masterpiece

This was partly an experiment to try out redbean, and also my first time using Lua, so the code is probably klunkier than it could be. It might benefit from a templating system, ala Jinja or bottle.py's native templates, rather than so many string concatenations and Write() statements. Would be nice to auto-close the console when the last tab closes, and maybe stop at page 10,000 or so for huge databases, unless the user confirms. PR's welcome!