#!/bin/bash

echo "── Stopping Kokoro server..."
pkill -f "kokoro-server" 2>/dev/null || true

echo "── Starting Kokoro server..."
python "$(dirname "$0")/start_kokoro.py"
