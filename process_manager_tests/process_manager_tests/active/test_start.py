import os
import tempfile
import unittest

from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStart(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_start_returns_true(self):
        result = self.pm.start("test", long_process())
        self.assertTrue(result)

    def test_start_writes_state(self):
        self.pm.start("test", long_process())
        state = self.pm._state.read("test")
        self.assertIsNotNone(state)
        self.assertIsNotNone(state["pid"])

    def test_start_process_is_alive(self):
        self.pm.start("test", long_process())
        self.assertTrue(self.pm.status("test")["running"])

    def test_start_already_running_returns_true_without_restart(self):
        self.pm.start("test", long_process())
        pid_before = self.pm.status("test")["pid"]
        self.pm.start("test", long_process())
        pid_after = self.pm.status("test")["pid"]
        self.assertEqual(pid_before, pid_after)

    def test_start_with_ready_fn_true_immediately(self):
        result = self.pm.start("test", long_process(), ready_fn=lambda: True, timeout=5)
        self.assertTrue(result)

    def test_start_with_ready_fn_timeout(self):
        result = self.pm.start("test", long_process(), ready_fn=lambda: False, timeout=2)
        self.assertFalse(result)
