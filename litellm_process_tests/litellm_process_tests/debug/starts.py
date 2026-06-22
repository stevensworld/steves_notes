import os
import sys
import urllib.request

from litellm_process import LiteLLMProcess

CONFIG = {
    "pid_directory": os.path.join(os.path.dirname(__file__), "pids"),
    "litellm_config_path": os.path.join(os.path.dirname(__file__), "../config/litellm_config.json"),
}


def get_proxy():
    return LiteLLMProcess(config=CONFIG)


def cmd_start():
    proxy = get_proxy()
    print("── Starting LiteLLM proxy...")
    result = proxy.start()
    s = proxy.status()
    if result:
        print(f"── Started. PID={s['pid']} started_at={s['started_at']}")
        print(f"── Health: http://localhost:4000/health")
    else:
        print(f"── Failed to start — health check timed out.")


def cmd_stop():
    proxy = get_proxy()
    proxy.stop()
    print("── Stopped.")


def cmd_status():
    proxy = get_proxy()
    s = proxy.status()
    print(f"── Status: running={s['running']} pid={s['pid']} started_at={s['started_at']}")


def cmd_health():
    url = "http://localhost:4000/health"
    try:
        with urllib.request.urlopen(url, timeout=3) as r:
            print(f"── Health check: {r.status} {r.reason}")
            print(r.read().decode())
    except Exception as e:
        print(f"── Health check failed: {e}")


COMMANDS = {
    "start":  cmd_start,
    "stop":   cmd_stop,
    "status": cmd_status,
    "health": cmd_health,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "start"
    if cmd not in COMMANDS:
        print(f"Usage: python starts.py [{' | '.join(COMMANDS)}]")
        sys.exit(1)
    COMMANDS[cmd]()
