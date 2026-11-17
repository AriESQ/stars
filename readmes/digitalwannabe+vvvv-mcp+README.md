# vvvv-mcp

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server for [vvvv gamma](https://vvvv.org) — giving AI agents deep knowledge of vvvv's node API, the ability to read, explain and **write** `.vl` patches, generate C# nodes and SDSL shaders, and optionally connect to a **live running vvvv instance** for real-time feedback.

Works **without a vvvv installation** for all knowledge, search, read, and generate tools. Live tools require the companion `VL.MCP.HDE` editor extension (see below).

---

## Install (end users)

Requires [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later.

```powershell
# Install globally
dotnet tool install -g vvvv-mcp

# Configure your MCP client (Claude Desktop, VS Code, Cursor, Kilo) automatically
vvvv-mcp --setup
```

`--setup` detects which MCP clients are installed, writes their config files, and prints the config snippet for anything it can't auto-detect. Run it again after updating.

### Update

```powershell
dotnet tool update -g vvvv-mcp
vvvv-mcp --setup   # re-run if paths changed
```

---

## What it does

- **Search** 6,400+ vvvv nodes by name, category, or keyword across all core packages
- **Read and explain** `.vl` patch files — parse the dataflow graph and describe it in natural language
- **Write** `.vl` patches — add nodes, connect pins, set values, create new patches
- **Generate** C# custom nodes (`[ProcessNode]`) and SDSL shaders from a description
- **Access the full vvvv knowledge base** — the entire Gray Book, all of tebjan's agent skills, and a curated package reference, served as MCP resources
- **Live vvvv bridge** *(via `VL.MCP.HDE`)* — read compilation errors, running documents, log output, and perform editor operations directly inside a running vvvv instance

---

## Help to Improve

- Anytime the MCP does a bad job/misunderstands vvvv, you can either dump the chat log (if non-sensitive) or ask the LLM to summarize what went wrong and how it would improve the MCP, then file it as an issue.
- When you create video-based tutorials, create a good transcript which we can add to the MCP's knowledge base.

---

## VL.MCP.HDE — In-editor AI assistant *(experimental preview)*

> <span style="color:red"><strong>Status:</strong> experimental preview — breaking changes expected. While the infrastructure itself is ok, the mcp still needs to improve a lot before this becomes truly useable. Don't expect any wonders (yet).</span>

`VL.MCP.HDE` is a companion vvvv gamma editor extension that adds two features:

| Feature | Activation | What it does |
|---|---|---|
| **Bridge** | always on | HTTP server on `localhost:7123` — exposes the live vvvv session to any external MCP client (VS Code + Kilo, Claude Desktop, etc.) |
| **Chat** | `Alt+C` toggle | Launches [Open WebUI](https://openwebui.com) as a chat panel directly inside the vvvv editor, pre-connected to the bridge's MCP tools |

### Install

```powershell
# Install via vvvv's NuGet package manager, or add to startup args:
nuget install VL.MCP.HDE
```

### Bridge mode (always on)

Runs an HTTP server inside vvvv at `localhost:7123` as soon as the extension is loaded. External MCP clients connect to it directly. The bridge exposes:
- All 12 live-editor tools (documents, errors, log, open/save/reload, undo/redo)
- MCP/SSE endpoint (`/mcp/sse`) for legacy clients
- **MCP Streamable HTTP endpoint** (`/mcp`) for Open WebUI and 2025+ clients

Configure your external MCP client (once):
```json
{
  "mcpServers": {
    "vvvv-bridge": {
      "command": "dotnet",
      "args": ["run", "--project", "path/to/VvvvMcp"]
    }
  }
}
```
Or point directly at the running bridge: `http://localhost:7123/mcp`

### Chat mode (`Alt+C`) — powered by [Open WebUI](https://openwebui.com)

Launches [Open WebUI](https://github.com/open-webui/open-webui) as an embedded browser panel inside vvvv. Open WebUI handles the full LLM chat interface; the vvvv MCP tools are automatically registered.

**Requirements:**
- [`uv`](https://docs.astral.sh/uv/) must be installed: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- An LLM endpoint — [Ollama](https://ollama.com) (local) or any OpenAI-compatible API

**First start:** `uv` downloads and installs Open WebUI (~500 MB, one-time). Subsequent starts are fast (~10 s). Chat history, settings, and uploaded documents are stored in `%LOCALAPPDATA%\vvvv-mcp\openwebui-data\`.

**Activating the vvvv tools in chat:**
The vvvv MCP server (`http://localhost:7123/mcp`) is automatically registered in Open WebUI on first launch. To use it in a conversation:
- Click the **Tool** button in the chat input bar → toggle on **vvvv-mcp**

To activate tools by default for a model (so you don't need to click **Tool** every time):
1. Open WebUI → **Workspace → Models**
2. Edit the model you want to use
3. Under **Tools**, enable **vvvv-mcp**
4. Save — tools will now be active in every new chat with that model

**Attribution:** Chat mode is powered by [Open WebUI](https://github.com/open-webui/open-webui) (BSD-3-Clause). Open WebUI is an independent project and is not affiliated with this repository.

---

## Tools

### Node Catalog

| Tool | Description |
|---|---|
| `search_nodes_live` | **(bridge)** Search the LIVE node registry of the running vvvv — exact pins, real types, only nodes actually placeable in the session. |
| `get_node_details_live` | **(bridge)** Exact pin names, real types, defaults, visibility for one node from the live registry. |
| `refresh_live_nodes` | **(bridge)** Rebuild the live node snapshot (e.g. after installing a pack). |
| `search_nodes` | Offline catalog search (two-phase: precise AND, then OR fallback). |
| `get_node_details` | Offline catalog details for a node by name (tolerant: variants, full names). |
| `list_categories` | All category namespaces, optionally filtered by prefix. |
| `list_packages` | All packages in the catalog. |

### Knowledge Base

| Tool | Description |
|---|---|
| `list_knowledge` | List all knowledge documents with descriptions. |
| `read_knowledge` | Read the full content of a knowledge document by name. |
| `search_knowledge` | Full-text search across all knowledge documents with snippet results. |
| `search_practical` | Search help patches, forum solutions, and code snippets from the community knowledge index. |
| `get_index_stats` | Row counts for the SQLite search index (knowledge, nodes, practical). |

### Patch Read Tools

| Tool | Description |
|---|---|
| `read_patch` | Parse a `.vl` file and return the structured graph (nodes, pins, links, IOBoxes, dependencies). |
| `explain_patch` | Natural-language explanation of a parsed patch. |
| `list_patch_dependencies` | List NuGet dependencies declared in a `.vl` file. |

### Patch Write Tools

| Tool | Description |
|---|---|
| **`build_patch`** | **The primary tool.** Builds a whole connected subgraph in ONE call: resolves nodes (live registry first), adds NuGet deps, declares pins with correct visibility, auto-layouts by dataflow, wires all links (incl. pin-group auto-indexing and links into existing pins), saves, reloads in vvvv, reports compile errors. |
| `create_patch` | Create a new empty `.vl` patch. `mode: "file"` (from scratch) or `"editor"` (also opens in vvvv). |
| `add_node` | Add a single node — pins auto-declared from the live registry/catalog, dependency auto-added, optional verify. |
| `add_pad` | Add a value pad (IOBox) to a patch with an optional initial value. |
| `connect_pins` | Connect an output pin (or pad) to an input pin. |
| `remove_node` | Remove a node and all its connected links from a patch. |
| `remove_link` | Remove a specific connection from a patch. |
| `set_value` | Set the default value of a pad or pin. |

### Code Generation Tools

| Tool | Description |
|---|---|
| `create_csharp_plugin` | Generate a C# `[ProcessNode]` or static operation from a description, with typed input/output pins. |
| `create_shader` | Generate a Stride SDSL shader — TextureFX (filter/mixer/source), ComputeFX, DrawFX, or ShaderFX. |
| `list_templates` | List all available vvvv project templates (VL, C#, SDSL). |
| `get_template` | Get the full content of a template file. |

### Live Editor Tools *(requires `VL.MCP.HDE`)*

| Tool | Description |
|---|---|
| `check_bridge_connection` | Check if the vvvv bridge is reachable and return runtime state. |
| `get_running_documents` | List all `.vl` documents currently open in the vvvv editor. |
| `get_vvvv_errors` | Get current compilation errors and warnings. |
| `get_vvvv_state` | Runtime state: running/paused, frame count, uptime. |
| `get_vvvv_log` | Recent log entries from the vvvv console (captures ILogger + System.Console output). |
| `get_open_tabs` | Get open canvas tabs in the patch editor. |
| `open_document_in_vvvv` | Open a `.vl` file in the editor. |
| `close_document_in_vvvv` | Close a document (optionally saving first). |
| `save_document_in_vvvv` | Save a document or all documents. |
| `reload_file_in_vvvv` | Force vvvv to hot-reload a file from disk. |
| `undo_in_vvvv` | Undo the last action on the active canvas. |
| `redo_in_vvvv` | Redo the last undone action. |

---

## Resources

### Knowledge (`vvvv://knowledge/`)

| URI | Content |
|---|---|
| `vvvv://knowledge/quickref` | XML cheat sheet: NodeReference patterns, critical .vl rules, VL.CoreLib categories, Stride scene, topic index |
| `vvvv://knowledge/file-format` | Complete `.vl` XML format reference |
| `vvvv://knowledge/fundamentals` | Live compilation model, frame-based execution, node categories |
| `vvvv://knowledge/patching` | Dataflow patterns, regions, channels, event handling, anti-patterns |
| `vvvv://knowledge/custom-nodes` | `[ProcessNode]` lifecycle, `Update()`, change detection, assembly import |
| `vvvv://knowledge/shaders` | SDSL TextureFX/DrawFX/ComputeFX, streams system, mixins, GPU patterns |
| `vvvv://knowledge/dotnet` | .csproj setup, NuGet packages, vector type interop, async, threading |
| `vvvv://knowledge/channels` | IChannelHub, `[CanBePublished]`, reactive subscriptions, bang channels |
| `vvvv://knowledge/spreads` | `Spread<T>`, `SpreadBuilder`, mapping, filtering, performance rules |
| `vvvv://knowledge/node-libraries` | Creating node libraries: ImportAsIs/Namespace/Type, service registration |
| `vvvv://knowledge/troubleshooting` | Common errors: pin order, missing ImportAsIs, shader mistakes, runtime issues |
| `vvvv://knowledge/packages` | 230 curated packages from Libraries.xml, organized by category |
| `vvvv://knowledge/gray-book/*` | Official Gray Book — language, extending, libraries, HDE, best-practice, getting-started |

---

## Developer / contributor setup

### Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)

### Build

```powershell
dotnet build src/VvvvMcp.sln
```

### Run locally (without installing as a global tool)

```powershell
dotnet run --project src/VvvvMcp -- --setup   # configure MCP clients to use this build
```

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector -- dotnet src/VvvvMcp/bin/Debug/net8.0/VvvvMcp.dll
```

### Publish a new version of the MCP server

```powershell
# 1. Bump version in src/VvvvMcp/VvvvMcp.csproj
# 2. Commit, tag, push — GitHub Actions publishes to NuGet.org automatically
#    (or push the version bump on main without a tag; the workflow now watches the csproj path too)
git add -A && git commit -m "release 0.x.0"
git tag v0.x.0
git push origin main --tags
```

### Publish VL.MCP.HDE (vvvv editor extension)

```powershell
# 1. Bump version in VL.MCP.HDE/VL.MCP.HDE.nuspec
# 2. Commit, tag, push — GitHub Actions workflow publishes to NuGet.org
#    (or push the version bump on main without a tag; the workflow now watches the nuspec path too)
git add -A && git commit -m "VL.MCP.HDE 0.x.0"
git tag vl-0.x.0
git push origin main --tags
```

---

## Repository Structure

```
vvvv-mcp/
│
├── src/                          # MCP server (.NET 8 dotnet tool)
│   ├── VvvvMcp.sln
│   ├── VvvvMcp/                  # Server entry point
│   │   ├── Program.cs
│   │   ├── Tools/                # search_nodes, read_patch, add_node, create_shader, ...
│   │   ├── Resources/            # vvvv://knowledge/* and vvvv://catalog/*
│   │   └── Prompts/              # explain_vl_patch, create_vl_patch, ...
│   ├── VvvvMcp.Core/             # Shared library
│   │   ├── Models/               # NodeModels, PatchModels, CatalogModels
│   │   └── Services/
│   │       ├── NodeCatalogService      # Node search & indexing
│   │       ├── KnowledgeService        # Knowledge document loading & search
│   │       ├── PatchReaderService      # .vl XML parser
│   │       ├── PatchWriterService      # .vl XML writer (add/connect/remove nodes)
│   │       ├── PatchExplainerService   # Natural language patch descriptions
│   │       ├── ShaderGeneratorService  # SDSL shader code generation
│   │       └── PluginGeneratorService  # C# ProcessNode code generation
│   └── VvvvMcp.Tests/            # Smoke tests
│
├── VL.MCP.HDE/                   # vvvv gamma editor extension (NuGet: VL.MCP.HDE)
│   ├── VL.MCP.HDE.vl             # HDE extension entry point (auto-loads in editor)
│   ├── VL.MCP.HDE.nuspec         # NuGet package spec
│   └── src/
│       ├── MCPBridgeServer.cs    # [ProcessNode]: HTTP server + MCP/SSE + chat host
│       ├── McpSseServer.cs       # MCP Streamable HTTP + legacy SSE endpoints
│       ├── McpChatHost.cs        # Open WebUI process manager (uv-based)
│       ├── BridgeState.cs        # vvvv runtime introspection via reflection
│       ├── LogCapture.cs         # ILoggerProvider + ConsoleTee for full log capture
│       └── VL.MCP.Bridge.csproj
│
├── VVVVNodeAnalyzer/             # Node catalog generator (no vvvv installation needed)
│
├── knowledge/                    # MCP knowledge base (677 KB, 24 files)
│   ├── The-Gray-Book/            # Git submodule: vvvv/The-Gray-Book
│   ├── tebjan-vvvv-skills/       # Git submodule: tebjan/vvvv-skills
│   └── ...
│
├── scripts/
│   ├── build-knowledge.ps1
│   ├── install-community-packs.ps1
│   └── update-catalog.ps1
│
└── .github/workflows/
    ├── publish.yml               # Publishes vvvv-mcp dotnet tool to NuGet.org
    └── publish-VL-package.yml    # Publishes VL.MCP.HDE to NuGet.org
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  External IDE (VS Code + Kilo / Claude Desktop / Cursor)        │
│       │  stdio MCP                                              │
│       ▼                                                         │
│  ┌──────────────────────────────────────┐                       │
│  │  vvvv-mcp  (dotnet tool, MCP server) │                       │
│  │  search, read, write, generate, ...  │                       │
│  └──────────────────────────────────────┘                       │
│       │  HTTP localhost:7123/api/*  (live tools only)           │
│       ▼                                                         │
│  ┌──────────────────────────────────────┐                       │
│  │  VL.MCP.HDE (inside vvvv.exe)        │                       │
│  │  MCPBridgeServer [ProcessNode]       │                       │
│  │  · /api/*   → REST for vvvv-mcp      │                       │
│  │  · /mcp     → Streamable HTTP MCP    │◄── Open WebUI         │
│  │  · /mcp/sse → legacy SSE MCP         │                       │
│  └──────────────────────────────────────┘                       │
│       ▲  Alt+C (HDE menu) · bridge always on                     │
│                                                                 │
│  vvvv.exe ────────────────────────────────────────────────────  │
│  running patches, compilation, editor state                     │
└─────────────────────────────────────────────────────────────────┘

Chat mode:
  vvvv (Alt+C) → McpChatHost → uv → Open WebUI (localhost:7125)
                                          │
                                          └─► /mcp (Streamable HTTP)
                                              → vvvv live tools
```

---

## Roadmap

- **Phase 1** ✅ Read-only tools — node search, patch reading, natural language explanations
- **Phase 1.5** ✅ Knowledge base — full Gray Book, tebjan's skills, 677 KB of documentation
- **Phase 1.6** ✅ Analyzer improvements — correct VL category resolution, getter/setter synthesis
- **Phase 2** ✅ Write capabilities — create/edit `.vl` patches, generate C# plugins and SDSL shaders
- **Phase 3** ✅ Live vvvv bridge — `VL.MCP.HDE` editor extension, console capture, hot-reload feedback
- **Phase 3.5** ✅ In-editor AI chat — Open WebUI embedded via CEF, MCP Streamable HTTP transport
- **Phase 4** 🔜 Community ecosystem — analyze all Libraries.xml packages, index help patches, per-node usage lookup
- **Phase 5** 🔜 Continuous improvement — forum/changelog scraper, knowledge updater

---

## Node Catalog

### Coverage

The current catalog covers **38 packages** with **~6,400 user-facing nodes** across **374 categories**.

### Extending the catalog

```powershell
./scripts/install-community-packs.ps1
dotnet run --project VVVVNodeAnalyzer/VVVVNodeAnalyzer.csproj -- batch packs-community VVVVNodeAnalyzer
```

---

## License

**Dual license** — see [LICENSE.md](LICENSE.md):

- **Free** for non-commercial use (hobbyists, students, educators, research, open-source) under the [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/) terms.
- **Commercial use** (any use by or on behalf of a business, paid client work, internal business tooling, commercial products/services) requires a paid license — individual / studio (seat-based) / enterprise via [polar.sh](https://polar.sh) (link at release).

Note: vvvv gamma itself is a separate product of the vvvv group with its own licensing — this tool does not replace or include it.

### Third-party attributions

See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) for the full list. In short:

- **[Open WebUI](https://github.com/open-webui/open-webui)** (BSD-3-Clause + branding terms) — used in Chat mode via `VL.MCP.HDE`; launched as a separate process via `uv`, not modified or redistributed.
- **[tebjan/vvvv-skills](https://github.com/tebjan/vvvv-skills)** — knowledge base content (**CC BY-SA 4.0**); derived knowledge files remain CC BY-SA with attribution.
- **[vvvv/The-Gray-Book](https://github.com/vvvv/The-Gray-Book)** — official vvvv documentation by the vvvv group; condensed here with attribution.
