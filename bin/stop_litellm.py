#!/usr/bin/env python3
import os
from litellm_process import LiteLLMProcess

PID_DIR = os.path.join(os.path.dirname(__file__), "pids")

proxy = LiteLLMProcess(config={"pid_directory": PID_DIR})
proxy.stop()
print("── LiteLLM proxy stopped.")
