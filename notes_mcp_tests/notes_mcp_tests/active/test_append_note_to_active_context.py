from notes_mcp_tests.lib.base_test import BaseTest
from notes_mcp.server import append_note_to_active_context


class TestAppendNoteToActiveContext(BaseTest):
    description = "proves append_note_to_active_context() adds a note and returns a success message"
    expected = "string containing 'Note appended successfully'"

    def test_append_note_to_active_context(self):
        result = append_note_to_active_context(
            name="Test Note", topic="testing", text="unique test content", tag="test"
        )
        self.assertIn("Note appended successfully", result)
