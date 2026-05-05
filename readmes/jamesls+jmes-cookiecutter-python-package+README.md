# JMES Cookiecutter Python Package Template

This is a [cookiecutter](https://github.com/cookiecutter/cookiecutter) template
for my preferences when creating a python package.

These preferences change over time and I occasionally add/remove
entire features from the template.  Use at your own risk, or I encourage
you to fork this repo and make your own version!

Features include:

* uv for dependency management
* `pyproject.toml` based build configuration
* Use Poe the Poet to manage common tasks
* Ruff for linting and formatting.
* pyright for type checking.
* Use pre-commit to help enforce all PR checks at commit time.
* Use jmeslog for changelog management.
* GitHub templates for creating issues
* Basic GitHub workflow for running tests on PRs.

# Usage

This repo is a cookiecutter template so you can use the `cookiecutter`
CLI to create a new project:


```
cookiecutter gh:jamesls/jmes-cookiecutter-python-package
```

However, I recommend using [cruft](https://github.com/cruft/cruft),
which is a wrapper over Cookiecutter, and can automatically merge
updates to this template into existing projects.

```
cruft create https://github.com/jamesls/jmes-cookiecutter-python-package
```

That way if there's any changes to this template, and you want to update
an existing project to pull in these updates you can just run:


```
cruft update
```
