import urllib.request
from process_manager import ProcessManager

CONFIG = {
    "host":           "localhost",
    "port":           4001,
    "health_path":    "/health",
    "ready_timeout":  60,
    "conda_env":      "notes",
    "pid_directory":  "./pids",
    "process_name":   "kokoro",
}


class KokoroProcess:
    def __init__(self, config: dict = None):
        self._config = {**CONFIG, **(config or {})}
        self._manager = ProcessManager(pid_dir=self._config["pid_directory"])

    def start(self) -> bool:
        return self._manager.start(
            name=self._config["process_name"],
            command=self._build_command(),
            ready_fn=self._ready_fn(),
            timeout=self._config["ready_timeout"],
        )

    def stop(self) -> None:
        self._manager.stop(self._config["process_name"])

    def status(self) -> dict:
        return self._manager.status(self._config["process_name"])

    def _build_command(self) -> list:
        return [
            "conda", "run", "--no-capture-output",
            "-n", self._config["conda_env"],
            "kokoro-server",
        ]

    def _ready_fn(self):
        url = f"http://{self._config['host']}:{self._config['port']}{self._config['health_path']}"
        def check():
            try:
                with urllib.request.urlopen(url, timeout=1):
                    return True
            except Exception:
                return False
        return check
