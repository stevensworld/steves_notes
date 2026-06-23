from .finesse import finesse
from .workspace import get_builder


def scrap(text: str, topic: str = "", tag: str = "", raw_source: str = ""):
    builder = get_builder()
    active_topic = topic if topic else builder.current_parent.name
    objective = builder.current_parent.name
    source = raw_source if raw_source else text

    print(f"Processing under context: '{objective}'...")
    polished = finesse(text, objective, active_topic)

    next_id = builder.generate_next_id("note")
    title = f"{active_topic} - Segment {next_id.split('_')[-1]}"

    note = builder.add_note(
        name=title,
        topic=active_topic,
        text=polished,
        tag=tag,
        raw_source=source,
    )

    if note:
        print(f"Saved -> [{note.node_id}] {title}")
        builder.show_tree()
    print(polished)


def show_tree():
    get_builder().show_tree()


def new_objective(name: str, description: str = ""):
    builder = get_builder()
    node = builder.add_objective(name=name, description=description)
    print(f"New objective: [{node.node_id}] {node.name}")
    builder.show_tree()


def set_objective(node_id: str):
    builder = get_builder()
    if builder.set_active_by_id(node_id):
        print(f"Context set to: [{node_id}] {builder.current_parent.name}")
    else:
        print(f"No node found with id: {node_id}")
