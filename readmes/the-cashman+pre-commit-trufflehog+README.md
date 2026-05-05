# pre-commit-trufflehog

An attempt at a pre-commit hook for [TruffleHog](https://github.com/trufflesecurity/trufflehog).

It doesn't work very well, since TruffleHog only supports scanning a directory recursively and is rather slow.

I wouldn't suggest using this as is. TruffleHog plans to support per file scanning in the future, at which time this pre-commit hook may become actually useful.