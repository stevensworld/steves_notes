#!/usr/bin/env python3
import os
from litellm_process import LiteLLMProcess

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../litellm_process/litellm_process/config/litellm_config.json")
PID_DIR = os.path.join(os.path.dirname(__file__), "pids")

proxy = LiteLLMProcess(config={
    "pid_directory": PID_DIR,
    "litellm_config_path": CONFIG_PATH,
})

print("── Starting LiteLLM proxy...")
result = proxy.start()
s = proxy.status()
if result:
    print(f"── Started. PID={s['pid']} started_at={s['started_at']}")
else:
    print("── Failed to start — health check timed out.")
