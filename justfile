#!/usr/bin/env -S just --justfile

log := "warn"
export JUST_LOG := log

# Install all dependencies
install:
    uv install
    brew install imagemagick

# Start notebook on localhost:8888
start:
    nohup jupyter lab &

# Kill notebook server
stop:
    jupyter server stop
