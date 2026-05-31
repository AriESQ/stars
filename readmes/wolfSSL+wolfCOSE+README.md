# wolfCOSE

wolfCOSE is a lightweight C library implementing [CBOR (RFC 8949)](https://www.rfc-editor.org/rfc/rfc8949) and [COSE (RFC 9052/9053)](https://www.rfc-editor.org/rfc/rfc9052) using [wolfSSL](https://www.wolfssl.com/) as the crypto backend.

## Main Features

- **Complete RFC 9052 message set**: all six COSE message types, including multi-signer `COSE_Sign` and multi-recipient `COSE_Encrypt` / `COSE_Mac`
- **Post-quantum signing**: ML-DSA (Dilithium) at all three security levels
- **40 algorithms** across signing, encryption, MAC, and key distribution
- **Zero dynamic allocation**: all operations use caller-provided buffers
- **Tiny footprint**: 7.5 KB `.text` minimal build (Sign1+ECC), 25.6 KB full (40 algorithms), zero `.data`/`.bss`
- **Full COSE lifecycle in ~<1KB RAM** (excluding wolfCrypt internals)
- **Path to FIPS 140-3** via wolfCrypt FIPS Certificate #4718 (sole crypto dependency)

## Supported Algorithms

**Signing:** `ES256, ES384, ES512, EdDSA (Ed25519/Ed448), PS256/384/512, ML-DSA-44/65/87`

**Encryption:** `AES-GCM (128/192/256), ChaCha20-Poly1305, AES-CCM variants`

**MAC:** `HMAC-SHA256/384/512, AES-MAC`

**Key Distribution:** `Direct, AES Key Wrap, ECDH-ES+HKDF`

## COSE Message Types (RFC 9052)

wolfCOSE has implemented all RFC 9052 messages both single-actor and multi-actor variants:

| Message | RFC 9052 | API | Purpose |
|---|---|---|---|
| `COSE_Sign1` | Sec. 4.2 | `wc_CoseSign1_Sign` / `wc_CoseSign1_Verify` | Single-signer signature |
| `COSE_Sign` | Sec. 4.1 | `wc_CoseSign_Sign` / `wc_CoseSign_Verify` | **Multi-signer** (independent signatures over the same payload) |
| `COSE_Encrypt0` | Sec. 5.2 | `wc_CoseEncrypt0_Encrypt` / `wc_CoseEncrypt0_Decrypt` | Single-recipient AEAD |
| `COSE_Encrypt` | Sec. 5.1 | `wc_CoseEncrypt_Encrypt` / `wc_CoseEncrypt_Decrypt` | **Multi-recipient** (one ciphertext, many recipients via Direct / AES-KW / ECDH-ES) |
| `COSE_Mac0` | Sec. 6.2 | `wc_CoseMac0_Create` / `wc_CoseMac0_Verify` | Single-recipient MAC |
| `COSE_Mac` | Sec. 6.1 | `wc_CoseMac_Create` / `wc_CoseMac_Verify` | **Multi-recipient** MAC (shared MAC key, distributed to recipients) |
| `COSE_Key` / `COSE_KeySet` | Sec. 7 | `wc_CoseKey_Encode` / `wc_CoseKey_Decode` | Key serialization for all key types |

## Prerequisites (wolfSSL)

wolfCOSE requires [wolfSSL](https://www.wolfssl.com/) as its crypto backend. **Minimum supported version: v5.8.0-stable** (first release with the public `wc_ForceZero` symbol alongside the FIPS 204 final ML-DSA and context-aware `wc_dilithium_*_ctx_msg` APIs). Older 5.x releases can technically be supported but require source-level changes; contact [wolfSSL](https://www.wolfssl.com/contact/) for commercial support.

Choose a build configuration based on the algorithms you need.

### Minimal Build (ECC + AES-GCM)

This gives you COSE Sign1 (ES256/384/512) and Encrypt0 (AES-GCM):

```bash
cd wolfssl
./autogen.sh
./configure --enable-ecc --enable-aesgcm \
            --enable-sha384 --enable-sha512 --enable-keygen
make && sudo make install
sudo ldconfig
```

**Algorithms enabled:** ES256, ES384, ES512, AES-GCM-128/192/256

### Minimal Build (Post-Quantum / ML-DSA only)

For pure post-quantum signing with ML-DSA-44/65/87:

```bash
cd wolfssl
./autogen.sh
./configure --enable-cryptonly --enable-dilithium
make && sudo make install
sudo ldconfig
```

**Algorithms enabled:** ML-DSA-44, ML-DSA-65, ML-DSA-87
(SHAKE-128/256 are pulled in automatically by `--enable-dilithium`.)

### Full Build (All Algorithms)

```bash
cd wolfssl
./autogen.sh
./configure --enable-ecc --enable-ed25519 --enable-ed448 \
            --enable-curve25519 --enable-aesgcm --enable-aesccm \
            --enable-sha384 --enable-sha512 --enable-keygen \
            --enable-rsapss --enable-chacha --enable-poly1305 \
            --enable-dilithium --enable-hkdf --enable-aeskeywrap
make && sudo make install
sudo ldconfig
```

## Build

```bash
# Core library (libwolfcose.a)
make

# Run unit tests
make test

# Build and run CLI tool round-trip tests (all algorithms)
make tool-test

# Run lifecycle demo (11 algorithms)
make demo
```

### Build Targets

| Target | Description |
|--------|-------------|
| `make all` | Build `libwolfcose.a` (core library only) |
| `make shared` | Build `libwolfcose.so` |
| `make test` | Build + run CBOR and COSE unit tests |
| `make tool` | Build CLI tool (`tools/wolfcose_tool`) |
| `make tool-test` | Round-trip self-test for all 17 algorithms |
| `make demo` | Build + run lifecycle demo (11 algorithms) |
| `make clean` | Remove all build artifacts |

## Quick Start

### Examples

See `examples/` for complete working code:
- `sign1_demo.c`, `encrypt0_demo.c`, `mac0_demo.c`: algorithm demos
- `lifecycle_demo.c`: full edge-to-cloud workflow
- `comprehensive/`: algorithm matrix tests
- `scenarios/`: firmware signing, attestation, fleet config

## CI / Testing

Runs on every push and PR:

- **Build + Test**: Ubuntu, macOS, GCC 10-14, Clang 14-18
- **Comprehensive Tests**: ~240 algorithm combination tests
- **Static Analysis**: cppcheck, Clang analyzer, GCC `-fanalyzer`
- **MISRA C 2012**: cppcheck `--addon=misra` checking all wolfCOSE code paths
- **MISRA C 2023**: strict GCC warnings and clang-tidy (`bugprone-*`, `cert-*`, `clang-analyzer-*`, `misc-*`)
- **Coverity Scan**: nightly defect analysis
- **Advanced Internal Static Analysis:** Fenrir wolfssl advanced static analysis tools
- **Code Coverage**: 99.3% for wolfcose.c, 100% for wolfcose_cbor.c

```bash
make coverage                  # Run tests with gcov
make coverage-force-failure    # Include crypto failure path testing
```

<a href="https://scan.coverity.com/projects/wolfcose">
  <img alt="Coverity Scan Build Status"
       src="https://scan.coverity.com/projects/32918/badge.svg"/>
</a>
<a href="https://github.com/aidangarske/wolfCOSE/actions">
  <img alt="CI Status"
       src="https://img.shields.io/github/actions/workflow/status/aidangarske/wolfCOSE/build-test.yml?label=CI&logo=github"/>
</a>
<a href="https://github.com/wolfssl/skoll">                                                                                                              <img alt="Skoll Review" src="https://img.shields.io/badge/skoll-passed-blue"/>                                                                     
</a>                                                                                                                                                 
<a href="https://github.com/wolfssl/fenrir">                                                                                                         
  <img alt="Fenrir Review" src="https://img.shields.io/badge/fenrir-passed-blueviolet"/>
</a>


## Documentation

Full documentation is available in the [Wiki](https://github.com/aidangarske/wolfCOSE/wiki):

- [Getting Started](https://github.com/aidangarske/wolfCOSE/wiki/Getting-Started): Build instructions and first steps
- [Message Types](https://github.com/aidangarske/wolfCOSE/wiki/Message-Types): All six RFC 9052 messages (Sign1, Sign, Encrypt0, Encrypt, Mac0, Mac) with code samples
- [Algorithms](https://github.com/aidangarske/wolfCOSE/wiki/Algorithms): Complete list of 40 supported algorithms with COSE IDs
- [API Reference](https://github.com/aidangarske/wolfCOSE/wiki/API-Reference): Function signatures, data structures, error codes
- [Macros](https://github.com/aidangarske/wolfCOSE/wiki/Macros): Compile-time configuration options
- [Testing](https://github.com/aidangarske/wolfCOSE/wiki/Testing): Test infrastructure, coverage, and failure injection
- [MISRA Compliance](https://github.com/aidangarske/wolfCOSE/wiki/MISRA-Compliance): MISRA C:2012 and C:2023 compliance status and deviation rationale
- [Project Structure](https://github.com/aidangarske/wolfCOSE/wiki/Project-Structure): Source file layout

## Blogs

Blogs and update can be found here:

[wolfCOSE Blogs](https://aidangarske.github.io/wolfCOSE/)

## License

wolfCOSE is free software licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).

Copyright (C) 2026 wolfSSL Inc.

## Support

> **Note:** While wolfCOSE is currently maintained by wolfSSL developers, it is not yet classified as an officially supported product. It was designed from the ground up to meet the same quality standards as the rest of the wolfSSL suite with future adoption in mind. We are eager to transition this to a fully supported product as demand grows; if your organization requires official support or has specific feature requirements or you just have general questions or guidance with product, please reach out.

For commercial licensing, professional support contracts, or to discuss moving wolfCOSE into your production environment, contact [wolfSSL](https://www.wolfssl.com/contact/).
