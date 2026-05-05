<div align="center" style="text-align: center;">
<h1>Token CLI</h1>

<p>A command-line tool to visualize tokenized text.</p>

[![PyPI - Version](https://img.shields.io/pypi/v/token-cli)](https://pypi.org/project/token-cli/)
[![GitHub License](https://img.shields.io/github/license/taha-yassine/token-cli)](LICENSE)


![Demo](demo.gif)

</div>

## Setup

Install using `pip`
```bash
pip install token-cli
```

Or using `uv`
```bash
uv tool install token-cli
```

Or using `pipx`
```bash
pipx install token-cli
```

You can also directly run it through the provided _Nix flake_
```bash
nix run github:taha-yassine/token-cli
```

Set up from source
```bash
git clone https://github.com/taha-yassine/token-cli.git
cd token-cli
uv sync
```

## Usage

```bash
token-cli [OPTIONS] [INPUT_FILE]
```

**From standard input:**

```bash
echo "Ceci n'est pas une pipe." | token-cli
```

**From a file:**

```bash
token-cli your_text_file.txt
```

## Options

```
usage: token-cli [-h] [--tokenizer TOKENIZER] [--mode {text,highlight}]
                [--hide-text] [--hide-stats] [--force-terminal] [input_file]

Visualize tokenized text.

positional arguments:
  input_file            Path to the input text file. Reads from stdin if not
                        provided.

options:
  -h, --help            show this help message and exit
  --tokenizer TOKENIZER
                        Tokenizer to use for tokenization. Possible values:
                        gpt-4o, o200k_base, cl100k_base, p50k_base, p50k_edit,
                        r50k_base, gpt2 (default: o200k_base)
  --mode {text,highlight}
                        Mode for displaying tokens: 'text' or 'highlight'.
                        (default: highlight)
  --hide-text           Hide the tokenized text.
  --hide-stats          Hide the token and character counts at the end.
  --force-terminal      Force terminal output.

```