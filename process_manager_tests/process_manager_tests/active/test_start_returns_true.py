from process_manager_tests.lib.base_test import BaseTest


def instant_process():
    return ["python", "-c", "import sys; sys.exit(0)"]


class TestStartReturnsTrue(BaseTest):

    description = "proves start() launches a process and returns True"
    expected = "True"

    def test_start_returns_true(self):
        result = self.pm.start("test", instant_process())
        self.assertTrue(result)
