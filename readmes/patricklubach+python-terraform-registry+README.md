# Python Client for Terraform Registry API

[Terraform Registry](https://www.terraform.io/registry/api-docs) allows you to use and publish your
Terraform Providers and Modules. `python-terraform-registry` allows you to interact with the
[Terraform Registry](https://www.terraform.io/registry/api-docs) API.

## Installation

Set up a Python development environment and install this library in a `venv`.
`venv` is a tool to create isolated Python environments. The basic problem it
addresses is one of dependencies and versions, and indirectly permissions.

Make sure you're using Python 3.7 or later, which includes `venv` by default.
With `venv`, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

Set up a Python development environment: <https://cloud.google.com/python/docs/setup>
`venv`: <https://docs.python.org/3/library/venv.html>

## Supported Python Versions

Python >= 3.7

## Test

The library is being tested by using `unittest`. You can run the tests by executing:

```bash
make test
```

in the root directory.
