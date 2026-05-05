# DSO Dojo 2022-11

## Overview

One of the projects I've been running at work is a DevSecOps and SRE Dojo. This repo is my solution for our November 2022 exercise.

### Exercise

The stated goal was to get [Gin's Quick Start](https://github.com/gin-gonic/gin#quick-start) on an EC2 server.

### Toolchain

My initial goal is to do the following

1. Create a build pipeline in GitHub Actions that will create a GitHub Release on tag events.
2. Use CDKTF to provision AWS.
3. Terratest everything for target state.

Right now I'm not sure about provisioning the the EC2 instance. Keeping with "do the most complicated thing" approach, Packer to create an AMI sounds pretty neat.

## Notes

### Lots to learn with CDKTF

Following the CDKTF quick start sets up a stack. Apparently these don't work with [resource assertions](https://github.com/hashicorp/terraform-cdk/issues/1850#issuecomment-1153883827).
