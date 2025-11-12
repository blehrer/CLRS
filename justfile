#!/usr/bin/env -S just --justfile

log := "warn"
export JUST_LOG := log

# direnv (quiet)
@direnv:
    [ $(which direnv) ] && [ $(which jq) ] \
      && [[ $(direnv status --json | jq '.state.foundRC.allowed' ) = 1 ]] \
      && echo 'direnv not allowed... allowing ....' \
      && direnv allow || exit 0

# Install all dependencies
install: direnv
    uv sync
    brew install imagemagick

# Start notebook on localhost:8888
start: direnv
    nohup jupyter lab &

# Kill notebook server
stop:
    uv run jupyter server stop
