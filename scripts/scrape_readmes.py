"""Scrape the README of every starred repo into the local corpus.

Reads the list of starred repos from `github_stars.json`, fetches
`/repos/{full_name}/readme` for each one, and writes the README to
`readmes/<owner>+<repo>+<filename>`. Per-repo `readme` metadata
(etag, sha, size, status, fetched_at) is stored back into
`github_stars.json` so subsequent runs can do conditional GETs and
skip unchanged READMEs via ETag.
"""

import base64
import json
import os
import random
import sys
import time
from datetime import datetime, timedelta, UTC
from pathlib import Path

import requests
from loguru import logger

# Reuse the git-remote username detection from the sibling scraper.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scrape_stars import get_git_remote_username  # noqa: E402

GITHUB_API = "https://api.github.com"
STARS_FILE = "github_stars.json"
README_DIR = Path("readmes")
CHUNK_SIZE = 50
RATE_LIMIT_THRESHOLD = 100
MISSING_TTL_DAYS = 30
MAX_RETRIES = 5
INITIAL_BACKOFF = 60  # seconds

logger.add("scrape_readmes.log", rotation="10 MB")


def load_existing_data():
    if os.path.exists(STARS_FILE):
        with open(STARS_FILE, "r") as f:
            return json.load(f)
    return {"last_updated": None, "repositories": {}}


def save_data(data):
    with open(STARS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def check_initial_rate_limit(token):
    url = f"{GITHUB_API}/rate_limit"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    remaining = data["resources"]["core"]["remaining"]
    reset_time = data["resources"]["core"]["reset"]

    if remaining <= RATE_LIMIT_THRESHOLD:
        wait = max(reset_time - time.time(), 0)
        logger.warning(
            f"Rate limit already low ({remaining} remaining). Resets in {wait:.0f}s."
        )
        return False

    logger.info(f"Initial rate limit OK. {remaining} requests remaining.")
    return True


def handle_rate_limit(response):
    remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))

    if remaining <= RATE_LIMIT_THRESHOLD:
        sleep_time = max(reset_time - time.time(), 0) + 1
        if sleep_time > 0:
            logger.warning(
                f"Rate limit low ({remaining} remaining). Sleeping {sleep_time:.0f}s."
            )
            time.sleep(sleep_time)


def exponential_backoff(attempt):
    return INITIAL_BACKOFF * (2 ** attempt) + random.uniform(0, 1)


def safe_filename(full_name: str, name: str) -> str:
    """Compose `<owner>+<repo>+<name>`.

    `+` is disallowed in GitHub usernames, repo names, and the README
    filenames returned by the API, so the result is unambiguous.
    """
    owner, repo = full_name.split("/", 1)
    for piece, label in ((owner, "owner"), (repo, "repo"), (name, "readme name")):
        if "+" in piece:
            raise ValueError(
                f"Unexpected '+' in {label} {piece!r} for {full_name}; aborting to avoid path collision."
            )
    return f"{owner}+{repo}+{name}"


def should_skip(readme_meta) -> bool:
    """Skip refetch if we recorded a 404 within the TTL window."""
    if not readme_meta or readme_meta.get("status") != "missing":
        return False
    fetched_at = readme_meta.get("fetched_at")
    if not fetched_at:
        return False
    try:
        last = datetime.fromisoformat(fetched_at)
    except ValueError:
        return False
    if last.tzinfo is None:
        last = last.replace(tzinfo=UTC)
    return datetime.now(UTC) - last < timedelta(days=MISSING_TTL_DAYS)


def fetch_readme(full_name, token, etag=None):
    """Fetch the README for a repo. Returns a dict describing the outcome.

    Outcome shapes:
      {"status": "not_modified"}
      {"status": "ok", "name", "sha", "size", "etag", "content"}  # content is bytes
      {"status": "missing"}
      {"status": "error", "reason"}
      {"status": "binary", "name", "sha", "size", "etag"}
    """
    url = f"{GITHUB_API}/repos/{full_name}/readme"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    if etag:
        headers["If-None-Match"] = etag

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request error for {full_name}: {e}")
            return {"status": "error", "reason": str(e)}

        if response.status_code == 304:
            return {"status": "not_modified"}

        if response.status_code == 404:
            return {"status": "missing"}

        if response.status_code in (403, 429):
            if attempt < MAX_RETRIES - 1:
                backoff = exponential_backoff(attempt)
                logger.warning(
                    f"Rate-limited ({response.status_code}) for {full_name}. "
                    f"Backing off {backoff:.1f}s (attempt {attempt + 1})."
                )
                time.sleep(backoff)
                continue
            return {"status": "error", "reason": f"rate-limited after {MAX_RETRIES} attempts"}

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error for {full_name}: {e}")
            return {"status": "error", "reason": str(e)}

        handle_rate_limit(response)

        body = response.json()
        new_etag = response.headers.get("ETag", "")
        name = body.get("name") or "README"
        sha = body.get("sha", "")
        size = body.get("size", 0)
        encoding = body.get("encoding")
        content_b64 = body.get("content", "")

        if encoding == "base64" and content_b64:
            raw = base64.b64decode(content_b64)
        else:
            # Empty content (>1MB) — fall back to download_url.
            download_url = body.get("download_url")
            if not download_url:
                return {"status": "error", "reason": "no content and no download_url"}
            try:
                dl = requests.get(download_url)
                dl.raise_for_status()
                raw = dl.content
            except requests.exceptions.RequestException as e:
                return {"status": "error", "reason": f"download_url fetch failed: {e}"}

        try:
            raw.decode("utf-8")
        except UnicodeDecodeError:
            return {
                "status": "binary",
                "name": name,
                "sha": sha,
                "size": size,
                "etag": new_etag,
            }

        return {
            "status": "ok",
            "name": name,
            "sha": sha,
            "size": size,
            "etag": new_etag,
            "content": raw,
        }

    return {"status": "error", "reason": "unreachable"}


def write_readme(full_name, name, content, readme_dir=README_DIR, known_paths=None):
    """Write README content to disk. Returns the relative path written."""
    filename = safe_filename(full_name, name)
    path = readme_dir / filename
    if known_paths is not None:
        existing_owner = known_paths.get(str(path))
        if existing_owner and existing_owner != full_name:
            raise RuntimeError(
                f"Path collision: {path} already claimed by {existing_owner}, "
                f"now requested by {full_name}."
            )
        known_paths[str(path)] = full_name
    readme_dir.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(content)
    return str(path)


def collect_known_paths(repositories):
    paths = {}
    for full_name, repo in repositories.items():
        readme = repo.get("readme") or {}
        path = readme.get("path")
        if path:
            paths[path] = full_name
    return paths


def process_repos(data, token, readme_dir=README_DIR):
    repositories = data["repositories"]
    full_names = sorted(repositories.keys())
    total = len(full_names)
    logger.info(f"Processing {total} repositories.")

    known_paths = collect_known_paths(repositories)
    processed_since_save = 0

    for i, full_name in enumerate(full_names, start=1):
        repo = repositories[full_name]
        readme_meta = repo.get("readme")

        if should_skip(readme_meta):
            continue

        etag = readme_meta.get("etag") if readme_meta else None
        result = fetch_readme(full_name, token, etag)
        now_iso = datetime.now(UTC).isoformat()

        if result["status"] == "not_modified":
            if readme_meta is not None:
                readme_meta["fetched_at"] = now_iso
            logger.debug(f"[{i}/{total}] {full_name}: 304 not modified")

        elif result["status"] == "ok":
            try:
                path = write_readme(
                    full_name, result["name"], result["content"], readme_dir, known_paths
                )
            except (RuntimeError, ValueError) as e:
                logger.error(f"[{i}/{total}] {full_name}: {e}")
                repo["readme"] = {
                    "etag": result["etag"],
                    "sha": result["sha"],
                    "size": result["size"],
                    "fetched_at": now_iso,
                    "status": "error",
                    "reason": str(e),
                }
            else:
                repo["readme"] = {
                    "path": path,
                    "etag": result["etag"],
                    "sha": result["sha"],
                    "size": result["size"],
                    "fetched_at": now_iso,
                    "status": "ok",
                }
                logger.info(f"[{i}/{total}] {full_name}: wrote {path} ({result['size']}B)")

        elif result["status"] == "missing":
            repo["readme"] = {
                "fetched_at": now_iso,
                "status": "missing",
            }
            logger.info(f"[{i}/{total}] {full_name}: no README (404)")

        elif result["status"] == "binary":
            repo["readme"] = {
                "etag": result["etag"],
                "sha": result["sha"],
                "size": result["size"],
                "fetched_at": now_iso,
                "status": "binary",
                "name": result["name"],
            }
            logger.info(f"[{i}/{total}] {full_name}: binary README, not stored")

        else:  # error
            existing = repo.get("readme") or {}
            existing.update({
                "fetched_at": now_iso,
                "status": "error",
                "reason": result.get("reason", "unknown"),
            })
            repo["readme"] = existing
            logger.warning(f"[{i}/{total}] {full_name}: error ({result.get('reason')})")

        processed_since_save += 1
        if processed_since_save >= CHUNK_SIZE:
            data["last_updated"] = now_iso
            save_data(data)
            processed_since_save = 0
            logger.info(f"Saved progress at {i}/{total}.")

    data["last_updated"] = datetime.now(UTC).isoformat()
    save_data(data)
    logger.info("README scrape complete.")


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        logger.error("GITHUB_TOKEN environment variable is not set.")
        raise ValueError("GitHub token must be provided via GITHUB_TOKEN.")

    username = os.environ.get("GITHUB_USERNAME") or get_git_remote_username()
    if username:
        logger.info(f"GitHub user: {username}")

    if not check_initial_rate_limit(token):
        logger.warning("Continuing despite low rate limit.")

    data = load_existing_data()
    if not data.get("repositories"):
        logger.error(
            f"No repositories found in {STARS_FILE}. Run scrape_stars.py first."
        )
        raise SystemExit(1)

    process_repos(data, token)


if __name__ == "__main__":
    main()
