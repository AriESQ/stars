# terrace

## Description

The root directory of this repository contains the configurations needed to build a Docker image for Terraform module testing. The image is stored within the GitHub container registry and can be reference via it's address: `ghcr.io/marshall7m/terrace:<tag>`.

## Built-in
- [tfenv](https://github.com/tfutils/tfenv)
- [tgswitch](https://github.com/warrensbox/tgswitch)
- [terraform](https://github.com/hashicorp/terraform) (version: latest)
- [terragrunt](https://github.com/gruntwork-io/terragrunt) (version: latest)
- [semtag](https://github.com/nico2sh/semtag)
- [gh](https://cli.github.com/)
- [git](https://github.com/git/git)
- [tflint](https://github.com/terraform-linters/tflint)
- [tfsec](https://github.com/aquasecurity/tfsec)
- [terraform-docs](https://github.com/terraform-docs/terraform-docs)

See `requirements.txt` for PyPi packages installed via pip

## Arguments

Within both images within the multi-stage build, a set of build arguments are available to pin defined versions of the packages mentioned above to suit your needs. These arguments can defined within the `docker build` command with each argument defined like so: `--build-arg TFSEC_VERSION=0.36.11 --build-arg TERRAFORM_VERSION=1.0.0`. 

## Notes

This image leverages the awesome Terraform binary manager tfenv and Terragrunt binary manager tgswitch to install and manage both binary versions. Future installations of the binaries are recommended be installed via these managers to prevent `$PATH` complications.
