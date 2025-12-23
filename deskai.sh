#!/usr/bin/env bash
set -e

FIFO="/tmp/deskai_cmd"

if [[ ! -p "$FIFO" ]]; then
  echo "deskai error: FIFO $FIFO does not exist"
  exit 1
fi

if [[ "$1" != "--task" ]]; then
  echo "usage: deskai --task \"your task here\""
  exit 1
fi

shift

TASK="$*"

if [[ -z "$TASK" ]]; then
  echo "deskai error: task cannot be empty"
  exit 1
fi

echo "$TASK" > "$FIFO"
