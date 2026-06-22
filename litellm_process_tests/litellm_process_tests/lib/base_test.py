import os
import tempfile
import unittest

from litellm_process import LiteLLMProcess

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/litellm_config.json")


class BaseTest(unittest.TestCase):

    description = "no description provided"
    expected = "no expected value provided"

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.proxy = LiteLLMProcess(config={
            "pid_directory": os.path.join(self.tmpdir.name, "pids"),
            "litellm_config_path": _CONFIG_PATH,
        })

    def tearDown(self):
        self.proxy.stop()
        self.tmpdir.cleanup()

    def get_description(self):
        return self.description

    def get_expected(self):
        return self.expected
