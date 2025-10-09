#!/usr/bin/env -S just --justfile

log := "warn"
export JUST_LOG := log

# Activate the .venv
venv:
    source "./.venv/bin/activate"

# Freeze dependencies. Useful right after doing a `pip install`.'
deps: venv
    pip freeze > "./requirements.txt"

# Install all dependencies
install: venv
    pip install -r "./requirements.txt"
    brew install imagemagick

# Start notebook on localhost:8888
start: venv
    jupyter lab

# Kill all jupyter processes
stop: venv
    jupyter notebook list | egrep -o 'localhost.\d+' | sed -e 's/localhost.//' | lsof -i | grep Python | awk '{print $2}' | uniq | xargs kill
