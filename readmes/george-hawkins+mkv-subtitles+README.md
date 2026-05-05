MKV subtitles and vobsub in particular
======================================

I was watching a Japanese movie in `.mkv` format and the only included English subtitles had content for the deaf ("crowd gasps" and the like) and this quickly gets tiring.

So, this is how I extracted the subtitles. And then as the subtitles were in vobsub format, which is image based rather than text, I needed to convert them to a text `.srt` file that I could then edit and remove the content for the deaf.

Note: often you can find existing subtitles on sites like [opensubtitles.org](https://www.opensubtitles.org/en/search/subs) (a completely ad-riddled site).

To work with `.mkv` you need to install `mkvtoolnix`:

```
$ brew install mkvtoolnix
```

Note: `mkvtoolnix` used to be hosted on GitLab but is now [here](https://codeberg.org/mbunkus/mkvtoolnix) on Codeberg.

Once `mkvtoolnix` is installed, you can look at your `.mkv` file:

```
$ mkvmerge -i 'Paprika (2006).mkv' 
File 'Paprika (2006).mkv': container: Matroska
Track ID 0: video (HEVC/H.265/MPEG-H)
Track ID 1: audio (AAC)
Track ID 2: audio (AAC)
Track ID 3: subtitles (VobSub)
Track ID 4: subtitles (VobSub)
Track ID 5: subtitles (VobSub)
Track ID 6: subtitles (VobSub)
Track ID 7: subtitles (VobSub)
Track ID 8: subtitles (VobSub)
...
```

Now you know that tracks 3 and on are subtitles but, for language information, you have to use the more verbose `mkvinfo` and search for `Language.*en`, i.e. the English one:

```
$ mkvinfo 'Paprika (2006).mkv' | less
    | + Track
    |  + Track number: 4 (track ID for mkvmerge & mkvextract: 3)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |  + Track UID: 824028482569575953
--> |  + Track type: subtitles
    |  + "Lacing" flag: 0
--> |  + Codec ID: S_VOBSUB
    |  + Codec's private data: size 348
--> |  + Language (IETF BCP 47): en
    |  + Content encodings
    |   + Content encoding
    |    + Content compression
```

Note: I first just read `Track number: 4` and used `4` but as you see, it then goes on to show the track ID to use with `mkvextract` etc., i.e. `3`.

So, you want the `subtitles` track with language `en` and if it shows as `S_VOBSUB` (as it does here), it means it's DVD subtitles encoded as an image stream.

You can also find an example, down below, of how to get language information using `mkvmerge` in combination with `jq`.

Now that we know the track (in this case `3`), extract the subtitles - specify the track, followed by a `:` and a base name for the subtitle files (in this case `paprika_en`):

```
$ mkvextract tracks 'Paprika (2006).mkv' 3:paprika_en
```

This is relatively slow but at least you get a progress percentage as it goes.

As we're extracting vobsub files, you'll end up with:

```
$ ls paprika_en.*
paprika_en.idx    paprika_en.sub
```

There are many tools to convert these into `.srt` but note that they depend on OCR and some do a better job than others.

I tried [`vobsubocr`](https://github.com/elizagamedev/vobsubocr). It's not paricularly popular but looking at the code, it seems like the task is relatively simple and no rocket science is needed (the hard work, i.e. the OCRing, is done by [Tesseract](https://github.com/tesseract-ocr/tesseract))

To install Rust (as described [here](https://www.rust-lang.org/tools/install)):

```
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

It adds a line to your `.bashrc` to set up the Rust environment, so either open a new terminal or just run this setup manually in your current shell:

```
$ source ~/.cargo/env
```

Then I just installed `vobsubocr`:

```
$ cargo install --git https://github.com/elizagamedev/vobsubocr
```

Then I ran it, specifying `paprika_en.idx` (and it assumes there's a corresponding `.sub` file):

```
$ vobsubocr -l eng -c tessedit_char_blacklist='|\/`_~' -o paprika_en.srt paprika_en.idx
```

Note: the `tessedit_char_blacklist`, this is a list of blacklisted characters that are unlikely to validly occur in the subtitles and without it, Tesseract sometimes e.g. interpreted `I` as `|`.

Even with this blacklist, it often mixed up `!` and `I`. The `!` appears in lots of places validly but I would have hoped, given that Tesseract has to be told what language is being converted, that it would e.g "know" that `!` generally only appears in very particular situations and definitely not at the start of sentences. I manually, cleaned up all the `!` issues (oddly, it never seemed to mistake an `!` for an `I` - it was always only the other way around).

Commont mistakes were:

* `!` instead of `I`.
* `1` instead of `I`.
* `lam` instead of `I am`.
* Oddly, two instances of `K` rather than `k` (both in the work `Know`) - all other capitalization seemed fine.

Running `vobsubocr` is surprisingly quick - clearly OCRing isn't a taxing job for modern computers.

I then edited the file to remove bits for the deaf (the whole point of this exercise).

These were the main patterns to look for and remove:

* `[in English] It's the greatest show time!`
* `-[crowd gasps, cheers]`
* `-[Atsuko] You mean you opened it.`
* `[crowd gasping]`
* `[Paprika] There's someone who keeps`

Note: in all case, I never deleted a line (except see the blank-line issue below), I just deleted character, sometimes leaving completely blank lines - whether this is the correct approach, I don't know - but I didn't want to change the structure of the file.

Things like `[in English] ...` tell you that the character is actually speaking English (even though in this case, it's a Japanese movie), so these lines can be removed completely (I just did a case-insensitive search for "english" and removed all characters on the relevant lines).

The `-` seems to be used to indicate that the noise is coming from a new source (whether the dialog is switching between people or e.g. a car makes a noise and then an animal does).

I didn't want to remove the `-` in the case where somebody is saying something, e.g. `-[Atsuko] You mean...` but did where it's nothing other than a sound, e.g. `-[crowd gasps, cheers]`

So, to remove things that were nothing more than sounds, I did:

```
:%s/-\[.*\]\s*$/
```

And then for everything else, I did:

```
:%s/\[.*\]\s*/
```

Creating blank lines did cause a problem, e.g.:

```
952
01:23:06,690 --> 01:23:09,210
[Konakawa]
Have we awoken from the dream?
```

This became: 

```
952
01:23:06,690 --> 01:23:09,210

Have we awoken from the dream?
```

And the `Have ...` is treated as a misformatted start of a new block and ignored.

So, I searched for timecodes followed by an empty line followed by at least one character of text like so:

`/^[0-9]\+.*\n\s*$\n.`

And properly deleted those cases.

That's it.

In Kodi, when selecting a subtitle, it presents those in the `.mkv` by default but you can also browse for the `.srt` file created by this process instead. Kodi usually remembers the audio and subtitle selections you make for a given movie so that next time you watch it, Kodi defaults to your previous choices. However, it doesn't remember you choosing an external subtitle file, rather than one of the `.mkv` internal ones, and next time you watch the movie, it reverts back to one in the `.mkv` file.

mkvmerge output
---------------

I find it a little odd that `mkvmerge -i foo.mkv` doesn't list the language for each track - apparently this was actively removed (see issue [#2263](https://gitlab.com/mbunkus/mkvtoolnix/-/issues/2263)) and if you want more detailed information, you have to select JSON output and pick out what you want using a tool like `jq` (as covered in this FAQ [entry](https://gitlab.com/mbunkus/mkvtoolnix/-/wikis/Transforming-mkvmerge's-JSON-output)).

So, copying the FAQ's example, you'd get the language information like so (`und` is undefined):

```
$ mkvmerge -J 'Paprika (2006).mkv' | jq -r '
  .tracks |
  map((.id | tostring) + " " + .properties.language + " " + .codec) |
  join("\n")
'
0 und HEVC/H.265/MPEG-H
1 jpn AAC
2 eng AAC
3 eng VobSub
4 ara VobSub
5 chi VobSub
...
```
