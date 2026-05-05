# Defanged Malware Stages — telnyx 4.87.1 / 4.87.2

Defanged copies of the telnyx 4.87.1 / 4.87.2 supply chain attack stages. Attacker-controlled URLs have been neutralized to prevent accidental execution or network contact.

This is the same threat actor (**TeamPCP**) behind the [litellm 1.82.8 compromise](https://github.com/HackingLZ/litellm_1.82.8_payload) — identical RSA-4096 public key, `tpcp.tar.gz` exfil filename, and hybrid AES+RSA encryption scheme.

## Files

| File | Stage | Description |
|------|-------|-------------|
| `stage0_trigger.py` | 0 - Trigger | Injected code from `telnyx/_client.py` — OS-specific routing, base64 obfuscation, module-level execution on `import telnyx` |
| `stage1_linux_orchestrator.py` | 1 - Linux Orchestrator | Decoded from embedded base64 blob. Downloads Stage 2 via WAV steganography from C2, encrypts output with AES-256-CBC + RSA-4096, exfils to C2 |
| `stage0_windows_deobfuscated.py` | 0w - Windows (deobfuscated) | Clean readable version of the Windows `setup()` function with all base64 strings decoded inline |
| `monitor_c2.py` | Research tool | Polls the C2 endpoint every 60s, logs responses, and saves any new payloads to `payloads/` |

## Defanging Applied

Only attacker-controlled infrastructure is defanged. Legitimate services the malware targets (AWS IMDS, K8s API) are left intact since they are not malicious endpoints.

| Defanged | Role |
|----------|------|
| `hXXp://83[.]142[.]209[.]203:8080/` | Credential exfiltration endpoint (POST) |

## Key Differences from litellm Compromise

| Aspect | litellm | telnyx |
|--------|---------|--------|
| Trigger | `.pth` file (any Python invocation) | `import telnyx` (SDK import) |
| Payload delivery | Base64 blob embedded directly | **WAV steganography** — payloads hidden in `.wav` audio files |
| Platforms | Linux only | **Windows + Linux** (separate code paths) |
| Stage 2 | Embedded in package | **Downloaded at runtime** from C2 |
| C2 | `models.litellm.cloud` / `checkmarx.zone` | `83.142.209.203:8080` (bare IP) |
| Obfuscation | Minimal | Base64 string encoding via `_d()` helper |
| Windows persistence | None | `%APPDATA%\...\Startup\msbuild.exe` |

## WAV Steganography

Both platforms use the same technique to hide payloads inside WAV audio files:

```
1. Download .wav file from C2
2. Read all audio frames via Python's wave module
3. Base64-decode the raw frame data
4. First 8 bytes = XOR key, remainder = ciphertext
5. XOR-decrypt to recover the actual payload
```

- `ringtone.wav` delivers a Python credential collector (Linux)
- `hangup.wav` delivers a native PE binary (Windows)

## Version Bug

In v4.87.1, the Windows path calls `Setup()` (capital S) but the function is defined as `setup()` (lowercase) — a **NameError** that silently prevents the Windows attack. Version 4.87.2 fixes this to `setup()`, enabling Windows exploitation.
