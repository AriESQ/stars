# TUI selector

Copyright (c) 2020-2021 [Antmicro](https://www.antmicro.com)

This is a simple TUI menu that lists and runs applications based on rules written in the JSON format.

## Building the project

The project requires `ncurses` library and a C++ compiler with C++17 support.
In order to build it, run:

    mkdir build && cd build
    cmake ..
    make -j24

## Usage

The `tui-selector` requires the path to the directory with JSON files that describe filters and run commands.

There can be multiple JSON files in the `rules_directory` directory.

The JSON files should have the following structure:

    [
        {
            "searchdirectory" : "path/to/directory/with/files",
            "regex" : "<file-regex>",
            "command" : "<command-to-run>",
            "entryformat" : "<how-entry-should-be-displayed"
        },
        ...
    ]

The root of the JSON file is the list of rules.
Each rule is a dictionary with four attributes where:

* `searchdirectory` says where the files or executables to be used as the menu entries are located,
* `regex` holds the regular expression by which the files in `searchdirectory` should be filtered,
* `command` describes how the file or executable should be executed,
* `entryformat` describes how the entry for a given file and rule should be displayed in the TUI menu.

Both `command` and `entryformat` are regex substitutions for the `regex` attribute.
This means that regex groups formed in `regex` can be accessed in `command` and `entryformat` by `$i`, where `i` is the ID of the group.

For example, for regex `"(^.*)\\/(.*)\\.pdf$"` and string `/directory/lab1-presentation.pdf` the `entryformat` with value `Open document $2 (okular)` will create entry `Open document lab1-presentation (okular)` in the menu.

## Examples of JSON rules

The examples of JSON files with rules are in the [json-samples directory](./json-samples).

Let's assume there are some images, videos, .txt or .pdf files in the Desktop directory.

Create a `rules/` directory and a `rules/multimedia.json` file with the following content (replace user with your user name):

    [
        {
            "searchdirectory" : "/home/user/Desktop",
            "regex" : "(^.*)\\/(.*\\.(mp4|avi))$",
            "command" : "vlc $1/$2",
            "entryformat" : "Video $2"
        },
        {
            "searchdirectory" : "/home/user/Desktop",
            "regex" : "(^.*)\\/(.*\\.(jpg|png))$",
            "command" : "gwenview $1/$2",
            "entryformat" : "Image $2"
        }
    ]
    
Then, add a `document.json` file:

    [
        {
            "searchdirectory" : "/home/user/Desktop",
            "regex" : "(^.*)\\/(.*)\\.pdf$",
            "command" : "okular $1/$2.pdf",
            "entryformat" : "Document $2"
        }
    ]

## Running `tui-selector`

Assuming the current directory is the root directory of the project, run:

    tui-selector ./json-samples

(if `tui-selector` is not installed but built, run `./build/tui-selector`)

The view should look something like this:

![tui-example](example-view.png)

The `tui-selector` also has a `--timeout <numseconds>` flag - with this flag the tool will select the default (first) option once the timeout specified in `<numseconds>` seconds is reached.

## Licensing

The sources are published under the Apache 2.0 License, except for files located in the `third-party/` directory.
For those files the license is either enclosed in the file header or in a separate LICENSE file.
