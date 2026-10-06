# FM-1 Transporter

Read and write the flash of the **M-VAVE FM-1** (JieLi AC791N / WL82) from a Mac, through a Seeed XIAO RP2040 wired to the FM-1's USB lines.

Seeed XIAO RP2040 を FM-1 の USB 信号線につなぎ、Mac から FM-1 の Flash を読み書きするツールです。

```
Mac ──USB──► XIAO RP2040 ──D+ / D- / GND──► FM-1
```

## Features / 機能

- Enter the mask-ROM UBOOT: by USB_KEY at power-on or after a watchdog reset, or by USB-MIDI soft key from stock V15
  マスク ROM の UBOOT に入る（電源投入時・ウォッチドッグリセット後は USB_KEY、純正 V15 からは USB-MIDI ソフトキー）
- Read chip info and dump the full 1 MiB flash in about 3 s
  チップ情報の取得と、1 MiB の Flash の全読み出し（約 3 秒）
- Write only the 4 KiB sectors that changed, verifying each one
  変更のあった 4 KiB セクタだけを書き込み、セクタごとに検証
- Load and run code in RAM (for research)
  RAM 上でのコード実行（研究用）

## Hardware / ハードウェア

Use a **Seeed XIAO RP2040**. Connect three wires only:
**Seeed XIAO RP2040** を推奨します。3 本だけ接続してください。

| XIAO RP2040 | FM-1 USB |
|---|---|
| D6 (GP0) | D+ |
| D7 (GP1) | D- |
| GND | GND |

**Do not connect VBUS.** The FM-1 runs on its battery.
**VBUS（5V）は接続しないでください。** FM-1 は内蔵バッテリーで動作します。

| Board / ボード | Status / 対応 |
|---|---|
| Seeed XIAO RP2040 | ✅ Recommended / 推奨 |
| Other RP2040 boards / その他の RP2040 ボード | ⚠️ Untested / 未検証 |
| Waveshare RP2350-USB-A | ❌ Not supported / 非対応 |

The Waveshare RP2350-USB-A doesn't work because RP2350 rev A2 has the GPIO pull-down erratum (E9), D+ has a 1.5 kΩ pull-up, and the USB-A port always outputs VBUS.
RP2350-USB-A は、RP2350 A2 の GPIO プルダウン不具合（E9）、D+ の 1.5 kΩ プルアップ、常時出力される VBUS のため使えません。

## Build / ビルド

You need pico-sdk 2.2.0, an ARM GCC toolchain, CMake and picotool. Get `wl82loader.bin` from [jl-uboot-tool](https://github.com/kagaimiq/jl-uboot-tool). It is not included in this repository.
pico-sdk 2.2.0、ARM GCC、CMake、picotool が必要です。`wl82loader.bin` は同梱していないので、jl-uboot-tool から用意してください。

```bash
git submodule update --init
```
```bash
cmake -S . -B build -DPICO_SDK_PATH=$HOME/pico-sdk -DPICO_BOARD=seeed_xiao_rp2040 -DFM1T_LOADER_BIN=/path/to/wl82loader.bin
```
```bash
make -C build -j8
```
```bash
picotool load -f -x build/fm1_transporter.uf2
```

## Usage / 使い方

First get the FM-1 into UBOOT. If stock V15 is running, `fm1t.py` does it by itself. Otherwise power the FM-1 on while the XIAO is connected.
まず FM-1 を UBOOT に入れます。純正 V15 が動いていれば自動で入ります。そうでなければ、XIAO を接続した状態で FM-1 の電源を入れてください。

`tools/fm1t.py` requires pyserial.
`tools/fm1t.py` には pyserial が必要です。

```bash
python3 tools/fm1t.py info
```
```bash
python3 tools/fm1t.py dump backup.bin
```
```bash
python3 tools/fm1t.py write --package FM-1_vNN.fwsc --ref backup.bin --write
```

Without `--write`, `write` only checks and changes nothing.
`write` は `--write` を付けない限り確認だけ行い、何も書き込みません。

## Cautions / 注意事項

- Use at your own risk. Always keep a dump before writing.
  自己責任で使用してください。書き込む前に必ずダンプを保存してください。
- Only `0x4000`–`0x93000` is ever written. The bootloader area and device data are never touched.
  書き込むのは `0x4000`–`0x93000` だけです。ブートローダー領域と機器データには書き込みません。
- To use the FM-1 over USB again after a session, power-cycle it.
  作業後に FM-1 を USB で使うときは、電源を入れ直してください。
- Not affiliated with M-VAVE or JieLi.
  M-VAVE および JieLi とは無関係です。

## Docs / ドキュメント

[Architecture](docs/ARCHITECTURE.md) · [Protocol](docs/PROTOCOL.md) · [Development log](docs/DEVLOG.md)

## License / ライセンス

MIT. Includes [Pico-PIO-USB](https://github.com/sekigon-gonnoc/Pico-PIO-USB) (MIT). Some routines are ported from [jl-uboot-tool](https://github.com/kagaimiq/jl-uboot-tool) (MIT).
MIT ライセンスです。Pico-PIO-USB（MIT）を含み、一部の処理は jl-uboot-tool（MIT）から移植しています。
