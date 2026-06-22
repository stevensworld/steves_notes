import os
import tempfile
import unittest
from process_manager import ProcessManager


class TestStopAllEmptyIsSilent(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_stop_all_empty_is_silent(self):
        print(f"\n  expected: no exception when stop_all called with no processes")

        try:
            self.pm.stop_all()
            print(f"  actual:   no exception raised")
        except Exception as e:
            print(f"  actual:   exception raised: {e}")
            raise
