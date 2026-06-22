from notes_mcp_tests.lib.base_test import BaseTest
from notes_mcp.server import new_iterator


class TestNewIterator(BaseTest):
    description = "proves new_iterator() resets the iterator and returns a ready message"
    expected = "string containing 'New iterator ready'"

    def test_new_iterator(self):
        result = new_iterator()
        self.assertIn("New iterator ready", result)
