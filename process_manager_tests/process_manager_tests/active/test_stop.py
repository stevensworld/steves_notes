import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStop(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_stop_kills_process(self):
        self.pm.start("test", long_process())
        self.pm.stop("test")
        self.assertFalse(self.pm.status("test")["running"])

    def test_stop_clears_state(self):
        self.pm.start("test", long_process())
        self.pm.stop("test")
        self.assertIsNone(self.pm._state.read("test"))

    def test_stop_unknown_process_is_silent(self):
        self.pm.stop("nonexistent")

    def test_stop_already_dead_process_is_silent(self):
        self.pm.start("test", long_process())
        self.pm.stop("test")
        self.pm.stop("test")
