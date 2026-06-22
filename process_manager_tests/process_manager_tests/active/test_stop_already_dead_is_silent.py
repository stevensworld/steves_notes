import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStopAlreadyDeadIsSilent(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_stop_already_dead_is_silent(self):
        self.pm.start("test", long_process())
        self.pm.stop("test")

        print(f"\n  expected: no exception when stopping already dead process")

        try:
            self.pm.stop("test")
            print(f"  actual:   no exception raised")
        except Exception as e:
            print(f"  actual:   exception raised: {e}")
            raise
