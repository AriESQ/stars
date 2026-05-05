A debugger for Linux. Partially inspired by RemedyBG.

Mom, can we have RAD Debugger on Linux?
No, we have debugger at home.
Debugger at home:

![screenshot](https://github.com/user-attachments/assets/e0b03f1e-c1d1-4e38-a992-2ace7321bb75)

Properties:
 * Fast.
 * TUI.
 * Not based on gdb or lldb, implemented mostly from scratch.
 * Works on large executables.

What we mean by "fast":
 * Operations that can be instantaneous should be instantaneous. I.e. snappy UI, no random freezes, no long waits.
   (Known exception: if the program has >~2k threads things become pretty slow. This will be improved.)
 * Operations that can't be instantaneous (loading debug info, searching for functions and types) should be reasonably efficient, multi-threaded, asynchronous, cancellable, and have progress bars.

Limitations:
 * Linux only
 * x86 only
 * 64-bit only
 * for native code only (e.g. C++, Rust, Zig, Odin, not Java or Python)
 * TUI only (no REPL, GUI, or IDE integration)
 * no remote debugging (but works fine over ssh)
 * single process (doesn't follow forks)
 * no record/replay or backwards stepping

Development status:
 * Most standard debugger features are there. E.g. breakpoints, conditional breakpoints, data breakpoints, stepping of all kinds, showing code and disassembly, watch expressions, built-in pretty-printers for most of C++ and Rust standard library. Many quality-of-life features are there (e.g. auto-downcasting abstract classes to concrete classes based on vtable). But I'm sure there are lots of missing features that I never needed but other people consider essential; let me know.
 * I use it every day and find it very helpful.
 * Not in active development right now. I fix reported bugs and add small requested features, but likely won't get around to implementing big features soon (e.g. redesigning the watch expression language to have loops etc, ARM support, Mac OS support, GUI, DAP).

Distributed as a single 6 MB executable file with no dependencies.

"Installation":
```bash
curl -L -o nnd 'https://github.com/al13n321/nnd/releases/latest/download/nnd'
chmod +x nnd
# try `./nnd --help` to get started
```

Or build from source:
```bash
rustup toolchain install 1.89
cargo +1.89.0 build --profile dbgo
# The executable is at target/dbgo/nnd
```

Run `nnd --help` for documentation.
