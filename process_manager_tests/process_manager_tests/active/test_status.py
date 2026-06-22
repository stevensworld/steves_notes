import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time; time.sleep(60)"]


def make_manager(tmpdir):
    return ProcessManager(pid_dir=os.path.join(tmpdir, "pids"))


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
