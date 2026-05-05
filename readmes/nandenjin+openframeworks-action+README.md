# ⚙️ openframeworks-action

[![Version released](https://img.shields.io/github/v/release/nandenjin/openframeworks-action?style=flat-square)](https://github.com/nandenjin/openframeworks-action/releases)
[![Build Status](https://img.shields.io/github/actions/workflow/status/nandenjin/openframeworks-action/checks.yaml?style=flat-square)](https://github.com/nandenjin/openframeworks-action/actions/workflows/checks.yaml)
[![License](https://img.shields.io/github/license/nandenjin/openframeworks-action?style=flat-square)](https://github.com/nandenjin/openframeworks-action/blob/dev/LICENSE)

GitHub Action for openFrameworks setup & build.

- ✅️ Cross-platform
  - ✅️ Tested: Windows & macOS
  - ⌛️ Linux

```yaml
# Download openFrameworks
- uses: nandenjin/openframeworks-action@v1
  with:
    command: setup-of

# Checkout your repo under `apps`
- uses: actions/checkout@v4
  with:
    path: 'apps/myRepo'

# Setup your project with projectGenerator
- uses: nandenjin/openframeworks-action@v1
  with:
    command: projectgenerator
    project_root: 'apps/myRepo/myApp'

# Build your project
- uses: nandenjin/openframeworks-action@v1
  with:
    command: build
    project_root: 'apps/myRepo/myApp'
```

## Commands

### `setup-of`

Downloads and extracts openFrameworks to the specified directory.

| Input        |             | Description                               | Example  | Default   |
| ------------ | ----------- | ----------------------------------------- | -------- | --------- |
| `of_version` | 🟢 Optional | The version of openFrameworks to download | `0.12.0` | `0.12.0`  |
| `of_path`    | 🟢 Optional | The path to the openFrameworks root dir   | `.`      | `.` (cwd) |

### `projectgenerator`

Generates a project for the specified directory using the projectGenerator.

| Input                   |             | Description                                | Example             | Default              |
| ----------------------- | ----------- | ------------------------------------------ | ------------------- | -------------------- |
| `project_root`          | 🟥 Required | The path to the project root directory     | `apps/myRepo/myApp` |                      |
| `of_root`               | 🟢 Optional | The path to the openFrameworks root dir    | `openFrameworks`    | `./openFrameworks`   |
| `project_generator_dir` | 🟢 Optional | The path to the projectGenerator directory | `projectGenerator`  | `./projectGenerator` |

### `build`

Builds the project in the specified directory.

- Windows: Uses MSBuild (**Requires additional step to setup `msbuild` command** e.g. `microsoft/setup-msbuild`)
- macOS: Uses make

| Input          |             | Description                             | Example             | Default            |
| -------------- | ----------- | --------------------------------------- | ------------------- | ------------------ |
| `project_root` | 🟥 Required | The path to the project root dir        | `apps/myRepo/myApp` |                    |
| `of_root`      | 🟢 Optional | The path to the openFrameworks root dir | `openFrameworks`    | `./openFrameworks` |

## Example

```yaml
jobs:
  build:
    strategy:
      matrix:
        # Cross platform build
        os: [windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}

    steps:
      # Download openFrameworks
      - name: Setup openFrameworks
        uses: nandenjin/openframeworks-action@v1
        with:
          command: setup-of
          of_version: 0.12.0

      # Checkout your repo under `apps`
      - uses: actions/checkout@v4
        with:
          path: 'apps/myRepo'

      # Setup your project with projectGenerator
      - name: Generate project
        uses: nandenjin/openframeworks-action@v1
        with:
          command: projectgenerator
          project_root: 'apps/myRepo/myApp'

      # (Required for MSBuild on Windows)
      - name: Setup MSBuild
        uses: microsoft/setup-msbuild@v2
        if: startsWith(matrix.os, 'windows')

      # Build your project
      - name: Build
        uses: nandenjin/openframeworks-action@v1
        with:
          command: build
          project_root: 'apps/myRepo/myApp'
```
