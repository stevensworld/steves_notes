import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStartReadyFnTrueImmediately(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_start_ready_fn_true_immediately(self):
        result = self.pm.start("test", long_process(), ready_fn=lambda: True, timeout=5)

        print(f"\n  expected: True — ready_fn returns True immediately")
        print(f"  actual:   {result}")

        self.assertTrue(result)
