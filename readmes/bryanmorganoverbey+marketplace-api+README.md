# Marketplace Scraper (Python + Apify Actor)

Scrapes Facebook Marketplace search results without logging in by calling Facebook's GraphQL endpoints. Provides simple Python helpers and an Apify Actor entrypoint that outputs results to the default dataset.

> Note: Use responsibly and review the website's Terms of Service before scraping.

### What’s included
- `MarketplaceScraper.py`: Core helpers
  - `getLocations(locationQuery)`
  - `getListings(latitude, longitude, listingQuery, numPageResults=1)`
  - `searchListings(locationQuery, listingQuery, numPageResults=1)` (convenience wrapper)
- `main.py`: Apify Actor entrypoint using the Python SDK
- `.actor/actor.json` + `.actor/INPUT_SCHEMA.json`: Actor metadata and input UI
- `Dockerfile`: Container to run on Apify/cloud
- `requirements.txt`: Runtime deps (`requests`, `apify`)

### Data model (output items)
Each listing item pushed to the dataset contains (best-effort; some fields can be empty):
```json
{
  "id": "string",
  "name": "string",
  "currentPrice": "string",
  "previousPrice": "string",
  "saleIsPending": "true|false",
  "primaryPhotoURL": "string",
  "sellerName": "string",
  "sellerLocation": "string",
  "sellerType": "string"
}
```

## Getting started (local, no Docker)
1. Python 3.11+
2. Install deps:
```bash
pip install -r requirements.txt
```

### Option A: Run the Apify entrypoint (uses defaults = Miami + bikes)
```bash
python main.py
```
- Output is written to local Apify storage at `./apify_storage/datasets/default`. You can inspect JSON/CSV there or via the Apify CLI.

### Option B: Call the helper directly
```python
from MarketplaceScraper import searchListings
status, error, data = searchListings("Miami", "bikes", numPageResults=1)
print(status, error)
print(data)
```

## Configure input (for the Actor)
The Actor reads input via Apify SDK (`Actor.get_input()`), with these fields:
- `locationQuery` (string, default: "Miami")
- `listingQuery` (string, default: "bikes")
- `numPageResults` (integer, 1–10, default: 1)

When running locally with `python main.py`, defaults are used if you don’t provide input. To provide input locally, create:
```
apify_storage/key_value_stores/default/INPUT.json
```
with content like:
```json
{
  "locationQuery": "Miami",
  "listingQuery": "bikes",
  "numPageResults": 2
}
```

## Run with Docker (locally)
1. Ensure Docker Desktop is running
2. Build image:
```bash
docker build -t marketplace-api-apify:latest .
```
3. Option A: Run with defaults
```bash
docker run --rm marketplace-api-apify:latest
```
4. Option B: Run with custom input by mounting local storage (reads INPUT.json and writes dataset):
```bash
# Prepare local storage layout and input
mkdir -p ./apify_storage/key_value_stores/default
cat > ./apify_storage/key_value_stores/default/INPUT.json << 'JSON'
{
  "locationQuery": "Miami",
  "listingQuery": "bikes",
  "numPageResults": 2
}
JSON

# Mount local ./apify_storage to container /apify_storage
# The base image uses /apify_storage as default storages root

docker run --rm -v "$PWD/apify_storage:/apify_storage" marketplace-api-apify:latest
```
- Results will appear under `./apify_storage/datasets/default`.

## Run on Apify platform
You can push and run this as an Apify Actor.

- Via Apify CLI (recommended):
```bash
# From this project directory
apify login
apify push
```
Then run the Actor in Apify Console. The input UI is defined by `.actor/INPUT_SCHEMA.json`.

- Or create a new Python Actor in Console and upload this repo/folder. The build uses the provided `Dockerfile`.

## Programmatic usage (outside Actor)
Use `MarketplaceScraper.py` helpers in your own code:
```python
from MarketplaceScraper import getLocations, getListings, searchListings

# Find coordinates
status, error, loc = getLocations("Miami")
latitude = loc["locations"][0]["latitude"]
longitude = loc["locations"][0]["longitude"]

# Search listings
status, error, data = getListings(latitude, longitude, "bikes", numPageResults=1)
# or use the one-call wrapper
status, error, data = searchListings("Miami", "bikes", numPageResults=1)
```

## Notes & limitations
- The response structure may change if upstream GraphQL responses change.
- Some fields can be missing or null; parsing is defensive to avoid crashes.
- Be mindful of rate limits and legal considerations.
