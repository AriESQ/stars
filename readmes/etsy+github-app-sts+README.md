# github-app-sts

`github-app-sts` is a Secure Token Service (STS) for GitHub App credentials. With it, you can define policies to federate GitHub App tokens with configured OIDC providers.

For example, you can grant GitHub Actions in `repository-a` access to read, write, or any other permission that GitHub Apps allows, `repository-b`.

## How it works

`github-app-sts` implements the [OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693) RFC.

A client can authenticate with an OIDC token from a configured identity provider (e.g., GitHub Actions) and request access to a target GitHub organization or repository via the `resource` parameter, and a policy file via the `scope` parameter.

The server will load the policy file from the target repository, or from a designated repository for a target organization. It then verifies the token's claims against the policy's identities, and mints a scoped GitHub App installation token with the permissions defined in the policy.

## Getting Started

This section will describe the bare minimum to federate tokens with GitHub Actions running in your organization.

### Prerequisites

- You will need at least one GitHub app installed in your organization. It should at least have the `contents: read` permission. See GitHub's documentation [here](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app). Note the **client ID** and **installation ID**.

### Write the server config

We'll first create a server configuration that uses the GitHub App you've created. For simplicity, we'll reuse the app as both the "policy reader" and the "target", but in production you can use a separate app with more permissions as the target.

```yaml
# The expected OIDC audience claim. OIDC tokens must have this value
# in their "aud" claim. Should be the public URL of your STS.
audience: "https://sts.example.com"

# The HTTP port to listen on.
port: 8080

allowed_issuers:
  - "https://token.actions.githubusercontent.com"

# The STS's own GitHub App, used only for reading policy files and
# finding installations. Should have minimal permissions (contents: read).
policy_reader_app:
  client_id: <your-client-id>

  private_key:
    env: <environment-variable-with-your-github-app-key-here>

  installations:
    <your-organization>: <your-installation-id>

# We'll reuse the policy reader app for simplicity, but in production you can use an app with more permissions.
sts_target_apps:
  example:
    client_id: <your-client-id>

    private_key:
      env: <environment-variable-with-your-github-app-key-here>

    installations:
      <your-organization>: <your-installation-id>

# Organization-level configuration.
# Maps org names to the repository that holds their trust policies.
org_policy_repos:
  <your-organization>: ".github-sts"
```

### Start the server

Binary releases are provided in the [Releases](https://github.com/etsy/github-app-sts/releases) page.

```shell
github-app-sts-server --config config.yaml
```

### Write a policy

We will write a policy that demonstrates cross-repository access.

Create a file called `.github/sts/demo-policy.yaml` in a repository in your organization:

```yaml
# The target app alias, as defined in sts_target_apps in your server config.
target_app: example

identities:
  - issuer: "https://token.actions.githubusercontent.com"
    subject: "repo:<your-organization>/.*"

permissions:
  contents: read
```

This will allow any repository in your organization to use an access token to read from this repository.

### Use the GitHub Action

In any other repository, include the following in your GitHub Action workflow YAML:

```yaml
jobs:
  read-other-repo:
    runs-on: ubuntu-latest
    permissions:
      id-token: write # Required to request an OIDC token
    steps:
      - name: Exchange for GitHub App token
        id: sts
        # Use the latest tag in the Releases page instead of this.
        uses: etsy/github-app-sts@action/v2.0.0
        with:
          sts-url: "https://sts.example.com"
          policy: "demo-policy"
          target: "https://github.com/<your-organization>/<target-repo>"

      - name: Clone the target repo
        run: git clone https://x-access-token:${{ steps.sts.outputs.token }}@github.com/<your-organization>/<target-repo>.git
```

## Documentation

- [Server Configuration Reference](docs/server-config.md)
- [Policy Reference](docs/policies.md)

## Differences from [Octo STS](https://github.com/octo-sts/app)

This project is inspired by Octo STS, but has quite a few differences.

1. This project can federate multiple _independent_ GitHub Apps, each with their own permissions. You can still use a single App if you want, but separate Apps also allows for custom identities when leaving comments or opening pull requests.
2. Each policy can support multiple identities.
3. Policies can use CEL expressions for more complex OIDC claim verification.
4. **Only organization policies are allowed to contain organization permissions**. For example, repository policies cannot grant the permission to manage organization members. This means that you do not need to worry about repositories escalating their access via a GitHub App.

This project is also not available as a managed service, unlike Octo STS. You must self-host it.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md).
