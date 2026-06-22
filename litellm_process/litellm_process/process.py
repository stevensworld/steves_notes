"""
LiteLLMProcess — manages the LiteLLM proxy subprocess.

All configuration lives in the CONFIG block at the top of this file.
Edit CONFIG to change runtime behaviour without touching any other code.
These keys are intentionally named for future refactor into a shared config layer.
"""

import urllib.request
from process_manager import ProcessManager, ProcessNotFoundError
from .exceptions import LiteLLMStartError, LiteLLMConfigError


# ── Configuration ─────────────────────────────────────────────────────
# Edit these values to match your local setup.
# Keys are named to mirror the fields in app_config / config.json.

CONFIG = {
    "proxy_host":            "localhost",
    "proxy_port":            4000,
    "proxy_health_endpoint": "/health",
    "proxy_ready_timeout":   30,

    "conda_environment":     "litellm_secure_env",
    "litellm_config_path":   "./config/litellm_config.json",

    "pid_directory":         "./config/pids",
    "process_name":          "litellm",
}

# ── Required keys — checked at instantiation ──────────────────────────

_REQUIRED_KEYS = [
    "proxy_host",
    "proxy_port",
    "proxy_health_endpoint",
    "proxy_ready_timeout",
    "conda_environment",
    "litellm_config_path",
    "pid_directory",
    "process_name",
]


class LiteLLMProcess:
    """Starts, stops, and monitors the LiteLLM proxy subprocess.

    Accepts an optional config dict to override any key in CONFIG.
    If no config is provided, the module-level CONFIG is used as-is.
    """

    def __init__(self, config: dict = None):
        merged = {**CONFIG, **(config or {})}
        self._validate(merged)
        self._config  = merged
        self._manager = ProcessManager(pid_dir=merged["pid_directory"])

    # ── public ────────────────────────────────────────────────────────

    def start(self) -> bool:
        """Start the LiteLLM proxy. Returns True when ready, False if timeout exceeded."""
        command = self._build_command()
        try:
            return self._manager.start(
                name     = self._config["process_name"],
                command  = command,
                ready_fn = self._ready_fn(),
                timeout  = self._config["proxy_ready_timeout"],
            )
        except Exception as e:
            raise LiteLLMStartError(str(e))

    def stop(self) -> None:
        """Stop the LiteLLM proxy."""
        self._manager.stop(self._config["process_name"])

    def restart(self) -> bool:
        """Restart the LiteLLM proxy."""
        try:
            return self._manager.restart(
                name     = self._config["process_name"],
                ready_fn = self._ready_fn(),
                timeout  = self._config["proxy_ready_timeout"],
            )
        except ProcessNotFoundError:
            return self.start()

    def status(self) -> dict:
        """Return status dict: name, running, pid, started_at."""
        return self._manager.status(self._config["process_name"])

    # ── private ───────────────────────────────────────────────────────

    def _build_command(self) -> list:
        return [
            "conda", "run", "--no-capture-output",
            "-n", self._config["conda_environment"],
            "litellm",
            "--config", self._config["litellm_config_path"],
            "--port",   str(self._config["proxy_port"]),
        ]

    def _ready_fn(self):
        url = (
            f"http://{self._config['proxy_host']}"
            f":{self._config['proxy_port']}"
            f"{self._config['proxy_health_endpoint']}"
        )
        def check():
            try:
                with urllib.request.urlopen(url, timeout=1):
                    return True
            except Exception:
                return False
        return check

    def _validate(self, config: dict) -> None:
        missing = [k for k in _REQUIRED_KEYS if k not in config]
        if missing:
            raise LiteLLMConfigError(f"Missing config keys: {missing}")
