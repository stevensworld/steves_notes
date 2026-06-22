from notes_mcp_tests.lib.base_test import BaseTest
from notes_mcp.server import append_note_to_node


class TestAppendNoteToNode(BaseTest):
    description = "proves append_note_to_node() adds a note to a specific node by id"
    expected = "string containing 'appended to node'"

    def test_append_note_to_node(self):
        result = append_note_to_node(
            node_id="obj_01", name="Targeted Note", topic="topic",
            text="targeted note content", tag="tag"
        )
        self.assertIn("appended to node", result)
