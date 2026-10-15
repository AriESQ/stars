# Reduce github_stars.json to the fields index.html reads, for publishing to GitHub Pages.
# The full file stays the source of truth; README/arXiv/etag bookkeeping is dropped here.
# Usage: jq -c -f scripts/slim_stars.jq github_stars.json > _site/github_stars.json
{
  username,
  profile,
  repositories: (.repositories | map_values({
    lists,
    metadata: ((.metadata // {}) | {
      description, language, stars, forks, open_issues, homepage,
      created_at, updated_at, pushed_at, starred_at
    })
  }))
}
