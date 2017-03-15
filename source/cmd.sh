#!/usr/bin/env bash
# This script is run from within the running container.
set -e


echo "Starting service in $EMIS_CONFIGURATION mode"

if [[ "$EMIS_CONFIGURATION" == @("development"|"test") ]]; then
    exec python server.py
else
    # Acceptance, production
    exec python server.py
fi
