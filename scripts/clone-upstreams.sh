#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$BASE/upstream"
git clone https://github.com/BareBrowser/bare-browser.git "$BASE/upstream/bare-browser"
git clone https://github.com/XiaoYouChR/Ghost-Downloader-3.git "$BASE/upstream/ghost-downloader-3"
