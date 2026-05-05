<div align="center">

# deb-rs

A library for extracting and installing deb files

</div>

## Requirements for use

You can install by adding the folowing to your `cargo.toml` file:

```toml
deb-rs = "0.1"
```

You need to have `ar` command (part of `binutils`) for decompressing the file archive. You also need the `tar` command to extract other archives. You need rust nightly to use this package.

Then you can use it in your program:

```rust
use std::io::Error;
use deb_rs::file::Deb;

fn main() -> Result<(), Error> {
  let mut deb = Deb::new("./example/assets/gnome_clocks.deb");
  deb.extract()?;

  deb.version()?; // Returns the version of the structure of the debian package.
  // NOTE: extract() will fail with versions that are not 2.0 as their structure is different

   deb.retrieve_control()?; // Will return some general information about the contents of the package

  deb.install_tree()?; // Returns an array of files that must be moved for the file package to work

Ok(())
}
```
