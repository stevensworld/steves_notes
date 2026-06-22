import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time; time.sleep(60)"]


def make_manager(tmpdir):
    return ProcessManager(pid_dir=os.path.join(tmpdir, "pids"))


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
            pm.stop("nonexistent")

    def test_stop_already_dead_process_is_silent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("test", long_process())
            pm.stop("test")
            pm.stop("test")
