# terraform-infra-reconcilers

> *"Reconciling the world not as it is, but as it should be."* — Matt Moore, CTO

Terraform modules for deploying reconciliation systems on Google Cloud Platform using the [DriftlessAF](https://github.com/driftlessaf/go-driftlessaf) framework.

## What is a Reconciler?

A **reconciler** implements a continuous feedback loop that makes systems self-healing and resilient. Adapted from Kubernetes controllers, the pattern is deceptively simple:

1. **Watch**: Observe the current state of the world
2. **Compare**: Compute the delta between desired and actual state
3. **Act**: Make changes to close the gap
4. **Repeat**: Forever

### Level-Based vs Event-Driven

Traditional event-driven systems are fragile: lost events mean lost actions, crashed services leave work incomplete, and state drifts over time. They're *edge-triggered*, reacting to moments of change without remembering the desired end state.

Reconciliation systems are **level-based**. The workqueue holds *keys*, not events—multiple events about the same resource collapse into a single reconciliation of its current state. Events are just hints to check state; the reconciler compares actual to desired and takes idempotent actions that are safe to repeat. This makes the system naturally resilient to event storms, duplicate notifications, and processing delays.

## Architecture Overview

```
                                    ┌────────────────────────────────────────────────────────┐
                                    │                    WORKQUEUE                           │
┌──────────────┐                    │  ┌─────────────┐    ┌─────────┐    ┌──────────────┐    │
│   Triggers   │                    │  │  Receiver   │───▶│   GCS   │───▶│  Dispatcher  │    │
│              │   enqueue keys     │  │  (Cloud Run)│    │ Bucket  │    │  (Cloud Run) │    │
│ • Cron Jobs  │───────────────────▶│  └─────────────┘    └─────────┘    └──────┬───────┘    │
│ • CloudEvents│                    │                                           │            │
│ • GitHub     │                    └───────────────────────────────────────────┼────────────┘
│   Webhooks   │                                                                │
└──────────────┘                                                                │ dispatch
                                                                                ▼
                                                                    ┌────────────────────┐
                                                                    │     Reconciler     │
                                                                    │    (Cloud Run)     │
                                                                    │                    │
                                                                    │  Your Go code that │
                                                                    │  processes each key│
                                                                    └────────────────────┘
```

### How It Works

1. **Triggers** (cron jobs, CloudEvents, GitHub webhooks) enqueue keys to the workqueue
2. **Receiver** accepts keys via gRPC and stores them in a GCS bucket
3. **Dispatcher** polls the bucket, dispatches keys to your reconciler with concurrency control
4. **Reconciler** (your code) processes each key and can requeue with delays on failure
5. **Dead Letter Queue** captures keys that exceed retry limits for manual inspection

### Key Properties

- **Deduplication by key**: Multiple events for the same resource (e.g., PR URL) collapse into one reconciliation
- **Key exclusion guarantee**: The same key is never processed concurrently across instances
- **Idempotent actions**: Reconcilers are safe to run repeatedly on the same key
- **Automatic retry**: Failed items are requeued with exponential backoff

## Reconciliation Patterns

This module supports two primary reconciliation patterns:

| Pattern | Key Type | Trigger | Use Cases |
|---------|----------|---------|-----------|
| **PR Reconciler** | PR URL (`github.com/org/repo/pull/123`) | CloudEvents from GitHub webhooks | PR validation, policy checks, automated fixes |
| **Path-Based Reconciler** | File path (`github.com/org/repo/blob/main/config.yaml`) | Push events + periodic resync | Config sync, GitOps, file monitoring |

## Modules

The table below highlights core modules. See [MODULES.md](./MODULES.md) for the complete catalog with descriptions and selection guidance.

| Module | Description | Pattern |
|--------|-------------|---------|
| [`regional-go-reconciler`](./modules/regional-go-reconciler/) | Complete reconciler with workqueue + regional Go service | PR Reconciler |
| [`cloudevents-workqueue`](./modules/cloudevents-workqueue/) | Bridge CloudEvents to workqueue based on event extensions | PR Reconciler |
| [`github-path-reconciler`](./modules/github-path-reconciler/) | File path reconciliation with push events + periodic resync | Path-Based |
| [`workqueue`](./modules/workqueue/) | Core workqueue infrastructure (receiver, dispatcher, GCS bucket) | Both |
| [`dashboard/workqueue`](./modules/dashboard/workqueue/) | Cloud Monitoring dashboard for workqueue metrics | Both |
| [`dashboard/reconciler`](./modules/dashboard/reconciler/) | Cloud Monitoring dashboard for reconciler services | Both |

## Getting Started

### Prerequisites

- GCP project with Cloud Run, Cloud Storage, and Pub/Sub APIs enabled
- Terraform >= 1.0
- Go 1.21+ for writing reconciler code

### Quick Start: Regional Go Reconciler

The `regional-go-reconciler` module is the easiest way to deploy a complete reconciler:

```hcl
module "my-reconciler" {
  source  = "driftlessaf/reconcilers/infra//modules/regional-go-reconciler"
  version = "~> 1.0"

  project_id = var.project_id
  name       = "my-reconciler"
  regions    = var.regions
  team       = "platform"

  service_account = google_service_account.reconciler.email

  # Build reconciler from source using ko
  containers = {
    "reconciler" = {
      source = {
        working_dir = path.module
        importpath  = "./cmd/reconciler"
      }
      ports = [{ container_port = 8080 }]
    }
  }

  # Workqueue configuration
  concurrent-work = 20  # Process 20 keys concurrently
  max-retry       = 100 # Move to DLQ after 100 failures

  notification_channels = var.notification_channels
}
```

### Implementing the Reconciler (Go)

Your reconciler implements the workqueue gRPC service. The key principle is **idempotent, level-based reconciliation**:

```go
package main

import (
    "context"
    "log"
    "net"
    "os"

    "github.com/driftlessaf/go-driftlessaf/workqueue"
    "github.com/driftlessaf/go-driftlessaf/reconcilers/githubreconciler"
    "google.golang.org/grpc"
)

type Reconciler struct {
    workqueue.UnimplementedWorkqueueServiceServer
    statusManager *statusmanager.StatusManager
}

func (r *Reconciler) Process(ctx context.Context, req *workqueue.ProcessRequest) (*workqueue.ProcessResponse, error) {
    // 1. Parse the key (e.g., PR URL)
    res, err := githubreconciler.ParseResource(req.Key)
    if err != nil {
        return nil, err
    }

    // 2. Fetch current state (cheap API call)
    pr, _, err := gh.PullRequests.Get(ctx, res.Owner, res.Repo, res.Number)
    if err != nil {
        return nil, err
    }
    sha := pr.GetHead().GetSHA()

    // 3. Check observed generation (idempotency)
    session := r.statusManager.NewSession(gh, res, sha)
    status, _ := session.ObservedState(ctx)
    if status != nil && status.Status == "completed" {
        return &workqueue.ProcessResponse{}, nil  // Already processed this SHA
    }

    // 4. Only now fetch expensive data (diff, file contents, etc.)
    // 5. Compute desired state
    // 6. Take action to align actual with desired

    return &workqueue.ProcessResponse{}, nil
}

func main() {
    lis, _ := net.Listen("tcp", ":"+os.Getenv("PORT"))
    srv := grpc.NewServer()
    workqueue.RegisterWorkqueueServiceServer(srv, &Reconciler{})
    log.Fatal(srv.Serve(lis))
}
```

**Key properties:**
- **Idempotent**: Running twice on the same SHA does nothing
- **Level-based**: Checks entire resource state, not just the triggering event
- **Lazy evaluation**: Expensive operations only when reconciliation is needed

### Enqueuing Work

Services can enqueue work to your reconciler:

```go
client, err := workqueue.NewWorkqueueClient(ctx, os.Getenv("WORKQUEUE_SERVICE"))
if err != nil {
    return err
}
defer client.Close()

// Enqueue a key for processing
_, err = client.Process(ctx, &workqueue.ProcessRequest{
    Key: "resource-id-123",
})
```

## Common Patterns

### GitHub Path Reconciler

Reconcile files in a GitHub repository when they change:

```hcl
module "config-sync" {
  source  = "driftlessaf/reconcilers/infra//modules/github-path-reconciler"
  version = "~> 1.0"

  project_id     = var.project_id
  name           = "config-sync"
  regions        = var.regions
  primary-region = "us-central1"
  team           = "platform"

  # Repository to watch
  github_owner      = "my-org"
  github_repo       = "config-repo"
  octo_sts_identity = "config-sync"

  # Match YAML files in the configs directory
  path_patterns = ["(configs/.+\\.yaml)"]

  # Resync all files every 6 hours
  resync_period_hours = 6

  # CloudEvents broker for push notifications
  broker = var.github_events_broker

  service_account       = google_service_account.reconciler.email
  containers            = { /* ... */ }
  notification_channels = var.notification_channels
}
```

### CloudEvents to Workqueue

Process GitHub pull requests via CloudEvents:

```hcl
module "pr-processor" {
  source  = "driftlessaf/reconcilers/infra//modules/cloudevents-workqueue"
  version = "~> 1.0"

  project_id = var.project_id
  name       = "pr-processor"
  regions    = var.regions
  team       = "platform"

  broker = module.cloudevent-broker.broker

  # Subscribe to PR-related events
  filters = [
    { "type" = "dev.chainguard.github.pull_request" },
    { "type" = "dev.chainguard.github.pull_request_review" },
  ]

  # Use PR URL as workqueue key (deduplicates concurrent events)
  extension_key = "pullrequesturl"

  workqueue = {
    name = module.workqueue.receiver.name
  }

  notification_channels = var.notification_channels
}
```

### Standalone Workqueue

For custom integrations, use the workqueue module directly:

```hcl
module "workqueue" {
  source  = "driftlessaf/reconcilers/infra//modules/workqueue"
  version = "~> 1.0"

  project_id = var.project_id
  name       = "my-workqueue"
  regions    = var.regions
  team       = "platform"

  concurrent-work = 10
  max-retry       = 5
  scope           = "global"  # Single multi-regional queue

  reconciler-service = {
    name = module.my-service.name
  }

  notification_channels = var.notification_channels
}
```

## Key Concepts

### Generation vs Observed Generation

Borrowed from Kubernetes, this concept enables idempotent reconciliation:

| Concept | Kubernetes | GitHub Reconcilers |
|---------|------------|-------------------|
| **Generation** | `metadata.generation` | HEAD commit SHA |
| **Observed Generation** | `status.observedGeneration` | SHA recorded in Check Run |
| **Change trigger** | Spec change | New commit pushed |

If generations match, the status already reflects your reconciliation of the current state—skip reprocessing. This ensures no-op reconciliations are fast and cheap.

### Workqueue Scope

- **`global`** (recommended): Single multi-regional GCS bucket provides accurate deduplication and concurrency control across all regions
- **`regional`**: Per-region buckets offer lower latency but cannot prevent concurrent processing of the same key across regions

### Dead Letter Queue

Keys that fail more than `max-retry` times are moved to a dead letter queue (`dead-letter/` prefix in the GCS bucket). To reprocess after fixing the underlying issue:

```bash
gcloud run jobs execute <workqueue-name>-reenqueue --region <region>
```

### Priority

Workqueue items support priority levels. Higher values are processed first. Use this to prioritize event-driven work (priority 100) over periodic resyncs (priority 0).

### Reconciler Efficiency

A well-designed reconciler should be **exceptionally cheap when nothing needs to change**. Use lazy evaluation: fetch only enough state to determine if work is needed, then fetch additional data only if reconciliation is actually required.

## Monitoring

Deploy dashboards for observability:

```hcl
module "workqueue-dashboard" {
  source  = "driftlessaf/reconcilers/infra//modules/dashboard/workqueue"
  version = "~> 1.0"

  name            = "my-reconciler"
  max_retry       = 100
  concurrent_work = 20
  scope           = "global"
}
```

The dashboard includes:
- Queue depth (work in progress, queued, added)
- Processing and wait latency
- Retry patterns and completion rates
- Dead letter queue monitoring

## Go Dependencies

Reconciler code imports from [`github.com/driftlessaf/go-driftlessaf`](https://github.com/driftlessaf/go-driftlessaf):

```go
import (
    "github.com/driftlessaf/go-driftlessaf/workqueue"
    "github.com/driftlessaf/go-driftlessaf/reconcilers/githubreconciler"
)
```

## License

Copyright 2026 Chainguard, Inc.
SPDX-License-Identifier: Apache-2.0
