"""
litellm_process — manages the LiteLLM proxy as a detached subprocess.

Usage:
    from litellm_process import LiteLLMProcess

    llm = LiteLLMProcess()          # uses module-level CONFIG
    llm = LiteLLMProcess(config={   # override specific keys
        "proxy_port": 4001,
        "conda_environment": "my_env",
    })

    llm.start()    # starts proxy, blocks until ready
    llm.status()   # {"name": "litellm", "running": True, "pid": ..., "started_at": ...}
    llm.stop()
    llm.restart()

Depends on: process_manager
"""

from .process import LiteLLMProcess
from .exceptions import LiteLLMStartError, LiteLLMConfigError

__all__ = ["LiteLLMProcess", "LiteLLMStartError", "LiteLLMConfigError"]
