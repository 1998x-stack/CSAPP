#!/usr/bin/env bash
# Backwards-compatible entry point; all edits are preview-only unless --apply.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/scripts/safe_transform.py" "$@"
