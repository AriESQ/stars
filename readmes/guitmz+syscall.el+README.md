# syscall.el

Linux syscall tables right inside Emacs, and they work offline.

Look up any syscall on several architectures and ABIs, for almost every kernel release. You get the number, the signature, which register holds each argument, and when it showed up or went away. The data comes from [api.syscall.sh](https://api.syscall.sh/docs) and gets cached the first time you need it, so after that you can work on a plane.

![The detail buffer for openat on x64, with its number, signature, registers, notes and its number on other architectures](https://syscall.sh/emacs/detail.webp)

## What it does

- **Look up syscalls.** Find one by name or by number, decimal or hex. The name at point is the default, so `SYS_read` or `__NR_read` in your code just works.
- **Browse tables.** List everything an architecture has, and filter it as you type. Type `59` or `0x3b` to jump straight to that number, or type any text to match names, arguments, descriptions, families and kconfig options like `CONFIG_EPOLL`.
- **Pick a kernel.** Use the latest release, any older one, or every syscall an architecture ever had with the removed ones struck through.
- **Compare.** See one syscall on every architecture, or diff two kernel releases to spot what was added and removed.
- **Check conventions.** See the registers and trap instruction for every architecture, plus ABI quirks like `syscall` clobbering `rcx` and `r11` on x64.
- **Write assembly.** Drop a ready stub into your buffer that loads the number and argument registers, then traps.
- **ElDoc.** Hover over `SYS_openat` in C or assembly and see its signature and number in the echo area.

![The x64 list filtered down to the epoll syscalls](https://syscall.sh/emacs/filter.webp)

![ElDoc showing the signature and number of SYS_openat in a C buffer](https://syscall.sh/emacs/eldoc.webp)

There are more screenshots and a walkthrough at [syscall.sh/emacs](https://syscall.sh/emacs/).

## Requirements

Emacs 29.1 or newer. No other packages needed.

## Install

With `use-package` on Emacs 30 or newer:

```elisp
(use-package syscall
  :vc (:url "https://github.com/guitmz/syscall.el" :branch "main")
  :bind-keymap ("C-c s" . syscall-command-map)
  :hook ((c-mode c-ts-mode asm-mode) . syscall-eldoc-mode))
```

With `package-vc` on Emacs 29:

```elisp
(package-vc-install '(syscall :url "https://github.com/guitmz/syscall.el"))
```

With straight.el:

```elisp
(straight-use-package '(syscall :type git :host github :repo "guitmz/syscall.el"))
```

With Elpaca:

```elisp
(elpaca (syscall :host github :repo "guitmz/syscall.el"))
```

Or clone it anywhere and load it yourself:

```elisp
(add-to-list 'load-path "/path/to/syscall.el")
(require 'syscall)
(keymap-global-set "C-c s" syscall-command-map)
```

## Quick start

Press `C-c s l` and type a syscall name. The first time, it asks to download the data (about 6MB, takes around 10 seconds). After that everything comes from the cache.

| Key | Command | What it does |
| --- | --- | --- |
| `C-c s l` | `syscall-lookup` | describe a syscall by name |
| `C-c s n` | `syscall-lookup-number` | describe a syscall by number, like `59` or `0x3b` |
| `C-c s L` | `syscall-list` | table of every syscall on an architecture |
| `C-c s c` | `syscall-compare` | one syscall across every architecture |
| `C-c s C` | `syscall-conventions-table` | registers and trap instruction per architecture |
| `C-c s d` | `syscall-diff` | what changed between two kernel releases |
| `C-c s i` | `syscall-insert-asm-stub` | insert assembly that makes the call |
| `C-c s a` | `syscall-set-arch` | change the default architecture |
| `C-c s k` | `syscall-set-kernel` | change the default kernel release |
| `C-c s u` | `syscall-update` | refresh the cache |

Add a prefix argument (`C-u`) to the lookup, compare and stub commands to pick a different architecture just once.

### In the detail buffer

`n` and `p` step through numbers, `a` switches architecture and `k` switches kernel. Press `l` to jump to the full list or `c` to compare. `m` opens the man page and `s` the kernel source. `w` and `W` copy the number in decimal or hex, and `i` copies an assembly stub.

### In the list

`RET` describes the syscall at point, `/` filters and `f` narrows to a family like `epoll` or `io_uring`. `a` and `k` switch architecture and kernel, `d` diffs against an older release, and `c` compares. `m`, `s`, `w`, `W` and `i` work like in the detail buffer.

### Assembly stubs

On x64 you get this:

```asm
; write(unsigned int fd, const char *buf, size_t count), x64 1
mov eax, 0x1  ; write
mov rdi, 0    ; unsigned int fd
mov rsi, 0    ; const char *buf
mov rdx, 0    ; size_t count
syscall
```

It uses `mov eax` on purpose, because that clears the top half of `rax`, which kernels older than 5.14 need. You get proper syntax on x86, ARM, AArch64, riscv64 and MIPS. On ARM, numbers too big for an immediate load with `ldr r7, =value`. Every other architecture gets the register assignments as comments. The comment character follows your buffer when it has one.

## Configuration

Run `M-x customize-group RET syscall RET` for everything. The ones you probably care about:

```elisp
(setq syscall-default-arch "arm64"          ; default is "x64"
      syscall-default-kernel nil            ; nil for latest, "all", or a release like "5.10"
      syscall-auto-update-interval 30       ; days between background refreshes, nil to turn off
      syscall-eldoc-bare-names nil)         ; t to also match plain words like read
```

The cache lives in `~/.emacs.d/syscall/` by default. Change `syscall-cache-directory` to put it somewhere else.

## How the cache works

Each architecture is one JSON file with every syscall it ever had, plus the release it appeared in and the one it was removed in. A syscall exists in a release when it showed up at or before it and was not removed yet. That single rule covers every release offline, and the results match what the API itself returns.

A few more details:
- **Updates are cheap.** `syscall-update` sends the stored ETags, so files that didn't change come back as a 304 with no download. Use `C-u M-x syscall-update` to grab everything again.
- **The API stays happy.** Requests go one at a time with a short pause between them, and rate limits or server errors get retried a few times.
- **Updates can't break your cache.** New files land in a staging folder and only replace the old ones once every request worked. Bad JSON or an empty architecture cancels the whole update.
- **Nothing phones home behind your back.** Only `syscall-update` and the monthly background refresh touch the network. ElDoc never downloads anything, and it stays quiet until the cache exists.

Other handy commands are `syscall-cache-info`, `syscall-cancel-update` and `syscall-clear-cache`.

One thing worth knowing: url.el normally answers a 304 by reading its own disk cache. syscall.el keeps its own cache, so it advises `url-cache-extract` to skip that step for its own requests only.

## Troubleshooting

- **The download failed.** Check `*Messages*` for the error and try `M-x syscall-update` again. Your old cache is still there.
- **A syscall seems missing.** It might not exist in the kernel you picked. Try `C-c s k` and choose `all`.
- **An architecture shows nothing for an old kernel.** Some were only scanned from later releases. For example mipso32 starts at 5.0.

## Tests

```sh
make compile test
```

The suite fakes the API, so it needs no network. `make live` runs two real updates against api.syscall.sh into a throwaway cache. CI runs on Emacs 29.4, 30.2 and 31.1.

See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to help out.

## Related

- [syscall.sh](https://syscall.sh) is the same data as a website
- [syscall.sh/emacs](https://syscall.sh/emacs/) shows this package in action
- [api.syscall.sh](https://api.syscall.sh/docs) is the JSON API this package reads

## License

MIT, see [LICENSE](LICENSE).
