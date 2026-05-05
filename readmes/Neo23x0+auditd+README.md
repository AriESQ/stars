[![Actively Maintained](https://img.shields.io/badge/Maintenance%20Level-Actively%20Maintained-green.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

        ___             ___ __      __
       /   | __  ______/ (_) /_____/ /
      / /| |/ / / / __  / / __/ __  / 
     / ___ / /_/ / /_/ / / /_/ /_/ /  
    /_/  |_\__,_/\__,_/_/\__/\__,_/   

Best Practice Auditd Configuration

## Idea

The idea of this auditd configuration is to provide a best-practice baseline that

- is designed to load out-of-the-box on major Linux distributions
- covers a broad set of security-relevant host activity
- prefers reusable telemetry over long lists of hard-coded detections
- keeps the detection logic in Sigma rules, SIEM content, or host-side analytics
- stays easy to read and adapt through sectioning and comments

The simplified ruleset intentionally keeps some high-value but potentially
high-volume telemetry, especially process creation, socket creation, and file
access failure events. Tune these sections to your environment if needed.

## Coverage

The current configuration focuses on the following coverage areas:

- self-auditing and audit configuration integrity
- noise filters and portability-oriented exclusions
- kernel, module, mount, swap, and time changes
- scheduled tasks, account databases, PAM, sudo, and login state
- network, firewall, startup, service, and boot-path configuration
- library paths, shell profiles, SSH, systemd, and MAC policy changes
- failed access attempts, DAC modifications, session files, and privilege-abuse heuristics
- special primitives such as `ptrace`, `memfd_create`, `bpf`, namespaces, `io_uring`, and `userfaultfd`
- software, container, and security-tooling configuration paths
- high-volume telemetry such as `execve`, `execveat`, socket creation, file deletion, and 32-bit ABI usage

## Related Projects

This ruleset is intended to stay agnostic of the downstream detection logic.
It focuses on collecting broadly useful audit telemetry that can then be
analyzed in different ways, for example with Sigma-based tooling or SIEM
queries.

One open source project that can make use of this audit data is
[Aurora Linux](https://github.com/Nextron-Labs/aurora-linux), a lightweight
and customizable Sigma-based agent for Linux that combines eBPF-based telemetry
with user-space enrichment and Sigma rule matching.

## Validation

This ruleset intentionally includes `-i` so that optional distro-specific paths
do not abort loading on systems where some binaries or directories are absent.
This keeps the default deployment simple, but it also means rule load errors are
ignored.

If you want a strict pre-deployment validation, test a temporary copy with the
`-i` line removed, for example:

```bash
grep -v '^-i$' audit.rules > /tmp/audit.rules.strict
auditctl -R /tmp/audit.rules.strict
```

The repository also includes GitHub Actions checks that lint the rules and
validate that a portable CI copy and a strict copy can both be loaded on Ubuntu.

## UID_MIN

Several rules in `audit.rules` use `auid>=1000 -F auid!=unset` to focus on
interactive user activity and exclude unset login sessions.

`1000` is the common `UID_MIN` on many Linux distributions, but it is not
universal. If your host uses a different `UID_MIN`, check `/etc/login.defs`
and replace `1000` in `audit.rules` before deployment:

```bash
awk '$1=="UID_MIN" { print $2 }' /etc/login.defs
```

## Sources

The configuration is based on the following sources and years of merged
improvements to the default ruleset:

Gov.uk auditd rules
https://github.com/gds-operations/puppet-auditd/pull/1

CentOS 7 hardening
https://highon.coffee/blog/security-harden-centos-7/#auditd---audit-daemon

Linux audit repo 
https://github.com/linux-audit/audit-userspace/tree/master/rules

Auditd high performance linux auditing
https://linux-audit.com/tuning-auditd-high-performance-linux-auditing/

### Further rules

Not all of these rules have been included. 

For PCI DSS compliance see: 
https://github.com/linux-audit/audit-userspace/blob/master/rules/30-pci-dss-v31.rules

For NISPOM compliance see:
https://github.com/linux-audit/audit-userspace/blob/master/rules/30-nispom.rules

## Video Explanations by IppSec

IppSec captured a video that explains how to detect the exploitation of the
OMIGOD vulnerability using auditd. The core auditd concepts in that video are
still useful, but the ruleset in this repository has since been simplified
significantly. Treat the video as historical background and an introduction to
auditd-based detection ideas, not as line-by-line documentation of the current
`audit.rules`.

https://www.youtube.com/watch?v=lc1i9h1GyMA

## Contribution

Please contribute your changes as pull requests
