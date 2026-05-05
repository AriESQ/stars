# terraform-aws-tardigrade-org-new-account-delete-cloudtrail

A Terraform module to delete the default cloudtrail when new AWS accounts
are added or invited to an AWS Organization.

The Lambda function is triggered for the account by an Event Rule that matches
the CreateAccountResult or InviteAccountToOrganization events. The function then
deletes the default cloudtrail and s3 objects and buckets for that account.

<!-- BEGIN TFDOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.3 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.9 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 4.9 |

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy_document.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_partition.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/partition) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_project_name"></a> [project\_name](#input\_project\_name) | Project name to prefix resources with | `string` | n/a | yes |
| <a name="input_assume_role_name"></a> [assume\_role\_name](#input\_assume\_role\_name) | Name of the IAM role that the lambda will assume in the target account | `string` | `"OrganizationAccountAccessRole"` | no |
| <a name="input_cloudtrail_name_prefix"></a> [cloudtrail\_name\_prefix](#input\_cloudtrail\_name\_prefix) | Name Prefix of the cloudtrail name to delete | `string` | `"cloudtrail-"` | no |
| <a name="input_dry_run"></a> [dry\_run](#input\_dry\_run) | Boolean toggle to control the dry-run mode of the lambda function | `bool` | `true` | no |
| <a name="input_error_not_found"></a> [error\_not\_found](#input\_error\_not\_found) | Error if the cloudtrail name/pattern is not found | `bool` | `true` | no |
| <a name="input_event_bus_name"></a> [event\_bus\_name](#input\_event\_bus\_name) | Event bus name to create event rules in | `string` | `"default"` | no |
| <a name="input_event_types"></a> [event\_types](#input\_event\_types) | Event types that will trigger this lambda | `set(string)` | <pre>[<br/>  "CreateAccountResult",<br/>  "InviteAccountToOrganization"<br/>]</pre> | no |
| <a name="input_lambda"></a> [lambda](#input\_lambda) | Object of optional attributes passed on to the lambda module | <pre>object({<br/>    artifacts_dir            = optional(string, "builds")<br/>    build_in_docker          = optional(bool, false)<br/>    create_package           = optional(bool, true)<br/>    ephemeral_storage_size   = optional(number)<br/>    ignore_source_code_hash  = optional(bool, true)<br/>    local_existing_package   = optional(string)<br/>    memory_size              = optional(number, 128)<br/>    recreate_missing_package = optional(bool, false)<br/>    runtime                  = optional(string, "python3.12")<br/>    s3_bucket                = optional(string)<br/>    s3_existing_package      = optional(map(string))<br/>    s3_prefix                = optional(string)<br/>    store_on_s3              = optional(bool, false)<br/>    timeout                  = optional(number, 300)<br/>  })</pre> | `{}` | no |
| <a name="input_log_level"></a> [log\_level](#input\_log\_level) | Log level for lambda | `string` | `"INFO"` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | Tags for resource | `map(string)` | `{}` | no |

## Outputs

No outputs.

<!-- END TFDOCS -->

## CLI Option

Steps to run via the CLI

1. Install and configure aws cli.
2. Set AWS_PROFILE and AWS_DEFAULT_REGION (account and region that can assume the role and run commands from)
3. Review the options for the script and run

### Script Options

```bash
Supported Environment Variables:
    'LOG_LEVEL': defaults to 'info'
        - set the desired log level ('error', 'warning', 'info' or 'debug')

    'DRY_RUN': defaults to 'true'
        - set whether actions should be simulated or live
        - value of 'true' (case insensitive) will be simulated.

    'CLOUDTRAIL_NAME_PREFIX': defaults to 'cloudtrail-'
        -sets the name of the cloudtrail to delete.

options:
  -h, --help            show this help message and exit

required arguments:
  --target-account-id TARGET_ACCOUNT_ID
                        Account number to delete default VPC resources in

  --assume-role-arn ASSUME_ROLE_ARN
                        ARN of IAM role to assume in the target account (case sensitive)
  OR
  --assume-role-name ASSUME_ROLE_NAME
                        Name of IAM role to assume in the target account (case sensitive)

usage: delete_default_cloudtrail.py [-h] --target-account-id TARGET_ACCOUNT_ID (--assume-role-arn ASSUME_ROLE_ARN | --assume-role-name ASSUME_ROLE_NAME)
```

### Sample steps to execute in venv

```bash
mkdir vpc_env
python3 -m venv vpc_env
source vpc_env/bin/activate
python3 -m pip install -U pip
pip3 install -r src/requirements.txt
python3 src/delete_default_cloudtrail.py --target-account-id=<TARGET ACCT ID> (--assume-role-arn=<ROLE ARN TO ASSUME> | --assume-role-name=<ROLE NAME TO ASSUME>)
deactivate
rm -rf vpc_env
```
