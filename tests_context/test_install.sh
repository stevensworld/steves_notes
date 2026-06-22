#!/bin/bash

# Creates a conda env, installs packages from the cloned repo, and runs the tests.

set -e

PACKAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_NAME="steves_notes_rebuild"
PYTHON_VERSION="3.11"

# ── Step 2: Create conda env ──────────────────────────────────────────

echo "── Creating conda env: $ENV_NAME (Python $PYTHON_VERSION)"

if conda env list | grep -q "^$ENV_NAME "; then
    echo "   Env already exists — skipping create."
else
    conda create -y -n "$ENV_NAME" python="$PYTHON_VERSION"
fi

# ── Step 3: Install packages ──────────────────────────────────────────

echo "── Upgrading setuptools"
conda run -n "$ENV_NAME" pip install --upgrade setuptools

echo "── Installing packages"

conda run -n "$ENV_NAME" pip install -e "$PACKAGES_DIR/process_manager"
conda run -n "$ENV_NAME" pip install -e "$PACKAGES_DIR/process_manager_tests"

# ── Step 4: Run tests ─────────────────────────────────────────────────

echo "── Running tests"
echo ""

conda run -n "$ENV_NAME" python -m unittest process_manager_tests.test_process_manager -v

echo ""
echo "── Done."
