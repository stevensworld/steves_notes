from notes_mcp_tests.lib.base_test import BaseTest
from notes_mcp.server import create_new_objective


class TestCreateNewObjective(BaseTest):
    description = "proves create_new_objective() adds an objective and returns a success message"
    expected = "string containing 'Objective successfully created'"

    def test_create_new_objective(self):
        result = create_new_objective(name="Test Objective", description="a test")
        self.assertIn("Objective successfully created", result)
