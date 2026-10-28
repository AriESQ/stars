# usb-macos-vm

`VZUSBPassthroughDevice` (macOS 27) for embedded development — capturing a physical debug probe
from the host and handing it to a Linux guest so `probe-rs` can flash and debug real hardware
from inside the VM.

A worked example, built without Xcode, of the whole chain: the restricted entitlement, the
signing, the AccessoryAccess handshake, the guest, and the attach. Along the way it documents
several requirements that are not written down anywhere, and two bugs filed with Apple
(**FB24018643**, **FB24018667**).

## Status

**Working end to end on macOS 27.0 (`26A428`).** A SEGGER J-Link is captured from macOS,
passed through to the Linux guest, and drives a Nordic Thingy:91 over SWD from inside the VM.
First working on beta 5 (`26A5406e`); re-verified on the release build on 2026-09-14, built
with both the Command Line Tools 27.0 SDK and Xcode 27.0 (`27A266`).

<img src="docs/menu-extra.png" alt="The Virtual Machine Accessories menu bar item, listing a J-Link with 'Use with usb-macos-vm' checked and 'Use with this Mac' below it" width="500">

That menu extra is the handover. It is also the thing that never appeared on beta 4 — see
[the beta 4 blocker](#the-beta-4-blocker).

| Phase | State |
|---|---|
| 0 — signing gate | ✅ **passed** — needs a provisioning profile; capability is listed as *Claim USB Accessory*. See [FINDINGS.md](FINDINGS.md) |
| 1 — enumerate probes | ✅ **done** — requires beta 5 or later; see [the sandbox bug](#the-beta-4-blocker) |
| 2 — Linux guest VM | ✅ **done** — Ubuntu 26.04 arm64, SSH, XHCI controller live |
| 3 — attach probe | ✅ **done** — J-Link captured exclusively by the VM, enumerated in the guest |
| 4 — probe-rs in guest | ✅ **done** — `probe-rs` reads live silicon over SWD |

`com.apple.security.virtualization` works with an ad-hoc signature, so the VM half needs no paid
account. `com.apple.developer.accessory-access.usb` does not — it needs an Apple Development
certificate and a provisioning profile, obtainable without Xcode.

## Requirements

- **macOS 27.0 (`26A428`).** Beta 5 (`26A5406e`) is the earliest seed that works — see
  [the beta 4 blocker](#the-beta-4-blocker).
- **A macOS 27.0 SDK** — the Command Line Tools or Xcode 27. The 26.x SDKs have no
  AccessoryAccess framework.
- **A paid Apple Developer membership.** `com.apple.developer.accessory-access.usb` is a
  restricted entitlement and needs a real certificate and provisioning profile. Xcode is not
  required; `scripts/import-identity.sh` does the whole chain with `openssl` and `security`.
- Apple silicon, and a USB debug probe.

`ProjectPaths.swift` defaults to `/Users/jberi/code/usb-macos-vm` because the sandbox grants
access by absolute path. Set `USB_MACOS_VM_ROOT` and edit the matching
`com.apple.security.temporary-exception.files.absolute-path.read-write` entry in
`Resources/vmhost.entitlements` to run it from elsewhere.

## Quick start

```bash
brew install qemu                  # for qemu-img
scripts/prepare-guest.sh           # qcow2 -> raw, resize, build cloud-init seed
BUNDLE_ID=<your App ID> scripts/vm.sh && open build/VMHost.app
scripts/ssh.sh lsusb               # once cloud-init finishes (~60s on first boot)
```

Then assign a probe to the VM from the **Virtual Machine Accessories** menu bar item; it is
attached automatically and appears in the guest.

The Ubuntu cloud image is not in the repo. Fetch it into `vm/ubuntu.qcow2` first:

```bash
curl -Lo vm/ubuntu.qcow2 \
  https://cloud-images.ubuntu.com/releases/resolute/release/ubuntu-26.04-server-cloudimg-arm64.img
```

## Layout

```
Sources/Common/      Log.swift, USBDescriptor.swift          shared
Sources/ProbeGate/   the Phase 0 entitlement gate            4 signing variants
Sources/VMHost/      the Linux guest host app                VMBuilder + AppKit shell
scripts/bundle.sh    build a ProbeGate variant (A|B|C|D)
scripts/vm.sh        build VMHost.app
scripts/prepare-guest.sh   disk conversion + cloud-init seed
scripts/ssh.sh       ssh into the guest
scripts/guest-ip.sh  resolve the guest IP from vmnet DHCP leases
scripts/console.sh   interactive serial console (screen)
scripts/console-run.py     run one command on the serial console
vm/                  disk images, keys, console log          gitignored
```

## Guest

Ubuntu 26.04 LTS aarch64, kernel 7.0.x, 4 vCPU / 4 GB / 30 GB disk, NAT networking.
Login user matches the host username, key at `vm/id_ed25519`; root autologin on the serial
console as a fallback if sshd is ever down.

Captured devices arrive on the XHCI controller. `probe-rs` is installed to `/usr/local/bin`
from the upstream `aarch64-unknown-linux-gnu` release, with probe-rs's udev rules in
`/etc/udev/rules.d/69-probe-rs.rules` and the login user in `plugdev`, so no `sudo` is needed:

```bash
scripts/ssh.sh 'probe-rs list'
scripts/ssh.sh 'probe-rs read --chip nRF9160_xxAA b32 0x00000000 4'
```

## Gotchas worth knowing

- **The 26.04 cloud image ships without `openssh-server`.** It must be in the cloud-init
  `packages:` list or the guest is unreachable over the network.
- **cloud-init only re-applies user-data when `instance-id` changes.** `prepare-guest.sh`
  bumps a serial on every run so edits actually take effect.
- **The serial PTY needs a reader or the guest stalls mid-boot.** `VMBuilder` owns the
  replica and drains it to `vm/console.log`; nothing else should read that tty.
- **`guest-ip.sh` matches on hostname, not MAC.** systemd-networkd sends an RFC 4361 client
  identifier, so the lease's `hw_address` is a DUID and MAC matching finds only stale leases.
- **`no such module 'AccessoryAccess'` means the wrong SDK is selected.** `swiftc` follows
  `xcode-select`, so an older Xcode left selected (26.x) wins over a newer Command Line Tools
  SDK. Install Xcode 27, or build with `DEVELOPER_DIR=/Library/Developer/CommandLineTools`.
- **Quitting VMHost with the guest running can hang.** On 27.0 an AppleEvent quit timed out
  and the app had to be killed; the guest disk survived and rebooted cleanly.

## End-to-end result

Assignment is user-driven by design: the **Virtual Machine Accessories** menu extra
([above](#status)) appears in the menu bar once a listener is registered, and the device is
handed over by picking the host app from its *Use with…* submenu. There is no API to request this.

On beta 5 the choice did not appear to persist across launches. On 27.0 it did: after one
assignment, every later launch of an app with the same bundle ID (VMHost, and ProbeGate
variants C and E) was handed the J-Link at registration with no further click — including
the unsandboxed variant C. Not yet tested across a replug, logout or reboot.

```
AA[vm]: ▶ accessory CONNECTED
  registryID=0x1000013bb  1366:0101  |  SEGGER (J-Link)
attach: ✓ 0x1000013bb captured — controller now holds 1 device(s)
```

| Where | Evidence |
|---|---|
| Host | capture is exclusive — IORegistry `UsbExclusiveOwner` is `com.apple.Virtualization.VirtualMachine`. On beta 5 the device vanished from `system_profiler`; on 27.0 it is still listed there |
| Guest | `Bus 003 Device 002: ID 1366:0101 SEGGER J-Link PLUS` |
| Guest kernel | `usb 3-1: New USB device found, idVendor=1366, idProduct=0101`, serial `000801032667` |
| probe-rs | `[0]: J-Link -- 1366:0101:000801032667` |
| Target | `probe-rs read --chip nRF9160_xxAA b32 0x00FF0140 2` → `0x00009160`; variant register `SICA` on beta 5, `0x00413142` on 27.0 |

The part code reads `0x9160` on both runs; the variant register differs.

`probe-rs info` cannot auto-identify the nRF9160 and reports *"The connected chip could not
automatically be determined"* — pass `--chip nRF9160_xxAA` explicitly. This is a probe-rs
limitation, unrelated to passthrough; memory reads over the same connection succeed.

## The beta 4 blocker

On `26A5388g` a correctly entitled app registered an `AAUSBAccessoryListener` successfully and the
system then never offered any device for assignment. The cause is fixed in beta 5:

> Fixed: Accessory Access does not work inside App Sandbox. (176815987)

There was no working configuration on beta 4. Sandboxed hit that bug; unsandboxed left
`com.apple.security.device.usb` inert, because it is a *sandbox* entitlement and does nothing
without `com.apple.security.app-sandbox`. Filed as **FB24018667**, now resolved.

**FB24018643 is still open, and unfixed in the 27.0 release (`26A428`)** —
`AAUSBAccessoryMatchingCriteria` rejects every documented way of building its matching
dictionary and accepts only the legacy `IOProviderClass = "IOUSBDevice"`.
The workaround in `KnownProbes.swift` is still load-bearing. Both are written up in
[FEEDBACK.md](FEEDBACK.md).

Requirements discovered the hard way, none of them documented:

- `com.apple.developer.accessory-access.usb` is listed in the developer portal as
  **"Claim USB Accessory"**, not by its documented name.
- `com.apple.security.device.usb` is also required — a sandbox entitlement, so it implies
  `com.apple.security.app-sandbox`. Found via
  [forums thread 831902](https://developer.apple.com/forums/thread/831902).

## License

Apache 2.0 — see [LICENSE](LICENSE).
