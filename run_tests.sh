#!/bin/bash

set -e

REPO_URL="https://github.com/stevensworld/steves_notes.git"
WORK_DIR="$(pwd)/testexecute"
mkdir -p "$WORK_DIR"

echo "── Working directory: $WORK_DIR"
echo "── Cloning $REPO_URL"

git clone "$REPO_URL" "$WORK_DIR/steves_notes"

echo "── Running tests"
bash "$WORK_DIR/steves_notes/tests_context/test_install.sh"

echo "── Done. Repo left at: $WORK_DIR/steves_notes"
