# AGHS testbed

Small workflows for exercising deployed STS, environment-gate, and actions-dispatch
instances from [github-services](https://github.com/astral-sh/github-services).
These demos call the services; they do not build or deploy them.

| Demo | Trigger | What it verifies |
| --- | --- | --- |
| [STS](.github/workflows/sts-demo.yml) | Run manually on `main` | A GitHub OIDC token can be exchanged for an App token scoped to this repository. The token is revoked after use. |
| [Environment gate](.github/workflows/release.yml) | Run manually on `main` | Human approval of `release-gate` allows the service to approve the subsequent `release` deployment in the same run. |
| [Dispatch](.github/workflows/dispatch-demo.yml) | Open a same-repository PR | A signed pull request webhook dispatches a workflow from trusted `main`, which replies on the PR with the verified head SHA and run link. |

## Connect the services

Deploy the service versions you intend to validate and install their GitHub Apps on
this repository. A published Serverless Application Repository version is not a
running service. Point the gate and dispatch Apps' webhooks at the corresponding
deployed `WebhookUrl` outputs, with their configured webhook secrets.

The policies below are complete examples for a dedicated demo deployment. Services
read their explicitly configured policy source; checking these files into a
repository does not automatically activate them.

| Service | Policy file | GitHub App access |
| --- | --- | --- |
| STS | [`.github/ost-simple-sts.json`](.github/ost-simple-sts.json) | Contents read on this repository and its policy repository |
| Environment gate | [`.github/environment-gate.json`](.github/environment-gate.json) (inline policy example) | Actions read and Deployments write on this repository |
| Dispatch | [`.github/ost-actions-dispatch.json`](.github/ost-actions-dispatch.json) | Actions write, Contents read, and Pull requests read; subscribe to Pull request events |

For STS and dispatch, set `PolicyRepository=astral-sh/aghs-testbed`,
`PolicyRepositoryId=1357148725`, `PolicyRef=main`, and `PolicyPath` to the
corresponding file above. They share the testbed App, so use its installation ID
for both services' `PolicyInstallationId`. The dispatch policy repository and
event repository must be covered by the same installation.

The testbed gate stack uses a separate App and `PolicySource=json`, with an inline
`PolicyJson` in Terraform matching the example above. To read the gate policy
from this repository instead, use `PolicySource=github`, an empty `PolicyJson`,
and the repository, path, and gate App installation settings described above.
That option also requires Contents read permission on the policy repository.

If STS or dispatch already reads a shared policy repository, add the demo's
repository alias and rules there instead. The gate's configured policy must match
the workflow and environment names in its example. Preserve unrelated policy rules.
Allow up to five minutes for a cached policy to refresh. Manage branch and
environment protections through
[github-policies](https://github.com/astral-sh/github-policies), and protect `main`
before granting service access.

Set these non-secret [repository variables](https://github.com/astral-sh/aghs-testbed/settings/variables/actions):

| Variable | Value |
| --- | --- |
| `STS_EXCHANGE_URL` | The STS stack's full HTTPS `ExchangeUrl`, including `/exchange` |
| `STS_AUDIENCE` | The same stack's HTTPS `PolicyAudience` |
| `GATE_APP_SLUG` | The deployed gate App's slug, as shown in its `github.com/apps/<slug>` URL |

No App private keys, webhook secrets, or AWS credentials belong in this repository.

## STS

Run **STS demo** from Actions, or:

```bash
gh workflow run sts-demo.yml --repo astral-sh/aghs-testbed --ref main
```

The job requests `contents: read` for this repository. It calls GitHub's
installation-repositories API with the issued token and checks that exactly this
repository, including its immutable ID, is accessible. Cleanup revokes the App
token even if that check fails. The built-in workflow token has no Contents grant.

The example calls the exchange API directly because a public repository cannot
consume the action housed in the private `github-services` repository.

The policy permits only `sts-demo.yml`, the `workflow_dispatch` event, and
`refs/heads/main`. To check rejection, create a temporary branch from `main` and
dispatch the same workflow on that branch: the exchange must fail with HTTP 403.
The policy uses GitHub's immutable OIDC subject format for newly created repositories.

## Environment gate

This demo requires a public repository on GitHub Team. Private and internal
repositories require Enterprise for custom deployment protection rules.
See [GitHub's requirements](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/create-custom-protection-rules).

Configure two environments:

- **`release-gate`**: require a human reviewer and restrict deployments to `main`.
- **`release`**: enable the deployed gate App's custom deployment protection rule
  and restrict deployments to `main`.

The gate App must subscribe to **Deployment protection rule** events. Keep normal
GitHub deployment creation enabled for both jobs.

Run **Environment gate demo**:

```bash
gh workflow run release.yml --repo astral-sh/aghs-testbed --ref main
```

The first job checks that the reviewer and configured App protections actually
exist. Review and approve the `release-gate` deployment in the run. Once that job
succeeds, GitHub asks the gate service to approve `release`; the protected job runs
only after approval. Look for the App's approval in the deployment history.

Rejecting the human review should keep the protected job from running. That checks
the human prerequisite; it does not by itself exercise the service's rejection
callback. A green workflow without a configured custom rule would not prove that
the service ran, which is why the setup check is required.

## Dispatch

The receiver workflow has only a `workflow_dispatch` trigger. The dispatcher
handles the `pull_request` webhook's `opened` action and calls that workflow on
`main`; the receiver does not check out or execute PR code. Its `GITHUB_TOKEN` has
`pull-requests: write` so it can post the result on the PR.

1. Open a non-draft PR from a branch **in this repository**. A small change is enough.
2. Expect a **Dispatch demo** run, followed by a reply from `github-actions[bot]`
   containing the verified PR head SHA, workflow ref and commit, dispatcher actor,
   and run link. The workflow ref should be `refs/heads/main`.

Open a new PR to repeat the demonstration. Comments, pushes to an existing PR,
and reopening a PR do not trigger it. Allow up to five minutes after a policy
change for the cache to refresh before opening the PR. The dispatcher fetches the
live PR and checks that its head SHA still matches the opening event. The workflow
can run even if the PR targets a branch other than `main`; the workflow itself
always comes from `main`.

Ordinary issues, draft/closed PRs, and fork PRs should not produce a run.
Running the receiver manually does not validate webhook handling.

For rejection evidence, correlate the GitHub App webhook delivery ID with the
webhook or worker logs. A webhook HTTP 202 acknowledges receipt; the linked
workflow run and PR reply are the positive end-to-end result.
