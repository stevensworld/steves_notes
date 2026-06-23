from steves_notes import Builder

_builder = None


def get_builder() -> Builder:
    global _builder
    if _builder is None:
        _builder = Builder()
    return _builder


def reset():
    global _builder
    _builder = None
