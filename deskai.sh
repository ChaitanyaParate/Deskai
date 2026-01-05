#!/usr/bin/env bash

DESKAI_DIR="$HOME/.local/share/deskai"

exec "$DESKAI_DIR/venv/bin/python" \
     "$DESKAI_DIR/client.py" "$@"
