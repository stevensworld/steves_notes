#!/bin/bash

# Pushes all packages to GitHub. Force overwrites remote.
# Requires: export GIT_HUB=git@github.com:username/repo.git

set -e

if [ -z "$GIT_HUB" ]; then
    echo "ERROR: GIT_HUB environment variable is not set."
    echo "Usage: export GIT_HUB=git@github.com:username/repo.git"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d ".git" ]; then
    git init
    git branch -M main
fi

if git remote get-url origin &>/dev/null; then
    git remote set-url origin "$GIT_HUB"
else
    git remote add origin "$GIT_HUB"
fi

git add .
git commit -m "packages: steves_notes, note_iterator, notes_mcp, litellm_process, process_manager" || echo "Nothing to commit."

git push --force origin main

echo "Done. Pushed to $GIT_HUB"
