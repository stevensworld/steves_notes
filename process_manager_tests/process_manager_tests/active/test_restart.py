import os
import tempfile
import unittest

from process_manager import ProcessManager, ProcessNotFoundError


def long_process():
    return ["python", "-c", "import time; time.sleep(60)"]


def make_manager(tmpdir):
    return ProcessManager(pid_dir=os.path.join(tmpdir, "pids"))


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
