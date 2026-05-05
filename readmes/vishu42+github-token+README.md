# GITHUB-TOKEN

```text
Get a GitHub token for a GitHub App

Usage:
  github-token [flags]

Flags:
      --app-id int                GitHub App ID
      --app-installation-id int   GitHub App installation ID
      --app-private-key string    GitHub App private key
      --config string             config file (default is $HOME/.github-token.yaml)
  -h, --help                      help for github-token
```

It stores the token in the file `"/tmp/githubtoken/token.txt"` and the token is valid for 1 hour. It fetches a new token only if the current stored token is expired. So running the command multiple times does not hammer the GitHub API.
