import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time; time.sleep(60)"]


class TestStopAll(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_stop_all_stops_multiple_processes(self):
        self.pm.start("a", long_process())
        self.pm.start("b", long_process())
        self.pm.start("c", long_process())
        self.pm.stop_all()
        self.assertFalse(self.pm.status("a")["running"])
        self.assertFalse(self.pm.status("b")["running"])
        self.assertFalse(self.pm.status("c")["running"])

    def test_stop_all_on_empty_is_silent(self):
        self.pm.stop_all()
