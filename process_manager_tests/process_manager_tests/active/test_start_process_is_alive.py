import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStartProcessIsAlive(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_start_process_is_alive(self):
        self.pm.start("test", long_process())
        running = self.pm.status("test")["running"]

        print(f"\n  expected: running=True")
        print(f"  actual:   running={running}")

        self.assertTrue(running)
