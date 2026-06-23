"""
notes_mcp server — exposes NoteNode tree operations as MCP tools.

All configuration lives in the CONFIG block at the top of this file.
"""

import io
import json
import os
from contextlib import redirect_stdout
from mcp.server.fastmcp import FastMCP
from steves_notes import Builder, setup_workspace
from note_iterator import NoteIterator


# ── Configuration ─────────────────────────────────────────────────────

CONFIG = {
    "notes_file":    os.environ.get("NOTES_FILE", "notes.json"),
    "module_id":     "mod_01",
    "module_name":   "Electrical Systems",
    "server_name":   "Note Tree Builder",
}

# ── Server setup ──────────────────────────────────────────────────────

mcp      = FastMCP(CONFIG["server_name"])
builder  = setup_workspace(filename=CONFIG["notes_file"])
iterator = NoteIterator(builder.root)


# ── Tools ─────────────────────────────────────────────────────────────

@mcp.tool()
def show_visual_tree() -> str:
    """Returns a visual terminal-style text layout of the structural modules and objectives."""
    f = io.StringIO()
    with redirect_stdout(f):
        builder.show_tree()
    return f.getvalue()


@mcp.tool()
def create_new_objective(name: str, description: str = "") -> str:
    """Creates a new objective node under the module root and shifts active focus to it."""
    new_node = builder.add_objective(name=name, description=description)
    return f"✅ Objective successfully created: {new_node.name} ({new_node.node_id}). Context locked."


@mcp.tool()
def append_note_to_active_context(name: str, topic: str, text: str, tag: str, raw_source: str = "") -> str:
    """Appends an individual content note under the currently locked objective parent context."""
    node = builder.add_note(name=name, topic=topic, text=text, tag=tag, raw_source=raw_source)
    if node is None:
        return "🚫 Blocked: A note with matching text content already exists in this module hierarchy."
    return f"📝 Note appended successfully: '{node.name}' under active parent '{builder.current_parent.name}'."


@mcp.tool()
def change_active_context_id(node_id: str) -> str:
    """Shifts the builder's operational context pointer to the node matching the given ID."""
    success = builder.set_active_by_id(node_id)
    if success:
        return f"🎯 Context shifted successfully. Currently locked onto: [{builder.current_parent.node_type.upper()}] {builder.current_parent.name}"
    return f"❌ Target Error: No node found matching identifier sequence '{node_id}'."


@mcp.tool()
def rename_active_objective(new_name: str) -> str:
    """Renames the currently selected target objective context name safely."""
    success = builder.rename_current_objective(new_name)
    if success:
        return f"✏️ Target node renamed successfully to: '{new_name}'"
    return "⚠️ Failed: The active system parent context is not set to an objective node type."


@mcp.tool()
def get_next_note() -> str:
    """Returns the next note in depth-first tree order and advances the cursor."""
    result = iterator.get_next()
    if result is None:
        return f"✅ All {iterator.total} notes visited. Call new_iterator to start over."
    return json.dumps(result, indent=2)


@mcp.tool()
def new_iterator() -> str:
    """Creates a fresh iterator, re-indexing the tree from disk."""
    global iterator
    iterator = NoteIterator(builder.root)
    return f"🔄 New iterator ready. {iterator.total} notes indexed."


@mcp.tool()
def append_note_to_node(node_id: str, name: str, topic: str, text: str, tag: str, raw_source: str = "") -> str:
    """Appends a note as a child of any node in the tree, targeted by its ID."""
    node = builder.append_note_to_node(
        node_id=node_id, name=name, topic=topic, text=text, tag=tag, raw_source=raw_source
    )
    if node is None:
        return f"❌ Failed: No node found with ID '{node_id}', or duplicate content detected."
    return f"📎 Note '{node.name}' ({node.node_id}) appended to node '{node_id}'."


# ── Entry point ───────────────────────────────────────────────────────

def run_server():
    mcp.run()
