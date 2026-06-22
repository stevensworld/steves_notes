import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time; time.sleep(60)"]


class TestStatePersistence(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pid_dir = os.path.join(self.tmpdir.name, "pids")
        self.pm = ProcessManager(pid_dir=self.pid_dir)

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_status_readable_by_new_instance(self):
        self.pm.start("test", long_process())
        pid = self.pm.status("test")["pid"]

        pm2 = ProcessManager(pid_dir=self.pid_dir)
        self.assertEqual(pm2.status("test")["pid"], pid)
        pm2.stop("test")

    def test_stop_by_new_instance(self):
        self.pm.start("test", long_process())

        pm2 = ProcessManager(pid_dir=self.pid_dir)
        pm2.stop("test")
        self.assertFalse(pm2.status("test")["running"])
