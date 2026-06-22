class ProcessNotFoundError(Exception):
    """Raised when an operation targets a process name with no recorded state."""
    pass
