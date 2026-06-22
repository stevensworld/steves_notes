from litellm_process_tests.lib.base_test import BaseTest


class TestStart(BaseTest):

    description = "proves the LiteLLM proxy starts and passes the health check — requires LM Studio running, expect 30s+"
    expected = "start() returns True, proxy reachable at /health"

    def test_start(self):
        result = self.proxy.start()
        self.assertTrue(result)
