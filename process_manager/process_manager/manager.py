"""
ProcessManager — starts, stops, and monitors named subprocesses.

Processes are detached from the parent session and tracked via JSON state
files in pid_dir. State persists across script restarts, so stop/status
work even if the process was started by a previous invocation.
"""

import os
import signal
import subprocess
import time

from .exceptions import ProcessNotFoundError
from .state import ProcessState


class ProcessManager:
    """Manages named subprocesses with persistent PID state."""

    def __init__(self, pid_dir: str):
        """pid_dir: directory where per-process JSON state files are stored."""
        self._state = ProcessState(pid_dir)

    # ── public ────────────────────────────────────────────────────────

    def start(self, name: str, command: list, ready_fn=None, timeout: int = 30) -> bool:
        """Start a named process. Returns True if running, False if ready check timed out.
        If the process is already alive, returns True immediately without restarting.
        ready_fn: optional callable that returns True when the process is ready to serve.
        """
        state = self._state.read(name)
        if state and self._is_alive(state["pid"]):
            return True

        proc = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,  # detach so process outlives this script
        )
        self._state.write(name, proc.pid, command)

        if ready_fn:
            return self._wait_ready(ready_fn, timeout)
        return True

    def stop(self, name: str, timeout: int = 10) -> None:
        """Stop a named process. Sends SIGTERM, waits, then SIGKILL if unresponsive.
        Silent if the process is not running or was never started.
        """
        state = self._state.read(name)
        if not state:
            return
        pid = state["pid"]
        if self._is_alive(pid):
            try:
                os.kill(pid, signal.SIGTERM)
                for _ in range(timeout * 20):
                    time.sleep(0.05)
                    if not self._is_alive(pid):
                        break
                else:
                    os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self._state.clear(name)

    def restart(self, name: str, ready_fn=None, timeout: int = 30) -> bool:
        """Stop then start a named process using its previously recorded command.
        Raises ProcessNotFoundError if no state exists for this name.
        """
        state = self._state.read(name)
        if not state:
            raise ProcessNotFoundError(name)
        command = state["command"]
        self.stop(name)
        return self.start(name, command, ready_fn=ready_fn, timeout=timeout)

    def status(self, name: str) -> dict:
        """Return a status dict for a named process.
        Keys: name, running (bool), pid (int or None), started_at (ISO string or None).
        """
        state = self._state.read(name)
        if not state:
            return {"name": name, "running": False, "pid": None, "started_at": None}
        alive = self._is_alive(state["pid"])
        return {
            "name":       name,
            "running":    alive,
            "pid":        state["pid"] if alive else None,
            "started_at": state.get("started_at"),
        }

    def stop_all(self) -> None:
        """Stop all processes that have a state file in pid_dir."""
        for name in self._state.all_names():
            self.stop(name)

    # ── private ───────────────────────────────────────────────────────

    def _is_alive(self, pid: int) -> bool:
        """Check if a PID is alive by sending signal 0 (no-op probe)."""
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True  # process exists but is owned by another user

    def _wait_ready(self, ready_fn, timeout: int) -> bool:
        """Poll ready_fn once per second up to timeout seconds."""
        for _ in range(timeout):
            time.sleep(1)
            if ready_fn():
                return True
        return False
