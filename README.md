# GitHub Stars Scraper, Organizer, and Dashboard
This project automatically scrapes and organizes your GitHub stars, including star lists (tags), using GitHub Actions. It also provides a web-based dashboard to explore and search through your starred repositories.

## Features
- Scrapes all starred repositories for a GitHub user
- Retrieves and organizes star lists (tags) for each repository
- Handles large collections (3000+ stars) gracefully
- Implements intelligent rate limiting to avoid API throttling
- Provides detailed logging for transparency and debugging
- Commits and pushes updates only when changes are detected
- Runs daily via GitHub Actions, with option for manual triggers
- Offers a web-based dashboard with D3 constellation chart, advanced search, language filtering, and star list filtering

## How it works
1. The GitHub Action runs daily at midnight UTC (or can be manually triggered).
2. It executes two main scripts:
   - `scripts/scrape_stars.py`: Fetches all starred repositories, their metadata, and user profile.
   - `scripts/update_star_lists.py`: Retrieves star lists for each repository.
3. The scripts:
   - Fetch all starred repositories and their metadata
   - Retrieve all star lists (tags) for the user
   - Associate each repository with its corresponding lists
   - Handle rate limiting using both preemptive and reactive strategies
   - Cache user profile data using ETags to minimize API calls
4. Results are saved in `github_stars.json`
5. If there are changes, the action commits and pushes the updated file to the repository
6. A static dashboard is deployed to GitHub Pages

## Setup
1. Fork this repository
2. Go to your forked repository's settings
3. Navigate to "Secrets and variables" > "Actions"
4. Add the following repository secret:
   - `GITHUB_TOKEN`: A GitHub personal access token with `repo` scope
5. (Optional) The forked repo includes large JSON data files from the original user. These accumulate significantly in git history. To clean them out using git's built-in `filter-branch`:
   ```bash
   # Remove the data files from all history
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch github_stars.json' \
     --prune-empty -- --all

   # Clean up the backup refs and garbage collect
   rm -rf .git/refs/original/
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive

   # Force push the cleaned history
   git push origin --force --all
   git push origin --force --tags
   ```
   After this, the first scrape run will regenerate these files with your own data.
6. The action will now run automatically every day, or you can trigger it manually from the "Actions" tab
7. Enable GitHub Pages in your repository settings, setting the source to **GitHub Actions** (Settings > Pages > Source)

## File Structure
- `scripts/scrape_stars.py`: Main script for fetching starred repositories and metadata
- `scripts/update_star_lists.py`: Script for retrieving and organizing star lists
- `.github/workflows/main.yml`: GitHub Actions workflow for data scraping
- `.github/workflows/update_star_lists.yml`: GitHub Actions workflow for star list updates
- `.github/workflows/deploy-to-gh-pages.yml`: GitHub Actions workflow for deploying the dashboard
- `containers/Containerfile`: Container definition for running the scraper
- `containers/Containerfile.dashboard`: Container definition for running the dashboard locally
- `index.html`: Single-file dashboard with inline CSS/JS and D3.js constellation chart
- `github_stars.json`: Output file containing all starred repository data

## Dashboard
The dashboard is a single `index.html` file using vanilla JavaScript and D3.js (loaded from CDN). It provides:
- D3 constellation scatter plot (star count vs starred date, colored by language)
- Text search across repository names and descriptions
- Advanced multi-condition search with AND/OR logic
- Language filtering via clickable legend
- Star list (tag) filtering
- 6 sort options with ascending/descending toggle
- Expandable repository cards with detailed metadata
- GitHub dark theme

To view the dashboard, visit `https://<your-github-username>.github.io/stars/` after the GitHub Actions workflow has completed.

## Local Testing

### Scraper

You can test the scraper locally using a Podman (or Docker) container:

```bash
# Build the container
podman build -t stars-test -f containers/Containerfile .

# Run with your GitHub token
podman run --rm -e GITHUB_TOKEN="$GITHUB_TOKEN" stars-test
```

Since all repos are already in `github_stars.json`, it should process all chunks with no changes and exit cleanly (no commit attempted).

### Dashboard

**Option 1 — uv (simplest):**

```bash
uv run python -m http.server 8080
```

Then open `http://localhost:8080`. No system Python needed; uv supplies it.

**Option 2 — Podman container:**

```bash
podman build -f containers/Containerfile.dashboard -t stars-dashboard .
podman run --rm -d --name stars-dashboard -p 8080:80 stars-dashboard
```

Then open `http://localhost:8080`. Note: on macOS, Podman runs inside a Linux VM — port forwarding works but large file serves (e.g. `github_stars.json`) may be slower than the uv option.

To stop the container: `podman stop stars-dashboard`

## Customization
You can customize the behavior of the scripts by modifying the following constants in the Python files:
- `STARS_FILE`: Name of the output JSON file
- `CHUNK_SIZE`: Number of repositories to process in each chunk
- `RATE_LIMIT_THRESHOLD`: Number of API requests to keep in reserve
- `DEFAULT_RATE_LIMIT` and `DEFAULT_RATE_LIMIT_WINDOW`: Default rate limiting for web scraping

## Limitations
- The script can only retrieve up to 3000 repositories per list due to GitHub's pagination limits.
- Web scraping is used for retrieving star lists, which may break if GitHub significantly changes their HTML structure.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is open source and available under the [MIT License](LICENSE).
