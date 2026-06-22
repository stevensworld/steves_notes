import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time; time.sleep(60)"]


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
