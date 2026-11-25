# esp32-usb-wifi

ESP32-S3 port of [pico-usb-wifi](https://gitlab.com/baiyibai/pico-usb-wifi): a driverless USB Wi-Fi
adapter (USB CDC-NCM device bridging to a Wi-Fi station).

Speeds are max USB 2.0 full speed. Speedtests show speeds of roughly 5.7Mbps.

![speedtest](images/speedtest.png)

Seeded from Espressif's `tusb_ncm` example (ESP-IDF v5.5,
`examples/peripherals/usb/device/tusb_ncm`, Unlicense/CC0.

* station MAC adoption + raw L2 forwarding (`esp_wifi_internal_*`, no `esp_netif`)
* reflection filter (drops the host's own frames echoed back by the AP)
* host IPv4/IPv6 snooping (the device holds no IP; the console reports the host's)
* **management console** on CDC-ACM (composite NCM + ACM): up to 8 credential
  _profiles_ in NVS (`set ssid`/`set pass` edit the active one, `list`/`use`/`del`
  manage the set), `scan` + `join <n>` to discover and stage networks, and
  `set debug on` for a 2 s stats stream (`dbg:`-prefixed) with association
  events and failure reasons (`badauth`/`nonet`). Changes apply immediately;
  `save` persists. Compile-time creds are only a never-provisioned fallback
* `tools/provision.py <ssid> [password]` — scripted provisioning over the console
* **automatic recovery with crash telemetry**: the task watchdog panics and
  reboots instead of hanging, and the tallies survive the warm reboot; see
  <a href="#automatic-recovery">Automatic Recovery</a>
* **status LED** on the board's WS2812, runtime-movable to any pin; see
  <a href="#status-led">Status LED</a>

## Provisioning

Provisioning is possible through three ways:

```sh
. ~/esp/esp-idf/export.sh          # or: pip install pyserial
tools/provision.py "MyNetwork" "hunter2"
```

Or interactively: `picocom /dev/cu.usbmodem1234561` (any baud), then `help`.

Or through a Python TUI.

```
uv run tools/tui.py
```

## Build

```sh
. ~/esp/esp-idf/export.sh
cp wifi_creds.defaults.example wifi_creds.defaults   # edit SSID/password
SDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.defaults.esp32s3;wifi_creds.defaults" \
  idf.py set-target esp32s3 build
```

(Changing credentials later: edit `wifi_creds.defaults`, delete `sdkconfig`,
re-run the build command — or just use `idf.py menuconfig` → Example
Configuration.)

## Flash and monitor

```sh
idf.py -p /dev/cu.usbmodem101 flash monitor
```

Note: the firmware takes over the S3's only USB port with the OTG peripheral
(NCM device), so after first flash the serial-JTAG console disappears and the
board re-enumerates as a USB network interface. To reflash, hold BOOT while
plugging in (download mode), then run the flash command again.

## What you should see on the host

The Mac/Linux host gets a new network interface (CDC-NCM, in-box driver) whose
MAC is the S3's Wi-Fi station MAC; once the station associates, DHCP on that
interface yields an address from the AP's own subnet.

## Automatic Recovery

If the firmware ever hangs or crashes, it recovers on its own instead of
sitting dead until a replug: the task watchdog is configured to panic, and a
panic reboots the chip, which re-enumerates and re-associates within a few
seconds.

The diagnostic trail survives the reboot. A crashlog in RTC noinit RAM (which
warm resets do not clear) holds the boots/hangs/faults tallies and a
once-per-second snapshot of the bridge counters, so after a recovery `show`
reports what the bridge was doing just before it died:

```
    health:    boots=3 hangs=1 faults=0
    RECOVERED from watchdog this boot; pre-crash ->wifi=4499 ->host=4004 ...
```

`boots` counts warm reboots since the last cold power-on; `hangs` are watchdog
recoveries, `faults` are panic recoveries. A cold power-on (replug) resets all
three — that is how you distinguish "recovered overnight" from "freshly
plugged in".

The path is self-testable: `crash` on the console faults on purpose (panic →
`faults`), `hang` spins until the task watchdog fires (~5 s → `hangs`). Either
way the device drops off USB, reboots, re-enumerates, and re-associates by
itself — no replug — and the next `show` carries the RECOVERED report.

## Status LED

The board's WS2812 LED mirrors the pico firmware's states:

| Pattern           | Meaning                                          |
|-------------------|--------------------------------------------------|
| Solid             | Associated — the normal running state            |
| Slow blink (1 Hz) | Wi-Fi configured, associating                    |
| Fast blink (5 Hz) | No Wi-Fi configured — provision over the console |
| Off               | USB not ready                                    |

The data pin varies between S3 boards (48 on ESP32-S3-DevKitC-1 v1.0, 38 on
v1.1, 35 on some third-party boards) and a wrong pin fails silently, so the
pin is runtime-configurable: `set led <gpio>` on the console moves it live and
persists it in NVS — try pins until the LED reacts, no reflash needed. The
compile-time default is `idf.py menuconfig` → Example Configuration.
