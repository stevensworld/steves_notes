import os
import tempfile
import unittest

from process_manager import ProcessManager, ProcessNotFoundError


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestRestart(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_restart_gives_new_pid(self):
        self.pm.start("test", long_process())
        pid_before = self.pm.status("test")["pid"]
        self.pm.restart("test")
        pid_after = self.pm.status("test")["pid"]
        self.assertNotEqual(pid_before, pid_after)

    def test_restart_process_is_alive_after(self):
        self.pm.start("test", long_process())
        self.pm.restart("test")
        self.assertTrue(self.pm.status("test")["running"])

    def test_restart_raises_if_never_started(self):
        with self.assertRaises(ProcessNotFoundError):
            self.pm.restart("nonexistent")
