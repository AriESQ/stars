# Defanged Malware Stages

Defanged copies of the litellm 1.82.8 supply chain attack stages. Attacker-controlled URLs have been neutralized to prevent accidental execution or network contact.

## Files

| File | Stage | Description |
|------|-------|-------------|
| `decoded_payload.py` | 1 - Orchestrator | Decodes/executes Stage 2, encrypts output with RSA-4096, exfils to C2 |
| `stage2_collector.py` | 2 - Credential Harvester | Collects SSH keys, cloud creds, K8s secrets, crypto wallets, env files, etc. Also performs K8s lateral movement and installs Stage 3 persistence |
| `stage3_persistence.py` | 3 - C2 Backdoor | Polls C2 server every ~50min, downloads and executes arbitrary binaries. Installed as systemd user service "sysmon.service" |
| `monitor_c2.py` | Research tool | Polls the C2 endpoint every 60s, logs responses, and saves any new payloads to `payloads/`. When the C2 returns a YouTube URL the backdoor treats it as a dormant/no-op signal — the default response observed is `https://www.youtube.com/watch?v=dQw4w9WgXcQ` |

## Defanging Applied

Only attacker-controlled infrastructure is defanged. Legitimate services the malware targets (AWS IMDS, K8s API, Slack, Discord, YouTube, amazonaws.com) are left intact since they are not malicious endpoints.

| Defanged | Role |
|----------|------|
| `hXXps://models[.]litellm[.]cloud/` | Credential exfiltration endpoint |
| `hXXps://checkmarx[.]zone/raw` | C2 polling endpoint |
