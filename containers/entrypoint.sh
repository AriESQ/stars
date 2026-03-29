#!/bin/sh
# Apply git identity if provided via env vars
git config --global user.name "${GIT_USER_NAME:-test}"
git config --global user.email "${GIT_USER_EMAIL:-container@test}"

# Re-commit any volume-mounted files so git starts clean
git add -A && git commit --amend --no-edit --allow-empty >/dev/null 2>&1

exec python scripts/scrape_stars.py
