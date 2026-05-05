# Terraform Credentials from the macOS Keychain

`terraform-credentials-keychain` is a shell script which implements the [Terraform credentials helpers API](https://www.terraform.io/docs/internals/credentials-helpers.html), allowing you to store and retrieve credentials for services like Terraform Cloud securely in the macOS Keychain.

**Note:** Consider using [bendrucker/terraform-credentials-helper](https://github.com/bendrucker/terraform-credentials-keychain), which is more likely to be maintained.

## Usage

1. Download the `terraform-credentials-keychain` file from this repository, and copy it to your global plugins path, `~/.terraform.d/plugins`.
1. Edit [your Terraform CLI configuration](https://www.terraform.io/docs/commands/cli-config.html) to enable the helper:

    ```hcl
    credentials_helper "keychain" {}
    ```
1. Ensure that you have manually configured an empty block for the public registry in the same file:

    ```hcl
    credentials "registry.terraform.io" {}
    ```

    This ensures that the helper is not triggered for API calls which install providers and modules.
1. Use [`terraform login`](https://www.terraform.io/docs/commands/login.html) to create a Terraform Cloud token and store it in your keychain.
1. Later you can remove the stored token with [`terraform logout`](https://www.terraform.io/docs/commands/logout.html)
