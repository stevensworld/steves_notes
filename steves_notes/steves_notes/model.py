import os
import json
from typing import List, Dict, Any, Optional

class NoteNode:
    """
    Represents a single node within a hierarchical, tree-structured note system.

    Attributes:
        node_id (str): Unique identifier for the node (e.g., 'mod_01', 'obj_02', 'note_03').
        node_type (str): The structural role of the node. Must be 'module', 'objective', or 'note'.
        name (str): The display title or header of the node.
        metadata (Dict[str, Any]): Key-value pairs containing node-specific details.
        children (List[NoteNode]): Nested child nodes belonging to this node.
    """
    def __init__(self, node_id: str, node_type: str, name: str):
        self.node_id = node_id
        self.node_type = node_type
        self.name = name
        self.metadata: Dict[str, Any] = {}
        self.children: List['NoteNode'] = []

    def add_child(self, child: 'NoteNode') -> 'NoteNode':
        """Appends a child node to this node's children list and returns self for chaining."""
        self.children.append(child)
        return self


class Builder:
    """
    Manages the lifecycle, modification, persistence, and navigation of a tree
    structured JSON data store of study modules, goals, and notes.
    """
    def __init__(self, filename: str = "notes.json", default_mod_id: str = "mod_01", default_mod_name: str = "Electrical Systems"):
        self.filename = filename
        self.root = self._load_or_create(default_mod_id, default_mod_name)
        self.activate_highest_objective()

    def _load_or_create(self, fallback_id: str, fallback_name: str) -> NoteNode:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return self._hydrate(data)
            except Exception as e:
                print(f"⚠️ Error reading file, generating fresh fallback: {e}")

        root_node = NoteNode(fallback_id, "module", fallback_name)
        root_node.metadata = {"module_id": fallback_id, "module_objective": "0"}
        initial_objective = NoteNode("obj_01", "objective", "Objective 1")
        initial_objective.metadata = {"description": "Initial system objective."}
        root_node.add_child(initial_objective)
        self.save_state(root_node)
        return root_node

    def _hydrate(self, data: Dict) -> NoteNode:
        node = NoteNode(data['id'], data.get('type', 'note'), data.get('name', ''))
        node.metadata = data.get('metadata', {})
        if 'make_audio' in data:
            node.make_audio = data['make_audio']
        if node.node_type == "note" and "raw_source_text" not in node.metadata:
            node.metadata["raw_source_text"] = node.metadata.get("text_content", "")
        for child in data.get("children", []):
            node.add_child(self._hydrate(child))
        return node

    def save_state(self, alternate_root: NoteNode = None):
        target_root = alternate_root if alternate_root else self.root
        payload = self._serialize(target_root)
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

    def _serialize(self, node: NoteNode) -> Dict[str, Any]:
        base_dict = {"id": node.node_id, "type": node.node_type, "name": node.name}
        if node.node_type == "note":
            base_dict["make_audio"] = getattr(node, "make_audio", True)
        base_dict["metadata"] = node.metadata
        base_dict["children"] = [self._serialize(c) for c in node.children]
        return base_dict

    def set_active_by_id(self, node_id: str) -> bool:
        found_node = self._find_node_by_id(self.root, node_id)
        if found_node:
            self.current_parent = found_node
            return True
        return False

    def _find_node_by_id(self, current_node: NoteNode, node_id: str) -> Optional[NoteNode]:
        if current_node.node_id == node_id:
            return current_node
        for child in current_node.children:
            result = self._find_node_by_id(child, node_id)
            if result:
                return result
        return None

    def generate_next_id(self, node_type: str) -> str:
        def count_nodes(node: NoteNode, target_type: str) -> int:
            count = 1 if node.node_type == target_type else 0
            for child in node.children:
                count += count_nodes(child, target_type)
            return count
        existing_count = count_nodes(self.root, node_type)
        prefix = {"module": "mod", "objective": "obj", "note": "note"}.get(node_type, "id")
        return f"{prefix}_{existing_count + 1:02d}"

    def _is_duplicate_text(self, current_node: NoteNode, search_text: str) -> bool:
        if current_node.node_type == "note":
            existing_content = current_node.metadata.get("text_content", "").strip().lower()
            if existing_content == search_text.strip().lower():
                return True
        for child in current_node.children:
            if self._is_duplicate_text(child, search_text):
                return True
        return False

    def activate_highest_objective(self) -> bool:
        objectives = [c for c in self.root.children if c.node_type == "objective"]
        if not objectives:
            self.current_parent = self.root
            return False
        def get_id_suffix(node: NoteNode) -> int:
            try:
                return int(node.node_id.split('_')[-1])
            except (ValueError, IndexError):
                return -1
        highest_obj_node = max(objectives, key=get_id_suffix)
        self.current_parent = highest_obj_node
        return True

    def add_objective(self, name: str = "Objective 1", description: str = "") -> NoteNode:
        obj_id = self.generate_next_id("objective")
        new_node = NoteNode(obj_id, "objective", name)
        new_node.metadata = {"description": description}
        self.root.add_child(new_node)
        self.current_parent = new_node
        self.save_state()
        return new_node

    def add_note(self, name: str, topic: str, text: str, tag: str, raw_source: str = "") -> Optional[NoteNode]:
        if self._is_duplicate_text(self.root, text):
            return None
        if self.current_parent.node_type == "module" and self.root.children:
            self.current_parent = self.root.children[-1]
        track_id = self.generate_next_id("note")
        new_node = NoteNode(track_id, "note", name)
        new_node.make_audio = True
        new_node.metadata = {"topic": topic, "text_content": text, "tag": tag, "raw_source_text": raw_source}
        self.current_parent.add_child(new_node)
        self.save_state()
        return new_node

    def append_note_to_node(self, node_id: str, name: str, topic: str, text: str, tag: str, raw_source: str = "") -> Optional[NoteNode]:
        """Appends a note as a child of any node in the tree, targeted by ID."""
        target = self._find_node_by_id(self.root, node_id)
        if target is None:
            return None
        if self._is_duplicate_text(self.root, text):
            return None
        track_id = self.generate_next_id("note")
        new_node = NoteNode(track_id, "note", name)
        new_node.make_audio = True
        new_node.metadata = {"topic": topic, "text_content": text, "tag": tag, "raw_source_text": raw_source}
        target.add_child(new_node)
        self.save_state()
        return new_node

    def rename_current_objective(self, new_name: str) -> bool:
        if self.current_parent and self.current_parent.node_type == "objective":
            self.current_parent.name = new_name
            self.save_state()
            return True
        return False

    def rename_module(self, new_name: str) -> None:
        self.root.name = new_name
        self.save_state()

    @property
    def current_objective_name(self) -> Optional[str]:
        if self.current_parent and self.current_parent.node_type == "objective":
            return self.current_parent.name
        return None

    def show_tree(self, node: NoteNode = None, indent: int = 0):
        if node is None:
            node = self.root
        prefix = "  " * indent
        marker = "📁" if node.node_type == "module" else "🎯" if node.node_type == "objective" else "📝"
        print(f"{prefix}{marker} [{node.node_id}] {node.name} ({node.node_type})")
        for child in node.children:
            self.show_tree(child, indent + 1)


def setup_workspace(filename: str = "notes.json", mod_id: str = "mod_01", mod_name: str = "Electrical Systems") -> Builder:
    """Factory function to instantiate and return a Builder instance."""
    builder_instance = Builder(filename=filename, default_mod_id=mod_id, default_mod_name=mod_name)
    builder_instance.show_tree()
    return builder_instance
