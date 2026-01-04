#!/usr/bin/env bash

DESKAI_DIR="$(cat "$HOME/.deskai_path")"

PYTHON="$DESKAI_DIR/desk/bin/python"
CLIENT="$DESKAI_DIR/client.py"

exec "$PYTHON" "$CLIENT" "$@"
