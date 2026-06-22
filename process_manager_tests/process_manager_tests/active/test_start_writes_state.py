import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStartWritesState(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_start_writes_state(self):
        self.pm.start("test", long_process())
        state = self.pm._state.read("test")

        print(f"\n  expected: state not None, pid not None")
        print(f"  actual:   state={state is not None}, pid={state['pid'] if state else None}")

        self.assertIsNotNone(state)
        self.assertIsNotNone(state["pid"])
