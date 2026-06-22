"""
notes_mcp — FastMCP server exposing the NoteNode tree as tools.

Usage:
    from notes_mcp import run_server

    run_server()
"""

from .server import run_server

__all__ = ["run_server"]
