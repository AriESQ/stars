# internet-archive

*Note: This package is no longer maintained. It is superseded by [annas-archive](https://github.com/benthamite/annas-archive).*

## Introduction

This simple Emacs package lets you download any PDF file from the [Internet Archive](https://archive.org/) seamlessly, as long as it can be borrowed for at least one hour.

## Requirements

- [ia](https://archive.org/developers/internetarchive/cli.html).
- [wget](https://www.gnu.org/software/wget/).
- [Adobe Digital Editions](https://www.adobe.com/solutions/ebook/digital-editions.html).
- [calibre](https://calibre-ebook.com/) with [DRM Removal plugin](https://www.epubor.com/calibre-drm-removal-plugins.html).

If you are on macOS and use Homebrew, you can install all of the above requirements by running

```shell
brew install internetarchive wget adobe-digital-editions calibre
```

## Installation

### Manual installation

Clone this repository and add this to your `init.el` file:

``` emacs-lisp
(add-to-list 'load-path "path/to/internet-archive")
```

Where `"path/to/internet-archive"` is the path to the local repository you just cloned.

### Elpaca/Straight

If you use the [elpaca](https://github.com/progfolio/elpaca) package manager, you just need to add this your `init.el` file:

``` emacs-lisp
(use-package internet-archive
  :ensure (internet-archive
           :host github
	   :repo "benthamite/internet-archive")
  :demand t)
```

If you use [straight](https://github.com/radian-software/straight.el), just replace `:ensure` with `:straight` in the formula above.

## One-time setup

When running for the first time:

1. *Configure the `ia` program.* Run `ia configure` and follow the instructions.
2. *Export your IA cookies file*. You can export the cookies by installing the [Get cookies.txt LOCALLY](https://github.com/kairi003/Get-cookies.txt-LOCALLY) browser extension. Then go to https://archive.org/, click on the extension, click on ‘export’, and save it to `~/.config/cookies.txt`. (If you would like to save it to different location, you need to manually set `internet-archive-cookies-file`.)

## Usage

### From Emacs

`M-x internet-archive`, followed by a URL or a title, depending on whether you already know the URL of the book you would like to download or need to search for it. If you choose to search for a book, you will also be prompted to enter an author (labelled `creator`). These fields are each, but not jointly, optional. (The fields are customizable; see below.)

### From the browser 

If you have `org-protocol` [installed](https://www.orgroam.com/manual.html#Installation-_00281_0029) and configured on your system, you can also trigger the function directly from your web browser, by creating a bookmark with the following JavaScript code:

``` javascript
javascript:location.href='org-protocol://internet-archive?url=%27 + encodeURIComponent(location.href);
```

Then simply click on this bookmark after clicking ‘Borrow for 1 hour’.

## Customization

- For running search queries, the fields `title` and `creator` are used by default. If you would like to use different fields, you can set `internet-archive-query-fields`. (The full list of admissible fields is [here](https://archive.org/developers/metadata-schema).) Note that the first of the fields in the variable will be used for the initial prompt upon invocation of `internet-archive`. For example, if you set `internet-archive-query-fields` to `("author" "title" "language")`, you will initially be prompted to enter a URL or an author (rather than a URL or a title), and this will be followed by prompts to enter a title and a language.

- When returning results, the fields `title` and `creator` are also used by default. If you would like to use different fields, you can set `internet-archive-metadata-fields`.

- Depending on where in your file system the relevant Calibre and Adobe Digital Editions are found, you may need to set the values of `internet-archive-calibre-directory` and `internet-archive-ade-directory` accordingly.

- Emacs should be able to find the `ia`, `wget` and `calibredb` executables. But if it doesn’t, you can specify their location manually by setting the value of `internet-archive-cli-file`, `internet-archive-wget-file` and `internet-archive-calibredb-file`, respectively.

- If you want Adobe Digital Editions to close once it is done downloading the PDF from the Internet Archive, set `internet-archive-ade-close-when-done` to `t`.  If you want Adobe Digital Editions to open in the background, set `internet-archive-ade-open-in-background` to `t`. Note that it seems like ADE will start downloading the file only when
it is in the foreground, so this option may be less useful than it appears.

- For the full list of user options, `M-x customize-group RET internet-archive`.

## FAQ

***I see more results when I run a search on the Internet Archive website than when I use your package.***

The search results we display are deliberately restricted to *books available for borrowing*. In addition, the search terms will only match results in the associated fields (`author` or `title`). So e.g. if you enter “borges” when prompted for an author, this will match *El aleph*, but will not match *[Borges](https://archive.org/details/borges-adolfo-bioy-casares)* (because Borges is not the author), *[Borges por él mismo](https://archive.org/details/cd_jorge-luis-borges-lee-sus-poemas_jorge-luis-borges)* (because it is not a book) or *[Ficciones](https://archive.org/details/obrascompletas0000borg)* (because it is not currently borrowable).

***“This book is not available to borrow at this time. Please try again later.”***

This sometimes happens with books that *are* available for borrowing. It appears to be a limitation of the Internet Archive CLI. If this happens, please go to the website, borrow the book manually, then run `internet-archive` again with the URL.

## Troubleshooting

The package has not been extensively tested. If you encounter any problems, feel free to open an issue.
