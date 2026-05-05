build.sh builds the Go 1.20.14 toolchain from source, bootstrapping via Go 1.17, Go 1.4, and the host's C compiler.  Its purpose is to create a trusted toolchain that can be used by [Source Spotter](https://sourcespotter.com) to verify the reproducibility of Go 1.21, 1.22, and 1.23.

build.sh produces a golang.org/toolchain module zip file at the root of the repository with a name like `v0.0.1-go1.20.14.GOOS-GOARCH.zip`.

build.sh must be run from the root of the repository.

## Operation

build.sh does the following:

1. Downloads source tarballs from <https://go.dev/dl/>. The SHA-256 digests are verified against [a list in this repository](src/SHA256SUMS) to ensure the source tarballs haven't changed.

2. Builds Go 1.4.3 using the host's C compiler, as specified by the `CC` environment variable (defaults to `gcc -no-pie`).

3. Builds Go 1.17.13 using Go 1.4.3.

4. Builds Go 1.20.14 using Go 1.17.13, for the target specified by the `GOOS` and `GOARCH` environment variables (defaults to the host OS / architecture).  Cgo is disabled, to make the output more reproducible.

5. Compiles the [distpack command](distpack/) located in this repository using Go 1.20 and runs it to create the module zip file.

### distpack

The source for distpack was [extracted from Go 1.21.0](https://cs.opensource.google/go/go/+/refs/tags/go1.21.0:src/cmd/distpack/) and modified as follows:

* The code to create source and binary archives was removed.

* The Go 1.20.14 release date is hard-coded in the source and used for file timestamps if the VERSION file lacks the time field.

## Reproducibility

As long as you run build.sh from the same directory, on a UNIX host, it should generally produce the exact same module zip file, byte-for-byte.  This has been verified in the following environments:

* Debian 12 on amd64, with GCC
* Debian 12 on amd64, with GCC, cross-compiling to linux-arm64
* Debian 12 on amd64, with clang
* Debian 12 on amd64, with clang, cross-compiling to linux-arm64
* Amazon Linux 2023 on amd64, with GCC
* Amazon Linux 2023 on amd64, with GCC, cross-compiling to linux-arm64

If you run build.sh from `/tmp/build-go1.20` it should produce zip files with the following SHA-256 digests:

```
6874388635be9f76bc7ad0ca53298cacd058554708e4d97c187ec577f236c7e1  v0.0.1-go1.20.14.linux-amd64.zip
b786c534bbe0f5ec346b891f43dace7d21317f002760e1432ee0c77f5a1698cf  v0.0.1-go1.20.14.linux-arm64.zip
```

However, Go 1.20 does not contain all the [reproducible build fixes for Go 1.21](https://github.com/golang/go/issues/24904), so your mileage may vary.
