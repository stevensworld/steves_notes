import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestRestartProcessAliveAfter(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_restart_process_alive_after(self):
        self.pm.start("test", long_process())
        self.pm.restart("test")
        running = self.pm.status("test")["running"]

        print(f"\n  expected: running=True after restart")
        print(f"  actual:   running={running}")

        self.assertTrue(running)
