Copyright (c) 2020 to date, Binare Oy (license@binare.io) All rights reserved.

FastCVE - fast, rich and API-based search for CVE and more (CPE, CWE, CAPEC)
==================

`fastcve` is a command-line tool that allows you to search for vulnerabilities in the Common Vulnerabilities and Exposures (CVE) database. The tool provides an easy way to search for vulnerabilities and retrieve relevant information about them, including their descriptions, CVSS scores, and references to related security advisories.

`fastcve` is designed to be fast, lightweight, and easy to use. It provides a simple interface for querying the CVE database, allowing you to search for vulnerabilities based on vendors, products, and other criteria. The tool can be used by security professionals, system administrators, and developers to stay informed about known security vulnerabilities and to assess the risk of their systems and applications.

Overall, `fastcve` is a useful tool for anyone who is interested in keeping up-to-date with the latest information about security vulnerabilities and how they can be addressed.

Technical details
-----------------

Some key technical characteristics of `fastcve`:

1. **Docker containerization**: Runs as a Docker Compose stack with two services: `fastcve` (API + CLI) and `fastcve-db` (PostgreSQL).

2. **Automatically creates the DB on first start**: PostgreSQL creates the initial database (`POSTGRES_DB`) when the DB volume is empty.

3. **Automatically creates and upgrades the DB schema if needed**: The schema is created/updated automatically on app start and before CLI commands run.

4. **Capability to populate the DB using external sources**: The `load` command can populate the DB from NVD (CVE/CPE via NVD 2.0 APIs) and additional sources (MITRE CWE/CAPEC, EPSS, CISA KEV).

5. **Incremental updates**: Re-running `load` fetches only changes since the last successful update (NVD increments are limited to `fetch.max.days.period`, default 120 days).

The tool is a comprehensive solution for managing a local vulnerability database and querying it via CLI and HTTP API.

It is optimized to handle many queries efficiently, and to keep vulnerability data up to date via incremental updates.


Build
----------


To build the application image:
```bash
docker compose build fastcve
```

This builds `${FASTCVE_DOCKER_IMG}:${FASTCVE_DOCKER_TAG}` (application / API / CLI). The default values are in `.env`.

The DB container uses an upstream PostgreSQL image (defaults to `postgres:16-alpine3.19`, configurable via `FASTCVE_DB_IMAGE`) and is not built from this repo.

If you need a custom tag, set `FASTCVE_DOCKER_TAG=<your_tag>` to generate `${FASTCVE_DOCKER_IMG}:<your_tag>`.


Migration (single-container -> split DB/app)
--------------------------------------------

Previous versions (-> v1.2.3) ran the PostgreSQL DB and the FastCVE API/CLI in the same `fastcve` container. The current `docker-compose.yml` splits this into two services: `fastcve-db` (PostgreSQL) and `fastcve` (API/CLI).

To migrate an existing deployment:

1. Stop the old container/stack **without deleting the DB volume**:
   ```
   docker compose down
   ```

2. Update your environment variables / `.env` for the new compose file:
   - Keep `FCDB_USER` and `FCDB_PASS` the same as before (so the existing DB user credentials still match).
   - `FCDB_USER`/`FCDB_PASS` are used for both:
     - the app connection (`postgresql://${FCDB_USER}:${FCDB_PASS}@...`), and
     - PostgreSQL initialization (`POSTGRES_USER`/`POSTGRES_PASSWORD`) when the DB volume is empty.
   - For Docker Compose deployments, set `INP_ENV_NAME=dev` (the default). (`setenv_dev.ini` points to the in-stack DB hostname `fastcve-db`.)
   - (Optional) Set `FASTCVE_DB_IMAGE` if you need a different PostgreSQL image/tag.

3. If you previously bind-mounted `/fastcve/config/setenv` from the host, ensure the *mounted* `setenv_${INP_ENV_NAME}.ini` matches the new split:
   - `FCDB_HOST=fastcve-db`
   - `FCDB_PORT=5432`

4. Start the new split stack:
   ```
   docker compose up -d
   ```

Notes:
- The DB data is still kept in the Docker volume `vol_fastcve_db`. Do not use `docker compose down -v` unless you intentionally want to wipe the DB.
- If your existing `vol_fastcve_db` was created by an older PostgreSQL *major* version, you must do a `pg_dump`/restore (PostgreSQL data directories are not forward-compatible across major versions).
- DB admin commands that used to run in `fastcve` now run in `fastcve-db` (example: `docker compose exec fastcve-db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"`).
- If you change `FCDB_PASS` for an already-initialized `vol_fastcve_db`, PostgreSQL will *not* automatically update the user password; you must run `ALTER USER ... PASSWORD ...` (or recreate the volume).


First Run
---------

Docker Compose reads `.env` automatically. The defaults in this repo are enough to start a local stack.

Create a local folder for the `/backup` bind-mount used by `fastcve-db` (Linux):
```bash
mkdir -p backup && chmod 1777 backup
```

If you want to override them, set variables in your shell or edit `.env`:
```bash
export INP_ENV_NAME=dev
export FCDB_USER=fastcve_db_user
export FCDB_PASS=fastcve_db_pass
export FASTCVE_DOCKER_IMG=binare/fastcve
export FASTCVE_DOCKER_TAG=latest
```

To start the stack:
```bash
docker compose up -d --build
```

Troubleshooting
---------------

- `password authentication failed for user ...`: the DB is stored in `vol_fastcve_db`, so if the volume was initialized with different credentials you must reset it with `docker compose down -v` (or manually `ALTER USER` inside Postgres).

Configuration parameters
------------------------

The application container contains the configuration under `/fastcve/config`:
- `/fastcve/config/setenv/config.ini` - main config (DB DSN, fetch URLs, sync settings, etc.)
- `/fastcve/config/setenv/setenv_${INP_ENV_NAME}.ini` - env-specific settings loaded by `/fastcve/config/setenv.sh`

In this repo, those files are located under `src/config` and are copied into the image during build.

For easier local edits, you can bind-mount config into the `fastcve` container (example):
```yaml
volumes:
  - ./src/config/setenv:/fastcve/config/setenv
  - ./src/config/setenv.sh:/fastcve/config/setenv.sh
```

For Docker Compose deployments, ensure `setenv_${INP_ENV_NAME}.ini` points to `FCDB_HOST=fastcve-db` and `FCDB_PORT=5432` (this is already true for `dev` and `prod` in this repo).

How To
------


- **Backup the DB (pg_dump, compact)**:
> Important:
> The dump is written inside the DB container to `/backup` (bind-mounted from the host via `docker-compose.yml`).
> Ensure the host `./backup` directory exists and is writable (Linux):
> `mkdir -p backup && chmod 1777 backup`

```bash
docker compose exec -T fastcve-db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -Z 9 -f "/backup/fastcve_vuln_db_$(date +%F).dump"'
```

Restore:
```bash
docker compose exec -T fastcve-db sh -c 'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists "/backup/fastcve_vuln_db_YYYY-MM-DD.dump"'
```

- **Populate the DB for the first time (CVE/CVE history/CPE/CWE/CAPEC/EPSS/KEV)**:
```bash
docker compose exec fastcve load --data cve cvehist cpe cwe capec epss kev
```

- **Update CVE/CVE history/CPE incrementally (and refresh EPSS/KEV)**:
```bash
docker compose exec fastcve load --data cve cvehist cpe epss kev
```

This fetches changes since the last successful update (for CVE/CVE history/CPE), with an upper limit of `fetch.max.days.period` (default 120 days) enforced by the loader.

If there is a need to repopulate the DB for the CWE/CAPEC info, then `--full` and `--drop` options are available for the load command. `--full` ignores the fact the data is already present and `--drop` drops existing data before loading. When using `--data epss` in combination with `--epss-now`, the loader fetches EPSS data for the current date; otherwise it defaults to the previous day.

- search for the data: **get the CVEs details (JSON) for a list of CVE-IDs**
```
docker compose exec fastcve search --search-info cve --cve CVE-YEAR-ID1 CVE-YEAR-ID2
```

- search for the data: **search CVEs by the summary text**
```
docker compose exec fastcve search --search-info cve --keyword '(buffer overflow|memory corruption).*before.*2\.1[0-9]'
```
Above will search CVE text and return details for CVEs that match the given keyword(s). Multiple `--keyword` values are treated as an AND condition. Each keyword can be a regular expression.

- search for the data: **get the CVEs IDs for a specific CPE**
```
docker compose exec fastcve search --search-info cve --cpe23 cpe:2.3:*:*:linux_kernel:2.6.32: --output id
```

Above will return the list of CVE-IDs that are related to the `linux_kernel` product for version 2.6.32.

To get the CVE details, request the output in JSON format: `--output json`.

To get only those CVEs that were modified in the last `n` days, add the option `--days-back n` i.e. `--days-back 10` - only created/modified in the last **10** days

Additional filters are available for CVE search:
```
--cvss-severity-v2 {low, medium, high}   # retrieve only those CVEs that has the severity as per CVSS score Version 2
--cvss-severity-v3 {low, medium, high, critical} # retrieve only those CVEs that has the severity as per CVSS score Version 3.x
--cvss-metrics-v2 CvssVector # CVSS V2.0 vector string to search for (default: None)
--cvss-metrics-v3 CvssVector # CVSS V3.x vector string to search for (default: None)
--cwe CWE [CWE ...]     # retrieve only those CVEs that are related to the specified list of CWE IDs
--pub-start-date    # retrieve only those CVEs that are published after the start date
--pub-end-date      # retrieve only those CVEs that are published before the end date
--last-mod-start-date # retrieve only those CVEs that are last modified after the start date
--last-mod-end-date   # retrieve only those CVEs that are last modified before the end date
```

- search for the data: **get CVE history rows for a CVE or change pattern**
```
docker compose exec fastcve search --search-info cvehist --cve CVE-2024-3094 --change-event 'Initial Analysis' --output json
```

Above will return the matching CVE history change records. `cvehist` supports filtering by CVE ID, change date range, `--change-event`, and `--change-type`.

- search for the data: **get the valid list of CPE names for a query on part/vendor/product/version etc**.

```
docker compose exec fastcve search --search-info cpe --cpe23 cpe:2.3:h:*:dl*:*: --output id
```

Above will search for all valid existing CPE 2.3 names that are of hardware type, for any vendor, product starts with `dl`*, and version is any

To see for the other options available for both `load` and `search` commands run these with `-h` option

```
docker compose exec fastcve search -h
docker compose exec fastcve load -h
```

The same search capabilities are exposed through the API (FastAPI). The API is exposed through port 8000 by default and can be changed in `docker-compose.yml`.

The following endpoints are exposed through HTTP requests
```
/status - DB status
/api/search/cve - search for CVE data
/api/search/cvehist - search for CVE history data
/api/search/cpe - search for CPE data
/api/search/cwe - search for CWE data
/api/search/capec - search for CAPEC data
```

OpenAPI docs:
```
http://localhost:8000/docs
```

Alternative docs view:
```
http://localhost:8000/redoc
```

Screenshots
============================
Example status API

![Screenshot example1](./docs/assets/api_status.png "Example 1")

Example search CVE API

![Screenshot example2](./docs/assets/api_cve.png "Example 2")

API documentation

![ScreenShot example3](./docs/assets/api_redoc.png "Example 3")

License
============================
This software is released under the BSD 3-Clause License

See the [LICENSE](./LICENSE.md) file

Authors
============================
See the [AUTHORS](./AUTHORS.md) file

Copyright
============================
Binare Oy (binare.io) © IoT Firmware Cybersecurity, 2020.

See the [COPYRIGHT](./COPYRIGHT.md) file
