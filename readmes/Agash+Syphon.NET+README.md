# Syphon.NET

[![NuGet](https://img.shields.io/nuget/v/Syphon.NET.svg)](https://www.nuget.org/packages/Syphon.NET)
[![build](https://github.com/Agash/Syphon.NET/actions/workflows/build.yml/badge.svg)](https://github.com/Agash/Syphon.NET/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

.NET bindings for [Syphon](https://syphon.info), the macOS framework for sharing video frames
between applications in real time. Publish frames for other apps to pick up, or receive frames
another app is sharing, with no pixel copies in between. Works with OBS, Resolume, TouchDesigner,
and other tools that speak Syphon.

> **Alpha.** Early and working, but largely untested in the wild and rough in places. Try it and file
> issues; expect breaking changes before 1.0.

## Requirements

- macOS on Apple Silicon or Intel, with a Metal-capable GPU.
- .NET 11 (the library targets `net11.0-macos` and uses Microsoft's macOS framework bindings).

## Install

```sh
dotnet add package Syphon.NET
```

The package bundles the native helper it needs; there is nothing else to install.

## Publish

```csharp
using Syphon.NET;

using var server = new SyphonServer("My Output");

// From CPU pixels (BGRA):
server.PublishPixels(bgraPixels, width: 1920, height: 1080);

// Or from a GPU IOSurface you already hold (zero-copy), e.g. a VideoToolbox CVPixelBuffer:
server.Publish(surface);
```

In OBS, add a **Syphon Client** source and choose "My Output".

## Receive

```csharp
using Syphon.NET;

using var directory = new SyphonServerDirectory();

// An app with a Cocoa run loop (MAUI/AppKit) discovers automatically. A plain console or server
// process pumps the run loop so discovery notifications arrive:
directory.PumpEvents(TimeSpan.FromMilliseconds(200));

using var client = directory.CreateClient(index: 0);

// Frames are Microsoft's IOSurface binding directly - dispose when done (it releases the retain).
using IOSurface.IOSurface? frame = client.TryGetFrame();
if (frame is not null)
{
    (int w, int h) = frame.PixelSize();
    byte[] pixels = new byte[w * h * 4];
    frame.CopyTightlyPacked(pixels);
}
```

Each frame is the shared `IOSurface` itself (`frame.Handle`), so you can read it on the CPU as shown
or hand it straight to VideoToolbox for a zero-copy hardware encode.

## Working with surfaces (`IOSurfaceExtensions`)

Frames and the surface returned by `AcquireSurface` are the Microsoft
[`IOSurface`](https://learn.microsoft.com/dotnet/api/iosurface.iosurface) binding directly - there is
no wrapper type. `IOSurfaceExtensions` adds the ergonomics the binding doesn't surface:

```csharp
using Syphon.NET;

(int w, int h) = surface.PixelSize();          // int-typed dimensions
bool bgra = surface.IsBgra();                   // format predicates (IsBgra / IsNv12)
(int cw, int ch, int stride) = surface.PlaneInfo(1); // per-plane dims + row stride

// Scoped CPU access yielding a Span; unlocks on dispose:
using (var locked = surface.LockBytes(readOnly: true))
{
    ReadOnlySpan<byte> bytes = locked.Bytes;    // row-padded; stride is locked.BytesPerRow
}

surface.CopyTightlyPacked(destination);         // copy out, stride collapsed to width * 4
surface.WritePixels(source);                    // copy tightly-packed rows in

var output = IOSurfaceExtensions.CreateBgra(w, h); // make a surface to draw into and publish
```

GPU transforms (colour conversion, channel folding) are the caller's job - drive Metal compute or
render through your own `Microsoft.macOS` Metal bindings and publish the resulting surface with
`server.Publish(surface)`.

## Building from source

```sh
git clone --recursive https://github.com/Agash/Syphon.NET
cd Syphon.NET
bash native/build-native.sh
dotnet build Syphon.NET.slnx
dotnet test
```

The native helper compiles the Syphon framework (a git submodule, built unmodified) and a small shim
into one universal binary; the server announces IOSurfaces directly through `SyphonServerBase`, so no
Metal renderer or shader library is involved. The managed library targets `net11.0-macos` and needs
the .NET 11 SDK with the `macos` workload.

## License

MIT. See [LICENSE](LICENSE). Bundled Syphon framework code is BSD licensed; see
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
