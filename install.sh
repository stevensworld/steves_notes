#!/bin/bash

set -e

REPO_URL="https://github.com/stevensworld/steves_notes.git"
WORK_DIR="$(pwd)/testexecute"
mkdir -p "$WORK_DIR"

echo "── Working directory: $WORK_DIR"

cat > "$WORK_DIR/uninstall.sh" << 'EOF'
#!/bin/bash
echo "── Removing conda env: prove_process_manager"
conda env remove -n prove_process_manager -y
echo "── Removing cloned repo"
rm -rf "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/steves_notes"
echo "── Done."
EOF
chmod +x "$WORK_DIR/uninstall.sh"
echo "── Uninstall script written to $WORK_DIR/uninstall.sh"

echo "── Cloning $REPO_URL"

git clone "$REPO_URL" "$WORK_DIR/steves_notes"

echo "── Running tests"
bash "$WORK_DIR/steves_notes/tests_context/test_install.sh"

echo "── Done. Repo left at: $WORK_DIR/steves_notes"
