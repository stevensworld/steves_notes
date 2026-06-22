"""
ProcessState — reads and writes per-process JSON state files.

Each process gets one file: {pid_dir}/{name}.json
Contents: pid, command, started_at (ISO timestamp).
"""

import json
import os
from datetime import datetime


class ProcessState:
    """Persists process state to disk so ProcessManager survives script restarts."""

    def __init__(self, pid_dir: str):
        self._pid_dir = os.path.abspath(pid_dir)
        os.makedirs(self._pid_dir, exist_ok=True)

    def path(self, name: str) -> str:
        return os.path.join(self._pid_dir, f"{name}.json")

    def write(self, name: str, pid: int, command: list) -> None:
        with open(self.path(name), "w") as f:
            json.dump({"pid": pid, "command": command, "started_at": datetime.now().isoformat()}, f, indent=2)

    def read(self, name: str) -> dict | None:
        path = self.path(name)
        if not os.path.exists(path):
            return None
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return None

    def clear(self, name: str) -> None:
        path = self.path(name)
        if os.path.exists(path):
            os.remove(path)

    def all_names(self) -> list:
        return [f[:-5] for f in os.listdir(self._pid_dir) if f.endswith(".json")]
