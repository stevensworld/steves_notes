#!/bin/bash

PACKAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
PM_ENV="prove_process_manager"
PYTHON_VERSION="3.11"


# ── Install phase ─────────────────────────────────────────────────────

install_phase() {
    set -e

    echo "── Creating conda env: $PM_ENV (Python $PYTHON_VERSION)"
    if conda env list | grep -q "^$PM_ENV "; then
        echo "   Env already exists — skipping create."
    else
        conda create -y -n "$PM_ENV" python="$PYTHON_VERSION"
    fi

    echo "── Upgrading setuptools"
    conda run --no-capture-output -n "$PM_ENV" pip install --upgrade setuptools

    echo "── Installing process_manager packages"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/process_manager"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/test_utils"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/process_manager_tests"

    echo "── Setting up litellm environment"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/litellm_process"
    conda run --no-capture-output -n "$PM_ENV" python "$PACKAGES_DIR/litellm_process/litellm_process/setup.py"

    echo "── Installing litellm_process_tests"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/litellm_process_tests"

    echo "── Installing notes_mcp packages"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/steves_notes"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/note_iterator"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/notes_mcp"
    conda run --no-capture-output -n "$PM_ENV" pip install -e "$PACKAGES_DIR/notes_mcp_tests"

    set +e
}


# ── Test phase ────────────────────────────────────────────────────────

run_process_manager_tests() {
    echo ""
    echo "── Running process_manager tests"
    conda run --no-capture-output -n "$PM_ENV" python "$PACKAGES_DIR/process_manager_tests/process_manager_tests/visit/visit.py"
}

run_litellm_tests() {
    while true; do
        echo ""
        echo "── Running litellm_process tests"
        conda run --no-capture-output -n "$PM_ENV" python "$PACKAGES_DIR/litellm_process_tests/litellm_process_tests/visit/visit.py"
        if [ $? -eq 0 ]; then
            break
        fi
        echo ""
        echo "   litellm tests failed. Is LM Studio running?"
        echo "   To resume tests without reinstalling:"
        echo "       bash $SCRIPT_PATH tests"
        echo ""
        read -p "   Try again? (y/n) " answer
        if [ "$answer" != "y" ]; then
            echo "── Exiting. Run 'bash $SCRIPT_PATH tests' when LM Studio is running."
            exit 1
        fi
    done
}

run_notes_mcp_tests() {
    echo ""
    echo "── Running notes_mcp tests"
    conda run --no-capture-output -n "$PM_ENV" python "$PACKAGES_DIR/notes_mcp_tests/notes_mcp_tests/visit/visit.py"
}

test_phase() {
    run_process_manager_tests
    run_litellm_tests
    run_notes_mcp_tests
}


# ── Entry point ───────────────────────────────────────────────────────

if [ "${1}" == "tests" ]; then
    test_phase
else
    install_phase
    test_phase
fi

echo ""
echo "── Done."
