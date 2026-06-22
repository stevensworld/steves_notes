from notes_mcp_tests.lib.base_test import BaseTest
from notes_mcp.server import append_note_to_active_context, get_next_note


class TestGetNextNote(BaseTest):
    description = "proves get_next_note() returns a note after one has been added"
    expected = "JSON string with note data"

    def test_get_next_note(self):
        append_note_to_active_context(
            name="Note A", topic="topic", text="some note text", tag="tag"
        )
        result = get_next_note()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
