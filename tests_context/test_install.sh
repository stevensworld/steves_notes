#!/bin/bash

# Clones steves_notes from GitHub, creates a fresh conda env,
# installs process_manager and process_manager_tests, and runs the tests.

set -e

REPO_URL="git@github.com:stevensworld/steves_notes.git"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/steves_notes"
ENV_NAME="steves_notes_rebuild"
PYTHON_VERSION="3.11"

# ── Step 1: Clone ─────────────────────────────────────────────────────

echo "── Cloning $REPO_URL"

if [ -d "$REPO_DIR" ]; then
    echo "   Repo already exists at $REPO_DIR — pulling latest."
    git -C "$REPO_DIR" pull
else
    git clone "$REPO_URL" "$REPO_DIR"
fi

PACKAGES_DIR="$REPO_DIR/packages"

# ── Step 2: Create conda env ──────────────────────────────────────────

echo "── Creating conda env: $ENV_NAME (Python $PYTHON_VERSION)"

if conda env list | grep -q "^$ENV_NAME "; then
    echo "   Env already exists — skipping create."
else
    conda create -y -n "$ENV_NAME" python="$PYTHON_VERSION"
fi

# ── Step 3: Install packages ──────────────────────────────────────────

echo "── Installing packages"

conda run -n "$ENV_NAME" pip install -e "$PACKAGES_DIR/process_manager"
conda run -n "$ENV_NAME" pip install -e "$PACKAGES_DIR/process_manager_tests"

# ── Step 4: Run tests ─────────────────────────────────────────────────

echo "── Running tests"
echo ""

conda run -n "$ENV_NAME" python -m unittest process_manager_tests.test_process_manager -v

echo ""
echo "── Done."
