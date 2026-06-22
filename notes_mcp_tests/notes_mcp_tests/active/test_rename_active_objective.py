from notes_mcp_tests.lib.base_test import BaseTest
from notes_mcp.server import rename_active_objective


class TestRenameActiveObjective(BaseTest):
    description = "proves rename_active_objective() renames the current objective and returns success"
    expected = "string containing 'renamed successfully'"

    def test_rename_active_objective(self):
        result = rename_active_objective("Renamed Objective")
        self.assertIn("renamed successfully", result)
