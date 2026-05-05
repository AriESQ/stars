# Claude Takeout

A Chrome extension to export Claude.ai conversations to Markdown, JSON, or comprehensive ZIP archives.

## Features

- **Multiple Export Formats** - Markdown, Embedded Markdown, ZIP Archive, JSON
- **ZIP Archive Export** - Full archive with responses, artifacts, metadata, code snippets
- **Bulk Export** - Export all your Claude conversations at once
- **Project Support** - Exports project files, system prompts, and prefixes filenames with project name
- **Keyboard Shortcuts** - Quick export with Alt+key combinations
- **Branched Conversation Handling** - Correctly follows conversation tree
- **Artifact Extraction** - Extracts and embeds created files
- **Thinking Blocks** - Preserves Claude's reasoning with proper summaries
- **Tool Use Display** - Formatted display of web search, bash, file operations
- **Sidebar Mode** - Keep the exporter open while browsing conversations
- **No Configuration Required** - Auto-detects your organization ID

## Installation

1. Download or clone this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable **Developer mode** (toggle in top right)
4. Click **Load unpacked**
5. Select the `claude-takeout` folder

## Usage

### Export Current Conversation

1. Navigate to a conversation on [claude.ai](https://claude.ai)
2. **Refresh the page** (required on first use to capture data)
3. Click the Claude Takeout extension icon
4. Choose your export format

### Export All Conversations

1. Navigate to [claude.ai](https://claude.ai) (any page)
2. Refresh the page once to capture your organization ID
3. Click the Claude Takeout extension icon
4. Choose your bulk export format:
   - **Export All (Markdown)** - One `.md` file per conversation
   - **Export All (Embedded)** - One `.md` file per conversation with artifacts inline
   - **Export All (Mega-Zip)** - Single zip containing all conversations
   - **Export All (JSON)** - One `.json` file per conversation
5. Watch the progress bar as conversations are exported

## Export Formats

### Markdown
**"Export Current (Markdown)"**
- Single `.md` file with full conversation
- Artifacts referenced (compatible with `replace_filepaths.py`)
- Includes thinking blocks, tool use, timestamps

### Embedded Markdown
**"Export Embedded (Artifacts Inline)"**
- Single `.md` file with artifacts embedded in code blocks
- Self-contained, no external file references

### ZIP Archive
**"Export as Zip (Full Archive)"**

Creates a comprehensive archive:

```
[Project_Name-project]_{conversation}_claude-chat.zip
├── README.md                    # Table of contents
├── meta.md                      # Statistics, word counts, metadata
├── prompts.md                   # All prompts with response links
├── responses_text_only.md       # Combined pure text responses
├── full_chat.md                 # Complete conversation (artifacts in code blocks)
├── integrated_chat.md           # Markdown artifacts flow seamlessly
├── integrated_chat.txt          # Plain text version (no markdown formatting)
├── code_snippets.md             # All extracted code blocks
├── links_and_sources.md         # URLs + web search sources by domain
├── original.json                # Original JSON export
├── responses/
│   ├── 001_title_response.md       # Pure text response
│   ├── 001_title_response.full.md  # Response with thinking/tools/embedded artifacts
│   └── ...
├── artefacts/
│   ├── document.md
│   ├── script.py
│   └── ...
├── attachments/                 # Pasted text files (extracted content)
│   ├── meeting_notes.txt
│   └── ...
├── project/                     # Claude Project data (if conversation is in a project)
│   ├── project.json                # Project metadata
│   ├── prompt_template.md          # System prompt/instructions
│   ├── docs.json                   # Document list metadata
│   ├── research_notes.md           # Full file (from API)
│   ├── large_file_truncated.md     # Truncated file (from view tool fallback)
│   └── ...
└── uploads/                     # Downloaded PDFs, images, etc.
    ├── document.pdf
    ├── image.png
    └── ...
```

*Note: The `[Project_Name-project]_` prefix only appears for conversations that are part of a Claude Project.*

### JSON
**"Export Current (JSON)"**
- Raw API response with complete data
- Useful for backup or custom processing

### Mega-Zip (Bulk Export)
**"Export All (Mega-Zip)"**

Creates a single archive containing all your conversations:

```
claude-takeout-2026-01-01.zip
├── index.md                         # Master list with links to all conversations
├── conversation_one/
│   ├── README.md
│   ├── meta.md
│   ├── prompts.md
│   ├── responses_text_only.md
│   ├── full_chat.md
│   ├── integrated_chat.md
│   ├── code_snippets.md
│   ├── links_and_sources.md
│   ├── original.json
│   ├── responses/
│   │   └── ...
│   ├── artefacts/
│   │   └── ...
│   └── project/
│       └── ...
├── conversation_two/
│   └── ... (same structure)
└── ...
```

Each conversation folder has the identical structure to individual ZIP exports.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt+M` | Export Current (Markdown) |
| `Alt+E` | Export Embedded |
| `Alt+Z` | Export as Zip |
| `Alt+J` | Export Current (JSON) |
| `Alt+R` | Refresh page |

*Shortcuts work when the popup or sidebar is open*

## Sidebar Mode

The extension can open as a sidebar panel that stays visible while you browse conversations.

### Opening the Sidebar

**One-time:**
- Right-click the extension icon → **Open side panel**

**Make it default:**
1. Click the extension icon to open popup
2. Click the gear icon (Settings)
3. Enable **"Open as sidebar by default"**
4. Now clicking the icon opens the sidebar instead of the popup

### Benefits of Sidebar Mode

- Stays open while navigating between conversations
- No need to re-open for each export
- Wider view on larger screens
- Auto-updates when conversation data changes

## Technical Features

### Branched Conversation Handling
Correctly traces the conversation tree via `current_leaf_message_uuid` to handle regenerated responses - only exports the active conversation branch.

### Artifact Extraction
Automatically extracts artifacts from both `create_file` and `artifacts` tool calls and makes them available in exports. Supports 24+ content types with automatic file extension mapping (e.g., `text/markdown` → `.md`).

### Text Attachments
Extracts pasted text files that have `extracted_content` in the JSON. These are files you pasted or dropped into the conversation. Saved to the `attachments/` folder in ZIP exports with full text content preserved.

*Note: Binary files (PDF, DOCX, XLSX, etc.) are saved as `.txt` since only the extracted text content is available in the JSON.*

### Project Support
When exporting conversations from Claude Projects, the extension provides comprehensive project data:

**Filename Prefix**: All exports from project conversations are prefixed with `[Project_Name-project]_` for easy identification:
- `[My_Research-project]_conversation_name.md`
- `[My_Research-project]_conversation_name_claude-chat.zip`

**Project Metadata** (ZIP exports):
- `project/project.json` - Full project metadata from API
- `project/prompt_template.md` - System prompt/instructions extracted as markdown
- `project/docs.json` - Document list metadata

**Project Documents**: Full project files are downloaded via API when available. Falls back to extracting viewed portions from conversation if API fails.
- Full files: `project/filename.md`
- Truncated files (from view tool): `project/filename_truncated.md`

### Uploaded Files (PDFs, Images)
Downloads uploaded files (PDFs, images, etc.) directly from Claude's servers using your session authentication. Saved to the `uploads/` folder in ZIP exports. Includes:
- PDF documents (with page count metadata)
- Images (PNG, JPG, etc.)
- Other uploaded file types

The extension tries multiple URL patterns when downloading, including constructing URLs from file UUIDs when no direct URL is available.

*Note: The Python companion script can only extract metadata for uploaded files since it doesn't have browser session access.*

### Web Search Sources
Extracts metadata from web search results, including:
- Source title and URL
- Site domain and name
- Citation status (citable, missing)

Sources are grouped by domain in `links_and_sources.md` alongside conversation links.

### Thinking Block Summaries
Uses Claude's actual `summaries` array when available for accurate thinking block descriptions.

### Dynamic Code Fences
Automatically uses ```` (4 backticks) when content contains ``` to prevent nesting issues.

### UTF-8 Encoding & Mojibake Repair
All markdown files include a UTF-8 BOM (Byte Order Mark) to ensure browsers correctly interpret encoding when opening files via `file://` URLs.

Additionally, text content is scanned and repaired for mojibake (UTF-8 bytes misinterpreted as Windows-1252). Supports comprehensive character ranges including Greek, Cyrillic, box drawing, mathematical symbols, subscripts/superscripts, and emojis.

### Tool Use Display
Specific formatting for common tools:
- `web_search` - Shows query and formatted results
- `web_fetch` - Shows URL being fetched
- `bash_tool` - Shows truncated command
- `str_replace` - Shows "Edit: filename"
- `view` / `read_file` - Shows "Reading: filename"
- `create_file` - Shows "Creating artifact: filename"
- `artifacts` - Shows "Creating/Updating artifact: title"

### Citation References
When Claude uses web search, citations are converted to linked references with Wikipedia-style back-links:

**In text:** `...text about Hildegard[[1]](#ref-1) and more[[1]](#ref-1)...`

**References:**
```
1. [Hildegard of Bingen](https://wikipedia.org/...) - wikipedia.org [[1]](#cite-1), [[1:1]](#cite-1-1), [[1:2]](#cite-1-2)
2. [Another Source](https://example.com/...) - example.com [[2]](#cite-2), [[2:1]](#cite-2-1)
```

- Each citation in text links to its reference
- Back-links `[[1]], [[1:1]], [[1:2]]` link back to each citation position
- Replaces multiple ↩︎ arrows with numbered clickable links

### Statistics & Metadata
ZIP export includes:
- **Model name** - Parsed to show variant (e.g., "Claude 4.5 Sonnet")
- **Duration** - Time between first and last message
- **Starred status** - Whether conversation is starred
- **Features used** - Web Search, Artifacts, Extended Thinking
- Message counts (prompts, responses)
- Word counts (prompts, responses, total)
- Artifact count
- Text attachment count
- Project file count
- Uploaded file count
- Web search sources count
- Code block count with language breakdown
- URL count grouped by domain
- Timeline (first message, last message, export time)

## How It Works

The extension uses two methods to capture data:

1. **Fetch Interception** - Injects a script that hooks into `window.fetch` to capture API responses as they happen

2. **Direct API Calls** - For bulk export, makes authenticated requests to:
   - `GET /api/organizations/{orgId}/chat_conversations` - List all conversations
   - `GET /api/organizations/{orgId}/chat_conversations/{id}` - Get full conversation

Your existing session cookies are used for authentication (no API keys needed).

## Files

| File | Purpose |
|------|---------|
| `manifest.json` | Extension configuration (Manifest V3) |
| `background.js` | Service worker for sidebar panel behavior |
| `injected.js` | Fetch interceptor (runs in page context) |
| `content.js` | Bridge between page and extension |
| `popup.html` | Extension popup UI |
| `sidepanel.html` | Sidebar panel UI |
| `popup.js` | Export logic and markdown conversion |
| `jszip.min.js` | ZIP generation library |

## Troubleshooting

### "Refresh page to capture data"
The extension needs to intercept API calls. Refresh the Claude page after installing.

### "Navigate to a conversation to export current"
You're on Claude but not viewing a specific conversation. Click into a chat.

### Export buttons disabled
The extension hasn't captured conversation data yet. Try:
1. Refresh the page
2. Navigate to a different conversation and back
3. Check that you're on `claude.ai`

### Bulk export is slow
Each conversation requires a separate API request. A 300ms delay is added between requests to avoid rate limiting. For 100 conversations, expect ~30 seconds.

### Some conversations failed to export
Check the browser console for error details. Common causes:
- Conversation was deleted
- Network timeout
- Rate limiting (try again later)

### ZIP export fails
- Check browser console for specific error
- Try exporting as Markdown first to verify data capture
- Large conversations may take a moment to process

## Privacy & Security

- **No external servers** - All processing happens locally in your browser
- **No API keys stored** - Uses your existing Claude session
- **No data collection** - Nothing is sent anywhere except to your downloads folder
- **Open source** - Full source code visible in extension files

## Technical Documentation

See [TECHNICAL.md](TECHNICAL.md) for a comprehensive technical writeup covering:
- JSON structure and data extraction
- Message chain/tree resolution for branched conversations
- Content block types (text, thinking, tool_use, tool_result)
- Artifact extraction from multiple tool types
- File handling (attachments, uploads, ephemeral blobs, project files)
- Web search sources and citation processing
- API endpoints and authentication

## Companion Script

Works with [claude_json_to_md.py](https://github.com/...) for command-line processing of exported JSON files.

## Changelog

### v1.5.0
- **Markdown escaping in README** - Response titles with special characters (backticks, asterisks, etc.) are now properly escaped to prevent malformed rendering
- **Artifact embedding in full_chat.md** - Artifacts from `create_file` tool now embedded as code blocks in `full_chat.md` and included in `code_snippets.md`
- **Plain text integrated chat** - Generates `integrated_chat.txt` with clean ASCII formatting (no markdown syntax)
- **Project filename prefix** - Exports from project conversations prefixed with `[Project_Name-project]_`
- **Full project file download** - Downloads complete project files via API (falls back to truncated view tool results)
- **Project metadata export** - Saves `project.json` and `docs.json` in ZIP exports
- **System prompt extraction** - Extracts `prompt_template` field as `prompt_template.md`
- **Truncated file indicator** - Files from view tool fallback named with `_truncated` suffix
- **UTF-8 BOM for markdown files** - Ensures browsers correctly render files opened via `file://` URLs
- **Bash heredoc artifact extraction** - Extracts files created via `bash_tool` with `cat > file << 'EOF'` commands
- **Mojibake repair** - Fixes UTF-8 encoding corruption with comprehensive character support:
  - Greek letters (α β γ ζ), Cyrillic
  - Box drawing (┌ ─ │ └), geometric shapes (□ ◇ ○)
  - Math symbols (∀ ∃ ∈ ∅), arrows (→ ← ↔)
  - Subscripts/superscripts (₀ ₁ ² ³)
  - Emojis (🔥 😀 🚀 🤔)

### v1.4.0
- **Project files extraction** - Extracts files from Claude Projects that were viewed during conversation
- **Attachment linking in prompts** - Attachments now properly linked in prompts.md, including auto-generated filenames
- **Empty filename handling** - Attachments without filenames get generated names like `attachment_1.txt`

### v1.3.0
- **Web search sources extraction** - Extracts and displays sources from web search results
- **Combined links_and_sources.md** - Links and web sources in a single file, grouped by domain
- **Model name detection** - Parses model to show variant (e.g., "Claude 4.5 Sonnet")
- **Enhanced metadata** - Duration, starred status, features used (Web Search, Artifacts, Extended Thinking)
- **Image URL construction** - Constructs download URLs for images without direct URLs in JSON
- **Binary attachment handling** - PDF/DOCX/etc. attachments saved as .txt (extracted text only)
- Renamed `embedded_full_chat.md` to `integrated_chat.md`

### v1.2.0
- Added sidebar mode (stays open while browsing)
- New setting: "Open as sidebar by default"
- Added Export All (Embedded) - bulk embedded markdown export
- Added Export All (Mega-Zip) - single zip with all conversations
- Each mega-zip conversation folder matches individual zip structure
- Added support for `artifacts` tool (in addition to `create_file`)
- Automatic file extension mapping for 24+ content types
- Individual response.full.md files now embed associated artifacts with syntax highlighting
- ZIP exports now include uploaded files (PDFs, images) downloaded from Claude's servers
- ZIP exports now include pasted text attachments with extracted content
- Citation footnotes - web search citations converted to footnote-style references
- Added background service worker
- Renamed to Claude Takeout

### v1.1.0
- Added ZIP export with full archive structure
- Added keyboard shortcuts
- Improved tool handling (bash, str_replace, view, etc.)
- Better thinking block summaries using summaries array
- Dynamic code fence selection
- Branched conversation handling
- Progress indicator for operations
- Enhanced error handling

### v1.0.0
- Initial release
- Markdown and JSON export
- Bulk export all conversations
- Basic artifact handling

## License

MIT License - Feel free to modify and distribute.
