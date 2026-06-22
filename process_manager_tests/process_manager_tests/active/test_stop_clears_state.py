import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStopClearsState(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_stop_clears_state(self):
        self.pm.start("test", long_process())
        self.pm.stop("test")
        state = self.pm._state.read("test")

        print(f"\n  expected: state=None after stop")
        print(f"  actual:   state={state}")

        self.assertIsNone(state)
