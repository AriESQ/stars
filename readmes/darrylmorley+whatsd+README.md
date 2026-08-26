# WhatSD

A macOS menu-bar app (and CLI) that surfaces the full truth about an SD card
inserted into your Mac: its real identity, whether it looks genuine, and (with
Pro) its real usable capacity.

**Status:** early development. The read layer works: `WhatSDCore` +
`WhatSDDarwinBackend` and the `whatsd` CLI read the built-in SD slot (identity,
negotiated link, volumes) and flag likely counterfeits. The menu-bar app shows
the same, styled.

## Why

SD cards are opaque and their printed badges (Class 10, U3, V30, A2) are poorly
understood and frequently faked. WhatSD answers two questions the Mac doesn't
answer cleanly:

1. **Is this card real?** Counterfeit SD cards are everywhere. WhatSD flags
   suspect cards from their identity registers, and the Pro capacity test proves
   the real usable size by writing and verifying data across the card.
2. **Is it as fast as the box claims?** macOS can't read the speed-class
   registers, so the only honest answer is a real measured benchmark.

## What it reads

On the built-in SD slot, `system_profiler` and IOKit expose the card's identity
(manufacturer, product, serial, manufacture date, spec version, capacity,
format) and the negotiated electrical link, with no special entitlements. macOS
does not expose UHS / Video / App speed classes, so real speed must be measured.
USB card readers hide the card's identity behind a generic bridge; WhatSD says
so rather than guessing.

## Layout

- `WhatSDCore` — pure models, formatting, counterfeit heuristics, and the
  capacity-test engine. No OS imports.
- `WhatSDDarwinBackend` — IOKit / DiskArbitration / `system_profiler` readers.
- `WhatSDAppKit` — shared UI plumbing (the Pro extension registry, font scaling).
- `WhatSDApp` — the SwiftUI menu-bar app.
- `whatsd-cli` — the `whatsd` command-line tool.

## Build

```
swift build
swift test
scripts/smoke-test.sh   # build + bundle WhatSD.app + smoke-test
```

## Licence

The app and its read layer are MIT licensed (see `LICENSE`). The Pro capacity
test is a separate paid feature and is not open source.
