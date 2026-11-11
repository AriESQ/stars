# sk-softkey / sk-hybrid

Two `SSH_SK_PROVIDER` middlewares for OpenSSH, implementing the same
`sk-api.h` ABI in two different ways:

- **`sk-softkey.c`** -- emulates a security key entirely in software.
  Private keys are generated and stored locally (encrypted at rest with
  a PIN-derived key). No hardware, no phone, no network. Good for local
  dev/CI.
- **`sk-hybrid.c`** -- emulates *nothing*. Instead it relays CTAP2
  commands to a real phone authenticator over FIDO hybrid transport
  (the QR-code-then-BLE-then-tunnel-server flow, aka caBLE), driving
  your existing [fido-hybrid-transport](https://github.com/joostd/fido-hybrid-transport)
  Python client as a subprocess. Private keys never leave the phone.

Pick whichever matches what you're testing: `sk-softkey` for protocol
plumbing with zero external dependencies, `sk-hybrid` for testing real
hybrid-transport UX and a real authenticator's signatures.

```
make            # builds both sk-softkey.{so,dylib} and sk-hybrid.{so,dylib}
make softkey    # just the software-emulated one
make hybrid     # just the phone-relay one
```

---

## sk-softkey: software-emulated security key

A software-emulated FIDO2/U2F "security key" implementing OpenSSH's
`SK_PROVIDER` middleware ABI (`sk-api.h`). Lets you use
`ssh-keygen -t ecdsa-sk` / `ed25519-sk`, resident keys, and `ssh-agent`
without real hardware -- for development, CI, and protocol testing.

### Build

    make softkey    # produces sk-softkey.so (needs libssl-dev)

### Use it

    export SSH_SK_PROVIDER=$(pwd)/sk-softkey.so
    ssh-keygen -t ecdsa-sk -O resident -O application=ssh:myhost -f ~/.ssh/id_ecdsa_sk
    # PIN prompt and "touch" are handled instantly/non-interactively in
    # software, no PIN/touch required unless you pass one yourself

    ssh-add -K                 # load resident keys back from the store
    ssh -i ~/.ssh/id_ecdsa_sk_sk user@host

Set `SSH_SK_PROVIDER` the same way on the agent side if you use `ssh-agent`.

### How it maps onto the real ABI

OpenSSH's `ssh-sk-client.c` `dlopen()`s whatever `SSH_SK_PROVIDER` points
at and calls four functions (`sk-api.h`, vendored alongside this file --
fetched verbatim from openssh-portable so the struct layouts match
exactly):

| sk-api function          | what this library does |
|---|---|
| `sk_api_version`          | returns `SSH_SK_VERSION_MAJOR` |
| `sk_enroll`                | generates an ECDSA P-256 or Ed25519 keypair in software, builds WebAuthn-style `authData` (`rpIdHash \|\| flags \|\| counter \|\| attestedCredData`), self-signs it as a stand-in attestation, and persists the private key |
| `sk_sign`                  | looks up the key by its handle, increments the (per-credential) signature counter, builds `authData` again, and signs `SHA256(authData \|\| clientDataHash)` |
| `sk_load_resident_keys`    | enumerates the on-disk store and returns metadata + public keys for keys marked resident, mirroring a real authenticator's discoverable-credential listing |

`sk_enroll`'s `key_handle` is a random 32-byte credential ID; for
non-resident keys OpenSSH stores this handle in your private key file and
hands it back on every `sk_sign` call, exactly as it would for a USB key.

### Storage & key protection

- Default location: `~/.ssh/sk-softkey/<hex-handle>.key` (override with
  `SK_SOFTKEY_DIR`), directory created `0700`, files `0600`.
- Each file holds a small cleartext header (algorithm, RP/`application`
  string, resident flag, signature counter) plus an AES-256-GCM-sealed
  blob containing the private key material: for Ed25519, the 32-byte
  seed; for ECDSA, the 32-byte private scalar *and* the 65-byte
  uncompressed public point (stored together so the public key never
  needs to be recomputed from the private one later).
- All EC operations use OpenSSL 3's provider-based `EVP_PKEY`/`OSSL_PARAM`
  API rather than the legacy `EC_KEY` API, so building against OpenSSL 3
  produces no deprecation warnings.
- The AES key is derived via PBKDF2-HMAC-SHA256 (100k iterations) from
  the PIN you pass to `sk_enroll`/`sk_sign` (OpenSSH forwards whatever you
  type at its PIN prompt, or empty string if you don't set one) plus the
  credential handle as salt.
- **This is not hardware-backed secrecy.** Anyone with read access to the
  store directory *and* the right PIN can extract the raw private key.
  There's no secure enclave, no tamper resistance, no resistance to an
  attacker who can run code as your user. Treat it like an unencrypted
  SSH key with a passphrase wrapper, not like a real authenticator.
- Enumeration of resident keys does **not** require the PIN to see *that*
  a credential exists, mirroring real authenticators (the discoverable
  metadata is enumerable; decrypting the private material is not).

### Things intentionally left simple (vs. a real authenticator)

- No real attestation chain (self-signed proof-of-possession only); fine
  for testing OpenSSH's client logic, not for relying parties that check
  attestation chains.
- No touch/biometric step -- `SSH_SK_USER_PRESENCE_REQD` is accepted but
  not enforced (you may wire in an `ask_user_input`-style confirmation
  if you want a deliberate friction step).
- COSE key encoding in `attestedCredData` is a minimal stand-in (OpenSSH
  doesn't parse it -- it gets the public key straight from
  `sk_enroll_response.public_key`).
- No CTAP2 PIN-retry-lockout emulation.

### Files

- `sk-api.h` -- OpenSSH's middleware ABI header, fetched verbatim from
  `openssh/openssh-portable` so struct layouts match exactly.
- `sk-softkey.c` -- the middleware implementation.
- `Makefile` -- builds `sk-softkey.so`.

### Debugging

    export SK_SOFTKEY_DEBUG=1     # prints enroll/sign/load activity to stderr

---

## sk-hybrid: relay CTAP2 to a phone over hybrid transport

Implements the same `sk-api.h` ABI, but instead of generating or storing
any key material itself, it relays `authenticatorMakeCredential` /
`authenticatorGetAssertion` CBOR commands to a real phone authenticator
over FIDO hybrid transport (QR code -> BLE advert -> tunnel-server
websocket -> Noise-encrypted channel -> CTAP2). The phone generates,
stores, and signs with the private key; this library never sees it.

It does this by driving your existing
[fido-hybrid-transport](https://github.com/joostd/fido-hybrid-transport)
Python client as a subprocess, rather than reimplementing BLE scanning,
the Noise handshake, or the tunnel-server protocol in C -- that logic is
already written, working, and yours; reusing it is both less code and
less risk than a parallel reimplementation.

### Setup

1. **Build:**

       make hybrid     # produces sk-hybrid.so / sk-hybrid.dylib (needs libcbor-dev)

   On Debian/Ubuntu: `apt install libcbor-dev`. On macOS: `brew install libcbor`
   (the Makefile picks it up automatically via `brew --prefix`, same as
   for OpenSSL).

2. **Point OpenSSH at it, and tell it where the script lives:**

       export SSH_SK_PROVIDER=$(pwd)/sk-hybrid.dylib
       export SK_HYBRID_SCRIPT=/path/to/fido-hybrid-transport/client/main.py
       export SK_HYBRID_PYTHON=python3   # optional, defaults to "python3" on $PATH

       ssh-keygen -t ecdsa-sk -O application=ssh:myhost -f ~/.ssh/id_ecdsa_sk

   This prints a QR code on your terminal and waits. Scan it with your phone,
   approve the request there, and the resulting credential's public key/handle/
   attestation come back through the tunnel exactly as if a USB key had
   produced them.

### How it works

```
ssh-keygen / ssh
      |  dlopen(SSH_SK_PROVIDER), calls sk_enroll()/sk_sign()
      v
 sk-hybrid.so  -- builds authenticatorMakeCredential/GetAssertion CBOR
      |           (libcbor), framed with a 4-byte length prefix
      |  fd 3 (write) / fd 4 (read) -- pipes to a child process
      v
 python3 main.py stdio-relay   (fido-hybrid-transport client with stdio-relay support)
      |           does the QR display, BLE advert scan, tunnel-server
      |           websocket connect, and Noise handshake exactly as it
      |           already does for get-info/make-credential/get-assertion;
      |           then relays opaque CTAP frames over the encrypted tunnel
      v
   phone (Chrome/Android, Safari/iOS, ...) -- does the actual CTAP2 work:
            generates/stores the key, asks for biometric/PIN approval,
            signs, sends the response back over the same tunnel
```

`sk-hybrid.so` parses the response (`authData` for the rpIdHash/flags/
counter/credId/COSE-key, `attStmt` for the attestation signature) using
libcbor, converts the COSE public key into the raw point format OpenSSH
expects (`0x04 || x || y` for ECDSA, raw 32 bytes for Ed25519), and
splits DER ECDSA signatures into raw `r`/`s` for `sk_sign_response`.

### What's implemented vs. not

| sk-api function | status |
|---|---|
| `sk_api_version` | full |
| `sk_enroll` | full: builds `authenticatorMakeCredential`, parses `authData`+`attStmt`, returns pubkey/handle/attestation |
| `sk_sign` | full: builds `authenticatorGetAssertion` with the credential ID in `allowList`, parses signature + counter |
| `sk_load_resident_keys` | **not implemented** -- returns success with zero keys. Real enumeration needs CTAP2.1 `authenticatorCredentialManagement`, which itself needs a `pinUvAuthToken` (ECDH key agreement + PIN handling) that isn't built here. `ssh-add -K` will complete without error but won't discover phone-resident credentials. |

### Known limitations (be aware of these before relying on it)

- **One QR scan per process, not per `ssh` session.** OpenSSH normally
  re-execs `ssh-sk-helper` fresh for each `sk_enroll`/`sk_sign` call (it's
  a sandboxing boundary), so each call means a fresh BLE discovery +
  tunnel handshake -- a few seconds, and a new QR code each time. This
  mirrors the underlying caBLE one-shot-per-tunnel model; it does *not*
  implement browsers' "linked device" mode (a long-lived paired secret
  that skips the QR step on subsequent uses).
- **No resident-key enumeration** (see table above).
- **No PIN forwarding to the phone.** The `pin` argument from OpenSSH is
  currently unused -- phone-side user verification (biometric/PIN) happens
  entirely on the phone's own lock screen, outside CTAP2's PIN protocol.
- **Attestation is passed through verbatim, unvalidated.** `sk-hybrid.so`
  doesn't check the attestation certificate chain; it just hands the
  signature/cert bytes to OpenSSH as-is, same as a real authenticator's
  transport would.
- **Requires the Python client to be reachable and runnable** at whatever
  path `SK_HYBRID_SCRIPT` points to, with its existing dependencies
  (`pyqrcode`, `bleak`, `cryptography`, `cbor2`, `websockets`, plus its
  own `cable_noise`/`ctap_usb` modules) already working -- this library
  doesn't vendor or reimplement any of that.

### Testing without a phone

`mock_relay.py` (in this bundle) implements just the fd-3/fd-4 framing
half of the contract with an in-process fake CTAP2 authenticator -- no
BLE, no tunnel server, no phone. It's how the C side's CBOR building and
response parsing were validated end-to-end (including verifying the
returned signatures cryptographically against the returned public keys,
not just checking byte lengths):

    SK_HYBRID_SCRIPT=./mock_relay.py ./your_test_program

This exercises everything except the actual hybrid-transport plumbing,
which is already proven by your existing `main.py` working against a
real phone.

### Debugging

    export SK_HYBRID_DEBUG=1   # prints relay spawn/call activity to stderr

### Files (sk-hybrid-specific)

- `sk-hybrid.c` -- the middleware implementation.
- `mock_relay.py` -- fake-phone test double for the relay protocol (not
  needed at runtime; only for testing `sk-hybrid.so` in isolation).