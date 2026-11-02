# qBtGuard — 0.2.0 candidate

One Windows PowerShell 5.1 engine for torrent inspection, opt-in deletion, PIA recovery, forwarded-port synchronization, and qBittorrent restart. **Release candidate: validated on one Windows installation, with audit mode retained as the installation default.**

## Defaults and operation

Installation starts in audit mode (`AuditOnly: true`). All corrective actions pass through a shared action gate: audit mode logs what would happen without switching VPN regions, changing ports, starting qBittorrent, or deleting torrents. Authentication/logout, logs and a temporary execution lock still operate.

Set `AuditOnly: false` only after QA and enable each desired action separately. Corrective-action flags default to false, including on older configurations. `DeleteProhibitedTorrents` removes the **entire offending torrent AND its downloaded data** through qBittorrent. `DeleteInvalidMkvTorrents` is separate and defaults off. An unreadable MKV alone never causes deletion.

| Setting | Meaning |
|---|---|
| `QuietLogging` | Suppress uneventful unscoped enforcement summaries on disk; retain the calendar-cutoff heartbeat and diagnostic messages |
| `QbtUrl`, `QbtUser` | User-supplied Web UI connection |
| `RemoteEndpoint` | Explicit remote API mode; skips local MKV inspection and blocks local PIA/restart controls |
| `EnablePia` | Require local PIA tunnel and qBittorrent interface binding |
| `EnableVpnRecovery` | Rotate configured PIA regions after disconnection or explicit forwarding failure |
| `EnablePortSync` | Apply and verify PIA's forwarded port |
| `EnableQbtRestart` | Start a missing local process after VPN and saved profile binding checks |
| `VpnInterface` | Exact local VPN adapter name; must match the saved display name; the live qBittorrent binding is checked against its saved internal ID |
| `QbtSettingsPath` | Intended user's qBittorrent INI file; restart requires its saved interface name (or legacy alias) to match; the live API must match the saved internal ID |
| `PiaCtl`, `QbtExe`, `QbtProcessName` | Local installation paths and process name |
| `PiaRegions`, `RegionCooldownMinutes` | User-selected region IDs and persistent recovery cooldown |
| `BlockNoExtension`, `BlockedExtensions` | File-name inspection policy |
| `VerifyMkvSignatures` | Inspect completed local MKV headers |
| `DeleteProhibitedTorrents`, `DeleteInvalidMkvTorrents` | Separate opt-in deletion policies |

PIA integration is optional. With it enabled, the API endpoint must resolve exclusively to this machine. The tunnel must report Connected, have a Preferred, non-link-local IPv4 address on the configured Up adapter, and qBittorrent must report the configured interface binding. qBtGuard is **not a kill switch**: configure PIA's kill switch and qBittorrent's interface binding independently. It does not stop an already running qBittorrent if the tunnel fails. Recovery can take up to 120 seconds; the scheduler prevents concurrent scheduled instances and the engine locks each installation against concurrent manual runs.

The first compatibility target is qBittorrent 4.3.6. Profile/interface naming, PIA behavior, x86/x64 paths and other versions require Windows validation. No user's addresses, credentials, logs, or preferred region list are embedded in the engine.

## Installation

Keep the installer, engine, launcher and `config.example.json` together. Run as the Windows user who will run the task:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Install-QbtGuard.ps1
```

The installer asks for URL/user/password and saves the password with Windows DPAPI. The default destination is `%LOCALAPPDATA%\qBtGuard`. It refuses existing destinations and existing task names. Use `-NoTask` for isolated QA; `-TaskName` permits a distinct test task. The task repeats every ten minutes while the installing user is logged on and runs hidden. Following a reboot, sign in with that user before expecting runs. Locking the session is supported; sleep and sign-out prevent normal execution. The supplied scheduler settings use Windows defaults for battery restrictions. Do not schedule multiple installations against the same qBittorrent instance.

After installation edit only the installed `config.json`. Paths, interface names, and PIA regions are configuration, not repository edits. For remote Web UI use set `RemoteEndpoint: true`; deletion still acts on that remote server if explicitly enabled. Remote downloads are not mapped into local paths by this candidate.

Run the installed engine manually and inspect its `qbtguard.log`. Completion entries include file findings, MKVs checked/skipped/unreadable, and torrent removals. A zero finding count with skipped MKVs does not mean every video was inspected. Header inspection accepts EBML, not full container integrity, codec validity, playable media, or absence of malware. MP4 or another legitimate format renamed `.mkv` will be flagged, so leave invalid-MKV deletion off until that policy is reviewed. No age-based disk cleanup is included.

API calls and PIA commands have timeouts. Failures log a stage and exception type rather than raw credential-bearing exceptions. Logs contain file/torrent names and must remain private. The engine rechecks torrent existence before deletion and verifies API removal; it does not independently establish all downloaded data has disappeared from disk.

## Migration and rollback

See [MIGRATION.md](MIGRATION.md). The candidate installer does not automatically disable any existing task or turn enforcement on. Preserve old scripts, credentials, task XML and state until the new installation has passed Windows QA. Do not copy personal logs/configuration into this repository.

Uninstall with `Uninstall-QbtGuard.ps1 -Destination <installed-directory>` and optional `-TaskName`. It removes only a task whose action matches that installation and retains installed files. Downloads are untouched.

## QA status

Windows PowerShell 5.1 syntax checks and 84 Pester 3.4.0 tests passed in CI and on the pilot machine. Live fixture and control tests passed, and the single replacement task was observed operating from October 15 through October 19, 2026. The latest reported task result was successful; the available log contained successful heartbeats and no recorded errors. Quiet logging does not provide a complete history of every scheduled run. See [QA.md](QA.md) for evidence and remaining compatibility limits, and [tests/README.md](tests/README.md) for the test procedure.

HTTP Web UI credentials are unencrypted in transit; use HTTPS or a trusted local connection. Do not expose the Web UI directly to the Internet. DPAPI files are tied to the installing Windows account and machine.

## License

[MIT](LICENSE).

### PIA public-IP discovery

The VPN readiness gate uses PIA's Connected state and the configured Up adapter with a usable Preferred local IPv4 address. The saved and live qBittorrent interface bindings remain separately checked. Public exit-IP discovery (`piactl get vpnip`) is not a gate: a live integration test observed `Unknown` alongside Connected, a usable WireGuard tunnel and an assigned forwarded port. This change avoids blocking port synchronization on unavailable address telemetry; it does not independently prove end-to-end Internet reachability. PIA CLI failures and unavailable local tunnel checks still fail the cycle. VPN BLOCKED log messages identify unsuccessful readiness checks.

### Asynchronous PIA recovery

The recovery action waits up to 30 seconds for Disconnected before changing region. It then polls for a connected tunnel in the selected region and an assigned forwarded port. Connect requests are sent only from Disconnected, at least 15 seconds apart, with a maximum of four requests during 24 five-second polling intervals. A CLI success exit is treated as request acknowledgment, not proof of connection. Native-command overhead adds to the polling duration. Disconnect settling timeouts withhold the region/connect commands, and failures remain visible in the log. Audit mode performs no disconnects, region changes, connect requests or recovery waits.

The first live recovery test required a manual reconnect; the revised implementation subsequently passed an unattended live recovery test. Future live testing must have an independent local reconnect fallback prepared before disconnecting the VPN; the kill switch can block the chat connection. Keep production protection restored between tests.

### One-torrent inspection and enforcement

Use `QbtGuard.ps1 -OnlyTorrentHash <hash>` to restrict file inspection and torrent deletion to one 40- or 64-character hexadecimal hash. The server query is filtered and the returned torrent list is filtered again locally. An absent target produces a scope message with zero matches and no torrent deletion. This option does not enable enforcement or override the configuration. VPN recovery, restart and port synchronization policies remain independent: disable those policies when doing a deletion-only fixture test. Omit the option for normal whole-queue operation.

### Quiet production logging and live QA

`QuietLogging` defaults to false. When enabled, an unscoped enforcement cycle with no findings or other log messages prints its completion summary to the console without appending it to disk. It writes a `HEARTBEAT` with the summary when the log is missing or was last modified before 00:01 on the previous local calendar day. This inherited rule can yield a heartbeat every other day; it is not a once-per-day timer. Audit runs, scoped QA, findings, actions, notices and failures retain normal logging. The heartbeat runs only after a successful cycle; it is not proof that skipped MKVs were inspected.

Live QA on the initial Windows/qBittorrent 4.3.6 system demonstrated guarded restart, forwarded-port synchronization, unattended recovery with the revised retry logic, and scoped deletion of prohibited-extension, extensionless and invalid-header MKV fixture torrents. Each successful deletion fixture also had both downloaded files verified absent. The first recovery attempt required manual assistance; the revised recovery test completed without it. A first extensionless fixture had unresolved location/completion issues; the repeated test used a verified 100% complete fixture. These observations do not establish clean-machine portability or full MKV integrity checking. The pilot was subsequently cut over to one enforcement task; the previous tasks were disabled and rollback files retained. See [QA.md](QA.md).
