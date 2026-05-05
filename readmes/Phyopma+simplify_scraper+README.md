# Simplify Job Application Tracker

A command-line tool to fetch and track job application data from Simplify Jobs.

## Overview

This tool interfaces with the Simplify Jobs API to extract your job application history and save it as JSON data. It supports various filtering options to help you track applications by date range, job type, and application status.

## Setup

### Requirements

- Python 3.6+
- `requests` library

### Installation

1. Clone this repository:

   ```
   git clone https://github.com/Phyopma/simplify_scraper.git
   cd simplify_scraper
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Generate Sample Config:

   - Run the script: `python main.py`
   - It will create `config.json.sample`

4. Create config.json:

   - Copy `config.json.sample` to `config.json`
   - Fill in the sensitive information:
     - `cookie`: Your full cookie string (e.g., authorization=...; csrf=...)
     - `x-csrf-token`: Your CSRF token
   - Get these from your browser's Developer Tools (Network tab) after logging into Simplify Jobs

   Example filled config.json (do not use these values):

   ```json
   {
     "cookie": "authorization=eyJhbGciOInR5cCpXVCJ9...; csrf=eyJhbGciOiiIsInR5cCI6IkpXVCJ9...",
     "x-csrf-token": "eyJhbGciOiJIUnCI6IkpXVCJ9..."
   }
   ```

## How to Get Your Credentials

To obtain your `cookie` and `x-csrf-token`:

1. Log in to your Simplify account in a browser
2. Open Developer Tools (F12 or right-click > Inspect)
3. Go to the Network tab
4. Look for API requests to `simplify.jobs`
5. Find the request headers and copy the values for:
   - `cookie` - Contains your authentication data
   - `x-csrf-token` - Contains your CSRF protection token

## Usage

### Basic Usage

```bash
python main.py --all
```

### Filter by Job Type

Available job types: `internship`, `part-time`, `full-time`

```bash
python main.py --job-type internship
```

### Filter by Application Status

Available statuses: `applied`, `saved`, `screen`, `interview`, `offer`, `withdrawn`, `ghosted`, `rejected`, `accepted`

```bash
python main.py --status screen
```

### Filter by Date Range

```bash
python main.py --after 2025-03-01 --before 2025-03-07
```

### Combined Filters

```bash
python main.py --job-type part-time --after 2025-03-01 --before 2025-03-07
```

```bash
python main.py --job-type internship --status screen
```

## Output

The tool saves results to `tracker_data.json` in the current directory. This file contains:

- Total number of items matching your filter
- Detailed information for each job application

## Available Filters

| Filter     | CLI Option   | Description                          | Available Values                                                                                   |
| ---------- | ------------ | ------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Job Type   | `--job-type` | Type of employment                   | `internship`, `part-time`, `full-time`                                                             |
| Status     | `--status`   | Application status                   | `applied`, `saved`, `screen`, `interview`, `offer`, `withdrawn`, `ghosted`, `rejected`, `accepted` |
| Start Date | `--after`    | Applications after date (inclusive)  | YYYY-MM-DD format (e.g., 2025-03-01)                                                               |
| End Date   | `--before`   | Applications before date (inclusive) | YYYY-MM-DD format (e.g., 2025-03-07)                                                               |
| All Data   | `--all`      | Fetch all data without filters       | Flag (no value needed)                                                                             |

## Notes

- This tool uses pagination to retrieve data (25 items per page)
- Include a 1-second delay between API calls to avoid rate limiting
- Your credentials in `config.json` are sensitive - keep them private

## License

This project is completely free to use, modify, and distribute. No attribution required. Do whatever you want with it.
