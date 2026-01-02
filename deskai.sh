#!/usr/bin/env bash

DESKAI_DIR="/home/chaitanyaparate/Downloads/deskai"
PYTHON="$DESKAI_DIR/desk/bin/python"
CLIENT="$DESKAI_DIR/client.py"

exec "$PYTHON" "$CLIENT" "$@"

