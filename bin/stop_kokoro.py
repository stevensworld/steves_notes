#!/usr/bin/env python3
import os
from kokoro_process import KokoroProcess

PID_DIR = os.path.join(os.path.dirname(__file__), "pids")

kp = KokoroProcess(config={"pid_directory": PID_DIR})
kp.stop()
print("── Kokoro TTS server stopped.")
