# Textport

A tiny, native Android app that reads the **SMS messages stored on your device**
and exports them to a file you save yourself. It's a personal backup tool meant
to be **sideloaded** — see the [Google Play caveat](#google-play-caveat) below.

Textport never uploads anything. Messages are read from the system SMS provider,
formatted on-device, and written to a location **you** pick via the Android file
picker. There is no network code.

## Features

- Read both **SMS** (`Telephony.Sms`) and **MMS** (`Telephony.Mms`, including
  each message's text parts and addresses) with the `READ_SMS` runtime
  permission, off the main thread. Every SMS box is read — inbox, sent, draft,
  outbox, and importantly **failed / queued** — and MMS is included because a
  text that fails to a number that can't receive it is frequently stored as an
  MMS in the outbox, not as an SMS. Reading MMS needs only `READ_SMS`; Textport
  never has to be your default SMS app.
- **Grouped by conversation**, like a messaging app: the main screen lists
  threads (contact/number, latest message, message count, and an "unsent" badge
  when a thread contains failed/queued/outbox messages). Tap a conversation to
  see it as chat bubbles, with unsent messages clearly marked.
- The load status shows a per-type breakdown (e.g. `received 300, sent 38,
  failed 4`) so you can confirm the unsent messages were captured.
- Export to **JSON**, **CSV**, or **HTML**:
  - **JSON** — an object with `exported_at`, `count`, and a `messages` array;
    ISO-8601 timestamps. Each message carries a `kind` of `sms` or `mms`.
  - **CSV** — RFC-4180 quoting, header row, a `kind` column, `body` column last.
  - **HTML** — a single self-contained, chat-style page grouped by thread,
    with light/dark support via `prefers-color-scheme`.
- Export **everything** or a **single conversation** (from that conversation's
  screen). Saves through the Storage Access Framework, so **no storage
  permission** is needed and you choose the destination. Suggested filenames:
  `textport-YYYY-MM-DD.<ext>` or `textport-<contact>-YYYY-MM-DD.<ext>`.

## Tech stack

- Kotlin, Jetpack Compose, Material 3
- MVVM: `ViewModel` + `StateFlow`, Kotlin coroutines
- Gradle Kotlin DSL with a version catalog (`gradle/libs.versions.toml`)
- `compileSdk`/`targetSdk` 35, `minSdk` 26, JDK 17

## Build & install

The Gradle wrapper is committed, so a JDK 17 and the Android SDK are all you need.

```bash
# Debug build (auto-signed with the Android debug key, directly installable)
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk

# Run the unit tests (export formatters)
./gradlew testDebugUnitTest

# Unsigned release build
./gradlew assembleRelease
```

You can also open the project in Android Studio and Run it on a device or
emulator.

### Prebuilt APKs (GitHub Actions)

The [`Release APK`](.github/workflows/release.yml) workflow builds a signed,
installable APK. There are two ways to cut a release:

- **From the Actions tab:** run the *Release APK* workflow manually and enter a
  `version` (e.g. `v1.0`). The workflow builds, signs, **creates the tag**, and
  publishes it as a GitHub Release — no local tag push needed. Leave `version`
  blank to just build the APK and download it as a run artifact.
- **By pushing a tag:** `git tag v1.0 && git push --tags` triggers the same
  build-sign-publish flow.

By default the workflow signs with a fresh self-signed key each run — installable,
but you must uninstall a previous build before installing a newer one. To sign
with a stable key (so releases upgrade in place), set these repository secrets:
`KEYSTORE_BASE64` (base64 of your `.jks`), `KEYSTORE_PASSWORD`, `KEY_ALIAS`,
`KEY_PASSWORD`.

### Granting the permission

On first load, Textport requests the `READ_SMS` permission. If you deny it (or
disable it later in **Settings → Apps → Textport → Permissions**), the app shows
a clear message and reads nothing. Grant it and tap **Load messages** again.

### Reading failed / unsent messages (temporary default-SMS-app mode)

Some **failed or unsent** texts — for example a note sent to a number that can't
receive it — are only visible to the device's **default SMS app**. A normal
read-only app can't see them, no matter its permissions. To include these:

1. On the main screen, in **"Read failed / unsent SMS"**, tap **Set Textport as
   default SMS app** and confirm the system dialog.
2. Tap **Load messages** — the previously hidden failed messages now appear (the
   status line's per-type breakdown will show a `failed`/`outbox` count).
3. Export as usual.
4. Tap **Switch back to your SMS app** and re-select your normal messaging app.

**Important, please read:** while Textport is your default SMS app it is *not* a
full messenger. It **saves incoming SMS to your inbox** so nothing is lost, but
it does **not** show notifications for them, and **incoming MMS during this
window is not downloaded/saved**. Hold the role only as long as it takes to load
and export, then switch back. Android does not let an app hand the default role
to another app, so the switch-back is a manual step (Textport opens the right
settings screen for you). This is another reason Textport is **sideload-only**.

## Scope

**SMS and MMS.** Textport reads text messages from both the SMS and MMS
providers — including failed, queued, outbox and draft messages, and the
**text** of MMS messages (the common landing spot for a text that failed to
send). It does **not** read:

- **MMS media** — only the text parts are exported, not attached images/audio.
- **RCS** (Google Messages "chat features") — not exposed to third-party apps.
  If RCS is on, an unsent message you typed may be held in the messaging app's
  private RCS store rather than the SMS/MMS providers, in which case no
  third-party app (including Textport) can read it. A message that failed to
  send over SMS *is* in the telephony provider, but the system only reveals it
  to the default SMS app — see [Reading failed / unsent
  messages](#reading-failed--unsent-messages-temporary-default-sms-app-mode).
- **iMessage / other chat apps** — not on Android.

**iOS is intentionally out of scope:** Apple provides no API for apps to read the
Messages store, so an equivalent iOS app isn't possible.

## Google Play caveat

Google Play restricts the `READ_SMS` permission to apps that are the device's
**default SMS handler**. Textport is a read-only backup utility, not an SMS app,
so it is **not intended for Play distribution** — install it by sideloading the
APK (see [Build & install](#build--install)).

## License

This project's code is released under the MIT License. See the existing
[`LICENSE`](LICENSE) file for the full text.
