<p align="center">
<a href="#component-status"><img src="https://img.shields.io/badge/status-proof--of--concept-yellow" alt="Status"></a>
<a href="#terminology-this-is-not-an-air-gapped-system"><img src="https://img.shields.io/badge/egress-zero-critical" alt="Egress"></a>
<a href="https://opentofu.org"><img src="https://img.shields.io/badge/IaC-OpenTofu-blueviolet" alt="IaC"></a>
<a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-green" alt="Python"></a>
<a href="#license"><img src="https://img.shields.io/badge/license-proprietary-lightgrey" alt="License"></a>
</p>

<p align="center">
  <img src="/assets/AIR-Kit_logo_bleu.png" alt="AIRKit" width="240"><br />
  <a href="https://air-kit.tech/">air-kit.tech</a>
</p>

---

# AI Incident Response Kit
<img src="/assets/tagline-bleu.svg" alt="Self-hosted, zero-egress incident analysis infrastructure for security operations teams.">


<br />

## Table of Contents

- [Background](#background)
- [Zero-egress](#zero-egress-not-air-gapped)
- [Architecture](#architecture)
- [Repository Layout](#repository-layout)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
  - [Install](#install)
  - [Smoke Test](#smoke-test)
- [Data Model](#data-model)
- [Adapter Model](#adapter-model)
- [Tool Contract](#tool-contract)
- [Operational Notes](#operational-notes)
- [Known Limitations](#known-limitations)
- [Non-goals](#non-goals)
- [Development](#component-status)
- [Roadmap](#roadmap)
- [License](#license)

---

## Background

AIRKit deploys an open-weight LLM (GLM-5.2, served via SGLang) inside a network-isolated AWS subnet, ingests SIEM/EDR/network telemetry through a pluggable adapter layer, and exposes a read-only analysis agent against that telemetry through ClickHouse and Qdrant.

This repository implements exactly one item from a larger [30/60/90 runtime-control-plane playbook](https://ctolunchnyc.substack.com/i/208099023/runtime-control-plane-and-emergency-insulation-30-days) for agentic systems: **Deploy Insulated SecOps Analysis Node.** It does not implement reachability management, circuit breakers, an out-of-band kill switch, or trajectory monitoring of other agentic deployments. Those are later, separate phases of that playbook and are out of scope here. Do not assume this system provides runtime governance over other agents in your environment. See [Non-goals](#non-goals) before you deploy this and start relying on it for something it wasn't built to do.

The reason for self-hosting rather than calling a commercial API: an analyst asking a question during an active incident needs a model that will engage with real exploit code, C2 traffic, malicious payloads, and attacker tooling on their behalf. Commercial hosted models' safety classifiers routinely refuse that content because they cannot distinguish an incident responder reconstructing an attack from an attacker extending one. AIRKit exists to remove that failure mode. Everything else in this repository from the subnet design to the adapter contract to the ClickHouse/Qdrant split, exists to make that self-hosted model useful against real telemetry without also making it a new attack surface.

## Zero-egress, not Air-gapped

Precision here matters because the wrong mental model leads to wrong security assumptions downstream.

An air gap means total physical and logical isolation: no wire, no wireless link, nothing connecting the system to any other network, ever. A true air-gapped analysis workflow looks like a write-blocked USB drive physically carried to a disconnected machine. If your incident response platform needs to ingest live SIEM/EDR telemetry in real time, issue containment actions, or pull updated detection rules, it categorically cannot be air-gapped and still do those things.

AIRKit is **zero-egress**, not air-gapped. The distinction:

| | Air-gapped | AIRKit (zero-egress) |
|---|---|---|
| Ingests live telemetry | No | Yes, inbound-only |
| Reachable from outside the VPC | No | No |
| Can reach outside the VPC | No | No, with one narrow exception below |
| Operational overhead | Extremely high (manual media transfer) | Standard IaC |

The private subnet has no route to an Internet Gateway or NAT Gateway, and the security group defines ingress rules only. AWS security groups default-deny all outbound traffic absent an explicit egress rule, and this repository never adds one. The **only** path out of the subnet is a VPC S3 Gateway Endpoint, used exclusively to hydrate model weights from an internal, pre-staged S3 bucket over the AWS backbone. This is not a route to the public internet; it is a private, single-purpose channel to one bucket you control. If you need a channel-level audit of the external attack surface of this system, that endpoint is the entirety of it, and it is worth reviewing before you deploy.

If an analyst pulls a live malware sample or an active C2 implant off an endpoint for detonation and reverse engineering, that artifact goes on a genuinely air-gapped, physically disconnected workstation, not on this node. AIRKit is for telemetry analysis, not malware detonation.

## Architecture

```
[ SIEM / EDR / Zeek / syslog sources, internal network ]
                    │
                    │  (inbound only, per-adapter protocol)
                    ▼ 
  ┌────────────────────────────────────────────────────────┐
  │              ZERO-EGRESS PRIVATE SUBNET                │
  │                                                        │
  │  Vector (per-adapter ingestion, canonical mapping)     │
  │       │                                                │
  │       ▼                                                │
  │  ClickHouse (structured telemetry, SQL)                │
  │  Qdrant (playbooks, detection rules, incident history) │
  │       │                                                │
  │       ▼                                                │
  │  MCP tool servers (read-only)                          │
  │       │                                                │
  │       ▼                                                │
  │  SGLang serving GLM-5.2 (8-way tensor parallel, H200s) │
  │                                                        │
  │  Egress: NONE, except S3 Gateway Endpoint → weights    │
  │           bucket (model hydration only)                │
  └────────────────────────────────────────────────────────┘
                    │
                    │  (analyst console / SGLang API, internal CIDR only)
                    ▼
        [ Analyst workstation, internal network ]
```

Provisioning is OpenTofu, not HashiCorp Terraform. (And not Pulumi for obvious reasons.) Not just because of Terraform's BSL 1.1 license but that OpenTofu (Linux Foundation, MPL 2.0) has native client-side state encryption, because the state file for this deployment contains subnet IDs, instance IPs, and volume IDs for a security-critical node. Treat it as sensitive, not disposable, but rather indispensable. 

## Repository Layout

```
airkit/
├── install/            Installer: preflight checks, state tracking, health checks,
│                       schema deployment, adapter wiring. Entry point: install.sh.
├── infra/              OpenTofu: VPC, zero-egress subnet, security group, KMS,
│                       GPU compute node, EBS weights volume, SGLang bootstrap.
├── schema/
│   ├── ocsf/           Canonical event schemas (alert, incident, process_event,
│   │                   network_event, auth_event, file_event, raw_telemetry).
│   ├── clickhouse/ddl/ Table definitions matching the canonical schema.
│   └── qdrant/         Collection definitions (playbooks, detection_rules,
│                       incident_history) with hybrid dense+BM25 search config.
├── adapters/           Vendor-specific ingestion configs. contract/ defines what
│                       every adapter must implement; crowdstrike/, splunk-hec/,
│                       zeek/, generic-syslog/ are reference adapters;
│                       _template/ is the starting point for a new one.
├── agent/              Agent system prompt, MCP tool servers (ClickHouse,
│                       Qdrant), and the runtime loop wiring them to SGLang.
├── console/            Analyst-facing triage UI. Not yet implemented.
├── docs/                Not yet populated.
└── airkit.config.yaml.example   Copy to airkit.config.yaml and edit before install.
```

## Setup

### Prerequisites

- AWS account with quota for `p5e.48xlarge` (or your chosen instance type) under the EC2 "Running On-Demand P instances" vCPU-based service quota. This is the single most common reason a first install fails; request the increase before you start, not after `tofu apply` errors out.
- An S3 bucket, in the target region, pre-staged with GLM-5.2 FP8 weights under `GLM-5.2/`. This repository does not download weights from the public internet at any point. You stage them into your own bucket first, and the node hydrates from there over the S3 Gateway Endpoint.
- `tofu`, `aws` CLI (configured with credentials), `docker`, `jq`, `yq`, `python3` with `pyyaml` and `jsonschema` on the machine running the installer.
- An SSH key with access to hosts inside your `internal_corporate_cidr`, since the installer configures ingress restricted to that CIDR only.

### Configuration

Copy `airkit.config.yaml.example` to `airkit.config.yaml` and edit it. At minimum, set `aws.weights_s3_bucket`, `aws.internal_corporate_cidr`, and `enabled_adapters`. `generic-syslog` is enabled by default so nothing is silently dropped for sources without a dedicated adapter yet; this is a deliberate fallback, not a placeholder to delete.

Set these environment variables before running the installer:

```bash
export AIRKIT_DEEP_LEARNING_AMI_ID=ami-xxxxxxxx   # Deep Learning AMI, NVIDIA drivers + Docker pre-installed, your region
export AIRKIT_SSH_KEY_PATH=/path/to/your/key.pem
```

### Install

```bash
git clone <this-repository>
cd airkit
cp airkit.config.yaml.example airkit.config.yaml   # then edit it — see Configuration above
cd install
./install.sh
```

The installer is idempotent and resumable. It records progress to `install/state/.install-state.json` after each step and skips any step already marked complete on a re-run; a failed adapter-wiring step does not force a re-apply of infrastructure that already succeeded.

```bash
./install.sh --status    # show recorded progress
./install.sh --reset     # wipe recorded progress and start clean
```

Sequence: preflight checks (tools, AWS credentials, instance quota, weights bucket reachability) → a small, separate OpenTofu apply provisioning the KMS key used for state encryption (see the comment in `infra/modules/state-encryption/main.tf` for why this is a two-phase bootstrap rather than a single apply) → main infrastructure apply (network, compute, storage) → poll until the node is running and SGLang is actually serving requests, not merely until EC2 reports the instance state as running → ClickHouse and Qdrant schema deployment → adapter validation and wiring.

Weight hydration for a roughly 1.5TB model can take a long time depending on your S3 throughput. The health-check step accounts for this with a generous timeout; if it still times out, check `/var/log/airkit-bootstrap.log` on the node before assuming something is broken.

### Smoke Test

Once install completes, it prints the SGLang endpoint. Confirm the agent can reach both data stores and produce a grounded answer:

```bash
AIRKIT_SGLANG_ENDPOINT=<endpoint-from-install-output>/v1 \
  python3 agent/runtime/loop.py 'What alerts have fired in the last hour?'
```

An empty or all-`generic-syslog` result set is expected on a fresh install with no adapters beyond the default enabled — that confirms the pipeline is wired correctly, not that anything is broken. Enable a real adapter and re-run `./install.sh` to start seeing structured telemetry.

## Data Model

Canonical event schemas live in `schema/ocsf/` and are deliberately OCSF-shaped rather than a bespoke taxonomy: reuse a maturing, vendor-backed open standard instead of inventing a new one that only this repository understands. Seven event classes: `alert`, `incident`, `process_event`, `network_event`, `auth_event`, `file_event`, and `raw_telemetry` as the catch-all for anything an adapter can't yet classify.

Structured, high-volume telemetry lives in ClickHouse (`schema/clickhouse/ddl/`): one typed table per event class plus a universal `raw_events` fallback every event also lands in. This gives the agent both fast indexed queries for the common cases and a schema-agnostic search path for forensic work where you don't know the shape of what you're looking for yet. Playbooks, detection rules, and narrative incident history live in Qdrant (`schema/qdrant/collections.yaml`) with hybrid dense-vector-plus-BM25 search, since exact term matches (a specific IP, a rule name) and semantic similarity ("find something like this behavior") are both routine queries against that material.

## Adapter Model

Every vendor-specific data source is an adapter under `adapters/<name>/`: a `manifest.yaml` validating against `adapters/contract/adapter.schema.json`, plus a Vector (or FluentBit) collector config performing the field mapping into the canonical schema. This split exists so onboarding a new SIEM or EDR product is a config change, not a product change; the canonical schema and ClickHouse/Qdrant deployment never need to change when a new source is added.

`manifest.yaml` requires a `field_mapping_notes` field documenting every lossy or ambiguous mapping decision: how a vendor's severity scale collapsed onto the canonical five-value enum, which vendor-specific fields have no canonical home and are preserved only in the `raw` blob. This is not enforceable by the JSON Schema, but `install/lib/validate_adapter.py` checks for it and fails the build if it's empty. An undocumented lossy field mapping is exactly the kind of defect that surfaces mid-incident, when an analyst queries a field that silently doesn't mean what they think it means, rather than at adapter-authoring time when it would cost nothing to document.

To add a new source: copy `adapters/_template/`, fill in the manifest, write the collector config, run `python3 install/lib/validate_adapter.py <name>` until it passes, add the name to `enabled_adapters` in `airkit.config.yaml`, and re-run the installer. `wire_adapters` picks it up on the next apply.

## Tool Contract

The agent (`agent/prompts/soc_analyst.md`) has exactly two tools: `clickhouse_tool` and `qdrant_tool`, both under `agent/runtime/mcp_servers/`. Both are read-only, and that guarantee is enforced in code, not left to prompt instruction-following. `clickhouse_tool/server.py` rejects any query containing `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, or several other mutating keywords before it ever reaches ClickHouse, and rejects multi-statement input outright. `qdrant_tool/server.py` exposes search only; no ingestion path exists through the MCP layer at all. Indexing new playbooks or detection rules is a separate, offline process, specifically so the agent, or attacker-controlled text it has ingested from telemetry, cannot poison the playbook corpus through a tool call.

The agent's system prompt states directly that all queried data (incl. log lines, alert payloads, and command-line arguments) may contain attacker-controlled text, and instructs the model to analyze it rather than follow any instructions embedded in it. Treat this as defense in depth alongside the tool-level read-only guard, not a substitute for it.

## Operational Notes

- **Retention.** ClickHouse tables default to a 90-day TTL on telemetry (180 days on the `alerts` table, since it's the triage record rather than raw noise). Adjust per your retention policy in `schema/clickhouse/ddl/`; this is a starting default, not a compliance-reviewed figure.
- **State file.** `install/state/.install-state.json` is local to the machine running the installer, not stored in the repository, and not itself encrypted; it contains only step-completion markers and non-sensitive resource IDs, no secrets. The OpenTofu state files, which do contain sensitive infrastructure detail, are encrypted at rest via the KMS-backed state encryption block in `infra/main.tf`.
- **Health checks are not resumable by design.** `wait_for_node_fully_ready` always re-runs on every install invocation, even when every other step is marked complete, because node health is a point-in-time fact. The node can reboot or SGLang can crash between installer runs, and a stale "healthy" marker would be actively misleading.
- **Cost.** `p5e.48xlarge` with 8x H200 GPUs is a substantial, ongoing cost commitment. Confirm quota and budget before running `install.sh`, not after.

## Known Limitations

- No high-availability story. This deploys a single inference node. A node failure is a full outage of the analysis capability until it's replaced.
- No authentication layer in front of the SGLang API or the analyst console beyond network-level restriction to `internal_corporate_cidr`. Anyone reachable from that CIDR can query the model and, transitively, the telemetry stores. If your internal network's trust boundary doesn't match your security requirements here, add an authentication layer before relying on the CIDR restriction alone.
- `console/` (the analyst-facing triage UI) does not exist yet. Interact with the agent via `agent/runtime/loop.py` directly, or build the console as a follow-on.
- The adapter set ships with four references (CrowdStrike, Splunk HEC, Zeek, generic syslog), and none of them have been validated against a live vendor feed. Treat them as structurally correct starting points, not certified integrations, until you've run one against real data from that source.

## Non-goals

Explicitly out of scope for this repository, by design, not oversight:

- **Runtime governance of other agentic systems.** No Reachable State Analysis, no reachability manifest, no denial matrix, no out-of-band kill switch, no irreversible-transition approval gates. This system does not watch your other agents.
- **Automated containment or remediation.** Every tool exposed to the agent is read-only (see [Tool Contract](#tool-contract)). The agent produces analysis; a human analyst decides what to do about it.
- **Detonating live malware.** Use a genuinely air-gapped, physically disconnected workstation for that. See [Terminology](#terminology-this-is-not-an-air-gapped-system).
- **A fully automated onboarding wizard.** The installer sequences infrastructure, schema, and adapter deployment, but adapter authoring for a new telemetry source is a manual, reviewed process (see [Adapter Model](#adapter-model)). This is intentional — silent, unreviewed field-mapping decisions in a security telemetry pipeline are a worse failure mode than a manual step.

## Component Status (development)

| Component | Status |
|---|---|
| Infrastructure (`infra/`) | Proof of concept — applies cleanly, not yet run through a real failure/DR drill |
| Canonical schema (`schema/`) | Stable for the seven event classes defined; extend before assuming full OCSF parity |
| Reference adapters (`adapters/`) | Structurally validated against the contract schema; not validated against live vendor payloads |
| Agent runtime (`agent/`) | Functional proof of concept; read-only tool guards implemented and unit-testable, not yet load-tested |
| Installer (`install/`) | Functional; resumable state tracking implemented; not yet exercised against a mid-run AWS failure |
| Analyst console (`console/`) | Not implemented |

## Roadmap

Later phases of the originating playbook, not implemented here and not assumed by anything in this repository:

- Reasoning as a Span: capturing an agent's own reasoning and tool-call trajectory as OTel span DAGs.
- Reachable State Analysis: continuous monitoring of your own deployed agents for composite trajectory risk — credential acquisition, privilege accumulation, recursive delegation, persistence, identity transitions, network expansion.
- Reachability management: a machine-readable agent manifest and denial matrix defining what agents are physically blocked from reaching.
- Irreversible Transition Blocks and an out-of-band kill switch, separate from any model's own orchestration layer.

Do not build on top of this repository as though those capabilities already exist. They don't, yet.

## License

Proprietary — All Rights Reserved. No public license has been finalized for this repository; the badge and this section are placeholders pending that decision, not a statement of an open license. Do not treat the absence of a `LICENSE` file as permission to redistribute.
