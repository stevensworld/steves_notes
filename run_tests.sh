#!/bin/bash

set -e

REPO_URL="https://github.com/stevensworld/steves_notes.git"
CLONE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/steves_notes"

echo "── Cloning $REPO_URL"

if [ -d "$CLONE_DIR" ]; then
    echo "   Repo already exists — pulling latest."
    git -C "$CLONE_DIR" pull
else
    git clone "$REPO_URL" "$CLONE_DIR"
fi

echo "── Running tests"
bash "$CLONE_DIR/packages/tests_context/test_install.sh"
