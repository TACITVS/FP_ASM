#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path-to-cloned-FP_ASM.wiki.git>" >&2
  exit 1
fi

wiki_dir="$1"
if [ ! -d "$wiki_dir/.git" ]; then
  echo "Expected a git repository at $wiki_dir" >&2
  exit 1
fi

script_dir="$(cd "$(dirname "$0")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

rsync -av --delete "$repo_root/github-wiki/" "$wiki_dir/"

pushd "$wiki_dir" >/dev/null
if ! git diff --quiet; then
  git add .
  git commit -m "Sync FP_ASM wiki content"
  echo "Changes committed. Run 'git push' to publish."
else
  echo "Wiki already up to date."
fi
popd >/dev/null
