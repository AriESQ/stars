# tailx

**The live system cognition engine.** Reimagines `tail` from "show me lines" to "what's happening, what matters, and why?"

```
47,000 log lines → 92 groups → 38 templates → 2 root causes → 1 diagnosis
In 3.1 seconds. Zero config.
```

## What just happened

We pointed tailx at a production web stack's logs — mixed JSON, syslog, and unstructured across multiple services. Without any configuration, rules, or prior knowledge of the system, it:

1. **Ingested** 47,000 log lines across 4 files at 15,000 events/sec
2. **Auto-detected** the log format per source — JSON for the API, syslog for the system, unstructured for legacy services
3. **Parsed** every line — extracted severity, service names, trace IDs, structured fields
4. **Fingerprinted** messages using Drain template extraction — collapsed 47,000 lines into 38 structural templates
5. **Grouped** events by template — 92 groups, ranked by severity × frequency × trend
6. **Emitted a JSON triage summary** — one structured object containing everything an AI (or human) needs to understand the system state

The result: a database connection pool exhaustion was identified as the root cause of 71% of all error volume, cascading through the API gateway → payment service → notification service. Three grouped patterns replaced 47,000 lines of noise.

**Without tailx**, that diagnosis requires: manually reading logs, mentally correlating timestamps across services, recognizing repeated patterns by eye, and understanding which log groups are related. A 30-minute task for an experienced SRE.

**With tailx**, it's one command:

```bash
tailx --json -s -n app.log api.log db.log worker.log | tail -1
```

## Install

```bash
# Build from source (requires Zig 0.14.0)
zig build -Doptimize=ReleaseSafe
cp ./zig-out/bin/tailx ~/.local/bin/

# That's it. No dependencies. No runtime. 144 KB binary.
```

## Usage

### Basic — just like tail, but smarter

```bash
tailx app.log                        # Tail with pattern grouping
tailx /var/log/*.log                 # Glob multiple files
cat app.log | tailx                  # Pipe anything in
dmesg | tailx --severity warn        # Kernel warnings and above
```

### What you see

```
ERR [payments] connection timeout to stripe
ERR [payments] connection timeout to stripe
ERR [payments] connection timeout to stripe
WRN [db] slow query on orders table
FTL [payments] circuit breaker opened
INF [api] GET /health 200

──────────────────────────────────────────────────────────────
 Pattern Summary  8 events  6 groups  6 templates  902 ev/s  8ms
──────────────────────────────────────────────────────────────
  🔥 [payments] circuit breaker opened (x1) ✨ new
  ✗ [payments] connection timeout to stripe (x3) ↑ rising
  ✗ [db] connection pool exhausted (x1) ✨ new
  ⚠ [db] slow query on orders table (x1) ✨ new
  ● [auth] user login successful (x1) ✨ new
  ● [api] GET /health 200 (x1) ✨ new
──────────────────────────────────────────────────────────────
```

Not 8 lines of text. 6 groups, ranked by what matters.

### Filters — no regex required

```bash
tailx --severity error app.log       # Only errors and above
tailx --grep timeout app.log         # Lines containing "timeout"
tailx --service payments app.log     # Only from payments service
tailx --field status=500 app.log     # Specific field values
tailx --last 5m app.log              # Only last 5 minutes
```

### Intent queries — say what you mean

```bash
tailx "errors related to payments" app.log
tailx "5xx from nginx" /var/log/nginx/*.log
tailx "why are payments failing" app.log
```

tailx decomposes natural language into structured filters. "errors" becomes `severity >= error`. "payments" becomes a message substring match. "from nginx" becomes a service filter.

### Trace reconstruction

```bash
tailx --trace app.log
```

```
TRACE req-001  4ms  FAILURE
 ├─ INF [auth] user login successful
 ├─ INF [api] GET /checkout
 ├─ WRN [db] slow query 2340ms
 └─ ERR [payments] timeout calling stripe

TRACE req-002  0ms  unknown
 ├─ INF [auth] user login successful
 └─ INF [api] GET /health
```

Events with the same `trace_id` are automatically grouped into request flows with outcome detection.

### Modes

```bash
tailx app.log                        # Pattern mode (default) — lines + summary
tailx --raw app.log                  # Classic tail — just lines
tailx --trace app.log                # Trace mode — group by trace ID
tailx --incident app.log             # Incident mode — only anomalies + top groups
tailx --json app.log                 # JSON mode — structured output for AI/tooling
```

## The AI interface

This is where tailx becomes a force multiplier. `--json` outputs structured JSONL that any AI agent can reason over:

```bash
tailx --json -s -n app.log db.log | tail -1
```

```json
{
  "type": "triage_summary",
  "stats": {
    "events": 47283,
    "groups": 92,
    "templates": 38,
    "events_per_sec": 15252.0
  },
  "top_groups": [
    {
      "exemplar": "connection pool exhausted, 0 available",
      "count": 8241,
      "severity": "ERROR",
      "trend": "rising",
      "service": "db"
    },
    {
      "exemplar": "connection timeout to downstream",
      "count": 6102,
      "severity": "ERROR",
      "trend": "rising",
      "service": "payments"
    }
  ],
  "anomalies": [
    {
      "kind": "rate_spike",
      "score": 0.87,
      "observed": 412.0,
      "expected": 85.0
    }
  ],
  "hypotheses": [
    {
      "causes": [
        { "label": "DB latency spike", "strength": 0.82, "lag_ms": 2000 }
      ],
      "confidence": 0.82
    }
  ],
  "traces": [
    {
      "trace_id": "req-001",
      "event_count": 4,
      "duration_ms": 234,
      "outcome": "failure",
      "events": [...]
    }
  ]
}
```

One object. Everything the engine computed — groups, anomalies, correlations, traces — machine-readable. An LLM reads this and immediately understands:

- What's happening (top groups by volume)
- What matters (severity-ranked, trend-aware)
- Why (correlation hypotheses with lag and confidence)
- Request flows (traces with outcomes)

### MCP / tool integration

```python
# As an MCP tool or subprocess call:
result = subprocess.run(
    ["tailx", "--json", "-s", "-n", "--last", "5m", "app.log"],
    capture_output=True
)
# Last line is always the triage summary
triage = json.loads(result.stdout.strip().split(b'\n')[-1])
```

The AI doesn't parse logs. tailx parses logs. The AI reasons over the structured triage.

## How it works

```
  Raw bytes
      │
      ▼
  ┌─────────────────┐
  │ Auto-detect      │  JSON? Logfmt? Syslog? Unstructured?
  │ format           │  Zero config. Per-source. Locks after 8 lines.
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Parse            │  Extract severity, service, message, trace_id,
  │                  │  structured fields. Arena-allocated. No heap in
  │                  │  steady state.
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Drain template   │  "Connection to 10.0.0.1 timed out after 30s"
  │ fingerprint      │  "Connection to 10.0.0.2 timed out after 45s"
  │                  │  → same template: "Connection to <*> timed out after <*>"
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Group + rank     │  Count, trend (rising/stable/falling),
  │                  │  severity escalation, multi-source tracking.
  │                  │  Top groups by recency × frequency × severity.
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Anomaly detect   │  EWMA + z-score for rate spikes/drops.
  │                  │  CUSUM for sustained shifts.
  │                  │  3σ minimum threshold. Zero false positives
  │                  │  over zero config.
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Correlate        │  Temporal proximity analysis.
  │                  │  "Error rate spiked. DB latency spiked 2s earlier.
  │                  │   Likely related (82% confidence)."
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Output           │  Terminal: colorized, grouped, ranked.
  │                  │  JSON: structured triage for AI agents.
  └─────────────────┘
```

**Statistical-first.** No LLM in the hot path. No cloud calls. No API keys. The intelligence comes from:

- Drain algorithm for template extraction
- EWMA dual-rate baselines for anomaly detection
- CUSUM for change-point detection
- HyperLogLog for cardinality estimation
- T-Digest for streaming percentiles
- Count-Min Sketch for frequency estimation
- Temporal proximity for correlation

All running at **69,000 events/sec** on a single core.

## Design principles

**Zero config to start.** Point it at a file. It works. No YAML. No rules. No training.

**Local-first.** Everything runs on your machine. No cloud. No telemetry. No network calls.

**Statistical-first.** No LLM in the core path. Math is fast, deterministic, and explainable.

**Zero dependencies.** Zig standard library only. No libc. No PCRE. No external crates.

**144 KB binary.** Fits in L2 cache. Starts in microseconds.

## The numbers

| Metric | Value |
|--------|-------|
| Binary size (stripped, ReleaseSmall) | 144 KB |
| Throughput | 69,000 events/sec |
| Memory (statistical engine) | < 1 MiB |
| Startup time | < 1ms |
| Dependencies | 0 |
| Lines of Zig | 8,347 |
| Tests | 219 |
| Config files needed | 0 |

## Building

Requires [Zig 0.14.0](https://ziglang.org/download/).

```bash
git clone https://github.com/copyleftdev/tailx.git
cd tailx
zig build test                       # Run all 219 tests
zig build -Doptimize=ReleaseSafe     # Build optimized binary
```

## License

MIT
