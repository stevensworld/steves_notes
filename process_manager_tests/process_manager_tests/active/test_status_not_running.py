import os
import tempfile
import unittest
from process_manager import ProcessManager


class TestStatusNotRunning(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_status_not_running(self):
        s = self.pm.status("unknown")

        print(f"\n  expected: name='unknown', running=False, pid=None, started_at=None")
        print(f"  actual:   name={s['name']}, running={s['running']}, pid={s['pid']}, started_at={s['started_at']}")

        self.assertEqual(s["name"], "unknown")
        self.assertFalse(s["running"])
        self.assertIsNone(s["pid"])
        self.assertIsNone(s["started_at"])
