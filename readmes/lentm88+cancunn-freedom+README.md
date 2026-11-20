# cancunn-freedom

Modem-only (`md1img`) SIM-lock evaluation patcher, microMIPS32 pattern scanner, CERT2 signer, and active-slot flash/revert tool for MediaTek-based Motorola devices.

Verified live on **Moto G Power 5G (2024) Tracfone (`XT2415V` / `cancunn`)**, build **`V1UDS35H.26-14-6-2-11`** (`MT6855N` / `NR15.R3.TC2`).

> **Credits & Upstream Projects:**
> Built upon the open-source research, auditing, and CERT2 signing tools from:
> * [andrewwm/vegas-freedom](https://github.com/andrewwm/vegas-freedom) (GNU AGPL-3.0)
> * [Articfox291/kansas-modem-unlock](https://github.com/Articfox291/kansas-modem-unlock) (MIT)

---

## Prerequisites
* **Bootloader already unlocked** (`fastboot getvar securestate` -> `flashing_unlocked`)
* **Root access** (`adb shell su`) for dumping the live `md1img` partition
* Python 3.9+ (standard library only; no external `pip` packages required)
* `adb` and `fastboot` in your system `PATH`

---

## Verified Device Profile (`profiles/cancunn.json`)
* **Model / SKU:** Moto G Power 5G (2024) / `XT2415V` (`cancunn`)
* **Build ID:** `V1UDS35H.26-14-6-2-11`
* **Baseband:** `MT6855N_TC2_SP_V44_P47_05_126R`
* **Stock Trimmed `md1img`:** `69,540,448` bytes (`SHA-256: 88867cb9305f09412f544fa2b40d92c4917a2939ec04de2366bddfe89155ce3f`)
* **Patched Signed `md1img`:** `69,540,544` bytes (`SHA-256: 3c597444764b56a4b7d052700c0687bf0a14d7d6ec128330640dead6977c9c64`)
---
## Warning, Disclaimer & Safety Rules

> **⚠️ WARNING — BRICK RISK & YMMV (Your Mileage May Vary):**
> * Flashing modem partitions via `fastboot` (including the `flash` and `revert` subcommands) **carries an inherent risk of soft-bricking or hard-bricking your device**, especially on untested models, carrier variants, or firmware builds.
> * **Use at your own risk.** While `unlock_modem.py` includes automated `flash` and `revert` wrappers with active-slot and integrity checks, **it is strongly recommended to either execute the `fastboot` commands manually after verifying `current-slot` and `securestate` yourself, or use the automated `flash` / `revert` steps with extreme caution.**
> * Results are strictly **YMMV** — live hardware verification applies only to `XT2415V` (`cancunn`, build `V1UDS35H.26-14-6-2-11`), and behavior on other devices or future OTAs is not guaranteed.

* **Never flash** `preloader`, `gpt`, `lk`, `efuse`, `seccfg`, `nvram`, `nvdata`, `protect1`, `protect2`, or the inactive modem slot.
* Always keep your verified stock backup (`backups/*_stock_trimmed.img`) safe before flashing anything.
* **Manual `fastboot` commands** (if you prefer not to use the automated `flash` / `revert` wrappers):
  ```bash
  fastboot getvar current-slot
  fastboot getvar securestate        # Must be: flashing_unlocked

  # Replace <a|b> with your active slot (e.g., md1img_a or md1img_b):
  fastboot flash md1img_<a|b> work/md1img_<profile_id>_patched.signed.img

  # To revert manually to stock:
  fastboot flash md1img_<a|b> backups/<device>_md1img_<a|b>_stock_trimmed.img

  fastboot reboot
  ```
---

## Quick Start (Default `cancunn` Profile)

### 1. Check Active Slot & Device Status
Shows current active slot (`_a` or `_b`), device SKU, baseband, SIM state, and matching profiles:
```bash
python unlock_modem.py status
```

### 2. Dump Stock `md1img` from Active Slot (`_a` or `_b`)
Automatically detects `ro.boot.slot_suffix`, dumps `/dev/block/by-name/md1img_<slot>`, trims trailing `0x00` padding, and verifies MKIMG + CERT2 integrity:
```bash
python unlock_modem.py dump
```
* Saves raw dump to `backups/<device>_md1img_<slot>_stock.img`
* Saves trimmed stock backup to `backups/<device>_md1img_<slot>_stock_trimmed.img`

### 3. Check Compatibility
Verifies structural/CERT2 integrity and locates the 8 patch sites via `md1_dbginfo` CATI symbols + microMIPS32 bitmask spine matching (works across both `NR15` and `NR17` modem branches):
```bash
python unlock_modem.py check backups/cancunn_md1img_b_stock_trimmed.img
```

### 4. Build, Patch, CERT2-Sign, and Audit
```bash
python unlock_modem.py build backups/cancunn_md1img_b_stock_trimmed.img
```
* Automatically reuses the existing SHA-256-matched trimmed stock backup in `backups/` (avoids duplicate trimmed copies).
* Saves intermediate raw patched image as `work/modem_work/md1img_<profile_id>_patched.raw.img`.
* Saves final signed image as `work/md1img_<profile_id>_patched.signed.img`.
* Verifies `compare_built` (only declared offsets differ) and full `CERT2` integrity (`layout_ok=True integrity=True`).

### 5. Flash to Active Slot Only
Automatically detects `current-slot` (`a` or `b`) in fastboot, verifies `securestate=flashing_unlocked` and that a matching stock backup exists, then flashes **only** the active slot (`md1img_a` or `md1img_b`):
```bash
python unlock_modem.py flash --reboot
```

### 6. Verify After Boot
```bash
adb shell getprop gsm.version.baseband
adb shell getprop gsm.sim.state
adb shell getprop vendor.gsm.sim.slot.lock.device.lock.remain.count
```
Expected: baseband intact, `gsm.sim.state=LOADED`, `remain.count=5`.

### 7. Revert to Stock (One Command)
Detects active slot (`a` or `b`), verifies the stock backup in `backups/` via `audit_image`, and flashes it back:
```bash
python unlock_modem.py revert --reboot
```

---

## Using a New / Custom Profile (Multi-Device Workflow)

When working with a different device, carrier build, or newer OTA:

1. **Dump the stock modem** from the device:
   ```bash
   python unlock_modem.py dump
   ```
2. **Run `check --emit-profile`** to auto-scan CATI symbols + microMIPS32 bitmask patterns and generate a new profile JSON:
   ```bash
   python unlock_modem.py check backups/<device>_md1img_<slot>_stock_trimmed.img --emit-profile profiles/new_device.json
   ```
3. **Build** using `--profile`:
   ```bash
   python unlock_modem.py build --profile profiles/new_device.json backups/<device>_md1img_<slot>_stock_trimmed.img
   ```
4. **Flash** using `--profile` (selects `work/md1img_new_device_patched.signed.img` and verifies the matching stock backup):
   ```bash
   python unlock_modem.py flash --profile profiles/new_device.json --reboot
   ```
5. **Revert** using `--profile` (selects the exact stock backup in `backups/` matching `new_device.json`'s SHA-256):
   ```bash
   python unlock_modem.py revert --profile profiles/new_device.json --reboot
   ```

> **Multi-image safety:** If multiple `.signed.img` or stock backups exist in `work/` or `backups/` and `--profile` is omitted, `flash` and `revert` attempt to match the connected device via ADB/Fastboot properties and will refuse to proceed if the target image is ambiguous.

---

## Audit Any `md1img` File Standalone
```bash
python unlock_modem.py audit work/md1img_cancunn_patched.signed.img
```

---

## License & Modifications
This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**, following upstream [andrewwm/vegas-freedom](https://github.com/andrewwm/vegas-freedom). Helper modules originally from [Articfox291/kansas-modem-unlock](https://github.com/Articfox291/kansas-modem-unlock) retain their original MIT copyright notices.

**Summary of modifications in `cancunn-freedom` (2026-11):**
* Removed bootloader/GSI components to focus exclusively on modem (`md1img`) workflows (`unlock_modem.py`).
* Added `profiles/cancunn.json` for Moto G Power 5G 2024 `XT2415V` (`MT6855N`, build `V1UDS35H.26-14-6-2-11`).
* Added microMIPS32 bitmask spine scanning in `smu_check_sml` to support both `NR15` and `NR17` modem branches (`--emit-profile`).
* Updated `imageaudit.py` (`compare_built`) to permit declared patch entries where individual bytes happen to equal their replacement value (e.g., `0xcab162` in `cancunn`).
* Added dynamic A/B active slot detection, per-command subprocess timeouts, stock-trimmed backup reuse, profile-scoped `modem_work` outputs, and multi-profile safe `flash` / `revert` commands.
