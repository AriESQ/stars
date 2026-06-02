# gstreamer-docs-offline

Automated weekly snapshot of GStreamer API documentation for offline/local use.

This is an unofficial project and is not affiliated with or endorsed by the GStreamer project.

## Download

```
gh release download latest
tar xzf gstreamer-docs.tar.gz
```

## Build locally

```
docker build -t gstreamer-docs .
docker run --rm -v $(pwd):/host gstreamer-docs cp -r /output/docs /host/
```

## Browse locally

```
docker run --rm -p 8000:8000 gstreamer-docs python3 -m http.server 8000 --directory /output/docs
```

Then open http://localhost:8000.

## How it works

A GitHub Actions workflow runs weekly, builds the full GStreamer documentation from source using the same toolchain as GStreamer's CI (Fedora + meson + hotdoc), and uploads the result as a release artifact.

## License

The GStreamer documentation is licensed under LGPL-2.1-or-later and CC-BY-SA-4.0. See [LICENSE](LICENSE) for details.
