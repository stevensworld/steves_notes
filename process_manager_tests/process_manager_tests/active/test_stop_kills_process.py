import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStopKillsProcess(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_stop_kills_process(self):
        self.pm.start("test", long_process())
        self.pm.stop("test")
        running = self.pm.status("test")["running"]

        print(f"\n  expected: running=False after stop")
        print(f"  actual:   running={running}")

        self.assertFalse(running)
