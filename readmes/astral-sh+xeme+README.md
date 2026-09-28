# Xeme

A streaming XML parser written in Rust, with an Expat-compatible C API.

> [!WARNING]
> This README is human-edited, but all code changes, PR summaries, and additional
> documentation were authored entirely by GPT-6 Astra in [Codex](https://openai.com/codex/).
> Use at your own risk.

## Highlights

- Parse XML incrementally, with namespaces, encodings, entities, and DTD attribute defaults.
- Check XML and inspect parser events from the command line.
- Embed the safe Rust parser or use the Expat-compatible C interface.

| Project XML | Xeme | Expat | Xeme / Expat |
| --- | ---: | ---: | ---: |
| .NET runtime | 2.133 ms | 1.938 ms | 1.089× |
| Apache Hadoop | 1.302 ms | 1.024 ms | 1.269× |
| LibreOffice | 1.597 ms | 0.638 ms | 2.530× |
| MuseScore | 9.795 ms | 6.425 ms | 1.523× |
| Qt translations | 6.630 ms | 2.133 ms | 3.018× |

Xeme passes the [W3C XML 1.0 Fifth Edition conformance suite](docs/compatibility.md#native-rust-conformance-gate)
and all six [CPython 3.12.13 XML test suites](docs/evidence/2026-09-13-cpython-grouping.md)
with both shared and static libraries. See [compatibility](docs/compatibility.md)
for known differences from Expat and the XML specification.

## Installation

Build from this checkout with Rust 1.96 or later:

```console
cargo install --path crates/xeme_cli --bin xeme --locked
```

See the [command-line guide](docs/usage.md) for allocator options, input handling,
and resource limits.

## Getting started

Given `message.xml`:

```xml
<message>Hello &amp; goodbye</message>
```

Check the document:

```console
xeme message.xml
```

Invalid XML exits with a nonzero status. Omit the filename or pass `-` to read
standard input. Xeme can also print parser events and expand namespaces:

```console
xeme --events message.xml
xeme --events --namespaces --chunk-size 4096 message.xml
```

See the [command-line guide](docs/usage.md), the [Rust library guide](docs/library.md),
or the [Expat interface](crates/xeme_expat/) for embedding and callback contracts.
The parser performs no filesystem or network I/O; applications supply input and
resolve external entities. The CLI does not fetch external resources.

See the [review guide](docs/review.md) for implementation and test entry points.

## License

Xeme is licensed under either of

- Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
  <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in Xeme
by you, as defined in the Apache-2.0 license, shall be dually licensed as above, without any
additional terms or conditions.
