import os
from steves_notes import Builder

_builder = None


def get_builder() -> Builder:
    global _builder
    if _builder is None:
        notes_file = os.environ.get("NOTES_FILE", "notes.json")
        _builder = Builder(filename=notes_file)
    return _builder


def new_objective(name: str, description: str = ""):
    """Create a new top-level objective (module)."""
    builder = get_builder()
    builder.root.name = name
    if description:
        builder.root.metadata["description"] = description
    builder.save_state()
    print(f"Objective set: [{builder.root.node_id}] {builder.root.name}")
    builder.show_tree()


def rename_objective(new_name: str):
    """Rename the current objective (module)."""
    builder = get_builder()
    builder.rename_module(new_name)
    print(f"Objective renamed to: {new_name}")
    builder.show_tree()


def new_subtopic(name: str, description: str = ""):
    """Create a new subtopic (objective) under the current objective."""
    builder = get_builder()
    node = builder.add_objective(name=name, description=description)
    print(f"Subtopic created: [{node.node_id}] {node.name}")
    builder.show_tree()


def rename_subtopic(node_id: str, new_name: str):
    """Rename a subtopic by node_id."""
    builder = get_builder()
    if builder.set_active_by_id(node_id):
        builder.rename_current_objective(new_name)
        print(f"Subtopic [{node_id}] renamed to: {new_name}")
        builder.show_tree()
    else:
        print(f"No subtopic found with id: {node_id}")


def set_subtopic(node_id: str):
    """Set the active subtopic context by node_id."""
    builder = get_builder()
    if builder.set_active_by_id(node_id):
        print(f"Active subtopic: [{node_id}] {builder.current_parent.name}")
    else:
        print(f"No subtopic found with id: {node_id}")


def list_subtopics():
    """List all subtopics (objectives) with their node IDs."""
    builder = get_builder()
    subtopics = [c for c in builder.root.children if c.node_type == "objective"]
    if not subtopics:
        print("No subtopics found.")
        return
    active_id = builder.current_parent.node_id
    for st in subtopics:
        marker = ">" if st.node_id == active_id else " "
        thought_count = len([c for c in st.children if c.node_type == "note"])
        print(f"  {marker} [{st.node_id}] {st.name}  ({thought_count} thoughts)")


def show_tree():
    """Print the full note tree."""
    get_builder().show_tree()
