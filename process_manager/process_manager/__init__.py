"""
process_manager — lightweight subprocess lifecycle manager.

Usage:
    from process_manager import ProcessManager, ProcessNotFoundError

    pm = ProcessManager(pid_dir="./config/pids")
    pm.start("litellm", ["litellm", "--config", "..."], ready_fn=..., timeout=30)
    pm.status("litellm")
    pm.stop("litellm")
    pm.stop_all()
"""

from .manager import ProcessManager
from .exceptions import ProcessNotFoundError

__all__ = ["ProcessManager", "ProcessNotFoundError"]
