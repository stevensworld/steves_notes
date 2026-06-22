import os


def list_tests():
    active_dir = os.path.join(os.path.dirname(__file__), "../active")
    return sorted([
        f for f in os.listdir(active_dir)
        if f.startswith("test_") and f.endswith(".py")
    ])


if __name__ == "__main__":
    for test in list_tests():
        print(test)
