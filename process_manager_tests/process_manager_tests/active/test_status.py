import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStatus(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_status_running(self):
        self.pm.start("test", long_process())
        s = self.pm.status("test")
        self.assertEqual(s["name"], "test")
        self.assertTrue(s["running"])
        self.assertIsNotNone(s["pid"])
        self.assertIsNotNone(s["started_at"])

    def test_status_not_running(self):
        s = self.pm.status("unknown")
        self.assertEqual(s["name"], "unknown")
        self.assertFalse(s["running"])
        self.assertIsNone(s["pid"])
        self.assertIsNone(s["started_at"])

    def test_status_after_stop(self):
        self.pm.start("test", long_process())
        self.pm.stop("test")
        self.assertFalse(self.pm.status("test")["running"])
