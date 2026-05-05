# gh-repo-settings

[![CI](https://github.com/myzkey/gh-repo-settings/actions/workflows/lint.yml/badge.svg)](https://github.com/myzkey/gh-repo-settings/actions/workflows/lint.yml)
[![Test](https://github.com/myzkey/gh-repo-settings/actions/workflows/test.yml/badge.svg)](https://github.com/myzkey/gh-repo-settings/actions/workflows/test.yml)
[![Go Version](https://img.shields.io/github/go-mod/go-version/myzkey/gh-repo-settings)](https://github.com/myzkey/gh-repo-settings)
[![Release](https://img.shields.io/github/v/release/myzkey/gh-repo-settings)](https://github.com/myzkey/gh-repo-settings/releases)

[日本語](./docs/README.ja.md) | [简体中文](./docs/README.zh-CN.md) | [한국어](./docs/README.ko.md) | [Español](./docs/README.es.md)

**Manage repository settings as code with YAML + GitHub CLI.**

A GitHub CLI extension to manage repository settings via YAML configuration. Inspired by Terraform's workflow - define your desired state in code, see planned changes, and apply them.

## Why gh-repo-settings?

GitHub repository settings are hard to manage consistently:

- Clicking through the Settings UI doesn't scale
- Repository admins often drift from the desired configuration
- Terraform's GitHub provider is powerful, but requires:
  - A separate backend (state management)
  - GitHub provider authentication setup
  - Managing HCL files separately from your repository

**gh-repo-settings** provides:

- **Zero backend** - No state files to manage
- **Zero external dependencies** - Works entirely through GitHub CLI
- **YAML configuration** - Lives alongside your code in `.github/`
- **Terraform-like workflow** - Familiar `plan` / `apply` commands
- **Workflow validation** - Detects mismatches between `status_checks` and actual workflow job names

## Features

- **Infrastructure as Code**: Define repository settings in YAML files
- **Terraform-like workflow**: `plan` to preview, `apply` to execute
- **Export existing settings**: Generate YAML from current repository configuration
- **Schema validation**: Validate configuration before applying
- **Multiple config formats**: Single file or directory-based configuration
- **Secrets/Env check**: Verify required secrets and environment variables exist
- **Actions permissions**: Configure GitHub Actions permissions and workflow settings

## Installation

### Via GitHub CLI (Recommended)

```bash
gh extension install myzkey/gh-repo-settings
```

### Upgrade

```bash
gh extension upgrade myzkey/gh-repo-settings
```

### Manual Installation

Download the latest binary from [Releases](https://github.com/myzkey/gh-repo-settings/releases) and add it to your PATH.

## Quick Start

```bash
# Initialize config interactively
gh repo-settings init

# Preview changes (like terraform plan)
gh repo-settings plan

# Apply changes
gh repo-settings apply
```

Default config paths (in priority order):
1. `.github/repo-settings/` (directory)
2. `.github/repo-settings.yaml` (single file)

## Commands

### `init` - Initialize configuration

Create a configuration file interactively.

```bash
# Create .github/repo-settings.yaml interactively
gh repo-settings init

# Specify output path
gh repo-settings init -o config.yaml

# Overwrite existing file
gh repo-settings init -f
```

### `export` - Export repository settings

Export current GitHub repository settings to YAML format.

```bash
# Export to stdout
gh repo-settings export

# Export to single file
gh repo-settings export -s .github/repo-settings.yaml

# Export to directory (multiple files)
gh repo-settings export -d .github/repo-settings/

# Include secret names
gh repo-settings export -s settings.yaml --include-secrets

# Export from specific repository
gh repo-settings export -r owner/repo -s settings.yaml
```

### `plan` - Preview changes

Validate configuration and show planned changes without applying them.

#### Example Output

```diff
Repository: owner/my-repo

repo:
  ~ description: "Old description" → "New description"

labels:
  + feature (color: 0e8a16)
  ~ bug: color ff0000 → d73a4a
  - old-label

branch_protection (main):
  ~ required_reviews: 1 → 2

Plan: 2 to add, 2 to change, 1 to delete
```

```bash
# Preview all changes (uses default config path)
gh repo-settings plan

# Specify config file
gh repo-settings plan -c custom-config.yaml

# Specify config directory
gh repo-settings plan -d .github/repo-settings/

# Show current GitHub settings (useful for debugging)
gh repo-settings plan --show-current

# Check secrets
gh repo-settings plan --secrets

# Check environment variables
gh repo-settings plan --env

# Show variables/secrets to delete (not in config)
gh repo-settings plan --env --secrets --sync
```

The `--show-current` option displays the current GitHub repository settings, which is useful for:
- Debugging configuration issues
- Finding settings that exist on GitHub but are not in your config file
- Verifying what's actually configured on the repository

**Status Check Validation**: When running `plan`, the tool automatically validates that `status_checks` names in your branch protection rules match the job names defined in your `.github/workflows/` files. If a mismatch is found, you'll see a warning:

```
⚠ status check lint not found in workflows
⚠ status check test not found in workflows
  Available checks: build, golangci-lint, Run tests
```

### `apply` - Apply changes

Apply YAML configuration to the GitHub repository.

```bash
# Apply changes (uses default config path)
gh repo-settings apply

# Auto-approve without confirmation
gh repo-settings apply -y

# Specify config file
gh repo-settings apply -c custom-config.yaml

# Apply from directory
gh repo-settings apply -d .github/repo-settings/

# Apply variables and secrets
gh repo-settings apply --env --secrets

# Sync mode: delete variables/secrets not in config
gh repo-settings apply --env --secrets --sync
```

### ⚠️ Sync Mode Warning

The `--sync` flag enables **destructive operations**:

- Deletes labels not defined in your config (when `labels.replace_default: true`)
- Deletes variables not defined in your config
- Deletes secrets not defined in your config

**Always run `plan --sync` first** to preview what will be deleted:

```bash
# Preview deletions BEFORE applying
gh repo-settings plan --env --secrets --sync

# Only then apply if the plan looks correct
gh repo-settings apply --env --secrets --sync
```

> **Tip**: Avoid using `--sync` in CI without human review.

## Configuration

### Single File

Create `.github/repo-settings.yaml`:

```yaml
repo:
  description: "My awesome project"
  homepage: "https://example.com"
  visibility: public
  allow_merge_commit: false
  allow_rebase_merge: true
  allow_squash_merge: true
  delete_branch_on_merge: true

topics:
  - typescript
  - cli
  - github

labels:
  replace_default: true
  items:
    - name: bug
      color: ff0000
      description: Something isn't working
    - name: feature
      color: 0e8a16
      description: New feature request

branch_protection:
  main:
    required_reviews: 1
    dismiss_stale_reviews: true
    require_status_checks: true
    status_checks:
      - ci/test
      - ci/lint
    enforce_admins: false

env:
  variables:
    NODE_ENV: production
    API_URL: https://api.example.com
  secrets:
    - API_TOKEN
    - DEPLOY_KEY

actions:
  enabled: true
  allowed_actions: selected
  selected_actions:
    github_owned_allowed: true
    verified_allowed: true
    patterns_allowed:
      - "actions/*"
  default_workflow_permissions: read
  can_approve_pull_request_reviews: false
```

### Directory Structure

Alternatively, split configuration into multiple files:

```
.github/repo-settings/
├── repo.yaml
├── topics.yaml
├── labels.yaml
├── branch-protection.yaml
├── env.yaml
└── actions.yaml
```

## Configuration Reference

### `repo` - Repository Settings

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Repository description |
| `homepage` | string | Homepage URL |
| `visibility` | `public` \| `private` \| `internal` | Repository visibility |
| `allow_merge_commit` | boolean | Allow merge commits |
| `allow_rebase_merge` | boolean | Allow rebase merging |
| `allow_squash_merge` | boolean | Allow squash merging |
| `delete_branch_on_merge` | boolean | Auto-delete head branches |
| `allow_update_branch` | boolean | Allow updating PR branches |

### `topics` - Repository Topics

Array of topic strings:

```yaml
topics:
  - javascript
  - nodejs
  - cli
```

### `labels` - Issue Labels

| Field | Type | Description |
|-------|------|-------------|
| `replace_default` | boolean | Delete labels not in config |
| `items` | array | List of label definitions |
| `items[].name` | string | Label name |
| `items[].color` | string | Hex color (without `#`) |
| `items[].description` | string | Label description |

### `branch_protection` - Branch Protection Rules

```yaml
branch_protection:
  <branch_name>:
    # Pull request reviews
    required_reviews: 1          # Number of required approvals
    dismiss_stale_reviews: true  # Dismiss approvals on new commits
    require_code_owner: false    # Require CODEOWNERS review

    # Status checks
    require_status_checks: true  # Require status checks
    status_checks:               # Required status check names
      - ci/test
    strict_status_checks: false  # Require up-to-date branches

    # Deployments
    required_deployments:        # Required deployment environments
      - production

    # Commit requirements
    require_signed_commits: false # Require signed commits
    require_linear_history: false # Prevent merge commits

    # Push/merge restrictions
    enforce_admins: false        # Include administrators
    restrict_creations: false    # Restrict branch creation
    restrict_pushes: false       # Restrict who can push
    allow_force_pushes: false    # Allow force pushes
    allow_deletions: false       # Allow branch deletion
```

### `env` - Environment Variables and Secrets

Manage repository variables and secrets:

```yaml
env:
  # Variables with default values (can be overridden by .env file)
  variables:
    NODE_ENV: production
    API_URL: https://api.example.com
  # Secret names (values come from .env file or interactive prompt)
  secrets:
    - API_TOKEN
    - DEPLOY_KEY
```

| Field | Type | Description |
|-------|------|-------------|
| `variables` | map | Key-value pairs for repository variables |
| `secrets` | array | List of secret names to manage |

#### Using `.env` File

Create a `.github/.env` file (gitignored) to store actual values:

```bash
# .github/.env
NODE_ENV=staging
API_URL=https://staging-api.example.com
API_TOKEN=your-secret-token
DEPLOY_KEY=your-deploy-key
```

**Priority**: `.env` file values override YAML defaults for variables.

#### Commands

```bash
# Preview variable/secret changes
gh repo-settings plan --env --secrets

# Apply variables and secrets
gh repo-settings apply --env --secrets

# Delete variables/secrets not in config (sync mode)
gh repo-settings apply --env --secrets --sync
```

If a secret value is not found in `.env`, you'll be prompted to enter it interactively during `apply`.

#### Loading Secrets from AWS Secrets Manager

You can automatically load secrets from AWS Secrets Manager and write them to `.env`:

```yaml
env:
  provider:
    name: secretsmanager
    secret: /myapp/prod/secrets  # Secret name in AWS Secrets Manager
    region: ap-northeast-1
```

This fetches all keys from the secret JSON and writes them to `.github/.env`.

**Example**: If your AWS secret contains:
```json
{
  "API_TOKEN": "secret-value",
  "DB_PASSWORD": "db-secret"
}
```

Running `gh repo-settings plan --secrets` will write to `.github/.env`:
```
# Added by provider: 2024-01-15 10:30:00
API_TOKEN=secret-value
DB_PASSWORD=db-secret
```

**Filter specific keys**: To load only specific keys, specify them in `secrets`:

```yaml
env:
  provider:
    name: secretsmanager
    secret: /myapp/prod/secrets
    region: ap-northeast-1
  secrets:
    - API_TOKEN  # Only load this key
```

**Memory mode**: To load secrets without writing to file (in-memory only):

```yaml
env:
  provider:
    name: secretsmanager
    secret: /myapp/prod/secrets
    region: ap-northeast-1
    output: memory
```

| Field | Type | Description |
|-------|------|-------------|
| `provider.name` | `secretsmanager` | Provider type |
| `provider.secret` | string | Secret name/path in AWS Secrets Manager |
| `provider.region` | string | AWS region |
| `provider.output` | `file` \| `memory` | Output mode (default: `file`) |

> **Note**: Requires AWS CLI configured with appropriate credentials.

### `actions` - GitHub Actions Permissions

Configure GitHub Actions permissions for the repository:

```yaml
actions:
  # Enable/disable GitHub Actions
  enabled: true

  # Which actions can be used: "all", "local_only", "selected"
  allowed_actions: selected

  # When allowed_actions is "selected"
  selected_actions:
    github_owned_allowed: true    # Allow actions from GitHub
    verified_allowed: true        # Allow actions from verified creators
    patterns_allowed:             # Allow specific action patterns
      - "actions/*"
      - "github/codeql-action/*"

  # Default GITHUB_TOKEN permissions: "read" or "write"
  default_workflow_permissions: read

  # Allow GitHub Actions to create/approve pull requests
  can_approve_pull_request_reviews: false
```

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Enable GitHub Actions for this repository |
| `allowed_actions` | `all` \| `local_only` \| `selected` | Which actions are allowed |
| `selected_actions.github_owned_allowed` | boolean | Allow actions created by GitHub |
| `selected_actions.verified_allowed` | boolean | Allow actions from verified creators |
| `selected_actions.patterns_allowed` | array | Patterns for allowed actions |
| `default_workflow_permissions` | `read` \| `write` | Default GITHUB_TOKEN permissions |
| `can_approve_pull_request_reviews` | boolean | Allow Actions to approve PRs |

### `pages` - GitHub Pages Configuration

Configure GitHub Pages for the repository:

```yaml
pages:
  # Build type: "workflow" (GitHub Actions) or "legacy" (branch-based)
  build_type: workflow

  # Source configuration (only for legacy build type)
  source:
    branch: main
    path: /docs  # "/" or "/docs"
```

| Field | Type | Description |
|-------|------|-------------|
| `build_type` | `workflow` \| `legacy` | How Pages is built |
| `source.branch` | string | Branch for legacy builds |
| `source.path` | `/` \| `/docs` | Path within the branch |

## Editor Integration (VSCode)

This project provides a JSON Schema for YAML validation and auto-completion in VSCode.

### Setup

1. Install the [YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)

2. Add to your `.vscode/settings.json`:

```json
{
  "yaml.schemas": {
    "https://raw.githubusercontent.com/myzkey/gh-repo-settings/main/schema.json": [
      ".github/repo-settings.yaml",
      ".github/repo-settings/*.yaml"
    ]
  }
}
```

### Features

- Auto-completion for all fields
- Hover documentation
- Enum suggestions (`public`/`private`/`internal`, `read`/`write`, etc.)
- Unknown field detection
- Type validation

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Repo Settings Check

on:
  pull_request:
    paths:
      - ".github/repo-settings.yaml"
      - ".github/repo-settings/**"

jobs:
  check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      actions: read

    steps:
      - uses: actions/checkout@v4

      - name: Install gh-repo-settings
        run: gh extension install myzkey/gh-repo-settings
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Check drift
        run: gh repo-settings plan
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Managing Multiple Repositories

This tool applies settings to **one repository per execution**. To manage multiple repositories with the same configuration, use GitHub Actions matrix strategy:

```yaml
name: Sync Settings Across Repos

on:
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - ".github/repo-settings.yaml"

jobs:
  sync:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        repo:
          - myorg/service-a
          - myorg/service-b
          - myorg/service-c
      fail-fast: false

    steps:
      - uses: actions/checkout@v4

      - name: Install gh-repo-settings
        run: gh extension install myzkey/gh-repo-settings
        env:
          GH_TOKEN: ${{ secrets.ADMIN_TOKEN }}

      - name: Apply settings to ${{ matrix.repo }}
        run: gh repo-settings apply -y -r ${{ matrix.repo }}
        env:
          GH_TOKEN: ${{ secrets.ADMIN_TOKEN }}
```

> **Note**: Requires a PAT (`ADMIN_TOKEN`) with admin access to all target repositories.

## Global Options

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Show debug output |
| `-q, --quiet` | Only show errors |
| `-r, --repo <owner/name>` | Target repository (default: current) |

## Authentication & Permissions

This extension uses the GitHub CLI (`gh`) for authentication. Make sure you're logged in:

```bash
gh auth login
```

### Required Token Permissions

| Feature | Required Scopes |
|---------|-----------------|
| Repository settings | `repo` |
| Branch protection | `repo` (admin access to repository) |
| Secrets check | `repo`, `admin:repo_hook` |
| Environment variables | `repo` |
| Actions permissions | `repo`, `admin:repo_hook` |

### Token Types

- **`GITHUB_TOKEN` (GitHub Actions)**: Works for most operations within the same repository. However, branch protection rules require admin access, which `GITHUB_TOKEN` may not have by default.
- **Personal Access Token (PAT)**: Required for cross-repository operations or when `GITHUB_TOKEN` lacks sufficient permissions. Use a fine-grained PAT with `Repository administration` permission for full functionality.

## FAQ

### Can I apply settings to multiple repositories at once?

Not directly. This tool manages **one repository per execution**.

To apply the same configuration across multiple repositories:
1. Place the same YAML config in each repository, or
2. Use GitHub Actions matrix strategy (see [Managing Multiple Repositories](#managing-multiple-repositories))

### Does this tool support multiple environments (dev/staging/prod)?

Not natively. The `env` block manages one set of variables/secrets per repository.

For environment-specific values, you can:
- Use different `.env` files (`.env.dev`, `.env.staging`, `.env.prod`) and switch them in CI
- Use GitHub Environments (not yet supported by this tool)

### What happens if I run `apply` without `plan` first?

The tool will show you the planned changes and ask for confirmation before applying. Use `-y` flag to skip confirmation (not recommended for first-time use).

### Can I manage organization-level settings?

No. This tool only manages repository-level settings. Organization settings require different API permissions and are out of scope.

## Development

```bash
# Build
make build

# Run tests
make test

# Lint (requires golangci-lint)
make lint

# Build for all platforms
make build-all

# Clean build artifacts
make clean
```

## License

MIT
