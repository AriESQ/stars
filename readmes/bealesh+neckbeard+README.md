# neckbeard
<p align="center">
  <img src="docs/assets/neckbeard.png" alt="neckbeard" width="320">
</p>

**A plugin for your coding agent that turns an app into reviewable cloud
infrastructure and a cost estimate.** Plans and scaffolds for AWS, GCP, or Azure,
with GitHub Actions or GitLab CI, from a bundled catalog of maintained OpenTofu
modules. Pre-alpha: deployment coverage and delivery automation are incomplete.

Inspired by [ponytail](https://github.com/dietrichgebert/ponytail). The neckbeard handles your infra so you don't have to.

```
you:    /neckbeard:analyze
agent:  reads your repo → evidence-backed profile → asks what code can't tell it
you:    resolve the draft's questions, pick a cloud and a tier
agent:  plan → estimate ($83/mo, here's the table) → scaffold → validate
you:    review the files and follow docs/bootstrap.md per environment
next:   configure cloud access and verify deployment (coverage varies by lane)
```

## Why this exists

Coding agents are good at app code and bad at freehanding infrastructure. The
failure mode is always the same: plausible-looking HCL that is subtly broken,
insecure by default, and unestimable. neckbeard inverts the roles:

- **Humans maintain the golden path** — versioned OpenTofu modules, pipeline
  templates, GitOps layouts, per cloud.
- **The agent analyzes, parameterizes, and explains.** It reads your app,
  figures out what it needs, and maps that onto catalog inputs — with file:line
  evidence for every claim it makes.
- **Everything in between is deterministic code.** Same inputs, same bytes:
  the planner emits a hash-verified `blueprint.yaml` lockfile, the renderer is
  a pure function of it, and regeneration never silently overwrites your edits.

**The agent never invents infrastructure.** Needs the catalog can't express
become named findings ("redis is outside the workload contract"), not
force-fits onto the nearest module.

## The part nobody else tells you: what it costs

The same reference app (HTTP service + worker + cron + Postgres), smallest
tier, all three environments, live prices via Infracost:

| | Cloud Run | Container Apps | ECS Fargate | EKS | GKE (regional) | AKS |
|---|---|---|---|---|---|---|
| monthly | **$77** | ~$98\* | $250 | $396 | $754 | ~$801\* |

\* Infracost can't price Container Apps compute yet — and instead of letting a
low number lie, the report **names every unpriced resource**. That's the house
style: `neckbeard estimate` gives you baseline-while-idle costs, explicit usage
assumptions (a tier name is not a usage estimate — the numbers are, and you can
edit them), low/expected/high scenario ranges, and a provenance footer. Cloud budget alerts are planned; the current CLI does
not configure them. When implemented, alerts will notify, not cap spending.

It also prices your *decisions*: the table above is why neckbeard tells solo
developers "you don't need Kubernetes yet" — with receipts.

## Honesty as architecture

Infrastructure tools love implying more than they've proven. neckbeard reports
in three verdicts, and the third one is the point:

```
V0   PASSED         tofu validate [prd]
V0   PASSED         checkov policy [prd]        ← every skip carries a written reason
V0   PASSED         kubeconform (clusters/)
V1   NOT EXERCISED  authenticated plan          requires cloud credentials
V2   NOT EXERCISED  deployment verification     release-harness only for now
```

- Static validation **never claims deployability** — V0/V1/V2 are distinct
  levels, each reported as exercised or not.
- Every checkov skip in the generated `.checkov.yaml` states its reason. A
  skip without a reason is a lie about your security posture.
- When live runs break, the failures become public
  [findings](docs/findings/) and then harness requirements. Our first real
  deployment produced ten of them; five became catalog fixes the same day.
- Placeholder pins say "placeholder". Degraded paths print why (Azure + GitLab
  merge-request plans can't federate — the pipeline says so instead of failing
  mysteriously).

## What you get

- **Three isolated environments** (dev/stg/prd) with independent state, sized
  by tier presets over explicit dimensions: traffic, availability, RPO/RTO,
  operating capacity. Every preset value is visible and overridable within the
  catalog's tested envelope — and values outside it are *marked*, not blessed.
- **Two runtimes per cloud**: serverless containers (Cloud Run / ECS Fargate /
  Container Apps) or Kubernetes (EKS / GKE / AKS) with Flux manifests for dev
  image automation. Complete promotion, rollback, and serverless release
  automation remain subsequent work; initial image references are placeholders.
- **CI/CD for GitHub Actions or GitLab CI** from one internal model: test →
  build → scan (trivy blocks HIGH/CRITICAL) → push; infra plans on PRs with a
  read-only role, applies on main with a write role, prd gated by environment
  protection. **Zero static cloud keys** — OIDC federation everywhere,
  enforced by a test that fails if a rendered pipeline ever mentions
  `AWS_SECRET_ACCESS_KEY`.
- **Security posture as explicit controls**: private-by-default networks,
  secrets managers holding *names* the operator fills (values never touch
  neckbeard, its state, or your git history), scoped CI identities, managed
  WAF rules where the tier enables them.
- **A bootstrap runbook** (`docs/bootstrap.md`) that takes a human with
  elevated credentials through federated CI setup per environment —
  state backend first, then OIDC trust, then CI roles.

## Quick start

As a Claude Code plugin:

```
/plugin marketplace add bealesh/neckbeard
/plugin install neckbeard@neckbeard
```

then, in your app's repo: `/neckbeard:analyze`.

**Codex CLI, Cursor, or any [SKILL.md](https://developers.openai.com/codex/skills)-speaking agent:**

```sh
go install github.com/bealesh/neckbeard/cmd/neckbeard@latest
neckbeard skill install                  # .agents/skills/ — the open standard
neckbeard skill install -target cursor   # + repo slash commands for Cursor
neckbeard skill install -scope user      # once, for every repo on this machine
```

The skill is the same operating manual everywhere; only the discovery path
differs. Codex invokes it via `/skills` or `$neckbeard`; Cursor loads it on
demand and gets `/neckbeard-analyze` and `/neckbeard-sync` as commands.

Or drive the CLI directly:

```sh
go install github.com/bealesh/neckbeard/cmd/neckbeard@latest

neckbeard doctor -for plan # checks the bundled catalog; no cloud access
neckbeard analyze          # draft profile + the questions code can't answer
$EDITOR app-profile.yaml   # resolve each assumption with a same-id confirmed answer
$EDITOR neckbeard.yaml     # cloud, region, tier, runtime, repo
neckbeard plan             # deterministic blueprint + topology summary
neckbeard doctor -for estimate
neckbeard estimate         # the money table, before anything exists
neckbeard scaffold         # infra/, pipelines, clusters/ — yours to review
neckbeard validate         # V0: fmt, validate, checkov, kubeconform
```

The binary bundles the catalog, schemas, presets, and installed skill references:
**no neckbeard source checkout is needed**. Use `neckbeard schema neckbeard`,
`neckbeard schema app-profile`, and `neckbeard presets` for exact inputs. See the
[onboarding guide](plugin/skills/neckbeard/references/onboarding.md) for a complete
config and examples for existing databases and unsupported dependencies.

The supported workload is **one image, up to 10 HTTP/worker/cron processes**, with
repository-root build context. Omitted or empty `command` preserves image defaults.
`plan` refuses unresolved assumptions, undecided datastore provisioning, and
unsupported findings without an explicit disposition. Existing services use
`mode: reference` and a connection `secret_name`; their lifecycle remains external.

Scaffold includes pinned module contents under `.neckbeard/catalog/`. Commit that
directory with the generated infrastructure and ownership manifest. Upgrading to
a different bundled catalog requires a new plan and review of the diff. Explicit
`-catalog` and `-catalog-source` remain available for catalog development.

Planning and scaffolding need no external tools or cloud credentials. Estimates
need Infracost **0.10.x** and its pricing login. Validation needs the pinned
OpenTofu version, with Checkov, kubeconform (Kubernetes), and actionlint (GitHub)
for their respective gates. `neckbeard doctor -for estimate|validate|all` reports
missing or incompatible tools; `validate` reports unavailable checks as
NOT EXERCISED. Doctor checks tool availability, not cloud permissions or quotas.

## Status: pre-alpha, and precise about it

| lane | rendered + statically validated (V0) | deployed & verified live (V2) |
|---|---|---|
| AWS serverless / EKS | ✅ / ✅ | not yet / not yet |
| GCP serverless / GKE | ✅ / ✅ | not yet / not yet |
| Azure serverless / AKS | ✅ / ✅ | **✅ (manually)** / not yet |

The six-lane static matrix runs on every PR using the bundled catalog. Tests also
run a built binary from three unrelated fixture apps across all 12 cloud/VCS/runtime
combinations, including an existing database and external Redis. These tests cover
onboarding and rendering; pricing is stubbed in the automated fixture test. Exactly one lane has survived a real
cloud so far — deployed, health-checked over its public FQDN, updated, torn
down ([the findings](docs/findings/2026-09-08-azure-v2.md) are a good read on
what static validation can't see). The automated release harness that runs all
lanes against real accounts is the current milestone; until a lane has been
through it, treat its golden path as *designed and validated*, not *proven*.

Also honest: landing zones (org structure, central audit, guardrails — the
Path F story in [DESIGN.md](DESIGN.md)) are designed but not yet built; the
adopt path (existing accounts/projects/subscriptions) is what ships today.

## How it hangs together

```
            you / your agent                      deterministic core
        ┌──────────────────────┐            ┌───────────────────────────┐
repo ──▶│ analyze: facts w/    │  profile   │ plan: catalog @ pinned    │
        │ evidence, questions, ├───────────▶│ versions → blueprint.yaml │
        │ judgment, answers    │  config    │ (hash-verified lockfile)  │
        └──────────────────────┘            └─────────┬─────────────────┘
                                       ┌──────────────┼──────────────┐
                                       ▼              ▼              ▼
                                   estimate       scaffold        validate
                                   Infracost,     ownership       V0 static,
                                   scenarios,     contract:       V1 plan,
                                   unpriced       never silently  V2 deploy —
                                   named          overwrite       each reported
```

Deep dives: [DESIGN.md](DESIGN.md) (the full design, kept honest since day
one) · [docs/findings/](docs/findings/) (what reality taught us) ·
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache-2.0 — see [LICENSE](LICENSE).
