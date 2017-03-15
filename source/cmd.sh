#!/usr/bin/env bash
# This script is run from within the running container.
set -e


if [[ "$EMIS_CONFIGURATION" == @("development"|"test") ]]; then
    python -m unittest discover emis/test *_test.py
    python -m unittest discover test *_test.py
    exec python server.py
else
    # Acceptance, production
    exec python server.py
fi
