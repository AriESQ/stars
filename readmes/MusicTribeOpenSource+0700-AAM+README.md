<p align="center">
  <img src="docs/images/social-preview.png" alt="Behringer KICK (BE 0700-AAM)" width="100%">
</p>

# Behringer KICK (BE 0700-AAM)

Source code for the Behringer KICK.

<p align="center">
  <img src="docs/images/kick-front.webp" alt="Behringer KICK" width="720">
</p>

## Key features

- AI camera for gesture control
- Touchscreen
- 16 RGB pads, 8 banks
- Sampler with sample editing, step sequencer and looper
- Over 300 built-in effects
- 4 assignable knobs and a jog wheel
- MIDI in/out, USB and 4 CV / Gate jacks

## Connections

<p align="center">
  <img src="docs/images/kick-rear.webp" alt="Behringer KICK rear panel" width="100%">
</p>

| Rear | Front |
|---|---|
| 12 V DC power input, power switch | SD card slot |
| LINK (RJ45) | Headphones output |
| USB-C, USB-A | |
| MIDI IN, MIDI OUT (5-pin DIN) | |
| Stereo output, stereo input | |
| CV / Gate (4 jacks) | |

## Repository

| Folder | Contents | License |
|---|---|---|
| [`Kick/`](Kick) | Application | AGPL-3.0-or-later |
| [`AudIO/`](AudIO) | Audio engine library | AGPL-3.0-or-later |
| [`ComProtocol/`](ComProtocol) | Hardware communication protocol | AGPL-3.0-or-later |
| [`Linux/`](Linux) | Buildroot Linux image | GPL-2.0 (Buildroot) |

The root [`LICENSE`](LICENSE) is the AGPL-3.0 text that covers the Music Tribe code (Kick, AudIO, ComProtocol).
Third-party components keep their original licenses. See the README in each folder.

## Community

- **Chat with us:** [Discord](https://discord.gg/gS6qtuShvw)
- **Contribute:** fork the repository and open a pull request. No membership needed. See the
  [contributing guide](https://github.com/MusicTribeOpenSource/.github/blob/main/CONTRIBUTING.md).
- **Report a security problem** privately: [Report a vulnerability](https://github.com/MusicTribeOpenSource/0700-AAM/security/advisories/new).

<details>
<summary>Product renders</summary>

<p align="center">
  <img src="docs/images/views.png" alt="KICK top, front, side and rear views" width="100%">
</p>
</details>

---

Behringer is a brand of MUSIC Tribe. The Behringer name and logo, and the KICK name and logo, are
trademarks and are not covered by the software licenses in this repository.

Copyright (c) MUSIC Tribe.
