from process_manager_tests.lib.base_test import BaseTest


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStatusRunning(BaseTest):

    description = "proves status() reports running=True with pid and started_at after start() — spawns a real process"
    expected = "running=True, pid not None, started_at not None"

    def test_status_running(self):
        self.pm.start("test", long_process())
        s = self.pm.status("test")
        self.assertTrue(s["running"])
        self.assertIsNotNone(s["pid"])
        self.assertIsNotNone(s["started_at"])
