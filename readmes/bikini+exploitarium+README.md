# Exploitarium

A consolidated archive of my public proof-of-concept and vulnerability research writeups.

Most folders contain one of my former standalone PoC repos, preserved with its original README and tracked files. New research entries are added directly here as self-contained folders.

## Contents

| Folder | Source | Tracked entries |
| --- | --- | ---: |
| `7zip-rar5-motw-chain-poc` | `bd9533f532c1e4ee6af783b9bb49d1133c600e2c` | 3 |
| `anydesk-printer-com-impersonation-poc` | `7491303301093b2d40bee9dadf6b38f757ce78e0` | 4 |
| `c-ares-tcp-uaf-calc-poc` | direct entry, June 24, 2026 | 7 |
| `docker-cp-copyout-destination-escape` | `d1367b1381736d7f961ac808ce88d4e24a633adc` | 5 |
| `firefox-smartwindow-private-url-exfil-poc` | direct entry, June 24, 2026 | 3 |
| `floci-apigateway-vtl-rce-poc` | direct entry, June 23, 2026 | 3 |
| `flowise-mcp-env-case-bypass-poc` | `ed9fab0086674f1b16467990b33bb9299e93429e` | 3 |
| `ghidra-12.1.2-rce-ace-calc-poc` | `52dee6362990c03c0d753d074c85428824d46368` | 9 |
| `gitea-act-runner-container-options-poc` | `f06d78fb111732f3e7737f4c07e77ef94c4b64bf` | 4 |
| `imagemagick-gs-delegate-hijack-poc` | `8140e8ee0ed78beaf5e8303a795b70b138f5891b` | 5 |
| `libssh2-cve-2026-55200-poc` | direct entry, June 23, 2026 | 3 |
| `lunar-modrinth-chain-poc` | `ffd02120708b6503f11585858ce3724872f3b7a7` | 6 |
| `mybb-limited-acp-to-admin` | `1610e0373943c2f6562a99f917d3a3d1fdd9056d` | 5 |
| `nmap-ipv6-extlen-wrap-poc` | direct entry, June 23, 2026 | 4 |
| `objdump-dlx-calc-poc` | `7df01e4e20c7375a89e8ccf760526c52eb6ad582` | 41 |
| `openvpn-connect-echo-script-ace-poc` | `d2f904d9272d4388c9862131d40e32e072e85e38` | 8 |
| `systeminformer-phsvc-trusted-host-lpe-poc` | direct entry, June 24, 2026 | 3 |
| `vlc-vp9-reschange-crash-poc` | `fae72b82f24d03cf2fb9cb55fbb2e7774f684ff3` | 3 |

## Consolidation Check

This section applies to the former standalone repositories listed above by commit hash.

The consolidation was checked from fresh GitHub clones on June 23, 2026 before the old standalone repos were removed.

The check compared each former standalone repo's `HEAD` tree against the matching folder here using Git tree data, not a loose filesystem diff. For every tracked entry, the check required:

- the same relative path;
- the same Git object type;
- the same tree mode, including executable bits;
- the same Git blob ID.

Matching Git blob IDs means the tracked file bytes are identical. The check covered 12 repos and 96 tracked entries with zero mismatches.

This repository preserves the contents of those PoCs. Repository-level metadata such as stars, issues, pull requests, releases, and separate Git history are not represented inside the folders.

Direct entries, including `c-ares-tcp-uaf-calc-poc`, `firefox-smartwindow-private-url-exfil-poc`, `floci-apigateway-vtl-rce-poc`, `libssh2-cve-2026-55200-poc`, `nmap-ipv6-extlen-wrap-poc`, and `systeminformer-phsvc-trusted-host-lpe-poc`, are tracked by this repository's commit history.
