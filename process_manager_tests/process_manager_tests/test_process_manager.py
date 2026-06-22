"""
Tests for ProcessManager.

No mocks. All tests use real processes and real files.
Each test gets its own temporary directory — nothing bleeds between tests.
"""

import json
import os
import tempfile
import time
import unittest

from process_manager import ProcessManager, ProcessNotFoundError
from process_manager.state import ProcessState


# ── Helpers ───────────────────────────────────────────────────────────

def long_process():
    """A real process that runs until killed."""
    return ["python", "-c", "import time; time.sleep(60)"]


def make_manager(tmpdir):
    return ProcessManager(pid_dir=os.path.join(tmpdir, "pids"))


# ── ProcessState ──────────────────────────────────────────────────────

class TestProcessState(unittest.TestCase):

    def test_write_and_read(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("test", 12345, ["python", "foo.py"])
            result = state.read("test")
            self.assertEqual(result["pid"], 12345)
            self.assertEqual(result["command"], ["python", "foo.py"])
            self.assertIn("started_at", result)

    def test_read_returns_none_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            self.assertIsNone(state.read("nonexistent"))

    def test_clear_removes_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("test", 12345, ["python", "foo.py"])
            state.clear("test")
            self.assertIsNone(state.read("test"))

    def test_clear_silent_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.clear("nonexistent")  # should not raise

    def test_all_names_returns_all(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("a", 1, [])
            state.write("b", 2, [])
            state.write("c", 3, [])
            names = state.all_names()
            self.assertCountEqual(names, ["a", "b", "c"])

    def test_all_names_empty_when_no_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            self.assertEqual(state.all_names(), [])

    def test_read_returns_none_on_corrupt_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            with open(state.path("bad"), "w") as f:
                f.write("not valid json {{{")
            self.assertIsNone(state.read("bad"))


# ── ProcessManager.start ──────────────────────────────────────────────

class TestStart(unittest.TestCase):

    def test_start_returns_true(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            result = pm.start("test", long_process())
            self.assertTrue(result)
            pm.stop("test")

    def test_start_writes_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            state = pm._state.read("test")
            self.assertIsNotNone(state)
            self.assertIsNotNone(state["pid"])
            pm.stop("test")

    def test_start_process_is_alive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            self.assertTrue(pm.status("test")["running"])
            pm.stop("test")

    def test_start_already_running_returns_true_without_restart(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            pid_before = pm.status("test")["pid"]
            pm.start("test", long_process())
            pid_after = pm.status("test")["pid"]
            self.assertEqual(pid_before, pid_after)
            pm.stop("test")

    def test_start_with_ready_fn_true_immediately(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            result = pm.start("test", long_process(), ready_fn=lambda: True, timeout=5)
            self.assertTrue(result)
            pm.stop("test")

    def test_start_with_ready_fn_timeout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            result = pm.start("test", long_process(), ready_fn=lambda: False, timeout=2)
            self.assertFalse(result)
            pm.stop("test")


# ── ProcessManager.stop ───────────────────────────────────────────────

class TestStop(unittest.TestCase):

    def test_stop_kills_process(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            pm.stop("test")
            self.assertFalse(pm.status("test")["running"])

    def test_stop_clears_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            pm.stop("test")
            self.assertIsNone(pm._state.read("test"))

    def test_stop_unknown_process_is_silent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.stop("nonexistent")  # should not raise

    def test_stop_already_dead_process_is_silent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            pm.stop("test")
            pm.stop("test")  # second stop should not raise


# ── ProcessManager.restart ────────────────────────────────────────────

class TestRestart(unittest.TestCase):

    def test_restart_gives_new_pid(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            pid_before = pm.status("test")["pid"]
            pm.restart("test")
            pid_after = pm.status("test")["pid"]
            self.assertNotEqual(pid_before, pid_after)
            pm.stop("test")

    def test_restart_process_is_alive_after(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            pm.restart("test")
            self.assertTrue(pm.status("test")["running"])
            pm.stop("test")

    def test_restart_raises_if_never_started(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            with self.assertRaises(ProcessNotFoundError):
                pm.restart("nonexistent")


# ── ProcessManager.status ─────────────────────────────────────────────

class TestStatus(unittest.TestCase):

    def test_status_running(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            s = pm.status("test")
            self.assertEqual(s["name"], "test")
            self.assertTrue(s["running"])
            self.assertIsNotNone(s["pid"])
            self.assertIsNotNone(s["started_at"])
            pm.stop("test")

    def test_status_not_running(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            s = pm.status("unknown")
            self.assertEqual(s["name"], "unknown")
            self.assertFalse(s["running"])
            self.assertIsNone(s["pid"])
            self.assertIsNone(s["started_at"])

    def test_status_after_stop(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            pm.stop("test")
            self.assertFalse(pm.status("test")["running"])


# ── ProcessManager.stop_all ───────────────────────────────────────────

class TestStopAll(unittest.TestCase):

    def test_stop_all_stops_multiple_processes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("a", long_process())
            pm.start("b", long_process())
            pm.start("c", long_process())
            pm.stop_all()
            self.assertFalse(pm.status("a")["running"])
            self.assertFalse(pm.status("b")["running"])
            self.assertFalse(pm.status("c")["running"])

    def test_stop_all_on_empty_is_silent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.stop_all()  # should not raise


# ── State persistence across instances ───────────────────────────────

class TestStatePersistence(unittest.TestCase):

    def test_status_readable_by_new_instance(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pid_dir = os.path.join(tmpdir, "pids")
            pm1 = ProcessManager(pid_dir=pid_dir)
            pm1.start("test", long_process())
            pid = pm1.status("test")["pid"]

            pm2 = ProcessManager(pid_dir=pid_dir)
            self.assertEqual(pm2.status("test")["pid"], pid)
            pm2.stop("test")

    def test_stop_by_new_instance(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pid_dir = os.path.join(tmpdir, "pids")
            pm1 = ProcessManager(pid_dir=pid_dir)
            pm1.start("test", long_process())

            pm2 = ProcessManager(pid_dir=pid_dir)
            pm2.stop("test")
            self.assertFalse(pm2.status("test")["running"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
