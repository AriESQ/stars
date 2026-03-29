#!/bin/env bash

# Build: podman build -f containers/Containerfile -t stars-test .
podman run --rm \
  -e GITHUB_TOKEN="$(gh auth token)" \
  -e GIT_USER_NAME="AriESQ" \
  -e GIT_USER_EMAIL="19827230+AriESQ@users.noreply.github.com" \
  -v ./github_stars.json:/app/github_stars.json \
  stars-test
