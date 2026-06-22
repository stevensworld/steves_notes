from litellm_process_tests.lib.base_test import BaseTest


class TestStatus(BaseTest):

    description = "proves status() reports running=True with pid and started_at after start() — requires LM Studio running, expect 30s+"
    expected = "running=True, pid not None, started_at not None"

    def test_status(self):
        self.proxy.start()
        s = self.proxy.status()
        self.assertTrue(s["running"])
        self.assertIsNotNone(s["pid"])
        self.assertIsNotNone(s["started_at"])
