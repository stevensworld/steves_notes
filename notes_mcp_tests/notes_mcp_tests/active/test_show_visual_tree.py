from notes_mcp_tests.lib.base_test import BaseTest
from notes_mcp.server import show_visual_tree


class TestShowVisualTree(BaseTest):
    description = "proves show_visual_tree() returns a non-empty string containing the module root"
    expected = "string containing module name"

    def test_show_visual_tree(self):
        result = show_visual_tree()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
