#!/usr/bin/env python3
import os
from litellm_process import LiteLLMProcess
from kokoro_process import KokoroProcess

PID_DIR = os.path.join(os.path.dirname(__file__), "pids")

services = [
    ("LiteLLM",  LiteLLMProcess(config={"pid_directory": PID_DIR})),
    ("Kokoro",   KokoroProcess(config={"pid_directory": PID_DIR})),
]

print("── Service Status ───────────────────────")
for name, svc in services:
    s = svc.status()
    state = "RUNNING" if s["running"] else "STOPPED"
    pid = s["pid"] or "-"
    started = s["started_at"] or "-"
    print(f"   {name:<10} {state:<8}  pid={pid}  started={started}")
print("─────────────────────────────────────────")
