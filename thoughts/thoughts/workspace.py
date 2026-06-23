import os
from steves_notes import Builder

_builder = None


def get_builder() -> Builder:
    global _builder
    if _builder is None:
        notes_file = os.environ.get("NOTES_FILE", "notes.json")
        _builder = Builder(filename=notes_file)
    return _builder


def reset():
    global _builder
    _builder = None
