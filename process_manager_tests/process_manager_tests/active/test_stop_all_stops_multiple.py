import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStopAllStopsMultiple(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_stop_all_stops_multiple(self):
        self.pm.start("a", long_process())
        self.pm.start("b", long_process())
        self.pm.start("c", long_process())
        self.pm.stop_all()

        a = self.pm.status("a")["running"]
        b = self.pm.status("b")["running"]
        c = self.pm.status("c")["running"]

        print(f"\n  expected: a=False, b=False, c=False after stop_all")
        print(f"  actual:   a={a}, b={b}, c={c}")

        self.assertFalse(a)
        self.assertFalse(b)
        self.assertFalse(c)
