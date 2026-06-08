# terraform-review-agent

[![CI](https://github.com/infiniumtek/terraform-review-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/infiniumtek/terraform-review-agent/actions/workflows/ci.yml)
[![Build Image](https://github.com/infiniumtek/terraform-review-agent/actions/workflows/build-image.yml/badge.svg)](https://github.com/infiniumtek/terraform-review-agent/actions/workflows/build-image.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?logo=langchain&logoColor=white)
![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?logo=terraform&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-D7FF64?logo=ruff&logoColor=black)
![mypy: strict](https://img.shields.io/badge/mypy-strict-2A6DB2?logo=python&logoColor=white)

**LLM providers:**
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-191919?logo=anthropic&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?logo=googlegemini&logoColor=white)

A reusable GitHub Actions workflow that reviews Terraform pull requests with a
LangGraph multi-agent system and posts a single, severity-ranked sticky comment.

Three specialists run in parallel over the PR's changed Terraform files:

| Agent | Scanners | Looks for |
|:--|:--|:--|
| 🔒 **Security** | `tfsec` + `checkov` | misconfigurations, insecure defaults, exposed resources |
| 💰 **Cost** | `infracost diff` | monthly cost deltas vs. the base branch |
| 🎨 **Style** | `tflint` + `terraform fmt -check` | lint findings and formatting drift |

Scanners own *detection and severity*; an LLM only rewords each finding into a
concise, actionable sentence — so the set of findings is deterministic run to
run. Results are merged, de-duplicated, severity-ranked, and upserted as one
comment (edited in place on every push) rather than stacking up.

Everything runs inside a prebuilt container (`ghcr.io/infiniumtek/terraform-review-agent`)
that bundles pinned `terraform`, `tfsec`, `tflint`, `infracost`, and `checkov`
binaries, so there are **no per-run tool installs**.

---

## Quick start

Add a workflow to your repo that calls the reusable workflow. A complete,
commented sample lives in [`examples/example-caller.yml`](examples/example-caller.yml);
the minimal version:

```yaml
# .github/workflows/terraform-review.yml
name: terraform-review

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
    paths:
      - "**/*.tf"
      - "**/*.tfvars"
      - "**/*.tf.json"
      - "**/*.tfvars.json"

jobs:
  terraform-review:
    uses: infiniumtek/terraform-review-agent/.github/workflows/terraform-review.yml@v1
    permissions:
      contents: read         # checkout
      pull-requests: write    # post/edit the sticky comment
    with:
      llm-provider: anthropic
      llm-model: claude-sonnet-4-5
      fail-on-severity: high  # fail the check on any high/critical finding
    secrets:
      anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
      infracost-api-key: ${{ secrets.INFRACOST_API_KEY }}   # optional; enables cost agent
```

Pin `@v1` (the major float) or a specific release tag such as `@v1.2.3`. The
`paths` filter on the trigger decides whether the job spins up at all; the agent
additionally early-exits if no Terraform files actually changed.

> **Manual re-runs:** `workflow_dispatch` events carry no PR context, so pass a
> `pr-number` input when triggering manually. See the example caller for the
> `github.event.pull_request.number || inputs.pr-number` pattern.

---

## Inputs

| Input | Default | Description |
|:--|:--|:--|
| `llm-provider` | `openai` | `openai` \| `anthropic` \| `google`. |
| `llm-model` | `gpt-4o` | Model id — **must match the provider**. The default suits `openai`; set this when choosing another provider (e.g. `claude-sonnet-4-5`). |
| `fail-on-severity` | `none` | Gate CI when a finding meets/exceeds this floor: `critical` \| `high` \| `medium` \| `low` \| `info` \| `none`. The comment is always posted first; `none` never fails the check. |
| `pr-number` | `""` | PR to review. Defaults to the triggering `pull_request` event; required for `workflow_dispatch` runs. |

## Secrets

| Secret | Required | Description |
|:--|:--|:--|
| `openai-api-key` / `anthropic-api-key` / `google-api-key` | one, matching `llm-provider` | LLM credentials. |
| `infracost-api-key` | optional | Enables the 💰 cost agent. When unset, cost review is skipped (security + style still run). Get a free key at [infracost.io](https://www.infracost.io/). |
| `github-token` | optional | Defaults to the caller's `${{ github.token }}`. Override only if you need broader scope. |

## Permissions

The calling job needs:

```yaml
permissions:
  contents: read          # checkout the PR merge ref
  pull-requests: write     # create/edit the sticky comment
```

---

## Sample comment

> ## Terraform Review Agent
>
> **5 findings** in 3 files — 1 critical, 2 high, 1 medium, 1 low
>
> _By agent:_ 🔒 Security 2 · 💰 Cost 1 · 🎨 Style 2
>
> 💰 **Infracost estimate:** **$520.50/mo** total · **+$120.00/mo** from this PR
>
> ### 🔴 Critical (1)
>
> | Severity | Issue | Location |
> |:--|:--|:--|
> | 🔴 🔒 | **S3 bucket has no server-side encryption configured.** <br> 💡 Add an `aws_s3_bucket_server_side_encryption_configuration` block. <br> <sub>`tfsec:aws-s3-enable-bucket-encryption`</sub> | `modules/s3/main.tf:12` |
>
> ### 🟠 High (2)
>
> | Severity | Issue | Location |
> |:--|:--|:--|
> | 🟠 💰 | **Estimated monthly cost change for `aws_instance.web`: +$120.00** <br> 💡 Consider a smaller instance type or autoscaling. <br> <sub>`infracost:resource-delta`</sub> | `.` |
> | 🟠 🔒 | **S3 bucket access logging is not enabled.** <br> 💡 Enable access logging to an audit bucket. <br> <sub>`checkov:CKV_AWS_18`</sub> | `modules/s3/main.tf:12` |
>
> ### 🟡 Medium (1)
>
> | Severity | Issue | Location |
> |:--|:--|:--|
> | 🟡 🎨 | **variable "region" is declared but never used.** <br> 💡 Remove the unused variable. <br> <sub>`tflint:terraform_unused_declarations`</sub> | `main.tf:9` |
>
> <details><summary>Low &amp; info (1)</summary>
>
> #### 🔵 Low (1)
>
> | Severity | Issue | Location |
> |:--|:--|:--|
> | 🔵 🎨 | **File does not match `terraform fmt` canonical style.** <br> 💡 Run `terraform fmt` locally and commit the result. <br> <sub>`terraform-fmt:unformatted`</sub> | `main.tf` |
>
> </details>

Critical / high / medium findings show inline; `low` and `info` collapse into a
`<details>` block so the comment stays scannable. Each location links to the
exact file and line at the PR head. On the next push, this same comment is
edited in place.

---

## How it works

```
GitHub PR event
  └─► reusable workflow (terraform-review.yml)
        └─► container: ghcr.io/infiniumtek/terraform-review-agent:v1
              └─► python -m terraform_review_agent.entrypoint
                    └─► LangGraph:
                          start ─► [security ∥ cost ∥ style] ─► aggregator ─► post_comment
```

- **start** filters the PR to Terraform files and early-exits if none changed.
- **security / cost / style** run their scanners, then an LLM rewords the
  findings (it cannot change severity, file, line, or rule).
- **aggregator** dedupes by `(file, rule, line)`, severity-ranks, and renders
  the markdown.
- **post_comment** upserts the sticky comment via a hidden HTML marker.

Scanner versions are pinned in the container image — bumping one is a
rebuild-image PR in this repo, not an edit to your workflow file.

---

## Local development

Requires Python 3.13 + [uv](https://docs.astral.sh/uv/). Scanners only run
inside the container; the host test suite mocks them.

```bash
make install              # create .venv and sync pinned deps
make fmt lint type test    # format, lint, mypy --strict, pytest
```

See [`CLAUDE.md`](CLAUDE.md) for the full project contract and layout.

### Run the agent against a real PR locally

`make run` executes the CLI **inside the container**, which bundles every
scanner (`terraform` / `tfsec` / `tflint` / `infracost` / `checkov`) — your host
`.venv` does not. For an external repo the entrypoint clones the PR's merge ref
into a scratch dir, scans it, and upserts the sticky comment on that PR, exactly
as the reusable workflow does in CI.

1. **Configure `.env`** (copy `.env.example`). For an end-to-end run you need:

   ```env
   GITHUB_TOKEN=ghp_...            # read access to the repo + write access to its PRs
   DEFAULT_LLM_PROVIDER=anthropic   # openai | anthropic | google
   DEFAULT_LLM_MODEL=claude-sonnet-4-5
   ANTHROPIC_API_KEY=sk-ant-...     # the key matching DEFAULT_LLM_PROVIDER
   INFRACOST_API_KEY=ico-...        # optional — enables the cost agent
   ```

2. **Build the image** (bundles the pinned scanners). Re-run only after a
   dependency or scanner-version bump; `./src` is bind-mounted, so code edits
   need no rebuild:

   ```bash
   make docker-build
   ```

3. **Review a PR.** Point `--repository`/`--pr-number` at any repo your token
   can reach. Using the sample Cloud Run service repo
   [`spanosg131/gcp-test-cloudrun-service`](https://github.com/spanosg131/gcp-test-cloudrun-service)
   — open (or reuse) a PR there that touches a `.tf` file, then:

   ```bash
   make run ARGS="--repository spanosg131/gcp-test-cloudrun-service --pr-number 2"
   ```

   The agent fetches the PR, runs the three specialists, and posts/edits the
   sticky comment on PR #2. (You can also set `GITHUB_REPOSITORY` /
   `GITHUB_PR_NUMBER` in `.env` and run `make run` with no `ARGS`.)

> **Notes**
> - The token needs `pull-requests: write` to post the comment and read access
>   to clone the PR; without `INFRACOST_API_KEY` the 💰 cost agent is skipped.
> - To inspect output without posting, point at a PR in a throwaway repo, or
>   review the structured logs the run prints to stderr.

---

## License

MIT
