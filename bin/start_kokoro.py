#!/usr/bin/env python3
import os
from kokoro_process import KokoroProcess

PID_DIR = os.path.join(os.path.dirname(__file__), "pids")

kp = KokoroProcess(config={"pid_directory": PID_DIR})

print("── Starting Kokoro TTS server...")
result = kp.start()
s = kp.status()
if result:
    print(f"── Started. PID={s['pid']} started_at={s['started_at']}")
else:
    print("── Failed to start — health check timed out.")
