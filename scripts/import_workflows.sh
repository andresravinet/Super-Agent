#!/usr/bin/env bash
set -euo pipefail

WORKFLOWS_DIR="${1:-workflows}"
N8N_CMD="${N8N_CMD:-n8n}"
IMPORT_OPTS=${N8N_IMPORT_OPTS:-}

if [ ! -d "$WORKFLOWS_DIR" ]; then
  echo "Workflows directory not found: $WORKFLOWS_DIR" >&2
  exit 1
fi

import_file() {
  local file="$1"
  echo "Importing $file"
  $N8N_CMD import:workflow --input="$file" $IMPORT_OPTS
}

if [ -d "$WORKFLOWS_DIR/tools" ]; then
  for file in "$WORKFLOWS_DIR"/tools/*.json; do
    [ -e "$file" ] || continue
    import_file "$file"
  done
fi

for file in "$WORKFLOWS_DIR"/*.json; do
  [ -e "$file" ] || continue
  import_file "$file"
done
