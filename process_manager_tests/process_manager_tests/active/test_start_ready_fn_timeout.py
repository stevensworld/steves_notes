import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStartReadyFnTimeout(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_start_ready_fn_timeout(self):
        result = self.pm.start("test", long_process(), ready_fn=lambda: False, timeout=2)

        print(f"\n  expected: False — ready_fn never returns True, timeout reached")
        print(f"  actual:   {result}")

        self.assertFalse(result)
