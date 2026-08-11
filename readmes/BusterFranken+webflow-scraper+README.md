# Webflow Website Scraper

A comprehensive Node.js tool for scraping Webflow websites and creating fully functional offline versions. This project was developed to scrape [FruitPunch AI](https://fruitpunch.ai) and create a complete offline copy with all assets, dynamic content, and working internal links.

## Features

- ✅ **Complete Website Scraping**: Downloads all HTML pages, CSS, JavaScript, images, fonts, and other assets
- ✅ **Dynamic Content Support**: Handles Webflow CMS content loaded via JavaScript/API calls
- ✅ **API Interception**: Captures and caches API responses for offline functionality
- ✅ **Cloudflare Bypass**: Supports manual Cloudflare challenge completion in headful mode
- ✅ **Link Rewriting**: Converts absolute internal links to relative paths for offline navigation
- ✅ **Asset Management**: Organizes all assets in a centralized `_assets` directory
- ✅ **Popup Removal**: Automatically hides/removes newsletter popups and tracking scripts
- ✅ **Incremental Scraping**: Re-scrape only blank or failed pages without re-downloading everything
- ✅ **Screenshot Capture**: Takes full-page screenshots of each scraped page for verification

## Requirements

- Node.js (v16 or higher)
- npm or yarn
- Playwright (automatically installed via npm)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/BusterFranken/webflow-scraper.git
cd webflow-scraper
```

2. Install dependencies:
```bash
npm install
```

## Usage

### Initial Scraping

Run the main scraper to download the entire website:

```bash
node scrape.mjs
```

This will:
- Fetch the sitemap from the target website
- Download all pages and assets
- Save everything to the `offline/` directory
- Generate a report in `offline/_report.json`

**Note**: The scraper runs in headful mode (visible browser) to allow manual completion of Cloudflare challenges if they appear.

### Re-scraping Blank Pages

If some pages come back blank (often due to dynamic content loading), use the re-scraper:

```bash
node rescrape-blank.mjs
```

This script:
- Identifies pages with minimal content
- Re-scrapes only those pages with extended timeouts
- Waits for CMS content to fully load
- Intercepts and caches API responses

### Fixing Internal Links

After scraping, fix internal links to work offline:

```bash
node fix-links.mjs
```

This converts all absolute internal links to relative paths.

### Generating Localhost Links

Generate a list of all localhost URLs for easy navigation:

```bash
node generate-links.mjs
```

This creates `offline/_localhost-links.txt` with all page URLs.

### Viewing the Offline Website

Start a local HTTP server to view the scraped website:

```bash
cd offline
python3 -m http.server 8000
```

Then open `http://localhost:8000/index/index.html` in your browser.

## Configuration

Edit `scrape.mjs` to customize:

- **Target Website**: Change the `BASE` constant (line ~27)
- **Output Directory**: Modify the `OUT` constant (line ~28)
- **Concurrency**: Adjust `CONCURRENCY` for parallel requests (line ~29)
- **Timeout**: Change `TIMEOUT` for page loading (line ~30)

## Project Structure

```
webflow-scraper/
├── scrape.mjs              # Main scraping script
├── rescrape-blank.mjs      # Re-scraper for blank pages
├── fix-links.mjs           # Link fixing utility
├── generate-links.mjs      # Localhost links generator
├── package.json            # Dependencies
├── .gitignore              # Git ignore rules
└── offline/                # Scraped website content
    ├── _assets/            # All downloaded assets (CSS, JS, images, fonts)
    ├── _api_data/          # Cached API responses for offline use
    ├── _report.json        # Scraping report
    ├── _sitemap.xml        # Cached sitemap
    ├── _localhost-links.txt # List of localhost URLs
    └── [page directories]/ # HTML pages organized by URL structure
        └── index.html       # Page content
        └── screenshot.png  # Full-page screenshot
```

## How It Works

### 1. Sitemap Parsing
The scraper fetches the website's sitemap.xml to discover all pages. If the sitemap is protected by Cloudflare, it uses Playwright to bypass the challenge.

### 2. Page Scraping
For each page:
- Navigates to the URL using Playwright
- Waits for Cloudflare challenges (if any)
- Detects CMS pages and waits for dynamic content to load
- Scrolls the page to trigger lazy-loaded content
- Intercepts API calls and caches responses
- Captures the fully rendered HTML from the DOM

### 3. Asset Downloading
- Intercepts all network requests to capture assets
- Downloads CSS, JavaScript, images, fonts, and other resources
- Parses CSS files to extract referenced assets (fonts, images in `url()`)
- Rewrites asset paths to point to local files

### 4. HTML Processing
- Removes tracking scripts and external dependencies
- Rewrites internal links to relative paths
- Injects API interceptor script for offline API calls
- Hides popups and overlays with CSS

### 5. API Interception
For Webflow CMS pages that load content dynamically:
- Intercepts `fetch()` and `XMLHttpRequest` calls to Webflow APIs
- Caches API responses as JSON files
- Injects client-side script to serve cached responses when offline

## Troubleshooting

### Pages Appear Blank
- Run `node rescrape-blank.mjs` to re-scrape blank pages
- Check browser console for JavaScript errors
- Verify API responses are cached in `offline/_api_data/`

### Cloudflare Challenges
- The scraper runs in headful mode - complete challenges manually in the browser window
- Reduce `CONCURRENCY` to 1 for easier manual intervention

### Missing Assets
- Check `offline/_report.json` for failed downloads
- Some assets may have very long filenames (ENAMETOOLONG errors) - these are logged but don't break functionality

### Links Not Working Offline
- Run `node fix-links.mjs` to rewrite internal links
- Ensure you're viewing via HTTP server, not `file://` protocol

## Limitations

- **Dynamic JavaScript**: Some JavaScript that requires live API connections may not work offline
- **External Services**: Forms, search, and other features requiring backend services won't function offline
- **Large Repositories**: The scraped content can be quite large (hundreds of MB) due to all assets being downloaded

## License

This project is provided as-is for educational and archival purposes.

## Acknowledgments

Developed to create an offline archive of the FruitPunch AI website.

