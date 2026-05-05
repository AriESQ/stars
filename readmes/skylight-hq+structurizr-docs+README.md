# Structurizr Documentation Template

> [!TIP]
> This project leverages `just` as a command runner. To learn more about `just`
> view their documentation at: [https://just.systems/man/en](). Run `just help`
> for a list of commands.

This project is a template for how Skylight projects can use Structurizr for
documentation within a single repository. Structurizr DSL provides a workspace
for C4 model data architecture which integrates documentation, decision records,
and diagrams in a single resource.

## Getting started

To get started, copy the `docs/` directory along with the `justfile` at the root
of this repository into any project. If your project leverages a `justfile`
already, you must incorporate the contents of this project's `justfile` into
your project's `justfile`. Specifically, the `mod ...` lines at the bottom of
this repository's `justfile`.

With these files and directories in your project, run `just structurizr start`
to get Structurizr Lite running in your browser.

## Writing Structurizr DSL

> [!IMPORTANT]
> If you're new to the [C4 model][docs-c4-model] for system architecture
> diagrams and/or [Structurizr DSL][docs-structurizr], please read through their
> documentation to get familiar with it.

[docs-c4-model]: https://c4model.com/#Abstractions "The homepage for the C4 model"
[docs-structurizr]: https://docs.structurizr.com/ "The homepage for Structurizr"

Structurizr DSL is based on the C4 model. A Structurizr workspace contains a
`model {}` and a `views {}` block. When writing in the DSL it helps to think of
your software components in the C4 data model as files in the `docs/`
directories. Conveniently, DSL blocks are already setup as directories with
`default.dsl` files.

### Using models 📁

This directory contains any number of subdirectories that make sense for the
architecture of what software systems you're trying to represent in C4. This
directory is also where you will include any documentation related to the
software system directories within an `md/` directory. With this, you can
include blocks of documentation within a software system very easily.

```dsl
!docs md
```

This will embed the Markdown in that directory to the system it is representing.
All documentation shows up by default but can be filtered. To make it easier to
read the Markdown outside of Structurizr, you can name the file `README.md` to
have it render automatically in a VCS system such as GitHub or Gitlab.

```
Name
├── docs
│  ├── models
│  │  ├── default.dsl
│  │  └── systemA
│  │     └── md
│  │        └── README.md
```

For more information on Documentation and how it renders in Structurizr, read
the following pages of documentation.

- [https://docs.structurizr.com/dsl/docs]()
- [https://docs.structurizr.com/ui/documentation/headings]()

##### Relationships between models

Due to the nature of how the models and views are separated into separate files,
Relationships between elements in the C4 model should be added within the model
`.dsl` files and not in the main `workspace.dsl` file. In other words,
Relationships should always be made implicitly rather than explicitly. For more
information, [read the DSL documentation on Relationships][s9r-relationship].

[s9r-relationship]: https://docs.structurizr.com/dsl/language#relationship

#### Decision records

When it comes to architecture decision records (ADRs), there should be a
`decisions/` directory at the root of the `docs/` directory. These ADRs must
follow the same format as the files created by `adr-tools`. The `justfile` in
this project already contains a module called `adr` where you can run `just adr
new "A title for the ADR"` to create sequential ADRs automatically. This command
works in both Unix and Windows environments that have Node installed.

### Using views 📁

This directory contains any number of `.dsl` files which represent different
diagram outputs. The files in here should be limited to a single diagram output
but can also be organized in a single `default.dsl` file.

### Using styles 📁

This directory contains a `branding.dsl` and a `styles.dsl` file with the
branding and styling definitions along with directories of images such as icons
and logos.
