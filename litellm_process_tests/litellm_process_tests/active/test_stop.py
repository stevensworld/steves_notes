from litellm_process_tests.lib.base_test import BaseTest


class TestStop(BaseTest):

    description = "proves the LiteLLM proxy stops cleanly — requires LM Studio running, expect 30s+"
    expected = "running=False after stop"

    def test_stop(self):
        self.proxy.start()
        self.proxy.stop()
        self.assertFalse(self.proxy.status()["running"])
