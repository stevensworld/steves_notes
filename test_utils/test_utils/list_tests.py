import os


def list_tests(active_dir):
    return sorted([
        f for f in os.listdir(active_dir)
        if f.startswith("test_") and f.endswith(".py")
    ])
