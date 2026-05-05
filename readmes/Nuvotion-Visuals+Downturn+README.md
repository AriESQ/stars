# Downturn

A markdown web browser. Convert any web page to clean markdown and browse the web in a distraction-free reader. Edit with live preview, open local files and folders, manage bookmarks and history.

Also works as an MCP server for AI agents, a browser extension, and a standalone HTTP API.

[GitHub](https://github.com/Nuvotion-Visuals/Downturn) | [npm](https://www.npmjs.com/package/downturn)

<img width="1181" height="998" alt="Screenshot_20260414_012630" src="https://github.com/user-attachments/assets/0ed28494-f59b-4166-a540-32ed20fef86f" />

## Web Browser

```bash
npm run dev
```

Open `http://localhost:4001`. Type a URL, search term, or domain and press Enter.

- **Browse the web in markdown** — click links to navigate, Ctrl+click to open in a new tab
- **Tabs** — drag to reorder, middle-click to close, Ctrl+T/W to create/close
- **Split view** — markdown editor + rendered preview, or toggle to single pane
- **Edit** — the markdown pane is always editable with live preview
- **Local files** — open `.md` files or entire folders with a file tree sidebar
- **Save** — Ctrl+S saves to the opened file, or triggers Save As
- **Bookmarks** — star icon bookmarks the current page, viewable in the sidebar
- **History** — automatic, searchable, grouped by date in the sidebar
- **Autocomplete** — URL bar suggests from history and bookmarks as you type
- **Search** — plain text searches the web; results render as markdown
- **YouTube** — paste a YouTube URL to get the video transcript as markdown with optional timestamps
- **GitHub** — paste a GitHub repo URL to view the README
- **Site navigation** — sidebar extracts nav links from the page, with a site home link
- **Themes** — Dark, Light, and Black (OLED). Auto-detects system preference
- **Typography** — choose editor and preview fonts with a visual picker, adjust font size, line height, and line width
- **Favicons** — shown in tabs, bookmarks, history, and autocomplete
- **PWA** — installable as a standalone app with offline support
- **Mobile** — responsive layout with touch targets, swipe navigation, and sidebar overlay
- **Zen mode** — hide all UI chrome to focus on content

## Browser Extension

Available for Chrome and Firefox. Converts the current page to markdown with one click — no server needed. Edit the result, copy to clipboard, or download as `.md`.

Build:
```bash
npm run ext:build
```

Load unpacked from `extension/dist/` in Chrome (`chrome://extensions`) or as a temporary add-on in Firefox (`about:debugging`).

## Deploy

```bash
npx wrangler deploy
```

Deploys automatically to Cloudflare Workers on version bump via GitHub Actions. Also publishes to npm and creates a GitHub release with the browser extension packages.

## MCP Server

```json
{
  "mcpServers": {
    "downturn": {
      "command": "npx",
      "args": ["-y", "downturn"]
    }
  }
}
```

Tools:
- **`url_to_markdown`** — fetch a URL and return markdown. GitHub repos return the README. YouTube videos return the transcript.
- **`html_to_markdown`** — convert an HTML string to markdown

| Parameter | Default | Description |
|-----------|---------|-------------|
| `output_path` | | Full file path to write markdown to |
| `output_dir` | | Directory to write to; filename auto-generated from page title |
| `include_title` | `true` | Prepend page title as H1 |
| `include_links` | `true` | Include hyperlinks |
| `include_images` | `true` | Include images |
| `use_readability` | `true` | Extract article content |
| `absolute_urls` | `true` | Resolve relative URLs to absolute |

## HTTP API

```bash
PORT=3000 node index.mjs
```

```
GET /?url=https://example.com&title=true&links=true&clean=true
POST / with html= and url= parameters
```

Returns `Content-Type: text/markdown` with CORS headers.

## Pipeline

1. Fetch page (follows redirects)
2. Strip scripts and styles
3. Extract article content (Mozilla Readability)
4. Convert to markdown (Turndown)
5. Resolve relative URLs to absolute
6. Strip empty permalink anchors and link titles
7. Encode parentheses in URLs
8. Apply site-specific filters (Wikipedia, Medium, Stack Overflow, etc.)

## Testing

```bash
npm test
```

580 tests covering the conversion pipeline, URL resolution, link title stripping, permalink anchor stripping, markdown rendering, worker API, MCP integration, nav extraction, title extraction, omnibox, favicons, and debounce. Tests run automatically in CI before deploy.

## Structure

```
worker.mjs                             Cloudflare Worker + local dev server
index.mjs                              HTTP API server
mcp.mjs                                MCP stdio transport
wrangler.toml                          Cloudflare deployment config
url_to_markdown_processor.mjs          Core conversion pipeline
url_to_markdown_common_filters.mjs     Post-processing filters
url_to_markdown_formatters.mjs         Code block and table pre-processing
url_to_markdown_readers.mjs            URL fetching, redirect following
url_to_markdown_apple_dev_docs.mjs     Apple developer docs parser
html_table_to_markdown.mjs             HTML table conversion
title_utils.mjs                        Title extraction and filename slugification

public/
  index.html                           Web UI
  ui.mjs                               Markdown renderer, omnibox, utilities
  db.mjs                               IndexedDB storage (settings, history, bookmarks, cache)
  themes.mjs                           Theme system (dark, light, black)
  sw.js                                Service worker for PWA/offline
  start.md                             Start page content
  site.webmanifest                     PWA manifest

extension/
  manifest.json                        Browser extension manifest (Chrome + Firefox)
  src/                                 Extension source files
  build.mjs                            esbuild bundler
  dist/                                Built extension (gitignored)

lib/
  html_parser.mjs                      DOM parser (vendored JSDOMParser)
  readability.mjs                      Content extraction (vendored Readability)
  turndown.mjs                         HTML to markdown (vendored Turndown)
  html_entities.mjs                    HTML entity decoder
  http_server.mjs                      HTTP server on node:http
  rate_limiter.mjs                     Sliding window rate limiter
```

## Credits

- [Mozilla Readability](https://github.com/mozilla/readability) (Apache 2.0)
- [JSDOMParser](https://github.com/mozilla/readability/blob/main/JSDOMParser.js) (MPL 2.0)
- [Turndown](https://github.com/mixmark-io/turndown) (MIT)

## License

MIT
