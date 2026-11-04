#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOCK="$ROOT/integration/upstream-lock.json"
DEST="$ROOT/upstream"

if [[ ! -f "$LOCK" ]]; then
  echo "Missing upstream lock file: $LOCK" >&2
  exit 1
fi

readarray -t SPECS < <(python3 - "$LOCK" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    lock = json.load(f)
for key, dirname in (("bare_browser", "bare-browser"), ("ghost_downloader", "ghost-downloader-3")):
    item = lock[key]
    print(item["repository"])
    print(item["commit"])
    print(dirname)
PY
)

mkdir -p "$DEST"
for ((i=0; i<${#SPECS[@]}; i+=3)); do
  url="${SPECS[i]}"
  commit="${SPECS[i+1]}"
  name="${SPECS[i+2]}"
  path="$DEST/$name"

  if [[ -d "$path/.git" ]]; then
    if [[ -n "$(git -C "$path" status --porcelain)" ]]; then
      echo "Refusing to overwrite local changes in $path" >&2
      exit 1
    fi
    git -C "$path" fetch --no-tags origin "$commit"
  else
    git clone --no-checkout "$url" "$path"
    git -C "$path" fetch --no-tags origin "$commit"
  fi

  git -C "$path" checkout --detach "$commit"
  actual="$(git -C "$path" rev-parse HEAD)"
  [[ "$actual" == "$commit" ]] || { echo "Commit mismatch for $name" >&2; exit 1; }
  echo "Pinned $name at $actual"
done

echo "Both upstreams are checked out at the exact commits in integration/upstream-lock.json."
