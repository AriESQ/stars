# PortWatch VI

**Does GTA VI run on PC yet?** A static GitHub Pages site that tracks every serious community effort to recompile, emulate or port the leaked Xbox Series build of GTA VI to PC. All efforts are scored on one ladder, and a scout refreshes the data every 3 hours.

- One headline progress bar shows the closest effort, with the top projects pinned to it.
- A live countdown runs to the missing executable's expected drop.
- A leaderboard card per effort shows its own bar, milestone ladder, groundwork breakdown, what works and what's blocking.
- Further sections cover the watchlist of early projects, a toolkit of asset tools, the scout's inbox of new candidates, and fake-download warnings.

No game files, keys or executables are hosted or linked, ever.

## Deploy on GitHub Pages

1. Create a new GitHub repository and push this folder to its `main` branch.
2. In the repo, open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Open **Settings → Actions → General** and make sure workflows are allowed.
4. Open **Actions → Scout → Run workflow** to run the first scout. It commits fresh data and deploys the site.

Each deploy also runs `scripts/build-site.mjs`, which turns `data/tracker.json` into pages search engines can read: one page per news story (`news/<id>.html`), a news archive, an RSS feed (`news/feed.xml`) and `sitemap.xml`. It then pings [IndexNow](https://www.indexnow.org/) (Bing, Yandex and others; no account needed) with the URLs that changed since the last deploy. For Google, add the site in Search Console and submit `sitemap.xml`.

From then on, `Scout` runs every 3 hours (00:17, 03:17, 06:17 … UTC) on GitHub's servers, so no computer of yours needs to be on. Any push to `main` redeploys the site through `Deploy site`. To change the frequency, edit the `cron` line in `.github/workflows/scout.yml`. For example, `17 6 * * *` runs it once a day. GitHub can delay scheduled runs by a few minutes when it's busy.

## What the scout does (`scripts/scout.mjs`)

1. **Refreshes** every tracked repo: stars, forks, issues, last push, commits in the last 7 days, and whether it's gone (404, or 451 for a DMCA block). It also hashes each README to notice changes.
2. **Spots claims.** If a README newly says GTA VI boots, reaches the menu or runs at some FPS, the card shows an "unverified claim" banner and the change feed records it.
3. **Discovers** new repos from GitHub and GitLab searches (`scout.queries` in `data/tracker.json`), Hacker News, Bluesky, Mastodon, Lemmy and 4chan, plus Reddit and X when keys are set, by pulling GitHub links out of posts. It also gathers **headlines** from the Google News and Bing News feeds, keeping only stories about the leak, ports, takedowns, scams or official news. And it **watches GitHub's public DMCA log** for new Take-Two or Rockstar notices, flagging any tracked project they name. On 4chan it uses the free read-only API, at one request per second. It opens only /v/ threads that mention GTA VI together with port terms (recomp, emulator, leak, executable, GitHub…), plus /vg/'s /gtag/ and /emugen/ generals. Change the boards with `scout.chan.boards`. Nothing from 4chan is shown on the site except, indirectly, repo names that pass every filter.
4. **Filters out spam** such as clone networks, download lures and "PC installer" repos. Their names are counted under *There is no download*, never linked.
5. **Filters out copies.** Re-uploads of tracked projects are flagged when they reuse a tracked project's name or have a README that is 60% or more identical, renamed copies included. Original fan games and repos without a real README are skipped too. Candidates already waiting are re-checked every run.
6. **Scores substance** from code language, size, technical depth, status tables, tests and commit activity. Repos with real code go to **New candidates**, shown as plain text and not linked until reviewed. Thin or off-topic ones are remembered and skipped.
7. **Writes news** (needs `ANTHROPIC_API_KEY`). Claude searches the web for takedowns, bans, confirmed leaks, legal news, scams and official announcements, then writes up to two short original articles. It runs at most every 11 hours, not on every 3-hourly scout run, to keep costs down. A source is kept only if it came up in Claude's own search. Each article's image is the source's preview image, credited and linked back; it falls back to a generated cover.
8. **Records** a change feed, the day's leader score for the sparkline, and a run summary.

### Optional secrets (Settings → Secrets and variables → Actions)

| Secret | What it enables |
|---|---|
| `ANTHROPIC_API_KEY` | **Claude review.** When a tracked README changes, or a new candidate shows up, Claude (`claude-opus-5-5`) reads the README and recent commits and re-scores the effort. It also promotes or rejects candidates automatically. Guardrails clamp the output: a GTA VI milestone only counts if Claude quotes text that really appears in the repo, and groundwork can rise at most 0.3 per run. Reviews are capped at 12 per run. Each costs very roughly $0.05–0.20, depending on README size. |
| `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` | Reddit search. Reddit blocks anonymous API and RSS access, so Reddit is skipped without these. The API is free for small non-commercial use, but since late 2025 every new app needs Reddit's manual approval. Create a "script" app at reddit.com/prefs/apps, request access, and paste the client ID and secret here once approved. |
| `X_BEARER_TOKEN` | X recent search. This needs a paid X API tier. |

Without any secrets the scout still runs on every keyless source, and new finds wait in *New candidates* for review.

### Daily Claude editor (alternative to an API key)

Instead of `ANTHROPIC_API_KEY`, a scheduled Claude session on the maintainer's PC can run once a day, following [EDITOR.md](EDITOR.md). It re-scores changed projects, reviews candidates, verifies leads, keeps the countdown accurate and writes news, then commits `data/tracker.json`. It also reads 4chan's /v/, /vg/ and /g/ in full through `tools/chan-scan.ps1`, which gathers GTA VI port discussion from live threads and the public archives into a local digest (`.chan/`, never committed). The scout only picks GitHub links out of those threads. It uses the maintainer's Claude plan and needs no separate billing. It runs while the Claude desktop app is open; a missed run happens on the next launch.

## Editing the data by hand

Everything lives in `data/tracker.json`:

- `efforts[]`: each effort has a `tier` (`tracked` puts it in the race, `watchlist` lists it below). Each also carries `groundwork` (four 0–1 values), `gta` (`loads`/`boots`/`menu`/`ingame` are 0, 0.5 or 1, plus `fps` and `stability`), and short `highlights` and `blockers`.
- `exe`: drives the countdown. If the release time is announced, set `expectedAt` (ISO time) and `timeAnnounced: true`. When it drops, set `status: "released"` and `releasedAt`, and the countdown turns into a "time since release" clock.
- `candidates[]`: move one into `efforts` to promote it, or into `ignored` to dismiss it.
- `site.heroImage`: the hero photo (see below). An optional `site.heroCredit` adds a credit line under it.

Scoring is in `assets/js/scoring.js`, shared by the site and the scout. Groundwork fills 0–25%. After that, milestones sit at Exe runs 25, First frame 40, Main menu 55, In-game 70, 30 FPS 85 and Stable 100.

## Hero photo

The hero shows an original sunset illustration until the photo loads. The photo is `assets/img/hero-miami.jpg` (2400px wide): Brickell, Miami, at night, by Steele Rutherford on Unsplash, free to use under the Unsplash License without a credit line. `assets/img/social-miami.jpg` (1200×630) is the share card, made from the same photo. Give a replaced image a new filename: images are cached for 4 hours in browsers and for days by link previews. Don't use GTA VI artwork or footage there.

## Local preview

Any static server works. On Windows without Node or Python:

```powershell
powershell -ExecutionPolicy Bypass -File tools/serve.ps1 -Port 8080
```

Then open http://localhost:8080. To try the scout locally with Node 20+, run `node scripts/scout.mjs --dry-run`. Setting `GITHUB_TOKEN` avoids the 60-requests-per-hour anonymous limit.

## Disclaimer

Fan-made and unofficial. Not affiliated with Rockstar Games, Take-Two or Microsoft. Scores are editorial estimates from public READMEs, commits and issues, and self-reported claims are labelled. Maintainers who think their project is mis-scored can open an issue with evidence.
