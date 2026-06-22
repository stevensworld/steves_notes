import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStartAlreadyRunningNoRestart(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_start_already_running_no_restart(self):
        self.pm.start("test", long_process())
        pid_before = self.pm.status("test")["pid"]
        self.pm.start("test", long_process())
        pid_after = self.pm.status("test")["pid"]

        print(f"\n  expected: pid unchanged — same process, no restart")
        print(f"  actual:   pid_before={pid_before}, pid_after={pid_after}, same={pid_before == pid_after}")

        self.assertEqual(pid_before, pid_after)
