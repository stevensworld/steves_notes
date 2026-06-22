import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStatusRunning(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_status_running(self):
        self.pm.start("test", long_process())
        s = self.pm.status("test")

        print(f"\n  expected: name='test', running=True, pid not None, started_at not None")
        print(f"  actual:   name={s['name']}, running={s['running']}, pid={s['pid']}, started_at={s['started_at']}")

        self.assertEqual(s["name"], "test")
        self.assertTrue(s["running"])
        self.assertIsNotNone(s["pid"])
        self.assertIsNotNone(s["started_at"])
