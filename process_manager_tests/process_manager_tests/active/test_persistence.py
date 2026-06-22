import os
import tempfile
from process_manager import ProcessManager
from process_manager_tests.lib.base_test import BaseTest


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestPersistence(BaseTest):

    description = "proves a second ProcessManager instance can read state and stop a process started by a different instance"
    expected = "running=False after stop by new instance"

    def test_persistence(self):
        self.pm.start("test", long_process())
        pid = self.pm.status("test")["pid"]

        pm2 = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))
        self.assertEqual(pm2.status("test")["pid"], pid)
        pm2.stop("test")
        self.assertFalse(pm2.status("test")["running"])
