#!/usr/bin/env python3
import subprocess
import sys
import os

script = os.path.join(
    os.path.dirname(__file__),
    "../notes_mcp_tests/notes_mcp_tests/debug/speak_notes.py"
)
subprocess.run([sys.executable, script])
