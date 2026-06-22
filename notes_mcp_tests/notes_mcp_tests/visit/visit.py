import os
from test_utils.visit import run

active_dir = os.path.join(os.path.dirname(__file__), "../active")

if __name__ == "__main__":
    run(active_dir)
