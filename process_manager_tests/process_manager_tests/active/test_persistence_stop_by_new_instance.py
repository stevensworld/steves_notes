import os
import tempfile
import unittest
from process_manager import ProcessManager


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestPersistenceStopByNewInstance(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pid_dir = os.path.join(self.tmpdir.name, "pids")
        self.pm = ProcessManager(pid_dir=self.pid_dir)

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def test_persistence_stop_by_new_instance(self):
        self.pm.start("test", long_process())

        pm2 = ProcessManager(pid_dir=self.pid_dir)
        pm2.stop("test")
        running = pm2.status("test")["running"]

        print(f"\n  expected: running=False — stopped by a different instance")
        print(f"  actual:   running={running}")

        self.assertFalse(running)
