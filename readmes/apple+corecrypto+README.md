<!-- Copyright (c) (2010,2012,2014-2023,2026) Apple Inc. All rights reserved.

 corecrypto is licensed under Apple Inc.’s Internal Use License Agreement (which
 is contained in the License.txt file distributed with corecrypto) and only to
 people who accept that license. IMPORTANT:  Any license rights granted to you by
 Apple Inc. (if any) are limited to internal use within your organization only on
 devices and computers you own or control, for the sole purpose of verifying the
 security characteristics and correct functioning of the Apple Software.  You may
 not, directly or indirectly, redistribute the Apple Software or any portions thereof.
-->

The corecrypto (cc) project
===========================

The Security framework, CryptoKit and CommonCrypto rely on the corecrypto library to
provide implementations of low-level cryptographic primitives. Although corecrypto
does not directly provide programming interfaces for developers and should not be used
by iOS, iPadOS, or macOS apps, the source code is available to allow for verification
of its security characteristics and correct functioning.

The main goal is to provide low-level fast math routines and cryptographic implementations which
can be used in various environments (Kernel, bootloader, userspace, etc.).  It
is an explicit goal to minimize dependencies between modules and functions so
that clients of this library only end up with the routines they need and
nothing more.


Building on macOS
-----------------
The easiest way to build the corecrypto project is to use the `xcodebuild` command. The project supports several schemes, including:
1. `corecrypto`: This scheme compiles corecrypto and produces a static library.
2. `corecrypto_test`: This scheme compiles corecrypto test files and links statically with the corecrypto debug library.
3. `corecrypto_perf`: This scheme compiles corecrypto performance measurement files and links statically with the corecrypto release library.
E.g., `xcodebuild -scheme corecrypto_test`


Running the formal verification
-------------------------------
Our formal verification is in the [`corecrypto_verify`](corecrypto_verify) subdirectory.
Please refer to the [`corecrypto_verify/README.md`](corecrypto_verify/README.md) for more details. For an overview of the process, see our [Formal verification in corecrypto: ML-KEM and ML-DSA in 2026](corecrypto_verify/technical_overview/formal-verification-for-apple-corecrypto.md) technical overview.



Licensing and Contributions
---------------------------
The publication of this code is primarily intended for security research and verification purposes. The default license for the corecrypto (cc) project is the evaluation-only corecrypto Internal Use License Agreement contained in [License.txt](License.txt).

Some Isabelle files, however, are intended for wider use and are also licensed under more permissive terms. For example, the files in:
* the directories in [`corecrypto_verify/isabelle/Apple_Isabelle_Libraries`](./corecrypto_verify/isabelle/Apple_Isabelle_Libraries) are available under per-subdirectory license files as referenced in individual file headers
* the directory [`corecrypto_verify/isabelle/Cryptol/cryptol-to-isabelle/isabelle`](./corecrypto_verify/isabelle/Cryptol/cryptol-to-isabelle/isabelle) are available under an [accompanying LICENSE file](./corecrypto_verify/isabelle/Cryptol/cryptol-to-isabelle/isabelle/LICENSE)

We are not currently accepting external code contributions to this repository. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for information about reporting security issues.

Contact
-------
To report security issues with this code, please use the instructions available [at this page](https://support.apple.com/en-us/102549).
