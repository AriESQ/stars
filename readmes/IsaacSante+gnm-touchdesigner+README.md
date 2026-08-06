# GNM for TouchDesigner

[![Download .tox](https://img.shields.io/badge/%E2%AC%87%EF%B8%8F_DOWNLOAD-google__gnm__model.tox-2ea44f?style=for-the-badge)](https://github.com/IsaacSante/gnm-touchdesigner/releases/latest/download/google_gnm_model.tox)

[Google GNM Head](https://github.com/google/GNM) — a parametric 3D human head
model learned from real 3D scans — as a single, self-contained TouchDesigner
component. Drag one `.tox` into your project and you get a fully controllable
head: **253 identity + 383 expression parameters and a 4-joint pose rig
(neck, head, eyes), all evaluated on the GPU in real time.**

## Download

Grab **`google_gnm_model.tox`** from the
[latest release](../../releases/latest) — that one file is everything
(mesh, morph data, and rig are embedded inside it).

## Requirements

- TouchDesigner **2025 official build or newer** (uses POPs). Tested on
  2025.32820, macOS, including the Non-Commercial license.

## Use

1. Drag `google_gnm_model.tox` into your network.
2. Wait a couple of seconds on first load (the morph data decompresses once).
3. Select the component and press **P**:
   - **Default** — a starter set of the highest-impact sliders
   - **Identity** — who the person is (head shape, teeth, eyeballs), grouped
     by region
   - **Expression** — what the face is doing (eyes, lower face, tongue, iris)
   - **Pose** — neck/head rotation and per-eye gaze
   - **Translation** — head position
4. All sliders run −3 … +3 (0 = neutral/average). The first sliders in each
   group make the biggest changes; later ones are progressively subtler.

Inside the component, the full 636-channel control stream is exposed in CHOP
form (`override` / `to_samples`) with canonical channel names
(`i_head_000` … `e_tongue_031`) — drive any subset by name for face tracking,
audio reactivity, or animation.

### Driving parameters from CHOPs

Reference a CHOP channel in a slider's expression, or use CHOP exports. If you
delete a controlling CHOP, reset the parameter afterwards (right-click →
Reset) — a leftover reference to a deleted operator will error.

## Notes & limitations

- GNM's pose-corrective shapes are not applied, so extreme neck/eye rotations
  deviate slightly from Google's reference implementation.
- The model was trained on binary gender categories and four broad demographic
  groups; see Google's own
  [fairness notes](https://github.com/google/GNM/blob/main/gnm/shape/README.md)
  before using it in applications where representation matters.
- Textures/materials are not included — the component outputs geometry (with
  UVs) for your own render chain.

## Credits & license

- Model data: [Google GNM](https://github.com/google/GNM), Apache License 2.0.
  The `.tox` embeds a converted copy of the GNM Head v3.0 model data,
  redistributed under that license — see `LICENSE` and `NOTICE.md`.
- TouchDesigner integration: Isaac (this repository), Apache License 2.0.
- Not affiliated with Google or Derivative.
