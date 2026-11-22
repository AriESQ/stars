# Moto G Power 2026 Straight Talk WiFi and persistent root guide

This guide documents a successful setup of a **Walmart Straight Talk Moto G Power 2026, XT2617V**, as a Wi-Fi gaming and app device **without purchasing or activating a Straight Talk plan**. It covers skipping the service activation setup, unlocking the bootloader with Val Protocol, installing persistent Magisk root, and reversibly hiding carrier and update apps.

**Verified on one phone on November 14, 2026. This is an experimental, firmware-specific procedure, not a guarantee for every XT2617V.** Bootloader modification can leave a phone unable to reach Fastboot. Backups do not constitute a guaranteed unbrick method.

## Start here

| Resource | Purpose |
| --- | --- |
| [Full step by step guide](GUIDE.md) | Prerequisites, commands, checkpoints, recovery limits, and post-root maintenance |
| [Reddit post](REDDIT_POST.md) | Copyable introduction and directions to this repository |
| [Latest release](https://github.com/parsimo2010/moto-g-power-2026-straight-talk-wifi-root-guide/releases/latest) | Guide kit ZIP, including the small helper and Magisk modules |
| [Carrier package manifest](carrier-debloat-manifest.json) | Exact 22 packages and APK directories hidden on the tested build |
| [Source and verification notes](VALIDATION.md) | What was actually tested and what remains unverified |

## Exact tested phone

| Item | Tested value |
| --- | --- |
| Retail model | Moto G Power 2026, Straight Talk, Walmart |
| Hardware model | XT2617V |
| Part number | XT2617VSS1PP |
| Box product code | STMXT2617VSSPWP |
| Bootloader product | vegas XT2617V 128 GB PVT |
| Android device name | vegas26 |
| Android | 16 |
| Build | W1WEOS36.48-22-3-3-4-2 |
| Security patch | 2026-04-01 |
| Kernel | 5.15.180-android13-8-00018-g9b2308ac0ad6-ab14563692 |
| Bootloader | MBM-3.1-vegas_og_vext-5d518d-W1WEOS36.48-22-3-3-4-2-36210f |
| CID | 0x0033, decimal 51 |
| Slot used | a |

**Do not substitute the Moto G Play, regular Moto G, Power 2025, a retail XT2617-1, or a different firmware build.** If your values differ, stop treating these instructions as validated for your phone.

## Result on the tested phone

- Android setup completed without buying a carrier plan.
- Test DPC's management role was cleared and its app uninstalled.
- Bootloader unlock confirmed with `securestate: flashing_unlocked`.
- Magisk 31.1 root verified after multiple full reboots, without DFRoot or KernelSU running.
- Google account sign-in, Play Store launch, and validated Wi-Fi internet worked.
- Motorola Software Update hidden through the reversible `wifi_ota_guard` module.
- Twenty-two carrier/finance APK packages hidden through `wifi_carrier_debloat`; Android's device-lock controller disabled separately.
- No active device administrator, financed-device-controller role holder, targeted carrier process, or updater restart alarm remained at verification time.

This retains stock Motorola Android. No custom ROM was installed. It does not establish a cellular SIM/network unlock, universal game compatibility, a measurable performance improvement, or immunity to every undocumented firmware restriction.

## What is included

The kit contains original helper source, a small compiled Android helper, module ZIPs, the module generator, and documentation. It contains **no firmware images, rooted boot images, APK installers, serial numbers, IMEIs, account data, or unlock keys**. Obtain third-party programs from their upstream links and back up/patch **your own phone's** images.

“Persistent root” here means root starts after a normal reboot. It does not mean root survives a firmware replacement, factory reset, Magisk removal, bootloader relocking, or every future software change.
