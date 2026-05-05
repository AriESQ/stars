# terraform-cloud-cli [![tests](https://github.com/bendrucker/terraform-cloud-cli/workflows/tests/badge.svg?branch=master)](https://github.com/bendrucker/terraform-cloud-cli/actions?query=workflow%3Atests) [![Project Status: WIP](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

> Interactive CLI for operating workspaces in Terraform Cloud

`terraform-cloud` is an interactive CLI that helps automate complex and repetitive tasks in [Terraform Cloud](https://www.terraform.io/docs/cloud/index.html). It is designed to compliment the [Terraform Enterprise Provider](https://www.terraform.io/docs/providers/tfe/index.html). The `tfe` provider can manage teams, workspaces, variables, and other Terraform Cloud resources. This CLI is not focused on being a complete API client.

**Status**: Early development. You will likely encounter bugs. Breaking changes will bump the `0.x` version until version `1.0.0`.

## Installing

Binaries are available for each [tagged release](https://github.com/bendrucker/terraform-cloud-cli/releases). Download an appropriate binary for your operating system and install it into `$PATH`.

You can also install with Homebrew:

```sh
brew tap bendrucker/terraform-cloud-cli
brew install terraform-cloud-cli
```

## Usage

<!-- go run . --help -->
```
Usage: terraform-cloud [--version] [--help] <command> [<args>]

Available commands are:
    migrate    Migrate a Terraform module from an existing backend to Terraform Cloud
    open       Opens the Terraform Cloud UI to the workspace
```

<hr>

<!-- go run . migrate --help -->
### `migrate`

```
Usage: terraform-cloud migrate [options]
	Migrate a Terraform module from an existing backend to Terraform Cloud

Options:
  --hostname string
    	Hostname for Terraform Cloud

  --modules string
    	A directory where other Terraform modules are stored. If set, it will be scanned recursively for terraform_remote_state references.

  --organization string
    	Organization name in Terraform Cloud

  --tfvars-filename string
    	New filename for terraform.tfvars

  --workspace-name string
    	The name of the Terraform Cloud workspace (conflicts with --workspace-prefix)

  --workspace-prefix string
    	The prefix of the Terraform Cloud workspaces (conflicts with --workspace-name)

  --workspace-variable string
    	Variable that will replace terraform.workspace
```

The `migrate` command performs the following file updates and runs `terraform init` to trigger Terraform to copy state to the new

* Configures a remote backend. ([?](https://www.terraform.io/docs/cloud/migrate/index.html#step-5-edit-the-backend-configuration)).
* Updates any [`terraform_remote_state`](https://www.terraform.io/docs/providers/terraform/d/remote_state.html) data sources that match the previous backend configuration.
* Replaces `terraform.workspace` with a variable of your choice, `var.environment` by default. ([?](https://www.terraform.io/docs/state/workspaces.html#current-workspace-interpolation))
* Renames `terraform.tfvars` to a name of your choice, `terraform.auto.tfvars` by default. ([?](https://www.terraform.io/docs/cloud/workspaces/variables.html#terraform-variables))

#### Examples

##### Basic

```sh
terraform-cloud migrate --organization my-org --workspace-name my-ws ./path/to/module
```

##### Remote State

Updates `terraform_remote_state` data sources in `~/src/tf`:

```sh
terraform-cloud migrate --modules ~/src/tf # ...
```

##### Terraform Enterprise

By default, `terraform-cloud` connects to Terraform Cloud at `app.terraform.io`. Terraform Enterprise users can set a custom hostname:

```sh
terraform-cloud migrate --hostname terraform.enterprise.host # ...
```


## License

MIT © [Ben Drucker](http://bendrucker.me)
