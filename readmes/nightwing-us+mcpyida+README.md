# MCPyIDA

An MCP (Model Context Protocol) server that exposes [IDA Pro](https://hex-rays.com/ida-pro/)
reverse-engineering capabilities to LLM clients.

MCPyIDA exposes binary analysis capabilities via MCP: decompilation, disassembly,
symbol lookup, cross-references, type inspection, structure recovery, binary patching,
and scriptable analysis.

> **Related project:** If you use Ghidra rather than IDA Pro, see
> [MCPyGhidra](https://github.com/nightwing-us/mcpyghidra) for an equivalent MCP
> server for Ghidra.

## Prerequisites

- **IDA Pro** 9.x or later with idalib (tested with IDA Pro 9.2+;
  [download](https://hex-rays.com/ida-pro/))
- **Python** 3.10–3.12

> **Note:** IDA Pro is commercial software. A valid IDA Pro license is required.
> MCPyIDA does not bundle or distribute IDA Pro; you must supply your own
> installation.

## Installation

### 1. Create a virtual environment (recommended)

```bash
python3 -m venv idavenv
source idavenv/bin/activate
```

### 2. Install MCPyIDA

```bash
pip install mcpyida
```

### 3. Register MCPyIDA as an IDA plugin

```bash
mcpyida_install
```

### 4. Configure IDA to use your virtual environment

Point IDA's IDAPython at the same virtual environment.  The exact steps depend
on your IDA Pro version and OS; see the
[IDA Pro documentation](https://hex-rays.com/products/ida/support/idadoc/) for
details on configuring IDAPython's Python interpreter.

## Quick Start

### GUI Mode (IDA Pro running interactively)

1. Launch IDA Pro and open a binary.
2. Go to **Edit → Plugins → MCPyIDA** (or the MCP menu added by the plugin).
3. Start the MCP server.
4. The server URL appears in the output window, e.g.:
   `http://127.0.0.1:6050/sse/`

### Headless Mode

Launch the MCP server without the IDA GUI (requires idalib):

```bash
export IDADIR=/path/to/idapro
mcpyida-headless --binary /path/to/firmware.elf
```

The server prints a JSON readiness signal to stdout:

```json
{"status": "ready", "host": "127.0.0.1", "port": 6050, "binary": "/path/to/firmware.elf"}
```

### Connecting an MCP Client

Point any MCP-compatible client (Claude Desktop, VS Code MCP extension, etc.)
at the running server:

```json
{
  "mcpServers": {
    "ida": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:6050/mcp"
    }
  }
}
```

## What's Exposed

MCPyIDA exposes tools organized into categories:

- **Listing & context:** list entries, inspect binary metadata, resolve functions
- **Analysis:** decompile, disassemble, cross-references, control-flow graphs
- **Types:** type enumeration and detailed inspection
- **Modification:** rename symbols, update variables, set comments, patch instructions
- **Scripting:** Python code execution with back-to-client RPC callbacks
- **Search:** binary pattern and instruction sequence matching

## Troubleshooting

**IDA does not load the plugin after `mcpyida_install`**

Ensure your IDAPython interpreter is pointing at the virtual environment where
`mcpyida` is installed.  The `mcpyida_install` command copies the plugin loader
into IDA's plugin directory; the loader itself must be able to `import mcpyida`
at runtime.

**`mcpyida-headless` exits immediately with an idalib error**

Set `IDADIR` to the root of your IDA Pro installation (the directory containing
`idalib.so` / `idalib.dll`).  Verify the path is correct and that your IDA Pro
license is valid and reachable.

**Port 6050 is already in use**

Pass `--port <number>` to `mcpyida-headless`, or configure the port in the
plugin's settings panel when running in GUI mode.

**MCP client reports connection refused**

Confirm the server started successfully (look for the JSON readiness signal or
check IDA's output window).  The default transport is `streamable-http` on
`http://127.0.0.1:6050/mcp`; older clients that only support SSE can connect to
`http://127.0.0.1:6050/sse/`.

## Development

### Setup

```bash
git clone https://github.com/nightwing-us/mcpyida.git
cd mcpyida
pip install -e ".[dev]"
```

### Testing

Unit tests (no IDA Pro required):

```bash
pytest tests/unit/ -v --tb=short
```

Integration and e2e tests require IDA Pro / idalib and are run in a CI
environment with an IDA Pro license available.

### Type Checking

```bash
mypy
```

### Linting

```bash
ruff check src tests
ruff format src tests
```

## Related Projects

MCPyIDA and MCPyGhidra are maintained in parallel as sister projects with
intended feature parity — MCPyIDA targets IDA Pro and MCPyGhidra targets Ghidra.

- [MCPyGhidra](https://github.com/nightwing-us/mcpyghidra) — equivalent MCP server
  for Ghidra (free, open-source RE tool)
- [pyghidra-decaf](https://github.com/nightwing-us/pyghidra-decaf) — Python-native
  Ghidra plugin development framework (underpins MCPyGhidra)

## License

Apache-2.0 — see [LICENSE](LICENSE) for details.

Copyright © 2026 Nightwing Group, LLC.
