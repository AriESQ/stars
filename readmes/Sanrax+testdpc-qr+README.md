# TestDPC COPE QR

#### https://sanrax.github.io/testdpc-qr/

A static, browser-local enrollment QR generator using the unmodified official
TestDPC APK. Open it on a computer, tablet or another phone, and scan the QR
from the phone you want to enroll.

## Enroll

1. Use an Android 11+ device already at its initial setup welcome screen, with
   support for Android Enterprise QR provisioning. An already-configured phone
   normally needs a reset to enter this setup flow. This project avoids a reset
   when **removing** the resulting work profile; it does not remove that initial
   provisioning requirement.
2. Open the generator on another screen. The official TestDPC defaults work
   without configuration. Optionally include Wi-Fi, then generate the QR.
3. Tap the phone's setup welcome screen six times to open the enrollment scanner.
   Scan the QR, connect to the internet and allow TestDPC to download.
4. In TestDPC, select **Use for work & personal** and finish setup. The QR itself
   does not force the mode; stock TestDPC returns the selected mode from its
   `ACTION_GET_PROVISIONING_MODE` activity. **Use for work only** is fully managed
   enrollment and is a different mode.
5. Open the briefcase-badged TestDPC in the Work tab and verify its status says:
   **This app is a profile owner of an organization-owned device.** A generic
   profile-owner status alone does not confirm COPE.

## Deprovision without a factory reset

On the phone, open **the work-profile TestDPC** (briefcase badge). Find:

**Data wipe → Remove work profile**

Leave the external-storage and reset-protection options unchecked, then confirm.
This deletes the work profile, its apps and its data. Android documents that
`wipeData(0)` called by the organization-owned managed-profile owner relinquishes
the device for personal use, removing that profile and its policies while
preserving the personal profile.

TestDPC also has **Factory reset device**, which erases the phone. Select the
explicit **Remove work profile** action for this use case. This project's QR
generator never issues either command; removal is a local action in TestDPC.

## Pinned release and checksum

- Upstream release: [TestDPC v9.0.12](https://github.com/googlesamples/android-testdpc/releases/tag/v9.0.12).
- Source tag commit: `7a8957beb7c2e01a1bf5776898542e24f6f288fb`.
- APK file SHA-256: `aad38c1f608b1c7289405c4e866977f5d231502643ce2e2401a7c305808f9c00`.
- Android URL-safe Base64 checksum: `qtOMH2CLHHKJQFxOhml39dIxUCZDzi4kAafDBYCPnAA`.

This will be updated as new TestDPC versions come out.

## Upstream references

- [TestDPC provisioning README](https://github.com/googlesamples/android-testdpc/blob/v9.0.12/README.md)
- [TestDPC mode selection](https://github.com/googlesamples/android-testdpc/blob/v9.0.12/src/main/java/com/afwsamples/testdpc/provision/GetProvisioningModeActivity.java)
- [TestDPC removal implementation](https://github.com/googlesamples/android-testdpc/blob/v9.0.12/src/main/java/com/afwsamples/testdpc/policy/PolicyManagementFragment.java)
- [Android 11 company-owned work profiles](https://developer.android.com/work/versions/android-11#work-profile-enhancements)
- [Android wipeData documentation](https://developer.android.com/reference/android/app/admin/DevicePolicyManager#wipeData(int,%20java.lang.CharSequence))
- [GitHub Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

Project code: MIT. Vendored QR encoder: MIT; see `dist/THIRD_PARTY_NOTICES.txt`.
TestDPC is downloaded from upstream and is not bundled or modified here.
