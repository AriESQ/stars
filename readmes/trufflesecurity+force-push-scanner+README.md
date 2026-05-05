# Force Push Secret Scanner

This tool scans for secrets in dangling (dereferenced) commits on GitHub created by force push events. A [force push](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force) occurs when developers overwrite commit history, which often contains mistakes, like hard-coded credentials. This project relies on archived force push event data in the [GHArchive](https://www.gharchive.org/) to identify the relevant commits. 

![Force Push Secret Scanner Demo](./demo.gif)

This project was created in collaboration with [Sharon Brizinov](https://github.com/SharonBrizinov). Please read [Sharon's blog post](https://trufflesecurity.com/blog/guest-post-how-i-scanned-all-of-github-s-oops-commits-for-leaked-secrets) to learn how he identified force push commits in the GH Archive dataset and made $25k in bounties.

## Quickstart (recommended)

1. Download the Force Push Commits SQLite DB (`force_push_commits.sqlite3`) via a quick Google Form submission: <https://forms.gle/344GbP6WrJ1fhW2A6>. This lets you search all force push commits for any user/org locally.

2. Install Python deps:

```bash
pip install -r requirements.txt
```
3. Scan an org/user for secrets:

```bash
python force_push_scanner.py <org> --db-file /path/to/force_push_commits.sqlite3 --scan
```

### Alternative Usage: BigQuery

If you prefer querying BigQuery yourself, you can use our public table based off the GHArchive dataset (queries are typically free with a Google account). 

```sql
SELECT *
FROM `external-truffle-security-gha.force_push_commits.pushes`
WHERE repo_org = '<ORG>';
```

Export the results as a CSV, then run the scanner:

```bash
python force_push_scanner.py <org> --events-file /path/to/force_push_commits.csv --scan
```

---

## What the script does

* Lists zero-commit **force-push events** for `<org>`.
* Prints stats for each repo.
* (Optional `--scan`) For every commit:
  * Identifies the overwritten commits.
  * Runs **TruffleHog** (`--only-verified`) on the overwritten commits.
  * Outputs verified findings with commit link.

---

## Command-line options (abridged)

Run `python force_push_scanner.py -h` for full help.

* `--db-file`     SQLite DB path (preferred)
* `--events-file` CSV export path (BigQuery)
* `--scan`        Enable TruffleHog scanning
* `--verbose`, `-v` Debug logging

---

## FAQs

### What is a Force Push?

A force push (`git push --force`) makes the remote branch pointer move to exactly where your local branch pointer is, even if it means the remote branch no longer includes commits it previously had in its history. It essentially tells the remote to forget its old history for that branch and use yours instead. Any commits that were only reachable through the remote's old history now become unreachable within the repository (sometimes called "dangling commits"). Your local Git might eventually clean these up, but remote services like GitHub often keep them around for a while longer according to their own rules. This action is often done when a developer accidentally commits data containing a mistake, like hard-coded credentials. For more details, see [Sharon's blog post](https://trufflesecurity.com/blog/guest-post-how-i-scanned-all-of-github-s-oops-commits-for-leaked-secrets) and git's documentation on [force pushes](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force).

### Does this dataset contain *all* Force Push events on GitHub?

**tl;dr:** No. This dataset focuses specifically on **Zero-Commit Force Push Events**, which we believe represent the most likely cases where secrets were accidentally pushed and then attempted to be removed.

#### Why focus only on Zero-Commit Force Pushes?

1. **Zero-Commit Force Pushes often indicate secret removal**  
   Developers who push secrets by accident frequently reset their history to a point before the mistake, then force push to remove the exposed data. These types of pushes typically show up as push events that modify the `HEAD` but contain zero commits. Our research indicates that this pattern is strongly correlated with attempts to delete sensitive content.

2. **Not all Force Pushes are detectable from GH Archive alone**  
   A force push is a low-level git operation commonly used in many workflows, including rebasing and cleaning up branches. Identifying every type of force push would require cloning each repository and inspecting its git history. This approach is not practical at the scale of GitHub and is outside the scope of this project.

#### What is an example of a Force Push that is not included?

Consider a scenario where a developer pushes a secret, then realizes the mistake and resets the branch to an earlier state. If they add new, clean commits before force pushing, the resulting `PushEvent` will include one or more commits. This example would not be captured because our dataset only includes push events with zero commits.

### What is the GHArchive?

The GH Archive is a public dataset of *all* public GitHub activity. It's a great resource for security researchers and developers to analyze and understand the security landscape of the GitHub ecosystem. It's publicly available on BigQuery, but querying the entire dataset is expensive ($170/query). We trimmed the GH Archive dataset to only include force push commits.

### Why not host the Force Push Commits DB publicly?

We gate large downloads behind a form to deter abuse; the public BigQuery dataset remains open to all.

### Dataset Updates

The SQLite3 Database and BigQuery Table are updated every day at 2 PM EST with the previous day's data. 

---

This repository is provided *as-is*; we'll review PRs when time permits.

**Disclaimer**: This tool is intended exclusively for authorized defensive security operations. Always obtain explicit permission before performing any analysis, never access or download data you're not authorized to, and any unauthorized or malicious use is strictly prohibited and at your own risk.
