import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time; time.sleep(60)"]


def make_manager(tmpdir):
    return ProcessManager(pid_dir=os.path.join(tmpdir, "pids"))


class TestStopAll(unittest.TestCase):

    def test_stop_all_stops_multiple_processes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.start("a", long_process())
            pm.start("b", long_process())
            pm.start("c", long_process())
            pm.stop_all()
            self.assertFalse(pm.status("a")["running"])
            self.assertFalse(pm.status("b")["running"])
            self.assertFalse(pm.status("c")["running"])

    def test_stop_all_on_empty_is_silent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pm = make_manager(tmpdir)
            pm.stop_all()
