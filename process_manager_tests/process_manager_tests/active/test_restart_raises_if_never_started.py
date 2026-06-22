import os
import tempfile
import unittest
from process_manager import ProcessManager, ProcessNotFoundError


class TestRestartRaisesIfNeverStarted(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_restart_raises_if_never_started(self):
        print(f"\n  expected: ProcessNotFoundError raised for unknown process")

        try:
            self.pm.restart("nonexistent")
            print(f"  actual:   no exception raised — UNEXPECTED")
            self.fail("Expected ProcessNotFoundError")
        except ProcessNotFoundError:
            print(f"  actual:   ProcessNotFoundError raised")
