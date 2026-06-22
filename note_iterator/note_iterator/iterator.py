from typing import Optional, List, Dict, Any
from steves_notes import NoteNode


class NoteIterator:
    """
    Walks a NoteNode tree depth-first, yielding one note node at a time.
    Maintains a cursor so callers can advance incrementally across LLM calls.
    """

    def __init__(self, root: NoteNode):
        self._notes: List[NoteNode] = []
        self._context: Dict[str, str] = {}
        self._cursor: int = 0
        self._index(root, parent_objective=None)

    def _index(self, node: NoteNode, parent_objective: Optional[str]):
        if node.node_type == "objective":
            parent_objective = node.name
        if node.node_type == "note":
            self._notes.append(node)
            self._context[node.node_id] = parent_objective or ""
        for child in node.children:
            self._index(child, parent_objective)

    def reset(self):
        self._cursor = 0

    @property
    def total(self) -> int:
        return len(self._notes)

    @property
    def position(self) -> int:
        return self._cursor

    def get_next(self) -> Optional[Dict[str, Any]]:
        if self._cursor >= len(self._notes):
            return None
        note = self._notes[self._cursor]
        self._cursor += 1
        return {
            "node_id":   note.node_id,
            "name":      note.name,
            "objective": self._context.get(note.node_id, ""),
            "topic":     note.metadata.get("topic", ""),
            "text":      note.metadata.get("text_content", ""),
            "tag":       note.metadata.get("tag", ""),
            "position":  self._cursor,
            "total":     self.total,
        }

    def peek(self) -> Optional[Dict[str, Any]]:
        """Returns the current note without advancing the cursor."""
        if self._cursor >= len(self._notes):
            return None
        note = self._notes[self._cursor]
        return {
            "node_id":   note.node_id,
            "name":      note.name,
            "objective": self._context.get(note.node_id, ""),
            "topic":     note.metadata.get("topic", ""),
            "text":      note.metadata.get("text_content", ""),
            "tag":       note.metadata.get("tag", ""),
            "position":  self._cursor + 1,
            "total":     self.total,
        }
