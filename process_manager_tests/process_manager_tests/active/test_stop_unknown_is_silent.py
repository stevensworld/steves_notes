import os
import tempfile
import unittest
from process_manager import ProcessManager


class TestStopUnknownIsSilent(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_stop_unknown_is_silent(self):
        print(f"\n  expected: no exception when stopping unknown process")

        try:
            self.pm.stop("nonexistent")
            print(f"  actual:   no exception raised")
        except Exception as e:
            print(f"  actual:   exception raised: {e}")
            raise
