#!/usr/bin/env bash
# Copy the web build into the website checkout's pyramid/ folder.
#   tools/sync-to-site.sh [path-to-williamrachuy.github.io]
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
site="${1:-$here/../williamrachuy.github.io}"
dest="$site/pyramid"
[[ -d "$site/.git" ]] || { echo "Not a site checkout: $site" >&2; exit 1; }
mkdir -p "$dest"
find "$dest" -mindepth 1 -delete
cp -R "$here/web/." "$dest/"
echo "Synced $here/web -> $dest ($(git -C "$here" rev-parse --short HEAD))"
