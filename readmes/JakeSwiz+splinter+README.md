# splinter
"Let me tell you why you're here. You're here because you know something. What you know you can't explain, but you feel it. You've felt it your entire life, that there's something wrong with the world. You don't know what it is, but it's there, like a splinter in your mind, driving you mad." — Morpheus

<img width="1625" height="1077" alt="image" src="https://github.com/user-attachments/assets/b2bd80d8-875c-45b5-8e96-a5309474d132" />

---

A BLE **privacy / anti-tracking decoy** for the ESP32. It continuously fabricates a
churning crowd of plausible-but-fake Bluetooth LE devices so that, in a space you
control, a tracking or scanning system sees lots of ordinary-looking traffic and your
real device(s) don't stand out.

## What it does

Every `SPLINTER_ROTATE_MS` (default 250 ms) splinter retires the current advertisement
and mints a new decoy with:

- a fresh **random-static MAC** — exactly what modern phones, watches and earbuds already
  do for privacy, so the churn looks realistic;
- a random vendor drawn from `main/decoy_vendors.h`, surfaced via the **Company ID in
  manufacturer-specific data** (the spec-defined vendor signal a scanner actually reads);
- an optional short device name and a benign random payload.

A scanner sampling over a few seconds therefore logs dozens of distinct, vendor-attributed
devices appearing and disappearing.

## What it deliberately does NOT do (non-intrusive BLE connections)

Advertising is **non-connectable** and the payload is never shaped like
Apple Continuity (`0x004C`), Microsoft Swift Pair (`0x0006`), or Google Fast Pair
(`0xFE2C`). Those formats trigger pairing pop-ups on bystanders' phones/PCs — a decoy
needs realistic *presence*, not pop-up spam aimed at people nearby, so those payloads are
never emitted. See the header comment in `main/decoy_vendors.h`.

This helps prevent annoying pop-ups that are seen in other "spammers" in other products and firmware variants. This is how we get around that. 

> Intended for privacy/anti-tracking use in a space you control. Don't point it at other
> people's devices.

## Hardware

**Primary target: ESP32-C5** (RISC-V, Bluetooth 5). BLE 5 extended advertising lets
splinter run several *genuinely concurrent* decoy instances (each with its own MAC) on
top of maximum churn — see `sdkconfig.defaults.esp32c5`. This is the build documented
below.

The classic **ESP32-WROVER-E** (BT 4.2) is also supported as a fallback — it runs one
legacy advertiser rotated at full rate. See [Classic ESP32](#classic-esp32-fallback) at
the end.

## Build & flash (ESP32-C5)

The C5 needs **ESP-IDF v5.5**. On this machine there are two IDF checkouts:

- `~/esp/esp-idf-v5.5` — **use this** (has the C5 RISC-V toolchain)
- `~/esp/esp-idf` — v5.4, **do not use** (no C5 toolchain; will fail with
  `riscv32-esp-elf-gcc ... not found`)

### 1. Load the environment

Sourcing the v5.4 env in a shell "sticks" its Python venv and breaks a later v5.5 source
(`Checking python dependencies ... FAILED`). Always clear the stale vars first — an alias
in `~/.bashrc` makes this painless:

```bash
alias get_idf='unset IDF_PYTHON_ENV_PATH IDF_PATH IDF_TOOLS_PATH; . ~/esp/esp-idf-v5.5/export.sh'
```

Then, in a fresh terminal:

```bash
get_idf
esptool.py version          # sanity check: must be v4.12.dev3, NOT 4.11.0
```

(The system `esptool 4.11.0` mis-parses C5 image headers — `Expected 23 but value was 0`.
Sourcing the right env puts IDF's `v4.12.dev3` ahead of it on `PATH`.)

### 2. Build

```bash
cd ~/Projects/splinter
idf.py --preview set-target esp32c5     # one-time; --preview is required (C5 is preview in 5.5)
idf.py build
cat build/flash_args                    # verify: bootloader at 0x2000, flash_freq 80m
```

> ⚠️ **Do not run `idf.py set-target esp32`.** That reconfigures for the classic chip
> (bootloader `0x1000`, `40m`) and the resulting image is rejected by the C5 hardware
> (`not an ESP32-C5 image`). If `flash_args` shows `0x1000`/`40m`, re-run the `--preview`
> command above.

### 3. Flash — manual download mode (required in the Parallels VM)

Inside the Parallels VM the USB layer **does not pass DTR/RTS**, so esptool's auto-reset
and plain `idf.py flash` fail with `No serial data received`. The chip's *native*
USB-Serial-JTAG port also re-enumerates on reset (→ `Write timeout`). So:

- Use the **CH343 UART-bridge** USB-C port — it enumerates as `/dev/ttyACM0`
  (USB id `1a86:55d3`) and stays put across resets.
- Put the chip into download mode by hand, and tell esptool not to reset:

```bash
cd ~/Projects/splinter
idf.py build                        # ← ALWAYS build first; esptool does NOT compile
cd build
# 1. press and HOLD the BOOT button
# 2. tap RST once (keep holding BOOT)
# 3. KEEP holding BOOT, then run:
esptool.py --chip esp32c5 -p /dev/ttyACM0 -b 115200 \
  --before no_reset --after no_reset write_flash "@flash_args"
# 4. release BOOT once "Writing…" appears
```

Holding BOOT through the whole connect is essential — the download-mode strap (GPIO9) is
only sampled at reset and must stay low.

> ⚠️ **`esptool.py write_flash` only flashes the existing `build/splinter.bin` — it does
> NOT rebuild.** Unlike `idf.py flash` (which auto-builds but can't reset the chip in this
> VM), the raw esptool path will silently re-flash a stale binary if you skip `idf.py
> build`. After every source edit: `idf.py build` first, then flash. Sanity check:
> `build/splinter.bin` should be newer than `main/splinter_main.c`.

### 4. Run & watch

```bash
# tap RST to leave the bootloader and start the firmware, then:
idf.py -p /dev/ttyACM0 monitor          # Ctrl+] to exit
```

You should see `rate: N refreshes/sec, 4 live instances` every second. Scan with a BLE
app (e.g. nRF Connect) to watch the decoy crowd. `monitor` is read-only, so it's the one
`idf.py` serial command that works normally here.

### Iteration loop

Once set up, each edit → test cycle is: **`idf.py build`** (never skip — esptool won't
compile) → BOOT-hold / tap RST / keep holding BOOT → the `esptool.py … write_flash
"@flash_args"` command → release BOOT → tap RST → `idf.py -p /dev/ttyACM0 monitor`.

A healthy boot logs `rate: N refreshes/sec, 4 live instances (fail=0)` with **no `rc=3`**
errors. If you see `rc=3` on every `configure instance`, an advertising parameter is
illegal — most commonly `SPLINTER_ADV_MS` below the 20 ms BLE floor (see Configuration).

## Configuration

Tunables live at the top of `main/splinter_main.c`:

| Macro | Default | Effect |
|-------|---------|--------|
| `SPLINTER_ADV_MS` | 100 | On-air advertising interval per decoy (ms). **Must be ≥ 20** — the BLE minimum; anything lower is rejected by NimBLE (`ble_gap_ext_adv_params_validate rc=3`) and nothing advertises. |
| `SPLINTER_EXT_REFRESH_MS` | 20 | C5: gap between per-instance identity refreshes (lower = denser churn; too low starves the single core) |
| `SPLINTER_NAME_PROB` | 60 | % chance a decoy advertises a device name |
| `SPLINTER_MFG_PROB` | 85 | % chance a decoy carries vendor manufacturer data |
| `SPLINTER_ROTATE_MS` | 250 | Classic-ESP32 paced mode only: delay between decoys |
| `SPLINTER_BENCHMARK` | 1 | `1` = flood/max-rate (reports devices/sec); `0` = paced decoy |

Concurrent-instance count on the C5 is a Kconfig value, not a macro:
`CONFIG_BT_NIMBLE_MAX_EXT_ADV_INSTANCES` (default 4, set in `sdkconfig.defaults.esp32c5`).
Change it via `idf.py menuconfig` → *Component config → Bluetooth → NimBLE Options*, or
edit the defaults file and rebuild.

Add more vendors/names to `main/decoy_vendors.h` for a denser, more varied crowd (keep
names ≤ 12 chars to stay within the 31-byte advertising budget).

## Troubleshooting

- **`Checking python dependencies ... FAILED` when sourcing v5.5** — the shell has a stale
  v5.4 venv path. Run the `get_idf` alias above (it `unset`s `IDF_PYTHON_ENV_PATH` first),
  ideally in a fresh terminal.
- **`riscv32-esp-elf-gcc ... not found`** — you sourced `~/esp/esp-idf` (v5.4). Use
  `~/esp/esp-idf-v5.5`.
- **`esptool.py v4.11.0` / `not an ESP32-C5 image` / `Expected 23 but value was 0`** —
  wrong esptool (env not sourced) or the target got reset to classic `esp32`. Re-source
  the env and `idf.py --preview set-target esp32c5`.
- **`No serial data received` when flashing** — auto-reset can't cross the VM. Use the
  manual BOOT/RST download-mode procedure above with `--before no_reset`.
- **`Write timeout`** — you're on the native USB-Serial-JTAG port, which drops on reset.
  Move to the CH343 UART-bridge port (`/dev/ttyACM0`, `1a86:55d3`).
- **Edits don't take effect / stale behaviour after flashing** — you skipped `idf.py
  build`. Raw `esptool.py write_flash` flashes the existing binary; it never compiles. Run
  `idf.py build` before every flash.
- **`ble_gap_ext_adv_params_validate rc=3` on every `configure instance`, then a
  `task_wdt` watchdog reset** — an advertising parameter is illegal (usually
  `SPLINTER_ADV_MS < 20`). `configure` fails, `set_data` cascades, and the error-log flood
  starves the idle task → reset. Raise `SPLINTER_ADV_MS` to ≥ 20 and rebuild.
- **`fatal error: nimble/nimble_port.h: No such file`** — `main/CMakeLists.txt` needs
  `REQUIRES bt nvs_flash` (already set here).
- **`apt` says "Release file ... is not valid yet"** — the system clock is wrong. Fix with
  `sudo date -s "$(curl -sI https://www.google.com | grep -i '^date:' | cut -d' ' -f2-)"`
  then `sudo timedatectl set-ntp true`.

## Classic ESP32 (fallback)

For the classic ESP32-WROVER-E (BT 4.2, one rotated legacy advertiser), using ESP-IDF
v5.4 at `~/esp/esp-idf`:

```bash
. ~/esp/esp-idf/export.sh
cd ~/Projects/splinter
idf.py set-target esp32            # generates sdkconfig from sdkconfig.defaults
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

On real (non-VM) hardware with a working USB-serial bridge, auto-reset works and plain
`idf.py flash` is fine. Serial access needs the `dialout` group
(`sudo usermod -aG dialout "$USER"`, then a fresh terminal or `newgrp dialout`).
