from process_manager_tests.lib.base_test import BaseTest


def long_process():
    return ["python", "-c", "import time\nwhile True: time.sleep(0.001)"]


class TestStopKillsProcess(BaseTest):

    description = "proves stop() kills a running process — spawns a real process, expect a few seconds"
    expected = "running=False after stop"

    def test_stop_kills_process(self):
        self.pm.start("test", long_process())
        self.pm.stop("test")
        running = self.pm.status("test")["running"]
        self.assertFalse(running)
