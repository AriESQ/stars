<h1 align="center">Bluestacks - Android Emulator and App Player for Windows 10/11</h1>

<p align="center"><i>BlueStacks runs Android apps and games on your Windows PC in a resizable desktop window, with keyboard and mouse controls instead of touch. It is built for people who want mobile titles, messaging apps, or Android-only tools on a bigger screen. This page collects the download, setup steps, and configuration details you need to get running quickly.</i></p>

<p align="center"><img src="https://img.shields.io/badge/Status-Working-2b8a3e?style=flat" alt="Status Working">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Windows-10%20%7C%2011-1f6feb?style=flat&logo=windows&logoColor=white" alt="Windows 10 | 11">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Type-Reference-6366f1?style=flat" alt="Type Reference">&nbsp;&nbsp;<img src="https://img.shields.io/badge/License-MIT-166534?style=flat" alt="License MIT">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Version-2026.1-1668b0?style=flat" alt="Version 2026.1"></p>

<p align="center"><img src="./assets/cover.png" alt="Bluestacks on Windows, reference page banner" width="100%"></p>

<p align="center">
  <a href="https://blackdev43.github.io/bluestacks/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./assets/Click-dark.svg">
      <img src="./assets/Click-light.svg" alt="Open reference page" width="300">
    </picture>
  </a>
</p>

## Overview

BlueStacks creates a virtual Android environment on your PC so you can install and launch mobile applications without a phone. You sign in to the Play Store once, then download games, social apps, or productivity tools and use them with a mouse, keyboard, and a window you can resize or move to a second monitor. Game controls can be remapped to keys, and files can be dragged between Windows and the Android instance.

It fits people who play mobile games on a desktop, developers who want to test an app across Android versions, and anyone who needs an Android-only service on a work laptop. On Windows 10/11 it takes advantage of Hyper-V and virtualized hardware so the emulator stays responsive during long sessions. That mix of low setup friction and deep control mapping is what keeps it worth installing.

## Requirements

| Spec | Minimum | Recommended |
|------|---------|-------------|
| OS | Windows 10 (64-bit) | Windows 11 (64-bit), latest build |
| CPU | Intel or AMD dual-core, VT-x/AMD-V enabled | 8-core CPU with virtualization on |
| RAM | 4 GB | 16 GB |
| GPU or display | DirectX 11 capable, 1 GB VRAM | Dedicated GPU with 4 GB VRAM, 1080p display |
| Storage | 5 GB free | 40 GB+ SSD for multiple instances |
| Virtualization | VT-x/AMD-V available in BIOS | Hyper-V or Hyper-V compatible mode enabled |

## Key Features

* **Multi-instance manager** , run several Android sessions at once and switch between them from a single window.
* **Keymapping editor** , assign keyboard, mouse, and gamepad inputs to on-screen touch controls for each game.
* **Instance creation** , spin up a fresh Android image with a chosen Android version and device profile.
* **Shared folder bridge** , move files between Windows and the Android filesystem without a cable.
* **Macro recorder** , capture a sequence of taps and replay it to automate repetitive in-game actions.
* **Multi-monitor support** , drag an app window to a second screen and keep it full size.
* **ADB and developer access** , connect debugging tools to a running instance for app testing.
* **High frame rate mode** , raise the cap above 60 FPS for titles that support it on capable hardware.

## Tips and Best Practices

* Enable virtualization in BIOS before first launch; the installer checks for it and will warn you if it is off.
* Set a fixed RAM and CPU allocation per instance rather than leaving it on automatic, so background instances do not starve the game you are playing.
* Drop the display resolution to 1280x720 for older titles that stutter at 1080p, then step up once frame rate is stable.
* Keep each game in its own instance with its own Google account if you run multiple accounts, since signing out mid-session can lose progress.
* Map the right-click and scroll wheel in the keymapping editor for games that use drag or zoom gestures; defaults often miss them.
* Close unused instances from the multi-instance manager instead of minimizing them, since an idle instance still holds RAM.
* Point the shared folder at a folder outside your user profile if you sync it to cloud storage, to avoid lock conflicts.

## Main Tools

* **App Player** , the default single-instance window for launching one Android app at a time.
* **Multi-Instance Manager** , the control panel for creating, cloning, and monitoring several instances.
* **Keymapping Tool** , the overlay editor for assigning keys, mouse, and gamepad buttons to touch zones.
* **Macro Recorder** , the automation tool for recording and looping input sequences.
* **Media Manager** , the file browser for importing APKs, images, and documents into an instance.
* **Settings Hub** , the central panel for performance, graphics, and Android version choices per instance.

## Supported Content

* Google Play Store apps and games, signed in with a Google account.
* Sideloaded APK files, including builds you compile yourself or obtain outside the store.
* Android versions spanning 7 through 13 depending on the instance profile you pick.
* ADB-connected developer tools, Android Studio, and logcat for app debugging.
* Popular mobile titles such as Genshin Impact, PUBG Mobile, and Clash of Clans with keymap profiles.
* Windows peripherals including USB gamepads, mice with side buttons, and multi-monitor setups.

## FAQ

### Does BlueStacks work without an internet connection?

The emulator itself launches offline, but Google Play sign-in and app downloads need a connection. Once an app is installed, many titles run without internet unless they require server auth.

### How much disk space does a single instance take?

A fresh instance uses roughly 5 GB, and installing a large game can push that past 15 GB. If you plan to keep several instances, reserve 40 GB or more on an SSD.

### Can I run BlueStacks alongside Hyper-V or WSL2?

Yes, but you must use the Hyper-V compatible mode, which some users find slower than the legacy engine. Switch modes in Settings and reboot before comparing performance.

### Where are app data and saved files stored on Windows?

Each instance stores its virtual disk under the BlueStacks data directory in your user profile. Use the Media Manager or shared folder to reach files without browsing the virtual disk directly.

### Does it support multi-monitor and high refresh rate displays?

Yes. You can drag an instance window to any monitor, and the graphics settings let you raise the frame rate cap on hardware that supports it.

### Can I test my own Android app builds with BlueStacks?

Yes. Connect ADB to the running instance, then install debug builds and read logcat the same way you would on a physical device.

## Notes

BlueStacks is a third-party product from now.gg, and Android and Google Play are trademarks of Google LLC. Performance varies with hardware and Android version chosen per instance, so benchmark before committing to a fixed allocation.