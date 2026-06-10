# cloudip — Cloud IP Attribution

You've got server logs full of IP addresses, and you want to know which ones are
AWS, which are Azure, which are a Cloudflare edge, and which are just some random
VPS. That's the problem cloudip solves: it's GeoIP-style attribution, but instead
of mapping IPs to *places*, it maps them to the *cloud provider* that owns them.

It works by gathering each provider's published IP ranges, normalizing them with
per-provider plugins, and baking the whole lot into a single MMDB (`DatabaseType:
Cloud-Attribution`). From there a thin reader library is wrapped by gRPC / HTTP /
CLI — and, because it's a real MMDB, the **same** file can be read directly by
nginx via `ngx_http_geoip2_module`, no custom module required. Here's how the
pieces fit together:

```
provider feeds            build time                     serve time
─────────────────         ──────────────                 ────────────────────
rezmoss repo  ─┐                                      ┌─ gRPC server
AWS json      ─┼─ plugins ─> normalized ─> mmdbwriter ─┼─ HTTP server
Azure tags    ─┤             entries        (Go)      ─┼─ CLI
GCP json      ─┘                │                      ├─ nginx (geoip2 module)
                               .mmdb  ──> CSV export ──┴─ Presto/Trino
```

How much of the cloud you cover depends on where you pull the data from. The
native `aws`/`azure`/`gcp` plugins parse each provider's own feeds when you ask
for `--source direct`. But if you want the widest net, `--source rezmoss-all`
pulls in **every** provider the rezmoss mirror tracks — about 24 of them: the
big-three clouds plus Cloudflare, Fastly, Oracle, Linode, DigitalOcean, Vultr,
GitHub, Zoom, Atlassian, and assorted bot networks.

Architecturally it's two binaries in spirit. There's a **builder**
(`cloudattr build`, built on [`mmdbwriter`](https://github.com/maxmind/mmdbwriter))
and a **reader/server** (`cloudattr serve`, on
[`maxminddb-golang/v2`](https://github.com/oschwald/maxminddb-golang)). They're
deliberately decoupled: the only things they share are the `.mmdb` file and the
record schema.

## Quick start

If you just want the data, skip the toolchain entirely: a fresh `cloud.mmdb`
(all ~24 rezmoss providers, enriched with origin ASNs) and a standalone
`asn.mmdb` (every routed range) are published daily to the rolling
[`mmdb-latest` release](https://github.com/ChrisLundquist/cloudip/releases/tag/mmdb-latest),
alongside a gzipped CSV and SHA-256 checksums:

```sh
curl -LO https://github.com/ChrisLundquist/cloudip/releases/download/mmdb-latest/cloud.mmdb
```

Otherwise, build the binary and point it at whichever data source suits you. The
most common path is the rezmoss CC0 mirror, but you can hit the providers' own
URLs or work entirely offline from local fixtures:

```sh
go build -o cloudattr ./cmd/cloudattr

# Build from the rezmoss CC0 mirror (default), or from provider URLs / fixtures:
./cloudattr build --source rezmoss     --out cloud.mmdb --csv cloud.csv  # aws/azure/gcp plugins
./cloudattr build --source rezmoss-all --out cloud.mmdb                  # ALL ~24 rezmoss providers
./cloudattr build --source direct      --out cloud.mmdb                  # hit AWS/Azure/GCP URLs
./cloudattr build --fixtures ./feeds   --out cloud.mmdb                  # offline, from local files

# --source rezmoss-all consumes the unified all_providers.json: aws, azure,
# googlecloud, cloudflare, fastly, oracle, linode, digitalocean, vultr, github,
# zoom, atlassian, and bot networks (~400k networks). Subset with --providers:
./cloudattr build --source rezmoss-all --providers aws,cloudflare,fastly --out edge.mmdb
```

Once you've got a database, querying it is the easy part — single IPs, batches
from a file or stdin, plus a couple of housekeeping commands:

```sh
# Query
./cloudattr lookup 52.94.0.1                      # single
./cloudattr lookup -f ips.txt --format json       # batch from file (or '-' for stdin)
./cloudattr verify --in cloud.mmdb                # walk + sanity counts
./cloudattr export --in cloud.mmdb --out cloud.csv

# Serve gRPC + HTTP (SIGHUP reloads an atomically-replaced file in place)
./cloudattr serve --in cloud.mmdb --http :8080 --grpc :9090
```

The HTTP surface is small and predictable — a full-record lookup, a fast
identity-only lookup, a batch variant, plus the usual operational trio:

```
GET /v1/lookup/{ip}        -> 200 {record} | 404 | 400
GET /v1/provider/{ip}      -> 200 {provider,region} | 404      # fast path
GET /v1/lookup?ip=&ip=     -> 200 [{ip,found,record}, ...]     # batch
GET /healthz  GET /metrics  GET /version
```

## Performance

The reader is fast: a membership check (`Contains`) is an allocation-free
search-tree traversal, and identity lookups (`LookupProvider` / `/v1/provider`)
run at **~50 ns with zero allocations** once the in-memory index is built
(`serve --index`). In a head-to-head on the same real cloud IPs, this matches or
beats [`rezmoss/go-cloudip`](https://github.com/rezmoss/go-cloudip) — **1.9× faster
on membership, 1.5× faster on provider lookup** — while carrying 24× more data and
keeping the database on disk (mmap'd, shareable, nginx-readable) rather than
duplicated on every process's heap. Full numbers and methodology in
[`BENCHMARKS.md`](BENCHMARKS.md); reproduce with `cd bench && go test -bench .`.

## Reputation feeds

Beyond "which cloud owns this IP", cloudip can also build a parallel database of
IP *reputation* — is this address a known botnet C2, a Tor exit, a hijacked
netblock? It reuses the exact same machinery (build, reader, servers, CSV), just
with a different set of plugins and a `categories` field instead of `services`:

```sh
./cloudattr build --reputation --out reputation.mmdb        # all reputation feeds
./cloudattr build --reputation --providers tor --out tor.mmdb
./cloudattr build --with-reputation --out cloud.mmdb        # ONE db: cloud + categories
./cloudattr lookup --in reputation.mmdb 171.25.193.25       # -> tor  anonymizer,tor_exit
```

Three feeds ship today, all free and bulk-downloadable:

| plugin | feed | categories | license |
|---|---|---|---|
| `feodo` | abuse.ch Feodo Tracker (botnet C2) | `botnet_c2`, `malware` | CC0 |
| `spamhaus` | Spamhaus DROP (hijacked netblocks) | `drop`, `hijacked` | free, attribution required |
| `tor` | Tor Project bulk exit list | `tor_exit`, `anonymizer` | open |

Because `categories` union *across* providers (unlike `services`), `--with-reputation`
builds cloud and reputation into one database, and a single lookup tells you
both — e.g. "AWS us-east-1, and also a known Tor exit". The builder inserts the
cloud feeds first, which matters: a reputation `/32` nested inside a cloud range
then *enriches* that record's categories rather than replacing its identity, and
the rest of the cloud range is untouched. Most reputation entries are single
hosts (`/32`); Spamhaus DROP contributes CIDR netblocks. Everything else about
the record schema is identical. Prefer two files (they go stale on very
different cadences)? nginx loads both happily — the geoip2 module accepts
multiple database blocks (see
[`deploy/nginx-geoip2.conf`](deploy/nginx-geoip2.conf)).

Reputation data goes stale fast — a decommissioned C2 or exit node is a false
positive waiting to happen — so per-entry `synced_at` tracks freshness where the
feed provides it (Feodo uses `last_online`), and `cloudattr verify` reports the
oldest/newest entry age so you can alert when a feed stops updating.

## ASN — which AS actually announces it

Provider feeds tell you who *claims* a range; BGP tells you who *announces* it,
and the two disagree in interesting places — most of AWS announces as AS16509
(AMAZON-02), but legacy us-east-1 space still announces as AS14618 (AMAZON-AES)
or AS7224 (Amazon.com), and GovCloud as AS8987, sometimes carving up a single
published CIDR. The data comes from [iptoasn.com](https://iptoasn.com) (public
domain, BGP-derived from RouteViews, refreshed hourly), and there are two ways
to use it:

```sh
./cloudattr build --asn --out asn.mmdb     # standalone: full IP->origin-AS DB (~700k networks)
./cloudattr build --with-asn               # enrich: stamp ext.asn/ext.as_org into cloud records
```

`--with-asn` splits entries at announcement boundaries, so a single AWS /22 can
come out as "52.94.8.0/23 → AS8987 GovCloud" next to "52.94.10.0/23 → AS16509":

```sh
$ ./cloudattr lookup --format json 3.2.64.1
# -> provider=aws region=us-east-1 ext={"asn":"14618","as_org":"AMAZON-AES",...}
```

Because the ASN lands in `ext` (stored strings), **nginx can read it** — unlike
the lookup-time `network` field, this one survives into the record leaves:
`$cloud_asn ext asn;` in the geoip2 block. The standalone `asn.mmdb` works as
yet another `geoip2` block, attributing *every* routed IP, cloud or not. An
unannounced piece of a published range simply carries no `asn` key, and a
cloud-claimed range announced by an unexpected ASN is worth alerting on — the
enrichment doubles as feed-vs-routing cross-validation.

## Record schema

Every network resolves to a **stable core** — the fields you can rely on being
there and querying uniformly across providers — alongside a provider-namespaced
`ext` map for the bits that are specific to one provider. In the MMDB it's stored
like this:

| key | type | notes |
|---|---|---|
| `provider` | utf8 | which plugin produced this (`aws`/`azure`/`gcp`) |
| `region` | utf8 | `""` when the provider gives none |
| `services` | array<utf8> | **unions** on overlapping prefixes (see below) |
| `categories` | array<utf8> | reputation tags (`tor_exit`, `drop`, …); unions across providers; omitted when empty |
| `ipv6` | boolean | derived from the network at build time |
| `source` | utf8 | provenance ref |
| `synced_at` | uint64 | unix epoch of the feed |
| `ext` | map<utf8,utf8> | provider-specific keys; strings so nginx can read them |

Lookups (Go API, HTTP, gRPC, CLI) additionally return a `network` field — the
matched range in CIDR form. It is **derived from the search tree at lookup time,
never stored in a record**: a stored network would go stale whenever an
overlapping insert splits a range, and would defeat the MMDB's record
deduplication. Two consequences: it can be *narrower* than the CIDR the provider
published (the tree fragments ranges that overlap — same semantics as MaxMind's
own `network` field), and nginx can't see it, since the geoip2 module only maps
stored record leaves to variables (exposing it there would mean patching the
module itself).

One detail worth calling out: **`services` is an array, not a scalar.** AWS lists
the same CIDR once per owning service, so rather than have the last write win, the
builder's merge inserter unions them — which is why `52.94.0.0/22` comes out as
`["AMAZON","EC2","S3"]`. For similar reasons `ext` stays `map<string,string>`:
nginx can only reach string leaves, and keeping everything as strings means it and
every other consumer see exactly the same shape.

## Adding a provider plugin

Adding a provider is meant to be a small, well-contained job. You implement
`attribution.Plugin` — `Name()`, `Refs()`, and a pure `Parse(ref, r)` that yields
normalized entries — and register it in `init()`. The builder owns all the messy
IO (rezmoss vs. direct, retries, caching), which keeps `Parse` a pure function
over bytes that's trivial to unit-test against a checked-in fixture. If your
provider has a stable direct URL you can also implement `DirectPlugin.DirectRefs()`
to support `--source direct`; the ones that don't (Azure) fall back to rezmoss
automatically. `plugins/aws/aws.go` is the worked example to copy from.

## nginx — no custom module

This is the part that's genuinely nice: there's nothing to build. Point the
existing `ngx_http_geoip2_module` at the very same `.mmdb` file and the record
keys show up as nginx variables. See
[`deploy/nginx-geoip2.conf`](deploy/nginx-geoip2.conf).

### Testing it with PROXY protocol

If you're terminating connections behind a load balancer, you'll want to attribute
the *real* client IP rather than the TCP peer. Here's a self-contained config that
pulls the client IP out of a PROXY-protocol header, attributes it, and writes the
result into both the log line and the response — handy for verifying the MMDB
end-to-end behind a real LB:

```nginx
load_module modules/ngx_http_geoip2_module.so;   # only if built as a dynamic module
events {}
http {
    geoip2 /path/to/cloud.mmdb {
        auto_reload 5m;
        # Look up the IP the upstream LB put in the PROXY header, not the TCP peer.
        $cloud_provider source=$proxy_protocol_addr provider;
        $cloud_region   source=$proxy_protocol_addr region;
        $cloud_service  source=$proxy_protocol_addr services 0;
    }

    map $cloud_provider $is_cloud { default 0; ~. 1; }

    log_format cloud '$proxy_protocol_addr cloud=$cloud_provider/$cloud_region '
                     'svc=$cloud_service is_cloud=$is_cloud "$request"';

    server {
        listen 8080 proxy_protocol;          # expect a PROXY v1/v2 header
        access_log /dev/stdout cloud;
        location = /whoami {
            default_type text/plain;
            return 200 '$cloud_provider $cloud_region $cloud_service\n';
        }
    }
}
```

Then drive it with curl, spoofing a cloud client IP in the PROXY header:

```sh
curl --haproxy-protocol --haproxy-clientip 52.94.0.1 http://127.0.0.1:8080/whoami
# -> aws us-east-1 AMAZON
```

And if you'd rather not wire that up by hand, `internal/nginxtest` automates
exactly this flow (and skips cleanly when nginx, the geoip2 module, or curl's
`--haproxy-clientip` aren't available):

```sh
go test ./internal/nginxtest/ -v
```

## Presto/Trino

For warehouse-side joins, `cloudattr export` emits both the human-readable CIDR
and integer range bounds — range joins on integers are the fastest pattern in
Presto/Trino, so that's what you'll usually join on:

```sql
SELECT e.*, c.provider, c.region
FROM events e
JOIN cloud_ranges c ON e.ip_int BETWEEN c.start_ip_int AND c.end_ip_int;
```

A sizing note: IPv4 bounds fit a `BIGINT`, but IPv6 bounds are full 128-bit
decimals, so reach for `DECIMAL`/`VARBINARY`, or split them hi/lo warehouse-side.

## Sync pipeline (ops)

Builds are designed to be safe to run on a cron without babysitting them.
`cloudattr build` is atomic: it writes `cloud.mmdb.tmp-*` in the target directory,
walks it to validate, refuses to publish if the network count drops more than
`--max-drop` (default 50%) versus the existing file, then renames into place.
Servers pick the new file up via SIGHUP (`cloudattr serve`) or nginx
`auto_reload`. The build epoch is stamped into MMDB metadata so `/version` and the
warehouse partition always agree on which build they're looking at.

## Deployment

The repo ships the operational glue so you don't have to invent it:

- **Docker** — a multi-stage [`Dockerfile`](Dockerfile) builds a static binary onto
  a distroless base, and [`docker-compose.yml`](docker-compose.yml) wires a
  build-once / serve / refresh-and-`HUP` flow.
- **systemd** — [`deploy/systemd/`](deploy/systemd) has a hardened `serve` unit
  (with `ExecReload` → SIGHUP hot-swap) plus a `build` oneshot + daily timer that
  rebuilds and reloads. [`deploy/cron.example`](deploy/cron.example) is the cron
  equivalent.
- **CI** — [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs gofmt, vet,
  `go test -race`, the build, and a Docker build on every push/PR.

A few flags matter for running this unattended:

- **`--keep-going`** (default on) isolates per-feed failures: if one provider's
  feed times out, the others still build and the run is flagged `DEGRADED` rather
  than failing wholesale. The drop/skip guards still refuse a build that lost too
  much. Set `--keep-going=false` for strict all-or-nothing.
- **`--pins pins.json` / `--print-digests`** verify the SHA-256 of each fetched
  feed against pinned digests, so a compromised or hijacked mirror can't silently
  inject networks. Generate the file with `--print-digests`, then pin it. (Pair
  with `--keep-going=false` if you want a tampered feed to hard-fail the build.)
- **`CLOUDIP_REZMOSS_BASE`** points the rezmoss source at an internal mirror or an
  air-gapped HTTP cache without forking.

## Operational robustness (partial / corrupt data)

A lot of care went into making the pipeline survive the ugly cases — disk-full,
crashes, half-finished copies. The guarantees, in detail:

- **Atomic builds.** `cloudattr build` writes a temp file in the target
  directory, walks it to verify every record decodes, refuses to publish if the
  network count dropped more than `--max-drop`, **fsyncs**, then atomically
  renames into place (and fsyncs the directory). A disk-full or mid-build error
  surfaces before the rename and leaves the previous database untouched — never a
  truncated `cloud.mmdb`. CSV export is atomic the same way.
- **Fail-closed sync.** Any fetch/parse error aborts the whole build (no
  partial publish); the previous `cloud.mmdb` keeps serving and the next cron run
  retries. `--max-drop` (default 0.5) refuses a build that shrank too much vs the
  existing file; `--max-skip` (default 0.25) refuses one where too large a
  fraction of entries were skipped (malformed/aliased) even on a first build.
  Transient HTTP failures (network/5xx/429/408) are retried with backoff before
  giving up.
- **Validated loads.** `OpenValidated` (used by the server) rejects a file that
  isn't a non-empty `Cloud-Attribution` database, so a truncated or garbage file
  (e.g. an interrupted `scp`) is refused rather than served. A failed `Reload`
  keeps the currently-loaded good database serving.
- **⚠️ Deploy via atomic rename, never in-place overwrite.** The reader mmaps the
  file. Replacing it in place (`rsync --inplace`, `cp` over it) corrupts the
  running reader's memory. Always write to a temp file on the destination and
  `mv`/`rename` it into place (and `nginx auto_reload` / `SIGHUP` will pick it
  up). `cloudattr build` already does this locally.

## Implementation notes (resolved design open questions)

A few decisions that came up along the way, and where they landed:

- **Reader version:** pinned to `maxminddb-golang/v2` (the `Lookup(ip).Decode()` API).
- **`ext` typing:** stored as `map<string,string>` so nginx can reach every leaf;
  empty values are dropped at build time.
- **Cross-provider conflicts:** `services` and `ext` union on overlapping prefixes;
  `provider`/`region` keep the first writer (build order is deterministic — plugins
  sorted by name). `provider` is still scalar; revisit if CDNs/BYOIP make multi-provider
  ownership common.
- **rezmoss reality:** the CC0 mirror does **not** republish the raw provider files —
  it normalizes every provider to a uniform `{ip_address, ip_type, service, region}`
  schema at `<provider>/<provider>_ips.json` (GCP is filed under `googlecloud/`). So
  `--source rezmoss` uses a single shared decoder (`ParseRezmoss`), while `--source
  direct` uses each plugin's native parser against the provider's own URL. The mirror
  carries no per-entry timestamp, so rezmoss-built records have `synced_at=0`; the
  build epoch is still stamped in MMDB metadata. Providers without a stable direct URL
  (Azure) fall back to rezmoss automatically.

## Licensing

One naming thing to be aware of: the MMDB `DatabaseType` is `Cloud-Attribution`,
**not** `GeoIP*` — that prefix is reserved and a MaxMind trademark. On the
dependency side, `mmdbwriter` is Apache-2.0/MIT and `maxminddb-golang` is ISC. The
rezmoss mirror itself is CC0, but keep in mind the upstream providers' own terms
still apply to the underlying data.

The reputation feeds have their own terms: abuse.ch Feodo Tracker is CC0, the Tor
exit list is published openly, and **Spamhaus DROP is free to use (including
commercially) provided you name Spamhaus as the source** — see
<https://www.spamhaus.org/drop/terms/>. cloudip honors that by tagging every DROP
record `provider=spamhaus` with its `source`; if you redistribute the DROP data
itself, retain Spamhaus's attribution and header.
