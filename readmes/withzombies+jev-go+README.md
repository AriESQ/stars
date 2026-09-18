# jev-go

**Typed answers from Jev, in idiomatic Go.**

[![CI](https://github.com/withzombies/jev-go/actions/workflows/ci.yml/badge.svg)](https://github.com/withzombies/jev-go/actions/workflows/ci.yml)
[Go 1.26+](go.mod) · [Apache-2.0](LICENSE) · Standard library only

A small, unofficial client for [TypeSafe's System One API](https://docs.typesafe.ai/api).
Ask questions about your data and get probabilities, categories, and scores back
as Go types. Configuration is explicit; HTTP clients and dependencies are yours
to supply.

[Library guide](docs/guide.md) · [API reference](docs/api.md) · [SDK parity](SDK_PARITY.md) · [Triage example](docs/triage.md) · [Development](docs/development.md)

## Install

```sh
go get github.com/withzombies/jev-go
```

Module: `github.com/withzombies/jev-go` · Package: `jev`

Requires a patched Go 1.26 or newer toolchain. CI tests Go 1.26.x and stable Go.

## Quickstart

Set `TYPESAFE_API_KEY` in your application's environment, then run:

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"
    "time"

    jev "github.com/withzombies/jev-go"
)

func main() {
    client, err := jev.NewClient(jev.Config{
        APIKey: os.Getenv("TYPESAFE_API_KEY"),
    })
    if err != nil {
        log.Fatal(err)
    }

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    result, err := client.SystemOne(ctx, jev.Request{
        State: "I was charged twice.",
        Questions: map[string]jev.Question{
            "billing": jev.Noul{Instructions: "Is this message about billing?"},
        },
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Probability of billing: %.2f\n", result.Nouls()["billing"].Noul)
}
```

The application reads the environment; the library receives an explicit API key.
See the [tested, offline example](docs/api.md#Client.SystemOne) for the same call
with an injected local HTTP server.

## Three kinds of questions

| Question | Ask for | Answer |
| --- | --- | --- |
| [Noul](docs/api.md#Noul) | Whether a statement is true | A probability from 0 to 1 |
| [Choice](docs/api.md#Choice) | Which category fits | A label, probabilities, and confidence |
| [Score](docs/api.md#Score) | Where input falls on a defined scale | An expected score, probabilities, confidence, and legend |

Each question is evaluated independently against the same state. Instructions
and criteria can be structured JSON. Responses include the resolved model, token
usage when available, request ID, and buffered HTTP metadata.

## Explore the library

| Documentation | What you will find |
| --- | --- |
| [Library guide](docs/guide.md) | Configuration, dependency injection, retries, errors, and context limits |
| [API reference](docs/api.md) | Every exported declaration, source links, and executable examples |
| [SDK parity](SDK_PARITY.md) | Python and TypeScript capability mappings and the audited versions |
| [PR triage example](docs/triage.md) | A one-shot CLI that asks Jev questions about a patch |
| [Development](docs/development.md) | Local checks, Go toolchains, and regenerating documentation |

> [!NOTE]
> Retries and logging are opt-in. The library does not truncate input.
> Its optional request-size cap measures bytes, not model tokens.

Documentation lives here on GitHub and is generated from standard Go comments
and tested examples. Run `go doc -all .` to read the API locally.

## Try the triage example

From a checkout of this repository, with `TYPESAFE_API_KEY` set:

```sh
go build -o triage ./cmd/triage
gh pr diff 123 --repo OWNER/REPO | ./triage
```

Replace `OWNER/REPO` and `123` with the target repository and pull request.
The command reports `approve`, `request_changes`, or `needs_human_review`.
Its default input budget evaluates the first 24,576 bytes. Recommendations apply
only to evaluated input; the command does not submit GitHub reviews.
See the [triage guide](docs/triage.md) for flags, thresholds, and limitations.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
