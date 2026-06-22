from process_manager_tests.lib.base_test import BaseTest


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestRestart(BaseTest):

    description = "proves restart() stops the old process and starts a new one with a different pid — spawns a real process"
    expected = "new pid after restart, running=True"

    def test_restart(self):
        self.pm.start("test", long_process())
        pid_before = self.pm.status("test")["pid"]
        self.pm.restart("test")
        pid_after = self.pm.status("test")["pid"]
        self.assertNotEqual(pid_before, pid_after)
        self.assertTrue(self.pm.status("test")["running"])
