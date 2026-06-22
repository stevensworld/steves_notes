import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time; time.sleep(60)"]


def make_manager(tmpdir):
    return ProcessManager(pid_dir=os.path.join(tmpdir, "pids"))


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
