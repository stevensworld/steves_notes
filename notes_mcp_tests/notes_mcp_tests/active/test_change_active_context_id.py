from notes_mcp_tests.lib.base_test import BaseTest
from notes_mcp.server import change_active_context_id


class TestChangeActiveContextId(BaseTest):
    description = "proves change_active_context_id() shifts context to a valid node id"
    expected = "string containing 'Context shifted successfully'"

    def test_change_active_context_id(self):
        result = change_active_context_id("obj_01")
        self.assertIn("Context shifted successfully", result)
