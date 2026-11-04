#!/usr/bin/env bash
set -euo pipefail
for cmd in docker git python3; do
  if command -v "$cmd" >/dev/null 2>&1; then echo "OK: $cmd"; else echo "MISSING: $cmd"; fi
done
df -h .
echo "Bare documented build: Docker, >=32 GB allocated RAM, ~100 GB free disk."
